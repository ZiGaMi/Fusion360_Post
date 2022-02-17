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

from file_manager import FileManager, GcodeParser, INTERMEDIATE_FILE_END

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

# ===============================================================================
# @brief:   Get all G-code files
#
# @param[in]    work_dir    - Working directory for searching
# @return       g_files     - List of founded G-code inside working directory 
# ===============================================================================
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
                
                # Ignore merged file
                if file_name.find("Merged") < 0:
                    print( " [%s] %s" % ( len(g_files)+1, file ))
                    g_files.append(work_dir + "\\" + file)

        print("\n")

    else:
        print("ERROR: Inputed directory does not exist!")

    return g_files

# ===============================================================================
# @brief:   Remove all intermediate G-code files
#
# @param[in]    work_dir    - Working directory for searching
# @return       void
# ===============================================================================
def remove_intermediate_files(work_dir):

    g_files = []

    print("Deleting intermediate files...")

    # Check if dir exist
    if os.path.isdir( work_dir ):
        for file in os.listdir( work_dir ):

            # Get file name and extension
            file_name, file_extension = os.path.splitext( file )

            # Filter files
            if INTERMEDIATE_FILE_END == file_extension:
                os.remove(work_dir + "\\" + file)

    else:
        print("ERROR: Inputed directory does not exist!")

    return g_files


def parse_g_files(g_files):
    g_files_parsed = []

    # Parse all g codes
    for idx, g_file in enumerate(g_files):
        g_files_parsed.append( GcodeParser(g_file) )

        # TODO: Remove when no more needed
        #print("------------------------------------------------------------------------------------------")
        #print(" [%s] %s\n" % (idx, g_file))
        #print("------------------------------------------------------------------------------------------")

    #print("\n")

    return g_files_parsed


def write_header(file, parsed_files):
    
    file.write( "( Copyright (c) 2022 Ziga Miklosic )\n" )
    file.write( "( All Rights Reserved )\n" )
    file.write( "( This file is automatically generated file )\n" )
    file.write( "( Merging script version: %s)\n" % SCRIPT_VERSION )
    file.write( "\n" )

    file.write( "( ================================================ )\n" )
    file.write( "( Post script version: %s )\n" % parsed_files[0].get_post_ver())
    file.write( "( ================================================ )\n" )


    file.write( "( File:   %s_Merged )\n" % parsed_files[0].get_file_name())
    file.write( "( Author: %s )\n" % parsed_files[0].get_author() )
    file.write( "( Date:   %s )\n" % parsed_files[0].get_date_time()[0] )
    file.write( "( Time:   %s )\n" % parsed_files[0].get_date_time()[1] )
    file.write( "( Brief:  %s )\n" % parsed_files[0].get_brief() )
    file.write( "\n" )





def write_list_of_tools(file, parsed_files):
    pass

def write_jobs(file, work_dir):
    pass

def write_end(file):

    file.write( "( ================================================ )\n" )
    file.write( "(           End of program                         )\n" )
    file.write( "( ================================================ )\n" )
    file.write( "(  M5  - STOP SPINDLE ) \n" )
    file.write( "(  M9  - COOLING OFF ) \n" )
    file.write( "(  M30 - PROGRAM END ) \n" )
    file.write( "M5\n" )
    file.write( "M30\n" )
    file.write( "\n" )
    
    # Close file at the end
    file.close()



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
    g_files_list = get_g_files(work_dir)

    # Parse g-code files
    g_files_parsed = parse_g_files(g_files_list)

    # Create merged file
    # NOTE: Merged file name is based on first in directory
    merged_file = FileManager(work_dir + "\\" + g_files_parsed[0].get_file_name() + "__Merged.tap", FileManager.WRITE_ONLY)

    # Write header to merged file
    write_header(merged_file, g_files_parsed)

    # Write used tools
    write_list_of_tools(merged_file, g_files_parsed)

    # Write jobs
    write_jobs(merged_file, work_dir)

    # Write end program
    write_end(merged_file)

    # Delete intermediate files
    remove_intermediate_files(work_dir)

    # Outro
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
#       MAIN ENTRY
# ===============================================================================
if __name__ == "__main__":
    main()
	
# ===============================================================================
#       END OF FILE
# ===============================================================================