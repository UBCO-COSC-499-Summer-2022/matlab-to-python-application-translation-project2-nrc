"""
This module allows reading of DM3 files.
It is based on the following DM3 Image Format description:
https://imagej.nih.gov/ij/plugins/DM3Format.gj.html
"""

from struct import Struct
import sys
import numpy as np

# https://en.wikipedia.org/wiki/Endianness
IS_SYSTEM_LITTLE_ENDIAN = sys.byteorder == "little"

TAG_GROUP_ENTRY = 20
TAG_DATA_ENTRY = 21

# mapping human readeable types to ids
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

# mapping ids to binary data structures
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

# mapping ids to types for numpy arrays
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
    """The root element of a DM3 image file."""

    def __init__(self, tag_group, version=3, size=None, is_little_endian=True):
        if version != 3:
            raise ValueError(f"invalid dm3 file version {version}")
        if is_little_endian != IS_SYSTEM_LITTLE_ENDIAN:
            raise NotImplementedError("DM3 file and system endianess differ")
        self.version = version
        self.size = size
        self.is_little_endian = is_little_endian
        self.tag_group = tag_group

    @classmethod
    def read(cls, file):
        """A DM3 file can be read via this class method."""
        version = read_big_endian_long(file)
        size = read_big_endian_long(file)
        is_little_endian = read_big_endian_long(file) == 1
        tag_group = DM3TagGroup.read(file)
        image = cls(tag_group, version, size, is_little_endian)
        return image


class DM3TagGroup:
    """
    A group of tag entries with labels.
    tags can be either: another nested tag group or data
    """

    def __init__(self, is_sorted, is_open):
        self.is_sorted = is_sorted
        self.is_open = is_open
        self.tags = []

    @classmethod
    def read(cls, file):
        is_sorted = read_byte(file) == 1
        is_open = read_byte(file) == 1
        entry_count = read_big_endian_long(file)
        tag_group = cls(is_sorted, is_open)
        for _ in range(entry_count):
            entry_type = read_byte(file)
            entry_label = read_label(file)
            if entry_type == TAG_GROUP_ENTRY:
                tag_group.tags.append((entry_label, DM3TagGroup.read(file)))
            elif entry_type == TAG_DATA_ENTRY:
                tag_group.tags.append((entry_label, DM3Data.read(file)))
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


class DM3Data:
    """
    A type that stores raw bytes and DM3 type information separately.
    decode() should be used to get a useful value.
    """

    def __init__(self, data_type, data_bytes):
        self.data_type = data_type
        self.data_bytes = data_bytes

    def decode(self):
        return self.data_type.decode(self.data_bytes)

    @classmethod
    def read(cls, file):
        if file.read(4) != b"%%%%":
            raise ValueError("invalid DM3 data encoding")
        type_encodiing_length = read_big_endian_long(file)
        if type_encodiing_length < 1:
            raise ValueError("DM3 encoded type length must be >1")
        data_type = DM3DataType.read(file)
        data_bytes = file.read(data_type.size())
        return cls(data_type, data_bytes)


class DM3DataType:
    """
    A description of a DM3 type.
    Can be a simple type or a complex nested type.
    """

    def __init__(
            self, encoded_type, length=None,
            array_type=None, struct_fields=None):
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
                return np.frombuffer(
                    data_bytes,
                    SCALAR_NUMPY_TYPES[self.array_type.encoded_type]
                )
            else:
                raise NotImplementedError("non-scalar array decoding")
        elif self.encoded_type == ENCODED_TYPES["STRING"]:
            return data_bytes.decode("utf-16-le")
        else:
            return None

    @classmethod
    def read(cls, file):
        encoded_type = read_big_endian_long(file)
        if encoded_type in SCALAR_STRUCT:
            return cls(encoded_type)
        elif encoded_type == ENCODED_TYPES["STRUCT"]:
            struct_name_length = read_big_endian_long(file)
            struct_field_count = read_big_endian_long(file)
            struct_fields = []
            for _ in range(struct_field_count):
                field_name_length = read_big_endian_long(file)
                field_type = DM3DataType.read(file)
                struct_fields.append((field_name_length, field_type))
            return cls(
                encoded_type,
                length=struct_name_length,
                struct_fields=struct_fields
            )
        elif encoded_type == ENCODED_TYPES["STRING"]:
            string_length = read_big_endian_long(file)
            return cls(encoded_type, length=string_length)
        elif encoded_type == ENCODED_TYPES["ARRAY"]:
            array_type = DM3DataType.read(file)
            array_length = read_big_endian_long(file)
            return cls(
                encoded_type, length=array_length, array_type=array_type)
        else:
            raise ValueError(f"unrecognized DM3 encoded type {encoded_type}")


def read_byte(file):
    """Reads a single byte from a file."""
    return Struct("B").unpack(file.read(1))[0]


def read_big_endian_short(file):
    """Reads a two byte BE short from a file."""
    return Struct(">H").unpack(file.read(2))[0]


def read_big_endian_long(file):
    """Reads a four byte BE long from a file."""
    return Struct(">I").unpack(file.read(4))[0]


def read_label(file):
    """
    Reads a 1 character per byte string from a file.
    encoding: https://en.wikipedia.org/wiki/ISO/IEC_8859-1
    """
    length = read_big_endian_short(file)
    return file.read(length).decode("latin-1")
