from nrcemt.qeels.engine.results import save_results
from tempfile import TemporaryFile


def test_save_results():
    save_results("ABC", ["a", "b", "c"])
    with TemporaryFile('w+b') as tempfile:
        # Save temp data
        
        # Read temp data
        
        # assert values
    pass
