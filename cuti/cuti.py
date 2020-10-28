#!/usr/bin/env python
# encoding: utf-8
'''
    This module provide functions to cut images
'''

from skimage import io
from os.path import dirname
from .tools_file import create_directory


__all__ = ['cut_image_ext', 'cut_image_area']
__version__ = 1.1
__date__ = '2018-01-25'
__updated__ = '2020-10-28'


def cut_image_ext(file_in,
                  file_out,
                  up_side=0,
                  down_side=0,
                  left_side=0,
                  right_side=0):
    """!@brief
        keep a side of image or combination left-up, left-down , right-up or
        right-down

        @param file_in (str) path of image
        @param file_out (str) path to save cut image
        @param up_side (int) number pixel keep to up images
        @param down_side (int) number pixel keep to down images
        @param left_side (int) number pixel keep to left images
        @param right_side (int) number pixel keep to right images
    """
    # Take image
    my_image = io.imread(file_in, plugin="matplotlib")

    # Create out directory
    create_directory(dirname(file_out))

    # Define variable to cut as we keep entire image
    size = my_image.shape[:2]
    im_up = 0
    im_down = size[0]
    im_left = 0
    im_right = size[1]

    # Keep up
    if up_side > 0:
        im_down = min(up_side, im_down)
    # Keep down
    elif down_side > 0:
        im_up = max(size[0] - down_side, 0)

    # Keep left
    if left_side > 0:
        im_right = min(left_side, im_right)
    # keep right
    elif right_side > 0:
        im_left = max(size[1] - right_side, 0)

    # Save new image
    io.imsave(file_out,
              my_image[im_up:im_down, im_left:im_right, :],
              plugin='pil')


def cut_image_area(file_in,
                   file_out,
                   up_side=0,
                   down_side=-1,
                   left_side=0,
                   right_side=-1):
    """!@brief
        keep a area of image

        @param file_in (str) path of image
        @param file_out (str) path to save cut image
        @param up_side (int) number pixel cut to up images
        @param down_side (int) number pixel cut to down images
        @param left_side (int) number pixel cut to left images
        @param right_side (int) number pixel cut to right images
    """
    # take image
    my_image = io.imread(file_in, plugin="matplotlib")

    # Create out directory
    create_directory(dirname(file_out))

    # Define variable to cut as we keep entire image
    size = my_image.shape[:2]
    im_up = 0
    im_down = size[0]
    im_left = 0
    im_right = size[1]

    # superposition case
    if (up_side + down_side) >= size[0]:
        temp = up_side
        up_side = size[0] - down_side
        down_side = size[0] - temp
    if (left_side + right_side) >= size[1]:
        temp = left_side
        left_side = size[1] - right_side
        right_side = size[1] - temp

    # Define up of area
    if up_side > 0:
        im_up = min(up_side, size[0])
    # Define down of area
    if down_side > 0:
        im_down = max(size[0] - down_side, 0)
    # Define left of area
    if left_side > 0:
        im_left = min(left_side, size[1])
    # Define right of area
    if right_side > 0:
        im_right = max(size[1] - right_side, 0)

    # save new image
    io.imsave(file_out,
              my_image[im_up:im_down, im_left:im_right, :],
              plugin='pil')
