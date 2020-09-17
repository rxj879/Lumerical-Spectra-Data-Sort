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

import glob, os
# Import library for reading, writing and removing files
 
import numpy as np
# Import the mathematical libraries

from CustomLib.Spectrum_Funcs import (Get_Dir, 
                                      Find_Line, 
                                      Create_Directory, 
                                      path_leaf, 
                                      Read_Line,
                                      Determine_ScaleFactor)
#Import custom functions required

from CustomLib.Spectrum_PickleJar import PickleJar
# Import the class for setting up preferences files

class DataClass_Spectra:
    """Class for multiple spectra to sort lumerical data"""
    
    def __init__(self):
        """Initialise require attributes"""
        self.Data_E_Field = []
        self.Data_H_Field = []
        self.FileName = []
        self.Directory = Get_Dir();
        self.NumOfFiles = int

    def Import_Data(self):
        """Lumerical Data"""
        os.chdir(self.Directory)
        self.NumOfFiles = np.size(glob.glob("*.txt"))

        for file in glob.glob("*.txt"):
            File_Path = self.Directory + "/" +file
            DIR , File_Name = path_leaf(File_Path)
            self.FileName.append(File_Name)
            Line_StartNumList = Find_Line(File_Path , 'Re(E)');
            Line_EndNumList = Find_Line(File_Path , 'spectrum');#
            Rows_to_Skip = Line_StartNumList[1] + 1
            Rows_to_End = Line_EndNumList[1] - Line_StartNumList[1] - 3
            Data=np.genfromtxt(file, delimiter = ',', skip_header = Rows_to_Skip, 
                               max_rows = Rows_to_End); 
            ColumnHeading1 = Read_Line(File_Path, Line_StartNumList[1])
            Scale_Factor = Determine_ScaleFactor(ColumnHeading1)
            Data[:,0] *= Scale_Factor
            self.Data_E_Field.append(Data)
            Line_StartNumList = Find_Line(File_Path , 'Re(H)');
            Rows_to_Skip = Line_StartNumList[1] + 1
            Data=np.genfromtxt(file, delimiter = ',', skip_header = Rows_to_Skip); 
            Data[:,0] *= Scale_Factor
            self.Data_H_Field.append(Data)

    def Write_New_Files(self):
        """Write the data to new files for the importing into the Spectra Plot program"""
        E_Field_File_Path = self.Directory + "/" + "E_Field"
        Create_Directory(E_Field_File_Path)
        PickleJar(E_Field_File_Path)
        
        H_Field_File_Path = self.Directory + "/" + "H_Field"
        Create_Directory(H_Field_File_Path)
        PickleJar(H_Field_File_Path)
        
        HEAD = '#Wave\t\t#Intensity'
        
        for i in range(0,self.NumOfFiles):
            E_Field_File_i = E_Field_File_Path + "/"  + self.FileName[i] + '_E_Field.txt'
            np.savetxt(E_Field_File_i, self.Data_E_Field[i],  fmt='%10.3f',
                       delimiter='\t', newline='\n', comments='',
                       header=HEAD, encoding=None)
            H_Field_File_i = H_Field_File_Path + "/"  + self.FileName[i] + '_H_Field.txt'
            np.savetxt(H_Field_File_i, self.Data_H_Field[i],  fmt='%10.3f',
                       delimiter='\t', newline='\n', comments='',
                       header=HEAD, encoding=None)