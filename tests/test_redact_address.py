from redactor import redact_address

def test_redact_address():
    data = "My address is 110 Boyd St."
    redacted, addresses, count = redact_address(data)
    
    assert redacted == "My address is ███████████."
    assert addresses == ['110 Boyd St']
    assert count == 1

def test_redact_address2():
    data = "110 Boyd St. Oklahoma City London Pakistan Oklahoma United Kingdom"
    redacted, addresses, count = redact_address(data)
    
    assert redacted == "███████████. ████████████████████ ████████ ███████████████████████"
    assert addresses == ['110 Boyd St', 'Oklahoma City London', 'Pakistan', 'Oklahoma United Kingdom']
    assert count == 4