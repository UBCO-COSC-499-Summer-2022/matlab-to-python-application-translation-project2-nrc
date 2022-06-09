# https://imagej.nih.gov/ij/plugins/DM3Format.gj.html

import struct
import sys
from typing import Type
import numpy as np
from struct import Struct
from collections import OrderedDict
import matplotlib.pyplot as plt

IS_SYSTEM_LITTLE_ENDIAN = sys.byteorder == "little"

TAG_GROUP_ENTRY = 20
TAG_DATA_ENTRY = 21

ENCODED_TYPES = {
    "SHORT": 2,
    "LONG": 3,
    "USHORT": 4,
    "ULONG": 5,
    "FLOAT": 6,
    "DOUBLE": 7,
    "BOOLEAN": 8,
    "CHAR": 9,
    "OCTET": 10,
    "STRUCT": 15,
    "STRING": 18,
    "ARRAY": 20
}

SCALAR_STRUCT = {
    2: Struct("h"),  # SHORT
    3: Struct("i"),  # LONG
    4: Struct("H"),  # USHORT
    5: Struct("I"),  # ULONG
    6: Struct("f"),  # FLOAT
    7: Struct("d"),  # DOUBLE
    8: Struct("?"),  # BOOLEAN
    9: Struct("b"),  # CHAR
    10: Struct("B")  # OCTET
}

SCALAR_NUMPY_TYPES = {
    2: np.int16,    # SHORT
    3: np.int32,    # LONG
    4: np.uint16,   # USHORT
    5: np.uint32,   # ULONG
    6: np.float32,  # FLOAT
    7: np.float64,  # DOUBLE
    8: np.bool8,    # BOOLEAN
    9: np.int8,     # CHAR
    10: np.uint8    # OCTET
}



class DM3Image:

    def __init__(self, version=3, size=None, is_little_endian=True, tag_group=None):
        if version != 3:
            raise ValueError(f"invalid dm3 file version {version}")
        if is_little_endian != IS_SYSTEM_LITTLE_ENDIAN:
            raise NotImplementedError("DM3 file and system endianess differ")
        self.version = version
        self.size = size
        self.is_little_endian = is_little_endian
        self.tag_group = tag_group

    @classmethod
    def read(cls, dm3_file):
        version = read_big_endian_long(dm3_file)
        size = read_big_endian_long(dm3_file)
        is_little_endian = read_big_endian_long(dm3_file) == 1
        tag_group = DM3TagGroup.read(dm3_file)
        image = cls(version, size, is_little_endian, tag_group)
        return image

    def __repr__(self):
        return '{"version":%r,"size":%r,"is_little_endian":%r,"tag_group":%r}' % (
            self.version, self.size, self.is_little_endian, self.tag_group
        )


class DM3TagGroup:

    def __init__(self, is_sorted, is_open):
        self.is_sorted = is_sorted
        self.is_open = is_open
        self.tags = []

    @classmethod
    def read(cls, dm3_file):
        is_sorted = read_byte(dm3_file) == 1
        is_open = read_byte(dm3_file) == 1
        entry_count = read_big_endian_long(dm3_file)
        tag_group = cls(is_sorted, is_open)
        for _ in range(entry_count):
            entry_type = read_byte(dm3_file)
            entry_label = read_label(dm3_file)
            if entry_type == TAG_GROUP_ENTRY:
                tag_group.tags.append((entry_label, DM3TagGroup.read(dm3_file)))
            elif entry_type == TAG_DATA_ENTRY:
                tag_group.tags.append((entry_label, DM3Data.read(dm3_file)))
            else:
                raise ValueError(f"invalid DM3 tag entry type {entry_type}")
        return tag_group
    
    def __getitem__(self, key):
        if isinstance(key, str):
            for entry_label, entry in self.tags:
                if key == entry_label:
                    return entry
            raise KeyError(f"label {key} does not exist in DM3 tag group")
        elif isinstance(key, int):
            entry_label, entry = self.tags[key]
            return entry
        else:
            raise TypeError("DM3 tag group key must be str or int")

    def __repr__(self):
        return '{"is_sorted":%r,"is_open":%r,"tags":%r}' % (
            self.is_sorted, self.is_open, self.tags
        )


