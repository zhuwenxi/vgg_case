#! /usr/bin/python
import argparse
import xlsxwriter
import yaml

parser = argparse.ArgumentParser(description='Filter layer time from caffe log file.')
parser.add_argument('knl', help='knl json file.')
parser.add_argument('p100', help='p100 json file.')
parser.add_argument('-o', default='output.xlsx', help='Output xlsx file')

args = parser.parse_args();

# Initial xlsx file
workbook = xlsxwriter.Workbook(args.o)

forward_worksheet = workbook.add_worksheet('forward')
forward_worksheet.set_column('A:F', 20)

backward_worksheet = workbook.add_worksheet('backward')
backward_worksheet.set_column('A:F', 20)

# Format
format = workbook.add_format()
format.set_align('center')

with open(args.knl, 'r') as knl_json, open(args.p100, 'r') as p100_json:
	knl_dict = yaml.safe_load(knl_json)
	p100_dict = yaml.safe_load(p100_json)

	#
	# write "forward" work sheet
	#
	forward_worksheet.write(0, 0, 'Layer Name', format)
	forward_worksheet.write(0, 1, 'KNL (ms)', format)
	forward_worksheet.write(0, 2, 'P100 (ms)', format)
	forward_worksheet.write(0, 3, 'KNL / P100 (%)', format)

	i = 1
	for layer, data in knl_dict.items():
		forward_worksheet.write(i, 0, layer)
		forward_worksheet.write(i, 1, float(data['forward']))
		i += 1

	i = 1
	for layer, data in p100_dict.items():
		forward_worksheet.write(i, 2, float(data['forward']))
		forward_worksheet.write(i, 3, float('%.2f' % (float(p100_dict[layer]['forward']) * 100 / float(knl_dict[layer]['forward']))))
		i += 1

	#
	# write "forward" work sheet
	#
	backward_worksheet.write(0, 0, 'Layer Name', format)
	backward_worksheet.write(0, 1, 'KNL (ms)', format)
	backward_worksheet.write(0, 2, 'P100 (ms)', format)
	backward_worksheet.write(0, 3, 'KNL / P100 (%)', format)

	i = 1
	for layer, data in knl_dict.items():
		backward_worksheet.write(i, 0, layer)
		backward_worksheet.write(i, 1, float(data['backward']))
		i += 1

	i = 1
	for layer, data in p100_dict.items():
		backward_worksheet.write(i, 2, float(data['backward']))
		backward_worksheet.write(i, 3, float('%.2f' % (float(p100_dict[layer]['backward']) * 100 / float(knl_dict[layer]['backward']))))
		i += 1

workbook.close()

