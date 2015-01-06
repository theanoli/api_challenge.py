import urllib
import urllib2
import json
import re
import dateutil.parser as dp
from datetime import datetime


url_prefix = 'http://challenge.code2040.org/api/'

# Arguments to POST request
reg_url = url_prefix + 'register'
reg_keys = json.dumps({'email': 'theanosaurus@gmail.com', 
			'github' : 'https://github.com/theanoli/api_challenge.py'})

# Send registration request and parse response
request = urllib2.Request(reg_url, reg_keys)
response = urllib2.urlopen(request).read()
token = json.loads(response)["result"]

# Save token as a JSON object
json_token = json.dumps({'token' : token})


# Function to get stage information
def post_token(get_name, do_encode):
	request = urllib2.Request(url_prefix + get_name, json_token)
	response = urllib2.urlopen(request).read()

	if do_encode: 
		return json.loads(response)["result"].encode('ascii')
	else: 
		return json.loads(response)["result"]


# Function to send output for validation
def validate(val_name, answer_key, answer_value):
	val_keys = json.dumps({ 'token' : token,
							answer_key : answer_value})
	validate_request = urllib2.Request(url_prefix + val_name, val_keys)


def reverse_string():
	# Retrieve string; need to encode as ascii
	string = post_token('getstring', True)

	# Reverse string
	reverse_string = string[::-1]

	validate('validatestring', "string", reverse_string)


def needle_in_haystack():
	# Retrieve dictionary containing needle and haystack, unpack
	response_dict = post_token('haystack', False)

	needle, haystack = response_dict["needle"], response_dict["haystack"]

	# Set counter; increment for every item we iterate over which isn't the needle
	counter = 0
	for item in haystack: 
		if item == needle: 
			break
		else: 
			counter += 1

	validate('validateneedle', "needle", str(counter))


def prefix(): 
	response_dict = post_token('prefix', False)

	prefix, array = response_dict["prefix"], response_dict["array"]

	pref_array = []

	# Use re.match to check beginning of string for prefix
	for string in array: 
		if re.match("%s.*" % prefix, string) == None: 
			pref_array.append(string)

	validate('validateprefix', "array", pref_array)


def dating_game(): 
	response_dict = post_token('time', False)

	# datestamp = ISO 8601 datestamp string, interval = nsecs
	datestamp, interval = response_dict["datestamp"], response_dict["interval"]

	# Parse date into date object and convert to seconds
	date_in_secs = dp.parse(datestamp).strftime('%s')

	# Add interval, convert back into date object and then to ISO format
	newtime_obj = datetime.fromtimestamp(int(date_in_secs) + interval)
	newtime_iso = datetime.isoformat(newtime_obj)

	validate('validatetime', "datestamp", newtime_iso)


reverse_string()
needle_in_haystack()
prefix()
dating_game()
