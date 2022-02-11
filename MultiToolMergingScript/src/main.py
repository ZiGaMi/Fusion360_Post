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
#       CLASSES
# ===============================================================================


def dbg_print(msg):
    if DEBUG_EN:
        print(msg)



class ExtTool:
    
    
    def __init__(self):

        self.tool_paths = []

        # Get all listed tools in file
        self.__read_tools()


    def __read_tools(self):

        # Get current directory
        cwd = str( os.getcwd() )
        
        # Remove src
        cwd = cwd[:-3]

        # Assemble path
        file_path = cwd + "tools\external_tools.txt"

        # Read file
        try:
            with open( file_path, "r" ) as tool_file:
                for n, line in enumerate(tool_file):
                    dbg_print(line)
                    for tool in SUPPORT_EXT_TOOL_NOTATION:
                        if line.find(tool) > 0:
                            dbg_print(line)
                            self.tool_paths.append( line.split("'")[0] )

            # Close file
            tool_file.close()

        except:
            print("Warning: Missing path to external tools! \nPlace external_tools.txt file into \\tools directory if you want to use external tools for visualization.\n")


        print(self.tool_paths)

    

# ===============================================================================
#       FUNCTIONS
# ===============================================================================



def open_editor(file_path):

    #path = r"C:/Users/zigam/AppData/Local/Programs/Microsoft VS Code/"
    subprocess.Popen(["C:/Users/zigam/AppData/Local/Programs/Microsoft VS Code/Code.exe"])


# ===============================================================================
# @brief:  Main entry function
#
# @return:       void
# ===============================================================================
def main():
    
    os.system("cls")
    print("Hello...")


    tool = ExtTool()


    input("Press any key to exit...\n")


# ===============================================================================
#       MAIN ENTRY
# ===============================================================================
if __name__ == "__main__":
    main()
	
# ===============================================================================
#       END OF FILE
# ===============================================================================