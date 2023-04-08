from redactor import redact_dates

def test_redact_dates():
    data = "The date is 01/01/2019."
    redacted, dates, count = redact_dates(data)
    
    assert redacted == "The date is ██████████."
    assert dates == ['01/01/2019']
    assert count == 1