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

/* The devicetree node identifier for the "led0" alias. */
#define LED0_NODE DT_ALIAS(led0)

static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

/* Set at startup from the pin's initial level */
static int led_on_level;
static int led_off_level;

static int led_on(void)
{
	return gpio_pin_set_raw(led.port, led.pin, led_on_level);
}

static int led_off(void)
{
	return gpio_pin_set_raw(led.port, led.pin, led_off_level);
}

int main(void)
{
	int ret;
	int initial;

	if (!gpio_is_ready_dt(&led)) {
		return 0;
	}

	/* Read the pin's initial raw level before driving it */
	ret = gpio_pin_configure(led.port, led.pin, GPIO_INPUT);
	if (ret < 0) {
		return 0;
	}
	k_msleep(10);   /* let the pin settle */
	initial = gpio_pin_get_raw(led.port, led.pin);
	if (initial < 0) {
		return 0;
	}

	if (initial) {
		/* Initially HIGH: LED is OFF when high, so ON = 0, OFF = 1 */
		led_on_level  = 0;
		led_off_level = 1;
	} else {
		/* Initially LOW: ON = 1, OFF = 0 */
		led_on_level  = 1;
		led_off_level = 0;
	}

	/* Now make it an output and start with LED OFF */
	ret = gpio_pin_configure(led.port, led.pin, GPIO_OUTPUT);
	if (ret < 0) {
		return 0;
	}
	ret = led_off();
	if (ret < 0) {
		return 0;
	}

	printf("Initial pin level: %s -> ON = %d, OFF = %d\n\n",
	       initial ? "HIGH" : "LOW", led_on_level, led_off_level);

	while (1) {
		/* Loop 5 times: 350 ms ON, 450 ms OFF */
		for (int i = 0; i < BLINK_COUNT; i++) {
			ret = led_on();
			if (ret < 0) {
				return 0;
			}
			printf("Iteration %d/%d - LED state: ON (350 ms ON)\n",
			       i + 1, BLINK_COUNT);
			k_msleep(ON_TIME);

			ret = led_off();
			if (ret < 0) {
				return 0;
			}
			printf("Iteration %d/%d - LED state: OFF (450 ms OFF)\n",
			       i + 1, BLINK_COUNT);
			k_msleep(OFF_TIME);
		}

		/* After 5 iterations: LED remains OFF for 1000 ms */
		ret = led_off();
		if (ret < 0) {
			return 0;
		}
		printf("Pause - LED state: OFF (1000 ms Pause)\n\n");
		k_msleep(SLEEP_TIME_MS);
	}

	return 0;
}
