import re
import os


file_sequence_expression = re.compile(r"^([\w\.]+)([0-9]{3})(\.[a-zA-Z0-9]+)$")


def list_file_sequence(first_filename):
    dirname = os.path.dirname(first_filename)
    first_basename = os.path.basename(first_filename)
    basename_match = file_sequence_expression.match(first_basename)
    first_start = basename_match.group(1)
    first_seq = basename_match.group(2)
    first_ext = basename_match.group(3)
    if first_seq != "001":
        raise ValueError("first sequence number must be 001")
    sequence_number = 1
    for basename in sorted(list_file_basenames(dirname)):
        basename_match = file_sequence_expression.match(basename)
        if basename_match.group(1) != first_start:
            continue
        if basename_match.group(2) != f"{sequence_number:03d}":
            continue
        if basename_match.group(3) != first_ext:
            continue
        sequence_number += 1
        yield os.path.join(dirname, basename)
    if sequence_number == 1:
        raise FileNotFoundError("first file in sequence not found")


def list_file_basenames(dirname):
    for basename in os.listdir(dirname):
        if os.path.isfile(os.path.join(dirname, basename)):
            yield basename
