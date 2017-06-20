#! /usr/bin/python
import argparse
import re
from collections import OrderedDict
import json

parser = argparse.ArgumentParser(description='Filter layer time from caffe log file.')
parser.add_argument('caffelog', help='Caffe log file.')
parser.add_argument('-o', default='layer_time.json', help='Output file path')

args = parser.parse_args();

# 
# record something we want
#
layer_time_dict = {}
average_forward_time = None
average_backward_time = None


#
# parameters from command line.
# 
caffe_log_file = args.caffelog;

if args.o:
	layer_time_log_file = args.o 

#
# helper function to retieve layer time and update dict
#
def update_layer_time(line):
	forward_line = re.search('\]\s*([^\s]*)\s*forward:\s*(\d+\.\d+)\s*ms', line)
	if forward_line:
		layer_name = forward_line.group(1)
		forward_time = forward_line.group(2)
		if layer_time_dict.get(layer_name) is None:
			layer_time_dict.update({layer_name: {'forward': forward_time, 'backward': 0}})
		else:
			layer_time_dict[layer_name]['forward'] = forward_time

	backward_line = re.search('\]\s*([^\s]*)\s*backward:\s*(\d+\.\d+)\s*ms', line)
	if backward_line:
		layer_name = backward_line.group(1)
		backward_time = backward_line.group(2)
		if layer_time_dict.get(layer_name) is None:
			layer_time_dict.update({layer_name: {'forward': 0, 'backward': backward_time}})
		else:
			layer_time_dict[layer_name]['backward'] = backward_time

	global average_forward_time
	average_forward_line = re.search('Average Forward pass:\s*(\d+\.\d+)\s*ms', line)
	if average_forward_line:
		average_forward_time = average_forward_line.group(1)
	global average_backward_time
	average_backward_line = re.search('Average Backward pass:\s*(\d+\.\d+)\s*ms', line)
	if average_backward_line:
		average_backward_time = average_backward_line.group(1)
	
#
# read caffe log file to retieve layer time
# 
with open(caffe_log_file, 'r') as f:
	for l in f:
		update_layer_time(l)

# update layer-time / total-tiem to the dict
for layer, data in layer_time_dict.items():
	layer_time_dict[layer]['forward_ratio'] = ("%.2f%%" % ((float(layer_time_dict[layer]['forward']) / float(average_forward_time)) * 100))
	layer_time_dict[layer]['backward_ratio'] = ("%.2f%%" % ((float(layer_time_dict[layer]['backward']) / float(average_backward_time)) * 100))

layer_time_dict = OrderedDict(sorted(layer_time_dict.items(), key=lambda t: t[0]))

json.dump(layer_time_dict, open(layer_time_log_file, 'w+'), indent=4)
