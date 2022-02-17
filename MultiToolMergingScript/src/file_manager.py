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
# @brief  File manager
# ===============================================================================
class FileManager:

    # Access type
    READ_WRITE  = "w+"  # This mode erase file content
    READ_ONLY   = "r"
    APPEND      = "a+"   # This mode puts pointer to EOF. Access: Read & Write
    
    # ===============================================================================
    # @brief:  Constructor
    #
    #       Create file if don't exsist jet.
    #
    # @param[in]    file   - File to operate with
    # @param[in]    access - File access type
    # @return       void
    # ===============================================================================
    def __init__(self, file_name, access=READ_ONLY):

        self.file_name = file_name

        try:
            if os.path.isfile(self.file_name):
                self.file = open( self.file_name, access )
                self.__dbg_print("Open.....%s" % self.file_name)
            
            else:
                self.file = open( self.file_name, access )
                self.__dbg_print("Created.....%s" % self.file_name)
        except Exception as e:
            print(e)
            
    # ===============================================================================
    # @brief  Desctructor
    #
    # @return      void
    # ===============================================================================
    def __del__(self):

        # Close the file
        self.close()

    # ===============================================================================
    # @brief  Read file line
    #
    # @return      void
    # ===============================================================================
    def read(self):

        line = ""
        try:
            line = self.file.readline()

        except Exception as e:
            print(e)

        return line

    # ===============================================================================
    # @brief  Read file content from line
    #
    # @param[in]    str     - String to insert to file
    # @return       void
    # ===============================================================================
    def write(self, str):
        try:
            self.file.write(str)

        except Exception as e:
            print(e)

    # ===============================================================================
    # @brief  Erase file content
    #
    # @return      void
    # ===============================================================================
    def erase(self):
        try:
            # Check if open
            if not self.file.closed:
               self.file.close()
            
            # Erase by opening for reading
            self.file = open( self.file_name, "w" )

            self.__dbg_print("Erasing.....%s" % self.file_name)

        except Exception as e:
            print(e)

    # ===============================================================================
    # @brief  Close working file
    #
    # @return      void
    # ===============================================================================
    def close(self):
        try:
            self.file.close()
            self.__dbg_print("Closing.....%s" % self.file_name)

        except Exception as e:
            print(e)

    # ===============================================================================
    # @brief  Debug print
    #
    # @note     All debug prints can be enabled/disabled via that function
    #
    # @param[in]    str     - String to print
    # @return       void
    # ===============================================================================
    def __dbg_print(self, str):
        print(str)



# ===============================================================================
# @brief  G-code Parser
#
# ===============================================================================
class GcodeParser(FileManager):

    def __init__(self):
        pass


            




# ===============================================================================
#       END OF FILE
# ===============================================================================