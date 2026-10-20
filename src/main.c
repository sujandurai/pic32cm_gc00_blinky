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

/* The devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)

/*
 * A build error on this line means your board is unsupported.
 * See the sample documentation for information on how to fix this.
 */
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
		/* Loop 5 times: 350 ms ON, 450 ms OFF */
		for (int i = 0; i < 5; i++) {
			/* Command: Turn LED ON for 350 ms */
			ret = gpio_pin_set_dt(&led, 0);
			if (ret < 0) {
				return 0;
			}
			led_state = true;
			printf("Iteration %d/5 - LED state: %s (350 ms ON)\n", i + 1, led_state ? "ON" : "OFF");
			k_msleep(ON_TIME);

			/* Command: Turn LED OFF for 450 ms */
			ret = gpio_pin_set_dt(&led, 1);
			if (ret < 0) {
				return 0;
			}
			led_state = false;
			printf("Iteration %d/5 - LED state: %s (450 ms OFF)\n", i + 1, led_state ? "ON" : "OFF");
			k_msleep(OFF_TIME);
		}

		/* Command: Pause - LED remains OFF for 1000 ms (1 second) */
		ret = gpio_pin_set_dt(&led, 1);
		if (ret < 0) {
			return 0;
		}
		led_state = false;
		printf("Pause - LED state: %s (1000 ms Pause)\n\n", led_state ? "ON" : "OFF");
		k_msleep(SLEEP_TIME_MS);
	}

	return 0;
}
