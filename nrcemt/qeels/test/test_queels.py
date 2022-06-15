from nrcemt.qeels.engine import qeels_engine_greeting


def test_main_message():
    assert qeels_engine_greeting() == "hello world from qeels engine!"
