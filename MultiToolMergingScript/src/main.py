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

# GUI
import gui.gui as GUI

# ===============================================================================
#       CONSTANTS
# ===============================================================================

# Supported G-code file extension
SUPPORT_FILE_END = [ ".tap", ".gcode" ]

# Show merge script at end of program
OPEN_END_SCRIPT = True


# ===============================================================================
#       CLASSES
# ===============================================================================


# ===============================================================================
#       FUNCTIONS
# ===============================================================================

# ===============================================================================
# @brief:  Main entry function
#
# @return:       void
# ===============================================================================
def main():
    
    # Run main application
    GUI.Application().run()


# ===============================================================================
#       MAIN ENTRY
# ===============================================================================
if __name__ == "__main__":
    main()
	
# ===============================================================================
#       END OF FILE
# ===============================================================================