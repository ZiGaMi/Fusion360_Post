# ===============================================================================
# @file:    main.py
# @note:    Fusion360 different tools G-code merging script
# @author:  Ziga Miklosic
# @date:    09.02.2022
# @brief:   This scripts merge together all selected G-code generated files
#           that are being post separately due to Fusion360 free licence limitation.
#
#           End script is result of concatanation of tool paths with different
#           milling jobs. Start and end of script stays the same only tool 
#           path section will be copied to the end script.
# ===============================================================================

# ===============================================================================
#       IMPORTS  
# ===============================================================================
import sys
import os
import time
import shutil

import subprocess
import xml.etree.ElementTree as ET

from file_manager import FileManager

# ===============================================================================
#       CONSTANTS
# ===============================================================================

# SCript version
SCRIPT_VERSION = "V0.0.1"

# Supported G-code file extension
SUPPORT_FILE_END = ".tap"

# Show merge script at end of program
OPEN_END_SCRIPT = True

# Debug enabled
DEBUG_EN = True


# ===============================================================================
#       FUNCTIONS
# ===============================================================================

# ===============================================================================
# @brief:   Debug mode prints
#
# @param[in]:    msg    - Debug message
# @return:       void 
# ===============================================================================
def dbg_print(msg):
    if DEBUG_EN:
        print(msg)

# ===============================================================================
# @brief:   Introduction text
#
# @return:       void 
# ===============================================================================
def intro():
    os.system("cls")
    print("===================================================================")
    print("     Fusion360 G-code Merging script")
    print("")
    print(" Version: %s" % SCRIPT_VERSION )
    print("===================================================================")
    print("")

        


def get_g_files(work_dir):

    g_files = []

    # Check if dir exist
    if os.path.isdir( work_dir ):

        # Get interresting files
        print("")
        print("List of G-code files (filter: *%s)" % SUPPORT_FILE_END )
        print("---------------------------------------------------------")
        for file in os.listdir( work_dir ):

            # Get file name and extension
            file_name, file_extension = os.path.splitext( file )

            # Filter files
            if SUPPORT_FILE_END == file_extension:
                print( " [%s] %s" % ( len(g_files)+1, file ))
                g_files.append(work_dir + "\\" + file)

        print("\n")

    else:
        print("ERROR: Inputed directory does not exist!")

    return g_files


# ===============================================================================
# @brief:  Main entry function
#
# @return:       void
# ===============================================================================
def main():
    
    # Intro 
    intro()

    # Get working directory
    work_dir = input( "Input working directory: " )

    # Get g-code files
    g_files = get_g_files( work_dir )

    # Open 1# file
    g_file_0 = FileManager( g_files[0])
    
    # Merged file
    g_file_merged = FileManager( work_dir + "\\out\\" + "Merged.tap")
    g_file_merged.erase()




    # Close files
    g_file_0.close()
    g_file_merged.close()

    # Create parser
    #parser = GcodeParser()

    #tool = ExtTool()
    #tool.open_file( "test" )

    input("\n\nPress any key to exit...\n")





# ===============================================================================
#       CLASSES
# ===============================================================================

# ===============================================================================
# @brief:  External tool class
#
#   Using external tool for visualization
#
# ===============================================================================
class ExtTool:
    
    # ===============================================================================
    # @brief:  Constructor
    #
    # @return:       void
    # ===============================================================================
    def __init__(self):

        # Get all listed tools in file
        self.__read_tools()


    # ===============================================================================
    # @brief:  Read XML file for external tool details
    #
    # @return:       data           - CAN payload 
    # ===============================================================================
    def __read_tools(self):

        # Get current directory
        cwd = str( os.getcwd() )

        # Assemble path
        file_path = cwd + "\external_tools.xml"

        try:
            # Read XML file
            tree = ET.parse( file_path )
            root = tree.getroot()

            # Get name, target and path location
            self.tool_name = root.find('Name').text
            self.tool_target = root.find('Target').text

        except:
            # If no file is found, use default windows editor
            self.tool_target = "notepad.exe"

    # ===============================================================================
    # @brief:  Open file with defined external tool
    #
    # @param[in]:   file - File to display
    # @return:      void 
    # ===============================================================================
    def open_file(self, file):
        try:
            subprocess.Popen(str(self.tool_target + " " + str(file)))
        except:
            subprocess.Popen(str("notepad.exe " + str(file)))


# ===============================================================================
# @brief:  G-code Parser
#
# ===============================================================================
class GcodeParser:

    def __init__(self):
        
        # List of interesting files
        self.g_code_files = []

        # Get files
        self.__get_files()

        # Create new merged file
        self.__create_new_file()

        # Merge files
        self.__merge_files()

        # Clean
        self.__clean()




    def __get_files(self):

        # Get working directory
        self.work_dir = input( "Input working directory: " )

        # Check if dir exist
        if os.path.isdir( self.work_dir ):

            # Get interresting files
            print("")
            print("List of G-code files [*%s]" % SUPPORT_FILE_END )
            print("---------------------------------------------------------")
            for file in os.listdir( self.work_dir ):

                # Get file name and extension
                file_name, file_extension = os.path.splitext( file )

                # Filter files
                if SUPPORT_FILE_END == file_extension:
                    print( " -> %s" % file )
                    self.g_code_files.append( file )

            print("\n")

        else:
            print("ERROR: Inputed directory does not exist!")


    def __create_new_file(self):

        # Is there any file to merge
        if len(self.g_code_files) > 0:

            # Get merged file name
            self.merge_file_name = input("Input end file name: ")

            # Create directory
            dir = self.work_dir + "\\out\\" 
            if not os.path.exists(dir):
                os.makedirs(dir)

            # Assemble path
            file_dir = dir + self.merge_file_name + SUPPORT_FILE_END

            # Copy firt TAP file
            shutil.copyfile( str(self.work_dir + "\\" + self.g_code_files[0]), file_dir )

            # Open merged file for read and append mode
            self.merged_file = open( file_dir, "r+" )

            # Change header
            self.merged_file.seek(0)
            self.merged_file.write("This is first line")

            #self.merged_file.close()


    def __merge_files(self):
        pass


    def __clean(self):
        pass




# ===============================================================================
#       MAIN ENTRY
# ===============================================================================
if __name__ == "__main__":
    main()
	
# ===============================================================================
#       END OF FILE
# ===============================================================================