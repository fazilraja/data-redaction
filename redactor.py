import argparse
import os
import glob
import spacy
import re
import nltk 
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# redact the file based on the arguments

# given a Word, redact it with a block char
def redact_word(word):
    return "█"*len(word)

# redact names
def redact_names(data):
    """
    Redact names from the data
    Returns the data with names redacted, names redacted and the number of names redacted
    """
    names = []
    count = 0

    # load the spacy model
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(data)
    # for loop through the entities
    for ent in doc.ents:
        # if the entity is a person
        if(ent.label_ == "PERSON"):
            # redact the word
            data = data.replace(ent.text, redact_word(ent.text))
            # add the name to the list of names
            names.append(ent.text)
            # increment count
            count += 1
    # return the data, names and count
    return data, names, count

# redact dates
def redact_dates(data):
    dates = []
    count = 0
    # load the spacy model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(data)

    # lets first do a regex to find dates then clean up with spacy
    pattern = r"\b(?:\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{1,2}[/-]\d{2}|\d{1,2}\s(?:JAN|NOV|OCT|DEC|jan|nov|oct|dec)\s\d{2,4}|[0-9]+(?:st|[nr]d|th)?\s(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*(?:\s|,)\s?\d{2,4}|\d{1,2}-[ADFJMNOS]\w*-\d{2,4}|\d{1,2}/\d{1,2})\b"
    #regex for Dec2000
    pattern1 = r"\\[A-Za-z_]+_([A-Za-z]+[0-9]{4})\\"

    matches1 = re.findall(pattern1, data)
    for match in matches1:
        data = data.replace(match, redact_word(match))
        dates.append(match)
        count += 1
    
    # go through the data and match with the pattern
    matches = re.findall(pattern, data)
    # for loop through the matches
    for match in matches:
        data = data.replace(match, redact_word(match))
        dates.append(match)
        count += 1

    for ent in doc.ents:
        # if the entity is a date
        if(ent.label_ == "DATE" or ent.label_ == "TIME"):
            # redact the word
            data = data.replace(ent.text, redact_word(ent.text))
            # add the name to the list of names
            dates.append(ent.text)
            # increment count
            count += 1
    
    return data, dates, count

# redact phone numbers
def redact_phones(data):
    phones = []
    count = 0
    
    pattern = r"\b(?:\d{3}[-.●]??\d{3}[-.●]??\d{4}|\(\d{3}\)\s*\d{3}[-.●]??\d{4}|\d{3}[-.●]??\d{4})\b"

    matches = re.findall(pattern, data)
    # for loop through the matches
    for match in matches:
        data = data.replace(match, redact_word(match))
        phones.append(match)
        count += 1

    return data, phones, count    

# redact genders
def redact_genders(data):
    genders_redacted = []
    count = 0
    pattern = r"\b(Male|he|women|mother|He|Mother|ms|Ms\.|hers|Father|she|Boy|girl|Brother|Himself|Sister|Herself|Men|Female|his|Her|him|Wife|sister|himself|Mr\.|wife|men|her|boy|mr|Girl|male|Husband|herself|Him|His|Women|brother|father|She|husband|female|Hers|Miss|miss)\b"

    match = re.findall(pattern, data)
    for m in match:
        data = re.sub(r"\b" + m + r"\b", redact_word(m), data)
        genders_redacted.append(m)
        count += 1

    return data, genders_redacted, count

# redact address
def redact_address(data):
    address_redacted = []
    count = 0
    nlp = spacy.load("en_core_web_lg")

    address_regex = r"\d+\s+\w+\s+\w+\s*\w*"
    match = re.findall(address_regex, data)

    for m in match:
        data = re.sub(r"\b" + m + r"\b", redact_word(m), data)
        address_redacted.append(m)
        count += 1

    doc = nlp(data)
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(ent)
            if(ent.label_ == "GPE" or ent.label_ == "LOC" or ent.label_ == "FAC"):
                data = data.replace(ent.text, redact_word(ent.text))
                address_redacted.append(ent.text)
                count += 1

    return data, address_redacted, count

# given data anda directory output the data to the directory in a file
def output(data, args, file):
    if args is None:
        output_path = ''
    else:
        output_path = args
    file = file.split("/")[-1]
    file = output_path + file
   
    # add .redacted to the file
    file = file + ".redacted"

    # check if the directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # write the data to the file
    with open(file, "w") as f:
        f.write(data)



# redact the file based on the arguments
def redaction(args, data, filename):
    # if args has names
    
    # open stat file
    stats = args.stats
    f = open(stats, "a")
    f.write(f"---------------------------Stats for {filename}-----------------------------\n")


    if(args.names):
        # print statement to show redaction
        print("Redacting names", args.names)
        data, names, names_count = redact_names(data)
        f.write("--------------------names redacted--------------------\n")
        f.write(str(names) + "\n")
        f.write(f"Number of names redacted: {str(names_count)}\n\n")

    # if args has dates
    if(args.dates):
        print("Redacting dates", args.dates)
        data, dates, date_count = redact_dates(data)
        f.write("--------------------dates redacted--------------------\n")
        f.write(str(dates) + "\n")
        f.write(f"Number of dates redacted: {str(date_count)}\n\n")

    # if args has phones
    if(args.phones):
        print("Redacting phones", args.phones)
        data, phones, phone_count = redact_phones(data)
        f.write("--------------------phones redacted--------------------\n")
        f.write(str(phones) + "\n")
        f.write(f"Number of phones redacted: {str(phone_count)}\n\n")

    # if args had genders
    if(args.genders):
        print("Redacting genders", args.genders)
        data, genders, gender_count = redact_genders(data)
        f.write("--------------------gender terms redacted--------------------\n")
        f.write(str(genders) + "\n")
        f.write(f"Number of genders redacted: {str(gender_count)}\n\n")

    # if args has address
    if(args.address):
        print("Redacting address", args.address)
        data, addresses, count = redact_address(data)
        f.write("--------------------address redacted--------------------\n")
        f.write(str(addresses) + "\n")
        f.write(f"Number of addresses redacted: {str(count)}\n\n")

    # close the file
    return data


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
    parser.add_argument("--output", type=str, help="output redacted files to this directory")

    #stats
    parser.add_argument("--stats", help="print stats about the redaction in this file")

    # parse the arguments
    args = parser.parse_args()

    #print the parser args
    print(args)

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
                        print("Redacting file", file)
                        data = redaction(args, data, file)
                        print("Redaction complete\n")
                        # if output is given
                        if(args.output):
                            # output the data to the directory
                            output(data, args.output, file)


    # redact the file based on the arguments

