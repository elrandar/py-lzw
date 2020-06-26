import csv
import argparse
import sys
import math
from pathlib import Path

def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper


def binary(str, nb_bits):
    print(str)
    binstr = bin(int(str))[2:]
    while (len(binstr) < nb_bits):
        binstr = '0' + binstr
    return binstr


def build_dico(filestring, filepath):
    ascii_occ = [0] * 256
    ascii_occ[ord('%')] = 1

    charnb = 0
    for char in filestring:
        if (char != '\n'):
            ascii_occ[ord(char)] = 1
            charnb += 1
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
    f = open(filepath + "_dico.csv", "w")
    f.write(str)
    f.close()

    return dict, counter - 1, charnb


def compress(filepath):
    p = Path(filepath)
    toto = p.stem


    f = open(filepath, "r")
    dict, counter, chars_in_input = build_dico(f.read(), toto)
    f.seek(0, 0)

    # First we have to build the dictionary, going through
    # the whole file, puttings the characters encountered
    # and sorting them in the lexicographical order

    bits = counter.bit_length()
    initial_bits = bits
    nb_bits_comp = 0
    output = ""
    buffer = ""
    input = f.read(1)

    with open(toto + "_LZWtable.csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Buffer", "Input", "New sequence", "Address", "Output"])

        while True:

            LZWrow = [None] * 5
            LZWrow[1] = input

            if (input == '\n'):
                input = f.read(1)
                continue

            if (buffer != ""):
                LZWrow[0] = buffer
                if buffer + input in dict:
                    if (bits < dict[buffer + input].bit_length()):
                        LZWrow[4] = "@[%]=" + str(dict['%'])
                        output += binary(dict["%"], bits)
                        nb_bits_comp += bits
                        bits += 1
                    buffer += input
                else:
                    counter += 1
                    LZWrow[2] = buffer + input
                    LZWrow[3] = counter
                    dict[buffer + input] = counter
                    output += binary(dict[buffer], bits)
                    LZWrow[4] = "@[" + buffer + "]=" + str(dict[buffer])
                    nb_bits_comp += bits
                    buffer = input
            else:
                buffer = input
            input = f.read(1)
            if (input == ''):
                if buffer != "":
                    output += binary(dict[buffer], bits)
                    LZWrow[4] = "@[" + buffer + "]=" + str(dict[buffer])
                    nb_bits_comp += bits
                writer.writerow(LZWrow)
                break
            else:
                writer.writerow(LZWrow)

    f.close()

    nb_bits_before = chars_in_input * initial_bits

    ratio = nb_bits_comp / float(nb_bits_before)
    ratio = truncate(ratio, 4)
    output += '\n' + "Size before LZW compression: " + str(nb_bits_before) + " bits\n"
    output += "Size after LZW compression: " + str(nb_bits_comp) + " bits\n"
    output += "Compression ratio: " + str(ratio)
    print(output)

    f = open(toto + ".lzw", "w")
    f.write(output)
    f.close

    print(nb_bits_before)
    print(nb_bits_comp)

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
    if (args.bool_comp):
        compress(args.filepath)
    else:
        uncompress(args.filepath)

