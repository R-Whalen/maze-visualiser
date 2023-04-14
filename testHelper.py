import json
import io
import os
from globals import testFileName

def get():
    # eject early if no file path is specified in globals
    if not testFileName: raise Exception('No test file path provided')
    
    # check if file exists already
    if os.path.isfile(testFileName) and os.access(testFileName, os.R_OK):
        # if file does exist grab file and return dump
        f = open(testFileName)
        data = json.load(f)
        f.close()
        
        # if the file has the appropriate structure, return it
        if data: 
            return data
        else: 
            # else give dummy information to populate the file with later
            return []
    else:
        # if not, initialise it using the testFilePath name
        # strip file name from string
        with io.open(testFileName, 'w') as file:
            file.write(json.dumps([]))
        return get() # loop back around now that there is a json

def write(data):
    with open(testFileName, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

def appendResult(dict):
    current = get()
    
    current.append(dict)
    
    write(current)