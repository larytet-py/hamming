#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''hamming.py

Read hashes from the file
Create a dictionary of all hashes with distances below certain threshold  

Usage:
  hamming.py -h | --help
  hamming.py -f <FILENAME> [-d <MAXDISTANCE>] 
Example:
    dockerfile_generator.py -c containers.yml
   
Options:
  -h --help                 Show this screen.
  -f --file=<FILENAME>    Data set
  -d --distance=<MAXDISTANCE>      Max distance between hashes
'''


import logging
import sys
import os
import re
try:
    from ruamel.yaml import YAML
    from docopt import docopt
except:
    print "Try pip install -r requirements.txt"
    exit(1)    
import glob
import socket
import string
import collections 