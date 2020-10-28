#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""!@brief
    The ``argument`` module
    =======================

    This module pool command line called
"""

from argparse import ArgumentParser, RawTextHelpFormatter

__all__ = ['arguments']


def arguments():
    """!@brief
        Take arguments for file when it call by command line

        @return Namespace with options
    """
    # Define all parameters

    description = '''%s

  Created by Marcellino PALERME.
  Copyright 2020 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
It has to indicate which zone we keep.
-Keep up
-keep down
-Keep left
-Keep right
-keep a 'center' area (-a -u 74 -d 42 -l 90 -r 14)
-keep combination up-left (e.g. -u 40 -l 25) or right
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
    parser.add_argument("-l", "--commandline", dest="line", action="store_true",
                        default=False, help="use command line")

    # Directory where are images with barcode
    parser.add_argument("-i", "--input", dest="input", type=str, default=".",
                        help="Directory where are images with barode")

    # Directory where are file to modified
    parser.add_argument("-o", "--output", dest="output", type=str,
                        help="Directory where we save results", default="out")

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

    # Verify use only two zone for external mode
    if not args.area & ((args.up + args.down + args.left + args.right) > 2):
        parser.error("There is too much defined zone")

    return args
