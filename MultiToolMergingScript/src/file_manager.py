# ===============================================================================
# @file:    file_manager.py
# @note:    Fusion360 different tools G-code merging script
# @author:  Ziga Miklosic
# @date:    09.02.2022
# @brief:   
# ===============================================================================

# ===============================================================================
#       IMPORTS  
# ===============================================================================
import sys
import os

# ===============================================================================
#       CONSTANTS
# ===============================================================================


# ===============================================================================
#       FUNCTIONS
# ===============================================================================


# ===============================================================================
#       CLASSES
# ===============================================================================

# ===============================================================================
# @brief:  File manager
# ===============================================================================
class FileManager:
    
    # ===============================================================================
    # @brief:  Constructor
    #
    #       Create file if don't exsist jet.
    #
    # @param[in]:    file - File to operate with
    # @return:       void
    # ===============================================================================
    def __init__(self, file_name):

        self.file_name = file_name

        try:
            if os.path.isfile(self.file_name):
                self.file = open( self.file_name, "a" )
                self.__dbg_print("Open.....%s" % self.file_name)
            
            else:
                self.file = open( self.file_name, "w" )
                self.__dbg_print("Created.....%s" % self.file_name)
        except:
            pass




    # ===============================================================================
    # @brief:  Desctructor
    #
    # @return:       void
    # ===============================================================================
    def __del__(self):

        # Close the file
        try:
            self.__dbg_print("Closing.....%s" % self.file_name)
        except:
            pass

    # ===============================================================================
    # @brief:  Read file content from line
    #
    # @param[in]    line - Line number
    # @return:      void
    # ===============================================================================
    def read(self, line):
        pass

    # ===============================================================================
    # @brief:  Read file content from line
    #
    # @param[in]    str     - String to insert to file
    # @param[in]    line    - Line number where to inject string
    # @return:      void
    # ===============================================================================
    def write(self, str, line):
        pass

    # ===============================================================================
    # @brief:  Find string in file
    #
    #   Return -1, -1 in case of no string is found!
    #
    # @param[in]    str         - String to find in file
    # @return:      line,col    - Line and column of string start location 
    # ===============================================================================      
    def find(self, str):
        pass

    def erase(self):
        try:
            # Check if open
            if not self.file.closed:
               self.file.close()
            
            # Erase by opening for reading
            self.file = open( self.file_name, "w" )

            self.__dbg_print("Erasing.....%s" % self.file_name)
        except:
            pass


    def close(self):
        try:
            self.__dbg_print("Closing.....%s" % self.file_name)
        except:
            pass


    def __dbg_print(self, str):
        print(str)






            




# ===============================================================================
#       END OF FILE
# ===============================================================================