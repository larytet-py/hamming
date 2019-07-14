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
    hamming.py -f hashes.txt -d 32
   
Options:
  -h --help                 Show this screen.
  -f --file=<FILENAME>    Data set
  -d --distance=<MAXDISTANCE>      Max distance between hashes
'''


import operator 
import multiprocessing
import random
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


def bit_count(n, max):
    count = 0
    while n > 0:
        if (n & 1 == 1): count += 1
        if count > max:
          break
        n >>= 1
    return count

def nCr(n,r):
    r = min(r, n-r)
    numer = functools.reduce(operator.mul, range(n, n-r, -1), 1)
    denom = functools.reduce(operator.mul, range(1, r+1), 1)
    return numer / denom

def update_dict(distances, hashes, c1, c2, distance):
  if not hashes is None:
    if not c1 in hashes.keys():
      hashes[c1] = []
    hashes[c1].append((c2, distance))

  if not distance in distances.keys():
    distances[distance] = 1
  else:
    distances[distance] = distances[distance] + 1

def plot_distances(distances, total, step = 5):
  plot_list = []
  for distance in distances:
    distance_normalize = distance/step
    while len(plot_list) <= distance_normalize:
      plot_list.append(0)
    plot_list[distance_normalize] += distances[distance]

  #logger.info("Plotting {0} {1}".format(plot_list, distances))
  i = 0
  s = "\nHamming distance/Count/% of total\n"
  while i < len(plot_list):
    count = plot_list[i]
    s = s + ("{0:4}-{1} {2} {3:2.4f}\n".format(i*5, (i+1)*5-1, count, (1.0*count)/total*100))
    i += 1
  logger.info(s)
       

def hamming(data_set, max_distance):
  '''
  Create dictionary of hashes with hamming distance less than max_distance
  '''
  combinations = nCr(len(data_set), 2)
  logger.info("Brute force {0} pairs for distances below {1}".format(combinations, max_distance+1))
  d = None # {}
  count = 0
  start_time = time.time()
  distances = {}
  for c in itertools.combinations(data_set, 2):
    count += 1
    xor_result = c[0] ^ c[1]
    bc = bit_count(xor_result, max_distance+1)
    if bc <= max_distance:
      update_dict(distances, d, c[0], c[1], bc)
      logger.debug("Found {0},{1} distance={2}".format(hex(c[0]).upper(), hex(c[1]).upper(), bc))
    if count & 0x7FFF == 0:
      elapsed_time = time.time()- start_time
      rate = (1.0*count)/elapsed_time
      expected_completion = (combinations-1.0*count)/rate
      completed = 100.0*count/combinations
      logger.info("Completed {0} from {1} {2:.4f}% at rate {3} completion in {4:.2f} hours".format(
        count, combinations, completed, rate, expected_completion/3600))
      plot_distances(distances, count)
  return d, distances



def read_data_set(f):
  '''
  Read the file line by line, convert hexadecimals to intergs, return the list
  '''
  data = []
  for l in f:
    l = "0x"+l.strip().lower()
    value = int(l, 16)
    value_str = hex(value)
    if l+"L" != value_str:
      logger.error("Bad conversion {0} {1}".format(l, value_str))
    data.append(value)

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

        max_distance = 3
        if not distance_arg is None:
          max_distance = int(distance_arg)


        result, f = open_file(data_file, "r")
        if not result:
          break        
        
        data_set = read_data_set(f)
        random.shuffle(data_set)
        data_set_size = len(data_set)
        if data_set_size == 0:
          logger.debug("No data in the input file {0}".format(data_file))
          break
        else:
          logger.debug("Read {0} hashes. First hash {1}".format(len(data_set), hex(data_set[0])))

        cpus = multiprocessing.cpu_count()
        cpus = 1
        started_jobs = []
        for cpu in range(cpus):          
          data_cpu_set_size = data_set_size/cpus
          start = data_cpu_set_size * cpu
          stop = data_cpu_set_size * (cpu+1)
          cpu_set = data_set[start:stop]
          job = multiprocessing.Process(target=hamming, args=(cpu_set, max_distance, ))
          started_jobs.append(job)
          job.start()
          for job in started_jobs:
            job.join()
        break
