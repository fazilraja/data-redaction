from redactor import redact_phones

def test_redact_phones():
    data = "My phone number is 123-456-7890."
    redacted, phones, count = redact_phones(data)
    assert redacted == "My phone number is ████████████."
    assert phones == ['123-456-7890']
    assert count == 1