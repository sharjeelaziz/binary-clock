binary-clock
============
A LED matrix binary clock built with a Raspberry Pi. The python code uses MAX7219 driver by Richard Hull https://github.com/rm-hull/max7219 and forecast.io wrapper by Ze'ev Gilovitz https://github.com/ZeevG/python-forecast.io

The binary clock displays weather information under the following conditions:

* Weather alerts are active for the area
* Current weather condition is rain, snow, sleet, wind or fog
* If precipitation is expected in the next hour


Pre-requisites
--------------
Ensure that the SPI kernel driver is enabled:

	pi@binclock ~/binary_clock $ dmesg | grep spi
	[    9.443124] bcm2708_spi bcm2708_spi.0: master is unqueued, this is deprecated
	[    9.593357] bcm2708_spi bcm2708_spi.0: SPI Controller at 0x20204000 (irq 80)

And that the devices are successfully installed in /dev:

	pi@binclock ~/binary_clock $ ls -l /dev/spi*
	crw-rw---T 1 root spi 153, 0 Dec 31  1969 /dev/spidev0.0
	crw-rw---T 1 root spi 153, 1 Dec 31  1969 /dev/spidev0.1

Refer to http://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md if the devices do not appear before proceeding.

GPIO pin-outs
-------------
The breakout board has an two headers to allow daisy-chaining:

| Board Pin | Name | Remarks | RPi Pin | RPi Function |
|--------:|:-----|:--------|--------:|--------------|
| 1 | VCC | +5V Power | 2 | 5V0 |
| 2 | GND | Ground | 6 | GND |
| 3 | DIN | Data In | 19 | GPIO 10 (MOSI) |
| 4 | CS | Chip Select | 24 | GPIO 8 (SPI CS0) |
| 5 | CLK | Clock | 23 | GPIO 11 (SPI CLK) |

Weather
-------
You need an API key to use it (http://developer.forecast.io). The key is free for 1000 calls per day.

References
----------
* https://github.com/rm-hull/max7219
* https://github.com/ZeevG/python-forecast.io
* http://www.raspberrypi.org/documentation/hardware/raspberrypi/spi/README.md
* http://developer.forecast.io
* https://developer.forecast.io/docs/v2#data-points

License
-------
Copyright 2014 Sharjeel Aziz (Shaji)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

	http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
