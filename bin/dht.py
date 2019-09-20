#!/usr/bin/python
# read in the content of the cronjob-triggered file

f = open("/tmp/fruitnanny_dht.txt","r")
if f.mode == 'r'
    contents = f.read()
    print(contents)

