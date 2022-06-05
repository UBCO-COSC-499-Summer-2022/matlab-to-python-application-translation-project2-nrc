from nrcemt.nanomi_optics.engine import nanomi_engine_greeting


def test_main_message():
    assert nanomi_engine_greeting() == "hello world from nanomi engine!"
