import argparse
import os
import glob

# redact the file based on the arguments

# redact names
def redact_names(data):
    return data

# redact dates
def redact_dates(data):
    return data

# redact phones
def redact_phones(data):
    return data

# redact genders
def redact_genders(data):
    return data

# redact address
def redact_address(data):
    return data

# redact the file based on the arguments
def redaction(args, data):
    # if args has names
    if(args.names):
        data = redact_names(data)


if __name__ == "__main__":
    #arg parser
    parser = argparse.ArgumentParser()
    
    # add arguments
    # input
    parser.add_argument("--input", type=str, dest="input", action="append", help="redact all the fils with this extension", required=True)

    #names
    parser.add_argument("--names", action="store_true", default=False, help="redact names from the files")

    #dates
    parser.add_argument("--dates", action="store_true", default=False, help="redact dates")

    #phones
    parser.add_argument("--phones", action="store_true", default=False, help="redact phone numbers")

    #genders
    parser.add_argument("--genders", action="store_true", default=False, help="redact anything that specifies gender")

    #address
    parser.add_argument("--address", action="store_true", default=False, help="redact adresses")

    #output
    parser.add_argument("--output", help="output redacted files to this directory")

    #stats
    parser.add_argument("--stats", help="print stats about the redaction in this file")

    # parse the arguments
    args = parser.parse_args()

    #print the parser args
    print(args)
    print(args.input)

    # read the input file of given extension
    if(args.input):
        #find files with the given glob
        # for loop through the list of files
        for extension in args.input:
            fileList = glob.glob(extension)
            if not fileList:
                print(f"No files found with this extension {extension}")
            else:    
                for file in fileList:
                    # open the file
                    with open(file, "r") as f:
                        # read the file
                        data = f.read()


    # redact the file based on the arguments

