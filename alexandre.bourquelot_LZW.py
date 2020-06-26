import csv
import argparse
import numpy as np
import sys


def build_dico(filestring, filepath):
    ascii_occ = [0] * 256
    ascii_occ[ord('%')] = 1

    for char in filestring:
        if (char != '\n'):
            ascii_occ[ord(char)] = 1

    dict = {}
    counter = 0
    str = ""
    for i in range(256):
        if (ascii_occ[i] == 1):
            if str != "":
                str += ','
            str += chr(i)
            dict[chr(i)] = counter
            counter += 1
    str += '\n'
    f = open(filepath[0:-4] + "_dico.csv", "w")
    f.write(str)
    f.close()

    return dict


def compress(filepath):

    f = open(filepath, "r")
    dict = build_dico(f.read(), filepath)

    # First we have to build the dictionary, going through
    # the whole file, puttings the characters encountered
    # and sorting them in the lexicographical order




    # Init the buffer = []
    # Then while the input is not empty
    #   input = next character
    #   if buffer not empty
    #       we check that the concat of buffer and input is in dictionary
    #       if it is
    #           if the current number of bits is not enough to write its
    #           corresponding adress, we write % to output
    #       else we add an entry for this character chain
    #   we write
    #
    #       D[buffer.tostring].tobinary(bits) to the output
    #   buffer = input


    pass

def uncompress(filepath):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", help="turn compression mode on", action="store_true", dest="bool_comp")
    group.add_argument("-u", help="turn decompression mode on", action="store_false")
    group.required = True
    required_named = parser.add_argument_group('required named arguments')
    required_named.add_argument("-p", "--path", action="store", dest="filepath", help="Path to the file",
                required=True)
    args = parser.parse_args()
    print(args.filepath)
    print(args.bool_comp)
    if (args.bool_comp):
        compress(args.filepath)
    else:
        uncompress(args.filepath)

