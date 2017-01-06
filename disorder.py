# -*- coding:utf-8 -*-

import random
import sys

if len(sys.argv) == 1:
    file_name = raw_input("input file name(no postfix): ")
else:
    file_name = sys.argv[1]

try:
    input_file_object = open(file_name + r'.md')
except:
    print "can not open file:", (file_name + r'.md')
    exit(0)

try:
    file_content = input_file_object.readlines()
except:
    print "can not read file: %s" %file_name
    input_file_object.close()
    exit(0)
input_file_object.close()
random.shuffle(file_content)
try:
    output_file_object = open(file_name + r'_disorder.md', 'w')
except Exception as e:
    print e
    print "can not open file: %s" % (file_name + r'_disorder.md')
    exit(0)
for sentence in file_content:
    output_file_object.write(sentence.rstrip() + '\n')
output_file_object.close()
