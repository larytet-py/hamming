#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''hamming.py

Read hashes from the file
Create a dictionary of all hashes with distances below certain threshold  

Usage:
  hamming.py -h | --help
  hamming.py -f <FILENAME> [-d <MAXDISTANCE>] 
Example:
    hamming.py -f hashes.txt
   
Options:
  -h --help                 Show this screen.
  -f --file=<FILENAME>    Data set
  -d --distance=<MAXDISTANCE>      Max distance between hashes
'''


import operator 
import functools 
import time
import logging
import sys
import os
import re
from docopt import docopt
import itertools
import math

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


def bit_count(n):
    count = 0
    while n > 0:
        if (n & 1 == 1): count += 1
        n >>= 1
    return count

def update_dict(d, c1, c2, distance):
  if not c1 in d.keys:
    d[c1] = []
  d[c1].append((c2, distance))

def nCr(n,r):
    r = min(r, n-r)
    numer = functools.reduce(operator.mul, range(n, n-r, -1), 1)
    denom = functools.reduce(operator.mul, range(1, r+1), 1)
    return numer / denom

def hamming(data_set, max_distance):
  '''
  Create dictionary of hashes with hamming distance less than max_distance
  '''
  combinations = nCr(len(data_set), 2)
  logger.info("Brute force {0} pairs".format(combinations))
  d = {}
  count = 0
  start_time = time.time()
  for c in itertools.combinations(data_set, 2):
    xor_result = c[0] ^ c[1]
    bc = bit_count(xor_result)
    if bc <= max_distance:
      update_dict(d, c[0], c[1], bc)
      logger.info("Found {0},{1} distance={2}".format(c[0], c[1], bc))
    count += 1
    if count & 0x7FFF == 0:
      elapsed_time = time.time()- start_time
      rate = count/elapsed_time
      expected_completion = (combinations-count)/rate
      logger.debug("Completed {0} from {1} at rate {2} completion in {3:.2f} hours".format(count, combinations, rate, expected_completion/3600))

  return d



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
    logger.setLevel(logging.DEBUG)


    data_file = arguments['--file']
    distance_arg = arguments['--distance']

    while True:

        if data_file is None:
          logger.info("Nothing to do")
          break

        max_distance = 3
        if not distance_arg is None:
          max_distance = int(distance_arg)


        result, f = open_file(data_file, "r")
        if not result:
          break        
        
        data_set = read_data_set(f)
        data_set_size = len(data_set)
        if data_set_size == 0:
          logger.debug("No data in the input file")
          break
        else:
          logger.debug("Read {0} hashes. First hash {1}".format(len(data_set), hex(data_set[0])))

        hamming_distances = hamming(data_set, max_distance)
        hamming_distances_size = len(hamming_distances)
        if hamming_distances_size == 0:
          logger.debug("No pairs found for maximum distance {0}".format(max_distance))
          break

        logger.info("Found {0} pairs:\n{1}".format(hamming_distances_size, hamming_distances))
        break
