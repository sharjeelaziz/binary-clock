#!/usr/bin/env python

import max7219.led as led
import max7219.canvas as canvas
import max7219.transitions as transitions
import time
import datetime
import forecastio
import json

weather_icons = {
'clear-day': [0x81,0x5a,0x3c,0x7e,0x7e,0x3c,0x5a,0x81], 
'clear-night': [0x0,0x0,0x81,0xc3,0x7e,0x3c,0x18,0x0],
'rain':[0x8c,0x5e,0x1e,0x5f,0x3f,0x9f,0x5e,0xc],
'snow':[0x14,0x49,0x2a,0x1c,0x1c,0x2a,0x49,0x14], 
'sleet':[0xac,0x1e,0x5e,0x1f,0x3f,0x9f,0x1e,0xac], 
'wind':[0x28,0x28,0x28,0x28,0x28,0xaa,0xaa,0x44], 
'fog':[0xaa,0x55,0xaa,0x55,0xaa,0x55,0xaa,0x55], 
'cloudy':[0xc,0x1e,0x1e,0x1f,0x1f,0x1f,0x1e,0xc], 
'partly-cloudy-day':[0x18,0x24,0x24,0x22,0x22,0x22,0x24,0x18],
'partly-cloudy-night':[0xe7,0xdb,0xdb,0xdf,0xdd,0xdd,0xdb,0xe7]
}


def format_unix_time(t):
	return time.strftime("%D %H:%M", time.localtime(int(t)))

def draw_weather_icon(icon):
	icon_bytes = weather_icons[icon]
	for col in range(8):
		led.send_byte(col + 1, icon_bytes[col])
		
def get_time_difference(d1, d2):
	d1_ts = time.mktime(d1.timetuple())
	d2_ts = time.mktime(d2.timetuple())
	return int(d2_ts - d1_ts) / 60
		
def check_weather(api_key, lat, lng):
		
	forecast = forecastio.load_forecast(api_key, lat, lng)
	
	current_data = forecast.currently()
	
	weather_statement = ''
	
	print current_data.icon
	print current_data.summary
	
	if (current_data.icon == 'rain' or 
		current_data.icon == 'snow' or 
		current_data.icon == 'sleet' or 
		current_data.icon == 'wind' or 
		current_data.icon == 'fog'):
				
		weather_statement = current_data.summary
		weather_statement += " %s Feels like %s " % (current_data.temperature, current_data.apparentTemperature)

	alerts = forecast.alerts()

	if (len(alerts) > 0):
		weather_statement += ' * ALERT * '
		for i in range(len(alerts)):
			weather_statement += alerts[i].title
			weather_statement += '*'

	minutely = forecast.minutely()

	minutely_data = minutely.data
	
	# A very rough guide is that a value of 0 in./hr. corresponds to no precipitation, 
	# 0.002 in./hr. corresponds to very light precipitation, 
	# 0.017 in./hr. corresponds to light precipitation, 
	# 0.1 in./hr. corresponds to moderate precipitation, 
	# and 0.4 in./hr. corresponds to heavy precipitation.

	for i in range(len(minutely_data)):
		try:
			if (float(current_data.precipIntensity) < 0.017):
				if (float(minutely_data[i].precipIntensity) >= 0.017 and float(minutely_data[i].precipIntensity) < .1):
					weather_statement += "Light %s in %s minutes" % (minutely_data[i].precipType, get_time_difference(current_data.time, minutely_data[i].time))
					break
				if (float(minutely_data[i].precipIntensity) >= 0.1 and float(minutely_data[i].precipIntensity) < .4):
					weather_statement += "Moderate %s in %s minutes" % (minutely_data[i].precipType, get_time_difference(current_data.time, minutely_data[i].time))
					break 
				if (float(minutely_data[i].precipIntensity) >= .4):
					weather_statement += "Heavy %s in %s minutes" % (minutely_data[i].precipType, get_time_difference(current_data.time, minutely_data[i].time))
					break 
		except:
			print "caught exception for starting"

	for i in range(len(minutely_data)):
		try:
			if (float(current_data.precipIntensity) > 0):
				if (float(minutely_data[i].precipIntensity) == 0):
					weather_statement += " %s stopping in %s minutes" % (current_data.icon, get_time_difference(current_data.time, minutely_data[i].time))
					break
		except:
			print "caught exception for stopping"
		
	return {'icon': current_data.icon, 'statement': weather_statement}		


def draw_wide_row(n, r):
	if ((n & 8) >> 3):
		canvas.set_on(r, 0)
		canvas.set_on(r, 1)
	else:
		canvas.set_off(r, 0)
		canvas.set_off(r, 1)
		
	if ((n & 4) >> 2):
		canvas.set_on(r, 2)
		canvas.set_on(r, 3)
	else:
		canvas.set_off(r, 2)
		canvas.set_off(r, 3)
	
	if ((n & 2) >> 1):
		canvas.set_on(r, 4)
		canvas.set_on(r, 5)
	else:
		canvas.set_off(r, 4)
		canvas.set_off(r, 5)
	if (n & 1):
		canvas.set_on(r, 6)
		canvas.set_on(r, 7)
	else:
		canvas.set_off(r, 6)
		canvas.set_off(r, 7)

def draw_bcd_row(n, r):
	tens = n // 10
	ones = n % 10
	
	if ((tens & 8) >> 3):
		canvas.set_on(r,0)
	else:
		canvas.set_off(r,0)
		
	if ((tens & 4) >> 2):
		canvas.set_on(r,1)
	else:
		canvas.set_off(r,1)
		
	if ((tens & 2) >> 1):
		canvas.set_on(r, 2)
	else:
		canvas.set_off(r, 2)
		
	if (tens & 1):
		canvas.set_on(r, 3)
	else:
		canvas.set_off(r, 3)

	if ((ones & 8) >> 3):
		canvas.set_on(r, 4)
	else:
		canvas.set_off(r, 4)
	
	if ((ones & 4) >> 2):
		canvas.set_on(r, 5)
	else:
		canvas.set_off(r, 5)
	
	if ((ones & 2) >> 1):
		canvas.set_on(r, 6)
	else:
		canvas.set_off(r, 6)
	
	if (ones & 1):
		canvas.set_on(r, 7)
	else:
		canvas.set_off(r, 7)
		
def draw_time():
	dt = datetime.datetime.now()
	hour = dt.hour
	if (dt.hour > 12):
		hour = dt.hour - 12;
		
	draw_wide_row(hour, 0)
	draw_wide_row(hour, 1)
		
	draw_bcd_row(dt.minute, 3)
	draw_bcd_row(dt.second, 5)
	canvas.render()
	time.sleep(0.30)
	

with open('config.json') as json_data_file:
	config = json.load(json_data_file)
	
api_key = config['forecastio']['api_key']
lat = config['forecastio']['lat']
lng = config['forecastio']['lng']
	
led.init()
led.brightness(0)
weather_interval = 120.0 # interval in seconds 
next_weather_check = time.time() + weather_interval 
weather_info = {}
	
while True:
	now = time.time() 
	if now > next_weather_check:
		try:
			weather_info = check_weather(api_key, lat, lng)
		except ValueError:
			print "check_weather raised an exception."	
		next_weather_check = now + weather_interval
		
	if (len(weather_info) > 0):
		if (len(weather_info['statement']) > 0):
			draw_weather_icon(weather_info['icon'])
			time.sleep(2)
			led.show_message(weather_info['statement'], transition = transitions.left_scroll)
	
	else:
		draw_time()
