# Fazil Raja
# cs5293 Spring 2023 Project 1

# Description
Whenever sensitive information is shared with the public, the data must go through a redaction process. That is, all sensitive names, places, and other sensitive information must be hidden. Documents such as police reports, court transcripts, and hospital records all contain sensitive information. Redacting this information is often expensive and time consuming.

In this project I am redacting any file given to me. The topics I will be redacting are names, addresses, dates, gender related pronouns and phone numbers. We use spacy, regexs and nltk to detect the data and then redact it.


Below is the tree for my project:
├── COLLABORATORS
├── LICENSE
├── Pipfile
├── Pipfile.lock
├── README.md
├── docs
│   ├── 1.
│   ├── 2.
│   ├── 3.
│   ├── address.md
│   ├── dates.txt
│   └── genders.txt
├── project1
│   └── main.py
├── redacted
│   ├── address.md.redacted
│   ├── dates.txt.redacted
│   └── genders.txt.redacted
├── redactor.py
├── setup.cfg
├── setup.py
├── stats.txt
└── tests
    ├── test_redact_address.py
    ├── test_redact_dates.py
    ├── test_redact_genders.py
    ├── test_redact_names.py
    └── test_redact_phones.py

# How to install
To install grab the github link and git clone it.

# How to run
Then run the command ```pipenv run python redactor.py --input 'docs/*.txt' --input 'docs/*.md'  --names --dates --phones --genders --address --output 'redacted/' --stats stats.txt``` and in order to run the tests you can use the command ```pipenv run python -m pytest```.

Each argument parser is as follows:
input: which globs of files you want to redact, if the glob is not found then it will say no files for this glob
names: enter this arg if you want to redact names
dates: enter this arg if you want to redact dates such as 4/9/2023, April 9th, 22/2/22, etc.
genders: redacts words that describe gender
phones: redacts phone numbers
address: redacts addresses
output: the output directory, in this case it is redacted/
stats: the stats file, in this case it is stats.txt, it outputs the number of redactions, the number of tokens and the number of files redacted for each file

# Demo
ATTENTION: The demo is a video and not a gif. Please click on the link to see the demo if it does not automatically play. Thank you. Sorry for the inconvenience.
![alt-text](https://github.com/fazilraja/cs5293sp23-project1/blob/main/docs/project1demo.mp4)

# Functions
Each function serves a different function. Since there are 5 different types of data to redact and othe auxilary function, I have 5 different redaction functions. For all redaction functions we return 3 variables, the redacted data, the number of redactions and the number of tokens. The functions are as follows:

## redact_word
Give a word it replaces it with blocks of the length of the word or token given.

## redact_names
This function takes in a string and then uses spacy to detect the names. I use the en_core_web_lg model to detect the names. Then I use the redact_word function to redact the names. If the entity is of type PERSON then it is redacted. Below is the function and the rest of the function follow similar logic
```def redact_names(data):
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
    return data, names, count```


## redact_dates
The same as other function but first we redact using a complex regex as the model cannot capture them all(Pokemon). Then we use the spacy model to redact the rest using the entity label DATE and TIME.

## redact_phones
For this one we use a regex to detect the phone numbers. Then we use the redact_word function to redact the phone numbers.

## redact_genders
This one is really similar to redact_phones, we use a regex. But when it come to replacing it with blocks we use the re.sub function in order to capture boundries. This was due to the fact that there was a bug where the term "he" was the only one being redacted in "she", "mother" etc. 

## redact_address
We first use a regex to redact, then we use the spacy model to handle the rest using label GPE, FAC and LOC.

## output
Here we output the redacted data to the file path given when calling the program. 

## redaction
This is the main function that calls all the other functions. It takes in all the args and then calls the other functions. It also outputs all the stats into the stats file

## main
Here we just create the argparser, get the glob and files and then call the redaction and output functions. 

# Tests
We have 5 tests, one for each type of data, except addresses where I created two tests for it. We test the number of redactions, the number of tokens and the redacted data. We also test the output function. All tests follow the same logic of reading the data, redacting it, check the output of the redaction, what what was redacted and how many entities were redacted.

Below is the test for redact_phones, and the rest of the tests follow the same logic.
```from redactor import redact_phones

def test_redact_phones():
    data = "My phone number is 123-456-7890."
    redacted, phones, count = redact_phones(data)
    assert redacted == "My phone number is ████████████."
    assert phones == ['123-456-7890']
    assert count == 1```

# Bugs and assumptions
One of the bugs is that for names, if you do not have a generic or obvious name then the model will not detect it. For example, if you have a name like "Fazil" then the model will not detect it. But if you have a name like "John" then the model will detect it. This is due to the fact that the model was trained on a lot of data and the names that were in the data were more common western names.

Another is addresses. This was a tough one as there are a lot of different ways an address can be listed. If it does not follow the regex or is not a popular geographical spot then it can be skipped. 

For genders theres just so many different pronouns that can describe an entity that I only redacted the most common ones.

