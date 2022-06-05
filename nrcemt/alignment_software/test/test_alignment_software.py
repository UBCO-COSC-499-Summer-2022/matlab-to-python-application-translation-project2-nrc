from nrcemt.alignment_software.engine import alignment_engine_greeting


def test_main_message():
    assert alignment_engine_greeting() == "hello world from alignment engine!"
