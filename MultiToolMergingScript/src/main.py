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
    merged_file = FileManager(work_dir + "\\" + g_files_parsed[0].get_file_name() + "__Merged.tap", FileManager.WRITE_ONLY)

    # Write header to merged file

    # Write used tools

    # Write jobs

    # Write end program

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