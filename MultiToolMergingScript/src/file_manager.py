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

# Intermediate G-code file extension
INTERMEDIATE_FILE_END = ".otap"

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
    WRITE_ONLY  = "w"       # Erase complete file
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
                self.file = open( self.file_name, "w" )
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
        #print(str)
        pass

    def name(self):
        return self.file.name.split("\\")[-1]

    def path(self):
        return self.file.name[0:-len(self.name())]


# ===============================================================================
# @brief  G-code Parser
#
# ===============================================================================
class GcodeParser(FileManager):

    # String for parsing basis
    SCRIPT_VER      = "Post script version:  "
    FILE_NAME       = "File:   "
    AUTHOR          = "Author: "
    DATE            = "Date:   "
    TIME            = "Time:   "
    BRIEF           = "Brief:  "
    TOOL_LIST       = "List of needed tools"
    FILE_END        = "End of program"

    # Possible CNC jobs
    LIST_OF_KNOWN_JOBS = [ "2D ADAPTIVE", "DRILL", "2D CONTOUR", "FACE" ]


    # ===============================================================================
    # @brief  Constructor
    #
    # @return      void
    # ===============================================================================
    def __init__(self, file_name):
        
        # Open file
        self.g_file = FileManager(file_name, FileManager.READ_ONLY)

        # File attributes
        self.g_file_attr = {
            "script"    : "",
            "file"      : "",
            "author"    : "",
            "date"      : "",
            "time"      : "",
            "brief"     : "",
            "tool"      : "",
            "jobs"      : [],
        }

        # Parse header
        self.__parse_header()

        # Parse tool
        self.__parse_tool()

        # Parse jobs
        self.__parse_jobs()

        # Close file at the end
        self.g_file.close()

        # TODO: Remove only debug
        #self.print_attr()

    # ===============================================================================
    # @brief  Desctructor
    #
    # @return      void
    # ===============================================================================
    def __del__(self):
        self.g_file.close()

    # ===============================================================================
    # @brief  Read line from file
    #
    # @note     Will remove comments if there are in the line
    #
    # @return      void
    # ===============================================================================
    def __read(self):
        return self.g_file.read().replace("( ", "").replace(" )", "")

    # ===============================================================================
    # @brief  Parse header
    #
    # @note     Parsed values are stored in class variable g_file_attr
    #
    # @return      void
    # ===============================================================================
    def __parse_header(self):

        # Read empty line
        self.__read()

        # Read first line
        line = self.__read()

        # Parse script version
        self.g_file_attr["script"] = line[len(self.SCRIPT_VER):-1] 

        # Read separator
        self.__read()

        # Read file details
        line = self.__read()
        self.g_file_attr["file"] = line[len(self.FILE_NAME):-1]

        line = self.__read()
        self.g_file_attr["author"] = line[len(self.AUTHOR):-1]

        line = self.__read()
        self.g_file_attr["date"] = line[len(self.DATE):-1]

        line = self.__read()
        self.g_file_attr["time"] = line[len(self.TIME):-1]

        line = self.__read()
        self.g_file_attr["brief"] = line[len(self.BRIEF):-1]

    # ===============================================================================
    # @brief    Parse tool
    #
    # @return      void
    # ===============================================================================
    def __parse_tool(self):
        
        while True:
            line = self.__read()

            if line.find(self.TOOL_LIST) > 0:
                
                # Ignore separator
                self.__read()

                # Get tool
                line = self.__read()
                self.g_file_attr["tool"] = line[1:-2]   # Ignore brackets

                # Exit
                break
            
            # Safe line
            if self.g_file.get_ptr_line() > 20:
                print("ERROR: Tool set not fund in %s" % self.g_file.file_name)
                break

    # ===============================================================================
    # @brief    Parse CNC jobs
    #
    # @note     Intemediate files has .otap extension
    #
    # @return      void
    # ===============================================================================
    def __parse_jobs(self):
        
        # Intermediate file name
        out_file_name = "%s%s%s" % ( self.g_file.path(), self.g_file.name().replace(".tap", ""), INTERMEDIATE_FILE_END)

        # Create intermediate file
        file = FileManager(out_file_name,self.WRITE_ONLY)
        
        file.write("( ================================================ )\n" )
        file.write("( Start of %s)\n" % self.g_file.name() )
        file.write("( ================================================ )\n" )
        file.write("\n")

        # Go thru file
        while True:
            #line = self.__read()
            raw_line = self.g_file.read()
            line = raw_line.replace("( ", "").replace(" )", "")

            # Reached end of file
            if line.find(self.FILE_END) > 0:
                break
            
            # Get number of detected jobs
            job_nb = len(self.g_file_attr["jobs"])

            # Find any of the known job
            for job_name in self.LIST_OF_KNOWN_JOBS:

                # Job founded
                if line.find(job_name) > 0:
                    self.g_file_attr["jobs"].append(line[1:-2]) # Ignore brackets
                    
                    if job_nb == 0:
                        file.write(raw_line)

            if job_nb > 0:
                file.write(raw_line) 

        # Mark end of this file operation
        file.write("( End of %s)\n" % self.g_file.name() )
        file.write("( ================================================ )\n" )
        file.write("\n")

        # Close file
        file.close()

    def name(self):
        return self.g_file.name()

    # ===============================================================================
    # @brief    Get G code file attributes
    #
    # @return      void
    # ===============================================================================
    def get_attr(self):
        return self.g_file_attr

    # ===============================================================================
    # @brief    Get post version
    #
    # @return      script - Post script version
    # ===============================================================================
    def get_post_ver(self):
        return self.g_file_attr["script"]

    # ===============================================================================
    # @brief    Get file name
    #
    # @return      file - G-code author
    # ===============================================================================
    def get_file_name(self):
        return self.g_file_attr["file"]

    # ===============================================================================
    # @brief    Get file name
    #
    # @return      author - Author of G-code
    # ===============================================================================
    def get_author(self):
        return self.g_file_attr["author"]

    # ===============================================================================
    # @brief    Get data & time
    #
    # @return      date, time - Date & time of generated G-code 
    # ===============================================================================
    def get_date_time(self):
        return self.g_file_attr["date"], self.g_file_attr["time"]

    # ===============================================================================
    # @brief    Get brief
    #
    # @return      brief - Brief description of project
    # ===============================================================================
    def get_brief(self):
        return self.g_file_attr["brief"]

    # ===============================================================================
    # @brief    Get tools
    #
    # @return      tool - Used tool
    # ===============================================================================
    def get_tool(self):
        return self.g_file_attr["tool"]

    # ===============================================================================
    # @brief    Get G code jobs
    #
    # @return      jobs - Name of founded jobs
    # ===============================================================================
    def get_jobs(self):
        return self.g_file_attr["jobs"]

    # ===============================================================================
    # @brief    Print g-code attributes
    #
    # @return      void
    # ===============================================================================
    def print_attr(self):
        print(" Post ver.: %s" % self.g_file_attr["script"] )
        print(" File:      %s" % self.g_file_attr["file"]   )
        print(" Author:    %s" % self.g_file_attr["author"] )
        print(" Date:      %s" % self.g_file_attr["date"]   )
        print(" Time:      %s" % self.g_file_attr["time"]   )
        print(" Brief:     %s" % self.g_file_attr["brief"]  )
        print(" Tool:      %s" % self.g_file_attr["tool"]   )
        print(" Jobs:      %s" % self.g_file_attr["jobs"]   )
    

        

# ===============================================================================
#       END OF FILE
# ===============================================================================