from redactor import redact_genders

def test_redact_genders():
    data = "My mother and father have been trying to have a girl. Why am I as a boy not enough for them? LOLOLLL"
    redacted, genders, count = redact_genders(data)
    
    assert redacted == "My ██████ and ██████ have been trying to have a ████. Why am I as a ███ not enough for them? LOLOLLL"
    assert genders == ['mother', 'father', 'girl', 'boy']
    assert count == 4