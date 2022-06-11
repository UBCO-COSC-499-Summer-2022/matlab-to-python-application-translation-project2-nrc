import os
import tempfile
import pytest
from nrcemt.alignment_software.engine.file_discovery import (
    list_file_sequence
)


def test_list_file_sequence():
    with tempfile.TemporaryDirectory() as temp_dirname:
        create_empty_file(os.path.join(temp_dirname, "test_001.txt"))
        create_empty_file(os.path.join(temp_dirname, "test_002.txt"))
        create_empty_file(os.path.join(temp_dirname, "test_003.txt"))
        create_empty_file(os.path.join(temp_dirname, "test_004.txt"))
        create_empty_file(os.path.join(temp_dirname, "abcd_002.txt"))
        create_empty_file(os.path.join(temp_dirname, "test_005.etc"))
        create_empty_file(os.path.join(temp_dirname, "Test_005.txt"))
        create_empty_file(os.path.join(temp_dirname, "test_006.txt"))
        first_filename = os.path.join(temp_dirname, "test_001.txt")
        assert list(list_file_sequence(first_filename)) == [
            os.path.join(temp_dirname, "test_001.txt"),
            os.path.join(temp_dirname, "test_002.txt"),
            os.path.join(temp_dirname, "test_003.txt"),
            os.path.join(temp_dirname, "test_004.txt")
        ]


def test_list_file_sequence_empty():
    with tempfile.TemporaryDirectory() as temp_dirname:
        create_empty_file(os.path.join(temp_dirname, "abcd_001.txt"))
        create_empty_file(os.path.join(temp_dirname, "test_001.etc"))
        first_filename = os.path.join(temp_dirname, "test_001.txt")
        with pytest.raises(FileNotFoundError):
            list(list_file_sequence(first_filename))


def test_list_file_sequence_no_dir():
    with pytest.raises(FileNotFoundError):
        first_filename = os.path.join("does-not-exist", "test_001.txt")
        list(list_file_sequence(first_filename))


def create_empty_file(filename):
    open(filename, 'wb').close()