class DM3Data:

    def __init__(self, data_type, data_bytes):
        self.data_type = data_type
        self.data_bytes = data_bytes

    def decode(self):
        return self.data_type.decode(self.data_bytes)

    @classmethod
    def read(cls, dm3_file):
        if dm3_file.read(4) != b"%%%%":
            raise ValueError("invalid DM3 data encoding")
        type_encodiing_length = read_big_endian_long(dm3_file)
        if type_encodiing_length < 1:
            raise ValueError("DM3 encoded type length must be >1")
        data_type = DM3DataType.read(dm3_file)
        data_bytes = dm3_file.read(data_type.size())
        return cls(data_type, data_bytes)

    def __repr__(self):
        return repr(self.decode())


class DM3DataType:

    def __init__(self, encoded_type, length=None, array_type=None, struct_fields=None):
        self.encoded_type = encoded_type
        self.length = length
        self.array_type = array_type
        self.struct_fields = struct_fields

    def size(self):
        if self.encoded_type in SCALAR_STRUCT:
            return SCALAR_STRUCT[self.encoded_type].size
        elif self.encoded_type == ENCODED_TYPES["STRUCT"]:
            size = self.length
            for field_name_length, field_type in self.struct_fields:
                size += field_name_length + field_type.size()
            return size
        elif self.encoded_type == ENCODED_TYPES["STRING"]:
            return 2 * self.length
        elif self.encoded_type == ENCODED_TYPES["ARRAY"]:
            return self.length * self.array_type.size()
        else:
            raise ValueError("unrecognized DM3 encoded type")

    def decode(self, data_bytes):
        if self.encoded_type in SCALAR_STRUCT:
            return SCALAR_STRUCT[self.encoded_type].unpack(data_bytes)[0]
        elif self.encoded_type == ENCODED_TYPES["ARRAY"]:
            if self.array_type.encoded_type in SCALAR_STRUCT:
                return np.frombuffer(data_bytes, SCALAR_NUMPY_TYPES[self.array_type.encoded_type])
            else:
                return None
        elif self.encoded_type == ENCODED_TYPES["STRING"]:
            return data_bytes.decode("utf-16-le")
        else:
            return None

    @classmethod
    def read(cls, dm3_file):
        encoded_type = read_big_endian_long(dm3_file)
        if encoded_type in SCALAR_STRUCT:
            return cls(encoded_type)
        elif encoded_type == ENCODED_TYPES["STRUCT"]:
            struct_name_length = read_big_endian_long(dm3_file)
            struct_field_count = read_big_endian_long(dm3_file)
            struct_fields = []
            for _ in range(struct_field_count):
                field_name_length = read_big_endian_long(dm3_file)
                field_type = cls(read_big_endian_long(dm3_file))
                struct_fields.append((field_name_length, field_type))
            return cls(encoded_type, length=struct_name_length, struct_fields=struct_fields)
        elif encoded_type == ENCODED_TYPES["STRING"]:
            string_length = read_big_endian_long(dm3_file)
            return cls(encoded_type, length=string_length)
        elif encoded_type == ENCODED_TYPES["ARRAY"]:
            array_type = DM3DataType.read(dm3_file)
            array_length = read_big_endian_long(dm3_file)
            return cls(
                encoded_type, length=array_length, array_type=array_type)
        else:
            raise ValueError(f"unrecognized DM3 encoded type {encoded_type}")


def read_byte(dm3_file):
    return struct.unpack("B", dm3_file.read(1))[0]


def read_big_endian_short(dm3_file):
    return struct.unpack(">H", dm3_file.read(2))[0]


def read_big_endian_long(dm3_file):
    return struct.unpack(">I", dm3_file.read(4))[0]


def read_label(dm3_file):
    length = read_big_endian_short(dm3_file)
    return dm3_file.read(length).decode("latin-1")


if __name__ == "__main__":
    FILEPATH = "/Users/luctowers/Documents/ubco/cosc499/matlab-to-python-application-translation-project2-nrc/scratch/nrc-matlab-legacy/Alignment Software V1.17/tilt series/image_001.dm3"
    with open(FILEPATH, "rb") as dm3_file:
        dm3 = DM3Image.read(dm3_file)
        image_array = dm3.tag_group["ImageList"][0]["ImageData"]["Data"].decode()
        width = dm3.tag_group["ImageList"][0]["ImageData"]["Dimensions"][0].decode()
        height = dm3.tag_group["ImageList"][0]["ImageData"]["Dimensions"][1].decode()
        image_data = np.reshape(image_array, (width, height))
        plt.matshow(image_data)
        plt.colorbar()
        plt.show()
