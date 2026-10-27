/*
 * Copyright (c) 2016 Intel Corporation
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>

/* Timing configurations (in milliseconds) */
#define SLEEP_TIME_MS   1000    /* Pause after 5 iterations: 1000 ms */
#define ON_TIME         350     /* LED ON time: 350 ms */
#define OFF_TIME        450     /* LED OFF time: 450 ms */
#define BLINK_COUNT     5

/* Logical levels. Swap these if your LED behaves inverted. */
#define LED_ON_LEVEL    1
#define LED_OFF_LEVEL   0

/* The devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

int main(void)
{
	int ret;

	if (!gpio_is_ready_dt(&led)) {
		return 0;
	}

	/* Initialize LED pin as output in INACTIVE (OFF) state */
	ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);
	if (ret < 0) {
		return 0;
	}

	/* Absolute schedule anchor (ms of uptime) */
	int64_t next = k_uptime_get();

	while (1) {
		/* Loop 5 times: 350 ms ON, 450 ms OFF */
		for (int i = 0; i < BLINK_COUNT; i++) {

			/* LED ON for 350 ms */
			ret = gpio_pin_set_dt(&led, LED_ON_LEVEL);
			if (ret < 0) {
				return 0;
			}
			printf("Iteration %d/%d - LED state: ON (350 ms ON)\n",
			       i + 1, BLINK_COUNT);
			next += ON_TIME;
			k_sleep(K_TIMEOUT_ABS_MS(next));

			/* LED OFF for 450 ms (every iteration, including the 5th) */
			ret = gpio_pin_set_dt(&led, LED_OFF_LEVEL);
			if (ret < 0) {
				return 0;
			}
			printf("Iteration %d/%d - LED state: OFF (450 ms OFF)\n",
			       i + 1, BLINK_COUNT);
			next += OFF_TIME;
			k_sleep(K_TIMEOUT_ABS_MS(next));
		}

		/* After 5 iterations: LED stays OFF for a further 1000 ms */
		printf("Pause - LED state: OFF (1000 ms Pause)\n\n");
		next += SLEEP_TIME_MS;
		k_sleep(K_TIMEOUT_ABS_MS(next));
	}

	return 0;
}
