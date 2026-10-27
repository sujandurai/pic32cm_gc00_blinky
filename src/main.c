/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>

/* Timing configurations (in milliseconds) */
#define SLEEP_TIME_MS   1000    /* Pause time: 1000 ms (1 second) */
#define ON_TIME         350     /* LED ON time: 350 ms */
#define OFF_TIME        450     /* LED OFF time: 450 ms */
#define BLINK_COUNT     5

/*
 * Logical levels. gpio_pin_set_dt() uses logical values, so 1 = ON when the
 * devicetree flags the LED correctly (GPIO_ACTIVE_LOW/HIGH).
 * If your LED behaves inverted, swap these two values.
 */
#define LED_ON_LEVEL    1
#define LED_OFF_LEVEL   0

/* The devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

int main(void)
{
	int ret;
	bool led_state;

	if (!gpio_is_ready_dt(&led)) {
		return 0;
	}

	/* Initialize LED pin as output in INACTIVE (OFF) state */
	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
	if (ret < 0) {
		return 0;
	}

	while (1) {
		for (int i = 0; i < BLINK_COUNT; i++) {
			/* LED ON for 350 ms */
			ret = gpio_pin_set_dt(&led, LED_ON_LEVEL);
			if (ret < 0) {
				return 0;
			}
			led_state = true;
			printf("Iteration %d/%d - LED state: %s (350 ms ON)\n",
			       i + 1, BLINK_COUNT, led_state ? "ON" : "OFF");
			k_msleep(ON_TIME);

			/* LED OFF */
			ret = gpio_pin_set_dt(&led, LED_OFF_LEVEL);
			if (ret < 0) {
				return 0;
			}
			led_state = false;

			if (i < BLINK_COUNT - 1) {
				/* Gap between blinks: 450 ms */
				printf("Iteration %d/%d - LED state: %s (450 ms OFF)\n",
				       i + 1, BLINK_COUNT, led_state ? "ON" : "OFF");
				k_msleep(OFF_TIME);
			} else {
				/* After the last blink, the pause replaces the 450 ms gap */
				printf("Pause - LED state: %s (1000 ms Pause)\n\n",
				       led_state ? "ON" : "OFF");
				k_msleep(SLEEP_TIME_MS);
			}
		}
	}

	return 0;
}
