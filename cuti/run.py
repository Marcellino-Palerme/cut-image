#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    The 'run' module
    ===============

    The module provide graphical interface or command line to use cuti
"""

from os.path import join, splitext, abspath
from cuti import create_directory, file_list, copy, arguments,\
                 cut_image_ext, cut_image_area, EmptyImage 
import logging
import cuti.cuti_interface as ci
from multiprocessing import Pipe, Process, freeze_support
from time import strftime, localtime
import shutil


__all__ = ['run']


def save_error(dir_input, dir_output, in_file, msg, i_log=None):
    """!@brief
        Save file have a problem and indicate the problem in log
        
        @param dir_input: str
            directory where is the file
        @param dir_output: str 
            output directory to save error
        @param file: str
            Name of rejected file
        @param msg: str
            reason of rejected
        @param i_log: str (optional)
            Name of log file
        @return: str
            Name of log file
    """
    logging.debug("IN")
    # create output directory
    create_directory(dir_output)
    # create error directory
    create_directory(join(dir_output, "error"))
    
    # Copy file in error directory
    shutil.copy2(join(dir_input, in_file), join(dir_output, "error"))
    
    o_log = i_log
    
    # Verify if i_log empty or not create
    if i_log is None or i_log not in file_list(dir_output):
        # https://www.jquery-az.com/python-datetime-now/
        o_log = strftime("%Y%m%d%H%M%S", localtime()) + '_log.txt'
    
    # Write error message in log file
    with open(join(dir_output,o_log), 'a') as f_log : 
        f_log.write(in_file + " : " + msg + "\n")    
    
    return o_log
    
    logging.debug("OUT")
    
    
def execute(my_args):
    """!@brief
        Execute functions of foma

        @param my_args All arguments to call functions of foma
    """
    logging.debug("IN")
    
    # Used absolu path
    my_args.input = abspath(my_args.input)
    my_args.output = abspath(my_args.output)
    
    # Create output directory
    create_directory(my_args.output)
    
    # Take all file of input directory
    in_files = file_list(my_args.input)
    log = None
    
    if my_args.area:
       used_function = cut_image_area
    else :
       used_function = cut_image_ext
    
    for my_file in in_files:
        try:
            used_function(file_in=join(my_args.input, my_file),
                          file_out=join(my_args.output, my_file),
                          left_side=my_args.left,
                          right_side=my_args.right,
                          up_side=my_args.up,
                          down_side=my_args.down)
        # Case we create a empty image
        except EmptyImage:
            log = save_error(my_args.input, my_args.output, my_file,
                             "Create a empty image", log)
            continue
        # We can't read the file like image
        except IOError:
            log = save_error(my_args.input, my_args.output, my_file,
                             "File isn't a image", log)
            continue
       
    logging.debug('OUT')


def execute_proc(recv_pipe, send_pipe):
    """!@brief
        process of execution

        @param recv_pipe reciever of arguments provide by interface
        @param send_pipe sender of result of execution
    """
    logging.debug("IN")
    while 1:

        args = recv_pipe.recv()
        try:
            execute(args)
            send_pipe.send(("Done", "Execution Done"))
        except Exception as my_error:
            logging.error("Global error catch ", exc_info=True)
            send_pipe.send(("Error", my_error))

    logging.debug("OUT")

def interface_proc(argument, send_pipe, recv_pipe):
    """!@brief
        Process of graphical interface

        @param argument
        @param send_pipe sender of argument to execution
        @param recv_pipe reciever of result from execution
    """
    logging.debug("IN")
    app = ci.CutiInterface(argument=argument, send_pipe=send_pipe, 
                           recv_pipe=recv_pipe)
    app.title("CUTI")
    app.mainloop()
    logging.debug("OUT")


def run():
    """!@brief
        Run cuti
    """
    # Configuration of logging
    my_format = '%(asctime)s--%(funcName)s--%(levelname)s: %(message)s'
    logging.basicConfig(format=my_format, filename='cuti.log',
                        level=logging.DEBUG, filemode='w')
    
    # Take all argument when run called by shelll
    my_args = arguments()

    # Use cab by graphical interface
    if my_args.line is False:
        # Create communication between two process
        int2ex_i, int2ex_o = Pipe()
        ex2int_i, ex2int_o = Pipe()
        # Initialize two process
        my_ex = Process(target=execute_proc, kwargs={"recv_pipe": int2ex_o,
                                                     "send_pipe": ex2int_i})
        my_inter = Process(target=interface_proc,
                           kwargs={"argument": my_args,
                                   "send_pipe": int2ex_i,
                                   "recv_pipe": ex2int_o})
        # Star two process
        my_ex.start()
        my_inter.start()
        my_inter.join()
        my_ex.terminate()

    # Use cab by command line
    else:
        execute(my_args)


if __name__ == "__main__":
    # necessary when we freeze with windows multiprocessing
    freeze_support()
    run()
