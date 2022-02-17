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
    READ_WRITE  = "r+"      # Puts pointer to start of file 
    READ_ONLY   = "r"
    APPEND      = "a+"      # This mode puts pointer to EOF. Access: Read & Write
    
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
        self.file_ptr_line = 0

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
            self.file_ptr_line += 1

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
            self.file_ptr_line += 1

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
    # @brief  Get file pointer
    #
    # @note     Pointer is being evaluated based on binary file value
    #
    # @return      void
    # ===============================================================================
    def get_ptr(self):
        return self.file.tell()

    # ===============================================================================
    # @brief  Set file pointer
    #
    # @note     Pointer is being evaluated based on binary file value
    #
    # @param[in]    offset  - Pointer offset
    # @return       void
    # ===============================================================================
    def set_ptr(self, offset):
        self.file.seek()

    # ===============================================================================
    # @brief  Get file pointer line
    #
    # @note     This is acutual line in file
    #
    # @return      void
    # ===============================================================================
    def get_ptr_line(self):
        return self.file_ptr_line

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

    # String for parsing basis
    HEADER_START    = "File:"
    HEADER_END      = "Brief:"
    TOOL_LIST       = "List of needed tools"
    END             = "End of program"

    # Possible CNC jobs
    LIST_OF_KNOWN_JOBS = [ "2D ADAPTIVE", "DRILL", "2D CONTOURS" ]




    def __init__(self, file_name):
        
        # Open file
        self.g_file = FileManager(file_name, FileManager.READ_ONLY)

        # File attributes
        self.g_file_attr = {
            "name"      : "",
            "author"    : "",
            "date"      : "",
            "time"      : "",
            "brief"     : "",
            "tool"      : "",
            "jobs"      : [],
        }


    def __del__(self):
        self.g_file.close()


    def __parse_header(self):
        pass



    def __parse_tool(self):
        pass
    

            




# ===============================================================================
#       END OF FILE
# ===============================================================================