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
SCRIPT_VERSION = "V0.1.0"

# Supported G-code file extension
SUPPORT_FILE_END = ".tap"

# Show merge script at end of program
OPEN_END_SCRIPT = False

# Debug enabled
DEBUG_EN = False


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

    #print("Deleting intermediate files...")

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

# ===============================================================================
# @brief:   Parse all founded G-files
#
# @param[in]    g_files         - All G-files founded inside working directory
# @return       g_file_parsed   - Parsed all G-files
# ===============================================================================
def parse_g_files(g_files):
    g_files_parsed = []

    # Parse all g codes
    for idx, g_file in enumerate(g_files):
        g_files_parsed.append( GcodeParser(g_file) )
        #print("Parsing %s..." % g_file)

    return g_files_parsed

# ===============================================================================
# @brief:   Write header to merged file
#
# @param[in]    file            - Merged file
# @param[in]    g_file_parsed   - Parsed all G-files
# @return       void
# ===============================================================================
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

    file.write( "( ================================================ )\n" )
    file.write( "(           List of merged files                   )\n" )
    file.write( "( ================================================ )\n" )
    for idx, parse_file in enumerate(parsed_files):
        file.write( "( [%s]  %s )\n" % ( idx+1, parse_file.name() ))
    file.write( "\n" )


# ===============================================================================
# @brief:   Write list of used tool to merged file
#
# @param[in]    file            - Merged file
# @param[in]    g_file_parsed   - Parsed all G-files
# @return       void
# ===============================================================================
def write_list_of_tools(file, parsed_files):
    
    file.write( "( ================================================ )\n" )
    file.write( "(           List of used tools                     )\n" )
    file.write( "( ================================================ )\n" )
    for idx, parse_file in enumerate(parsed_files):
        file.write( "( [%s]  %s  )\n" % ( idx+1, parse_file.get_tool() ))
    file.write( "\n" )

# ===============================================================================
# @brief:   Write list of operations to merged file
#
# @param[in]    file            - Merged file
# @param[in]    g_file_parsed   - Parsed all G-files
# @return       void
# ===============================================================================
def write_list_of_operations(file, parsed_files):

    file.write( "( ================================================ )\n" )
    file.write( "(           List of operations                     )\n" )
    file.write( "( ================================================ )\n" )
    for idx, parse_file in enumerate(parsed_files):
        file.write( "( [%s]  %s  )\n" % ( idx+1, str(parse_file.get_jobs()).replace("[","").replace("]","")))
    file.write( "\n" )

# ===============================================================================
# @brief:   Write safe starupt line to merged file
#
# @param[in]    file            - Merged file
# @return       void
# ===============================================================================
def write_safe_startup(file):

    file.write( "( ================================================ )\n" )
    file.write( "(            Save Starup Line                      )\n" )
    file.write( "( ================================================ )\n" )
    file.write( "(    G90  - ABSOLUTE POSITION )\n" )
    file.write( "(    G94  - FEEDRATE PER MINUTE )\n" )
    file.write( "(    91.1 - INCREMENTAL ARC POSITION )\n" )
    file.write( "(    G40  - TOOL RADIUS COMPENSATION OFF )\n" )
    file.write( "(    G49  - TOOL HEIGHT COMPENSATION OFF )\n" )
    file.write( "(    G17  - XY WORKPLANE )\n" )
    file.write( "(    G21  - USING MILIMITERS )\n" )
    file.write( "G90 G94 G91.1 G40 G49 G17 G21\n")
    file.write( "\n" )

# ===============================================================================
# @brief:   Write all collected jobs
#
# @param[in]    file        - Merged file
# @param[in]    work_dir    - Working directory
# @return       void
# ===============================================================================
def write_jobs(file, work_dir):
    
    file.write( "( ================================================ )\n" )
    file.write( "(           CAM Features Start Code                )\n" )
    file.write( "( ================================================ )\n" )
    file.write( "\n" )

    for work_dir_file in os.listdir( work_dir ):

        # Get file name and extension
        file_name, file_extension = os.path.splitext( work_dir_file )

        # Filter files
        if INTERMEDIATE_FILE_END == file_extension:
            
            inter_file = FileManager(work_dir+"\\"+work_dir_file, FileManager.READ_ONLY)

            while True:
                line = inter_file.read()

                if '' == line:
                    break
                else:
                    file.write(line)

            inter_file.close()

# ===============================================================================
# @brief:   Write end statement to merged file
#
# @param[in]    file            - Merged file
# @return       void
# ===============================================================================
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

    # Write list of operations
    write_list_of_operations(merged_file, g_files_parsed)

    # Write safe starup file
    write_safe_startup(merged_file)

    # Write jobs
    write_jobs(merged_file, work_dir)

    # Write end program
    write_end(merged_file)

    # Delete intermediate files
    remove_intermediate_files(work_dir)

    # Success
    print("Merging successfully finised!")
    print("Output file: %s" % work_dir+"\\"+merged_file.name())

    # Outro
    if OPEN_END_SCRIPT:
        ext_tool = ExtTool()
        ext_tool.open_file(work_dir + "\\" + merged_file.name())

    print("")
    input("Press any key to exit...\n")


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