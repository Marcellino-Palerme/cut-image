#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""!@brief
    The ``argument`` module
    =======================

    This module pool command line called
"""

from argparse import ArgumentParser, RawTextHelpFormatter
from os.path import abspath
import sys

__all__ = ['arguments']


def arguments():
    """!@brief
        Take arguments for file when it call by command line

        @return Namespace with options
    """
    # Define all parameters

    description = '''%s

  Created by Marcellino PALERME.
  Copyright 2020 INRAE. All rights reserved.

  Licensed under CeCILL 2.1
  https://cecill.info/licences/Licence_CeCILL_V2.1-fr.html
  https://cecill.info/licences/Licence_CeCILL_V2.1-en.html

USAGE
It has to indicate which zone we keep.
-Keep up
-keep down
-Keep left
-Keep right
-keep a 'center' area (-a -u 74 -d 42 -l 90 -r 14)
-keep combination up-left (e.g. -u 40 -l 25)
-Keep combination down-left or right (e.g. -d 80 -r 75)

Several combinations in same time is impossible instead of use area
The value of pixel after option is number of lines or rows of pixel to keep
from a side of image. For example image 800*600 if we have -b 100 we obtain
a image 800*100 and keep the down of image.
With area option, we delete lines or rows indicate by others option.For example
image 800*600 if we have -a -b 100 we obtaina image 800*700 and keep the up of
image.

'''

    parser = ArgumentParser(conflict_handler='resolve', description=description,
                            formatter_class=RawTextHelpFormatter)

    # use command line
    parser.add_argument("-c", "--commandline", dest="line", action="store_true",
                        default=False, help="use command line")

    # Directory where are images with barcode
    parser.add_argument("-i", "--input", dest="input", type=str, default=".",
                        help="Directory where are images with barode")

    # Directory where are file to modified
    parser.add_argument("-o", "--output", dest="output", type=str,
                        help="Directory where we save results", default="./out")

    # option to define a zone to keep
    parser.add_argument("-a", "--area", dest="area", default=False,
                        action="store_true", help="keep a area of images")
    parser.add_argument("-u", "--up", dest="up", help="", default=0, type=int)
    parser.add_argument("-d", "--down", dest="down", help="", default=0,
                        type=int)
    parser.add_argument("-l", "--left", dest="left", help="", default=0,
                        type=int)
    parser.add_argument("-r", "--right", dest="right", help="", default=0,
                        type=int)


    # Take value of arguments
    args = parser.parse_args()

    # Verify parameters only in command line
    if not args.line:
        return args

    nb_direction = (int(args.left > 1) + int(args.right > 1) +
                    int(args.up > 1) + int(args.down > 1))

    # miss direction to cut
    if nb_direction == 0:
        parser.error("Miss a direction")

    # in mode external no choice opposite direction
    if not args.area and (((args.left > 1) and (args.right > 1)) or
                           ((args.up > 1) and (args.down > 1))):
        parser.error("use opposite direction")

    # protection of overwrite
    args.input = abspath(args.input)
    args.output = abspath(args.output)
    if args.input==args.output:
        answer = input("You are about overwrite your files. Continue: y/n? ")

    if answer!='y' or answer!='Y':
       sys.exit(0)

    return args
