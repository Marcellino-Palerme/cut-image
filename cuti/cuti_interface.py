#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module provide the interface class
"""

import logging
from tkinter import Tk, IntVar, StringVar, Spinbox, BooleanVar
from tkinter.filedialog import askdirectory, askopenfilename
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo, showerror, askyesno, showwarning
from os.path import basename


def choose_dir(old_dir):
    """!@brief
        Generic function to choose a directory

        @param old_dir (str)
            Old path of directory

        @return (str)
            Path of choose directory
    """
    temp_str = askdirectory()

    # https://stackoverflow.com/questions/15010461/askopenfilename-handling-cancel-on-dialogue
    if not temp_str:
        temp_str = old_dir
    return temp_str


def choose_file(old_file, **args):
    """!@brief
        Generic function to choose a file

        @param old_file (str)
            Old path of file

        @param args (**)
            Parameters of askopenfilename

        @return (str)
            Path of choose file
    """
    temp_str = askopenfilename(**args)

    # Verify if click on cancel
    if not temp_str:
        temp_str = old_file
    return temp_str


def disable_elemens(part):
    """!@brief
        disable all element of part

        @param part (tk object)
            graphical part
    """
    for child in part.winfo_children():
        # we can't disable scrollbar and frame
        if ('scrollbar' not in child._name and
            'frame' not in child._name):
            child.configure(state='disabled')


def enable_elemens(part):
    """!@brief
        enable all element of part

        @param part (tk object)
            graphical part
    """
    for child in part.winfo_children():
        # we can't enable scrollbar and frame
        if ('scrollbar' not in child._name and
            'frame' not in child._name):
            child.configure(state='normal')


def reduce_path(path):
    """!@brief
       reduce path of directory to keep only name of directory
       
       @param path (str)
           complete path
    """
    return '... ' + basename(path)
    
    
    
class CutiInterface (Tk):
    """!@brief
        define global windows
    """
    # Class of global windows
    direction = ["left", "right", "up", "down"]

    def __init__(self, argument, send_pipe=None, recv_pipe=None, parent=None):
        """!@brief
            constructor

            @param argument (namespace)
                namespace of arguments
            @param send_pipe
                sender of argument to execution
            @param recv_pipe
                reciever of result from execution
            @param parent : object
                whose called
        """
        logging.debug("IN")
        # Create Windows
        Tk.__init__(self, parent)
        self.option_add("*background", "white", 100)
        self.parent = parent
        self.args = argument
        self.send_pipe = send_pipe
        self.recv_pipe = recv_pipe
        # State of interface
        self.execute = False
        self.advice = False
        row = 0

        # Input directory
        ttk.Label(self, text="Input Directory").\
            grid(column=0, row=row, columnspan=2, sticky='W')
        row += 1

        ttk.Button(self, text="...", command=self.choose_dir_i).\
                   grid(column=0, row=row, sticky='W')
        self.input = StringVar(value=".")
        self.input_show = StringVar(value=self.input.get())
        ttk.Label(self, textvariable=self.input_show,
                  wraplength=1200, style='path.TLabel').\
            grid(column=1, row=row, columnspan=5, sticky="W")
        row += 1

        # Output directory
        ttk.Label(self, text="Output Directory").\
            grid(column=0, row=row, columnspan=2, sticky='W')
        row += 1

        ttk.Button(self, text="...", command=self.choose_dir_o).\
                   grid(column=0, row=row, sticky='W')
        self.output = StringVar(value=self.input.get())
        self.output_show = StringVar(value=self.input.get())
        ttk.Label(self, textvariable=self.output_show,
                  wraplength=1200, style='path.TLabel').\
            grid(column=1, row=row, columnspan=5, sticky="W")
        row += 1

        # mode of cuti
        self.area = BooleanVar(value=False)
        rb_area = ttk.Radiobutton(self, text="external", variable=self.area,
                                  value=False, command=self.verify_all_disable)
        rb_area.grid(column=1, row=row)
        rb_area.select()
        ttk.Radiobutton(self, text="area",
                        variable=self.area, value=True,
                        command=self.verify_all_disable).grid(column=2, row=row)

        row += 1

        # zones
        self.dict_zone = {}
        for direction in self.direction:
            self.dic_zone[direction + "_state"] = IntVar(value=0)
            ttk.Checkbutton(self, text=direction, 
                            command=lambda : self.change_direction(direction)
                            variable=self.dic_zone[direction + "_state"]).\
                            grid(column=0, row=row)
            self.dic_zone[direction] = StringVar(value="0")
            self.dic_zone[direction + "_sp"] = Spinbox(self, from_=0, width=4,
                                                       textvariable=self.left)
            self.dic_zone[direction + "_sp"].grid(column=2, row=row)

            row += 1

        # Create Launcher part
        self.launch = ttk.Frame(self.parent)
        self.launch.grid(column=0, row=row, sticky="N", columnspan=9)
        self.gowait = ttk.Button(self.launch, text="GO",
                                 command=self.star_execute)
        self.gowait.grid(column=4, row=row, columnspan=2)

        # Capture closed windows
        self.protocol("WM_DELETE_WINDOW", self.close)
        logging.info("OUT")

        self.verify_all_disable()


    def choose_dir_i(self):
        """!@brief
            Take directory for input
        """
        logging.debug("IN")
        logging.debug(self.input.get())

        self.input.set(choose_dir(self.input.get()))
        self.input_show.set(reduce_path(self.input.get()))
        
        # TODO : while output not modify use value of input 

        logging.debug("OUT")

    def choose_dir_o(self):
        """!@brief
            Take directory for output
        """
        logging.debug("IN")
        logging.debug(self.output.get())

        self.output.set(choose_dir(self.output.get()))
        self.output_show.set(reduce_path(self.output.get()))

        logging.debug("OUT")

    def change_direction(self, direction):
        """!@brief
            Enable or disable a zone
            @param direction : str
                left, right, up, down
        """
        if self.dic_zone[direction + "_state"].get() == 1:
            self.dic_zone[direction + "_sp"].configure(state='normal')
        else:
            self.dic_zone[direction + "_sp"].configure(state='disabled')

        self.verify_all_disable()
        

    def star_execute(self):
        """!@brief
            all actions when click on button GO
            disable all elements
            launch waiting bar
            take all configuration parameters
            launch execution
        """
        logging.debug("IN")
        # Take size of windows
        width_win = self.winfo_width()
        # Delete GO Button
        self.gowait.destroy()
        # Create progessbar
        self.gowait = ttk.Progressbar(self.launch, mode='indeterminate',
                                      length=width_win)
        self.gowait.grid(column=0, row=18, columnspan=8)
        self.gowait.start(20)
        
        # Indicate start of execution
        self.execute = True
        
        # Disable all configuration part
        disable_elemens(self)

        # Affect all parameters
        args = self.args
        args.input = self.input.get()
        args.output = self.output.get()
        args.area = self.area.get()

	# https://stackoverflow.com/questions/16878315/what-is-the-right-way-to-treat-python-argparse-namespace-as-a-dictionary/16878364#16878364
	# take value of each direction
	d_args = vars(args)     
	for direction in self.direction:
	    if self.dict_zone[direction + "_state"].get() == 1:
	        d_args[direction] = int(self.dict_zone[direction])
	    else:
	    	d_args[direction] = 0

        # send all parameters
        self.send_pipe.send(args)

        # Verify if execution finished
        self.after(20, self.maj)

        logging.debug("OUT")

    def maj(self):
        """!@brief
            Verify if execution finished
        """
        self.update()

        if self.execute == True:
            # verify if execution sent the result
            if self.recv_pipe.poll(0.01) is True:
                logging.info("it captured end execution")
                # take result of execute
                val = self.recv_pipe.recv()
                # show the result
                if val[0] == "Done":
                    showinfo(val[0], val[1])
                else:
                    showerror(val[0], val[1])
                # Put interface in configuration state
                self.finish_execute()

        # restart in 20ms the verification
        self.after(20, self.maj)
            

    def finish_execute(self):
        """!@brief
            Put interface in configuration state
        """
        logging.debug("IN")

        # Delete ProgressBar
        self.gowait.destroy()
        # Put GO Button
        self.gowait = ttk.Button(self.launch, text="GO",
                                 command=self.star_execute)
        self.gowait.grid(column=4, row=18, columnspan=2)
        self.update()
        # Enable all configuration part
        enable_elemens(self)
        self.change_valid()
        
        # Indicate end of execution
        self.execute = False

        logging.debug("OUT")

    def close(self):
        """!@brief
            close application
        """
        logging.debug("IN")

        # Ask confirmation
        if askyesno("Quit", "Do you really wish to quit?"):
            # Kill the execution if it is running
            if hasattr(self, "thread"):
                if self.thread.isAlive():
                    self.thread._Thread__stop()
            # Close all
            self.destroy()

        logging.debug("OUT")

    def verify_all_disable(self):
        """!@brief
            disable GO button if number of selected directions isn't correct
        """
        # Take number of selected directions
	nb_direction = 0
        for direction in self.direction:
        	nb_direction = nb_direction + 
        	               self.dict_zone[direction + "_state"].get()
        	          
        if (self.area.get() and nb_direction < 3 ) or
           (!self.area.get() and nb_direction > 2)

            disable_elemens(self.launch)
        else:
            enable_elemens(self.launch)


