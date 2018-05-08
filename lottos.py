#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup
import requests


def get_result():
	'''Get all prizes of ketqua.net'''
	respond = requests.get('http://ketqua.net')
	mixed = BeautifulSoup(respond.text, 'html.parser').find('tbody').get_text(' ').split()
	all_numbers = [numb for numb in mixed if numb.isdigit()]
	return all_numbers


def all_results(*input_data2):
    print('''
Đặc biệt:   | {0:>5} |
Giải nhất:  | {1:>5} |
Giải nhì:   | {2:>5} | {3:>5} |
Giải ba:    | {4:>5} | {5:>5} | {6:>5} | {7:>5} | {8:>5} | {9:>5} |
Giải tư:    | {10:>5} | {11:>5} | {12:>5} | {13:>5} |
Giải năm:   | {14:>5} | {15:>5} | {16:>5} | {17:>5} | {18:>5} | {19:>5} |
Giải sáu:   | {20:>5} | {21:>5} | {22:>5} |
Giải bảy:   | {23:>5} | {24:>5} | {25:>5} | {26:>5} |
    '''.format(*input_data2))


def solve(numb_argv):
    all_prizes = get_result()
    found = False
    for numb in numb_argv:
    	count = 0
    	for prize in all_prizes:
    		if prize[-2:] == str(numb):
    			found = True
    			count = count + 1
    	if count > 0:
    		print('Chuc mung ban! {} trung {} nhay'.format(numb, count))
    	else:
    		print('{} truot'.format(numb))
    if not found:
    	all_results(*all_prizes)
    return None


def main():
	input_data1 = []
	for arg in sys.argv[1:]:
		input_data1.append(arg)
	solve(input_data1)


if __name__ == '__main__':
	main()