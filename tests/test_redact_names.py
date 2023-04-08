from redactor import redact_names

def test_redact_names():
    data = "John Smith is a person. He lives in New York."
    redacted, names, count = redact_names(data)
    assert redacted == "██████████ is a person. He lives in New York."
    # print names and type of object
    print(type(names))
    print(names)
    assert names == ['John Smith']
    assert count == 1 