import csv
import argparse
import numpy as np
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", help="turn compression mode on", action="store_true")
    group.add_argument("-u", help="turn decompression mode on", action="store_true")
    group.required = True
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-p", "--path", action="store", dest="filepath", help="Path to the file",
                required=True)
    args = parser.parse_args()
    print(args.filepath)


