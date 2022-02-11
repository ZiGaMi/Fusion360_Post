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

import subprocess
import xml.etree.ElementTree as ET

# ===============================================================================
#       CONSTANTS
# ===============================================================================

# Supported G-code file extension
SUPPORT_FILE_END = [ ".tap" ]

# Name of supported external tools
SUPPORT_EXT_TOOL_NOTATION = [ "VSCode", "Notepad++", "Notepad" ]

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
# @brief:  Main entry function
#
# @return:       void
# ===============================================================================
def main():
    
    os.system("cls")


    tool = ExtTool()

    tool.open_file( "test" )

    input("Press any key to exit...\n")


def to_raw(string):
    return fr"{string}"


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
        
        # Remove src from current directory
        cwd = cwd[:-3]

        # Assemble path
        file_path = cwd + "tools\external_tools.xml"

        try:
            # Read XML file
            tree = ET.parse( file_path )
            root = tree.getroot()

            # Get name, target and path location
            self.tool_name = root.find('Name').text
            self.tool_path = root.find('Path').text
            self.tool_target = root.find('Target').text

            # Check if path exist
            if ( False == os.path.isfile( self.tool_target )) or ( False == os.path.isdir( self.tool_path )):
                print("WARNING: External tool path invalid! \nWARNING: Change specified paths inside >>>tools\\external_tools.xml<<< in order to use external tools for visualization.")
                self.tool_target = "notepad.exe"

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
        subprocess.Popen(str(self.tool_target + " " + str(file)))


    

# ===============================================================================
#       MAIN ENTRY
# ===============================================================================
if __name__ == "__main__":
    main()
	
# ===============================================================================
#       END OF FILE
# ===============================================================================