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
from docopt import docopt

def open_file(filename, flags, print_error=True):
    '''
    Open a text file 
    Returns handle to the open file and result code False/True
    '''
    try:
        file_handle = open(filename, flags) 
    except Exception:
        if print_error:
            logger.error('Failed to open file {0} {1}'.format(filename, sys.exc_info()))
        return (False, None)
    else:
      return (True, file_handle) 

def hamming(data_set, max_distance):
  '''
  Create dictionary of hashes with hamming distance less than max_distance
  '''
  pass



def read_data_set(f):
  '''
  Read the file line by line, convert hexadecimals to intergs, return the list
  '''
  data = []
  for l in f:
    data.append(int(l, 16))

  return data

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.1')
    logging.basicConfig()    
    logger = logging.getLogger('hamming')
    logger.setLevel(logging.INFO) 


    data_file = arguments['--file']
    distance_arg = arguments['--distance']

    while True:

        if data_file is None:
          logger.info("Nothing to do")
          break

        max_distance = 32
        if not distance_arg is None:
          max_distance = int(distance_arg)


        result, f = open_file(data_file, "r")
        if not result:
          break        
        
        data_set = read_data_set(f)
        logger.debug("Read {0} hashes".format(len(data_set)))
        hamming_distances = hamming(f, max_distance)
        break

