import os
import argparse
import sys
import glob
import re

def Verbose(file_to_be_changed, change, results):
    if results.verbose == True:
        print ("Changed " + file_to_be_changed + " to " + change + ".")
    return
    
def Interactive(file_to_be_changed, change):
   return raw_input("Do you want to change " + file_to_be_changed + " to " + change + "? Y/N\n")
   
def Change_file(new_files, change, i, results):
    if results.interactive == True:
        choice = Interactive(new_files[i], change)
        if choice in('Y','y','yes','Yes','YES','YEs','yES','yEs','yeS','YeS'):
            Verbose( new_files[i], change, results )
            new_files[i] = change
    else:
        Verbose( new_files[i], change, results )
        new_files[i] = change
   
def main():
    parser = argparse.ArgumentParser(description = "batch file renaming program")
    
    parser.add_argument( "-v", action = "store_true", dest = "verbose", default = False, help = "verbose output, print old and new filenames during processsing." )
    
    parser.add_argument( "-i", action = "store_true", dest = "interactive", default = False, help = "interactive mode, ask user prior to renaming each file." )
    
    parser.add_argument( "-l", action = "store_true", dest = "lwrcase", default = False, help = "convert filenames to lowercase." )
    
    parser.add_argument( "-u", action = "store_true", dest = "uprcase", default = False, help = "convert filenames to uppercase." )
    
    parser.add_argument( "-t", action = "append", dest = "n", help = "trim n chars from the start of each filename if n is positive, trim n hcars from the end of each filename if n is negative." )
    
    parser.add_argument( "-r", action = "append", nargs = 2, dest = "replace", help = "replace oldstring with newstring in filenames\nstrings should be treated as regular expressions." )
    
    parser.add_argument( "-n", action = "store", dest = "countstring", help = "rename files in sequence using countstring\n#'s in countstring become numbers; e.g., ## becomes 01, 02,..." )
    
    #collect all file names that user wishes to apply renaming to
    parser.add_argument("file_list", nargs = "*", help = "Enter any number of files you want to perform operations on, either at the beginning or end of the command line.\nWildcards are supported")
    
    #process command line options
    results = parser.parse_args()
    
    if results.verbose == True:
        print("-v flag supplied")
        
    if results.interactive == True:
        print("-i flag supplied")
        
    if results.lwrcase == True:
        print("-l flag supplied")
        
    if results.uprcase == True:
        print("-u flag supplied")
        
    if results.n is not None:
        print("-t flag supplied")
        
    if results.replace is not None:
        print("-r flag supplied with", results.replace)
        
    if results.countstring is not None:
        print("-n flag supplied with", results.countstring)
    
    # from the files listed by user at command line, look in current directory for those files and create a list of lists.
    og_files = []
    for file in results.file_list:
        og_files.append(glob.glob(file))
    
    # from the list of lists (og_files), create a single list    
    unique_files = [val for sublist in og_files for val in sublist]
    # remove any duplicates in the list of files supplied by user
    unique_files = list(set(unique_files))
    # sort the list
    unique_files.sort()
    
    # create copy of unique_files. flag operations will be done on the files in this list. Later, the order of these files will be matched with unique_files.
    new_files = unique_files[:]
    
    #find the order of command line arguments
    count = 0
    sys.argv.pop(0)
    
    while (count < len(sys.argv)):
        #help is handled by argparse
        if sys.argv[count] == "-h":
            count += 1
            
        #verbose is handled Verbose function at top
        elif sys.argv[count] == "-v":
            count += 1
        
        #interactive is handled by Interactive function at top
        elif sys.argv[count] == "-i":
            count += 1
            
        #convert file list to all lowercase
        elif sys.argv[count] == "-l":
            i = 0
            for x in new_files:
                new_files[i] = new_files[i].lower()
                #Change_file(new_files,change, i, results)
                i += 1
            count += 1
            
        elif sys.argv[count] == "-u":
            #convert file lsit to all uppercase
            i = 0
            for x in new_files:
                change = new_files[i].upper()
                Change_file(new_files,change, i, results)
                i += 1
            count += 1
                
        elif sys.argv[count] == "-t":
            #increment arg to get to amount to trim files by
            count += 1
            trim_amt = int(sys.argv[count])
            count += 1
            
            # loop through the file list and trim off the front of the 
            # file is trim_amt >0, else trim off the back
            i = 0
            if trim_amt < 0:
                for x in new_files:
                    change = x[:trim_amt]
                    Change_file(new_files,change, i, results)
                    i += 1
            else:
                for x in new_files:
                    change = x[trim_amt:]
                    Change_file(new_files,change, i, results)
                    i += 1
                    
        #replace old file name with new file name
        elif sys.argv[count] == "-r":
            i = 0
            for x in new_files:
                #use sub() to look for the old file name and replace it with the
                #new file name.
                change = re.sub( sys.argv[count+1], sys.argv[count+2], x )
                Change_file(new_files,change, i, results)
                i += 1
    
            #increment count by 3 to skip over -r <old> <new>
            count += 3
            
        #for option -n, takes args '##..' and counts up and appends this to the 
        #beginning of the file name. ### -> 000, 001, etc
        elif sys.argv[count] == "-n":
            count += 1
            digits = sys.argv[count].count('#')
            i = 0
            for x in new_files:
                change = str(i).zfill(digits) + '_' + x
                Change_file(new_files,change, i, results)
                i += 1
        else:
            #must be file list
            count += 1
        
    #Go through the old filenames (unique_files) and replace each
    #index with the respective element of new_files
    i = 0
    for x in new_files:
        os.rename(unique_files[i], x)
        i += 1

if __name__ == "__main__":
    main()
