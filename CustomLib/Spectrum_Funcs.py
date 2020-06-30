# -*- coding: utf-8 -*-
"""
   Copyright 2020 DR ROBIN RAFFE PRYCE JONES
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from tkinter import filedialog
from tkinter import Tk
# Import ask save / open file and directory dialogue box library

import os
# Import os library for removing files

import re
# import the regular expression operations library for the scientific notation

import ntpath
# import the library for handling windows paths

def path_leaf(path):
    """ Function for splitting the file path"""
    head, tail = ntpath.split(path)
    return head, tail.split(".")[0] 

def Create_Directory(dirName):
    """Check and create a directory"""
    try:
        # Create target Directory
        os.mkdir(dirName)
        
    except FileExistsError:
        pass     
    
    if not os.path.exists(dirName):
        os.mkdir(dirName)

    else:    
        pass
    
def Get_Dir (Idir = None):
    "This uses tkinter to ask for the directory where the data is in text files"
    root = Tk();
    root.directory =  filedialog.askdirectory(initialdir = Idir, title = "Select directory/folder with the text data. Then hit import!");
    root.withdraw();
    return root.directory;

def Find_Line(File , Text_Search):
    """Function to find the line number where a string appears in the file """
    with open(File,'r') as f:
        content = f.readlines()

    index = [x for x in range(len(content)) if Text_Search in content[x]]
    f.close()
    return index

def Extract_NumberData(string):
    """ Function to import data in scientific notation """
    scinot = re.compile('[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)')
    List = [float(s) for s in re.findall(scinot, string)]
    return List

