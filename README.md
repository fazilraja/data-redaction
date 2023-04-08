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

![alt-text](https://github.com/fazilraja//cs5293sp23-project1/docs/project1vid.mp4)