"""
This module allows reading and writing of DM3 files.
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

    def write(self, file):
        """A DM3 file can be writtend via this method."""
        write_big_endian_long(file, self.version)
        file_size_pos = file.tell()
        write_big_endian_long(file, 0)
        write_big_endian_long(file, 1 if self.is_little_endian else 0)
        self.tag_group.write(file)
        file_end_pos = file.tell()
        file_size = file_end_pos - file_size_pos - 4
        file.seek(file_size_pos)
        write_big_endian_long(file, file_size)
        file.seek(file_end_pos)
        # the dm3 files we received as samples all had 8 bytes of padding
        # at the end, no idea why
        write_big_endian_long(file, 0)
        write_big_endian_long(file, 0)

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

    def write(self, file):
        write_byte(file, 1 if self.is_sorted else 0)
        write_byte(file, 1 if self.is_open else 0)
        write_big_endian_long(file, len(self.tags))
        for entry_label, entry in self.tags:
            if isinstance(entry, DM3TagGroup):
                write_byte(file, TAG_GROUP_ENTRY)
            elif isinstance(entry, DM3Data):
                write_byte(file, TAG_DATA_ENTRY)
            else:
                raise ValueError("invalid DM3 tag entry type")
            write_label(file, entry_label)
            entry.write(file)

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

    def write(self, file):
        if len(self.data_bytes) != self.data_type.size():
            raise ValueError("DM3 data length does not match type")
        file.write(b"%%%%")
        type_length_pos = file.tell()
        write_big_endian_long(file, 0)
        self.data_type.write(file)
        data_pos = file.tell()
        type_length = (data_pos - type_length_pos - 4) // 4
        file.seek(type_length_pos)
        write_big_endian_long(file, type_length)
        file.seek(data_pos)
        file.write(self.data_bytes)

    @classmethod
    def read(cls, file):
        if file.read(4) != b"%%%%":
            raise ValueError("invalid DM3 data encoding")
        type_length = read_big_endian_long(file)
        if type_length < 1:
            raise ValueError("DM3 encoded type length must be >1")
        data_type = DM3DataType.read(file)
        data_bytes = file.read(data_type.size())
        return cls(data_type, data_bytes)


class DM3DataType:
    """
    A description of a DM3 type.
    Wraps an underlying, which is one of:
    - DM3ScalarType
    - DM3StructType
    - DM3StringType
    - DM3ArrayType
    """

    def __init__(self, encoded_type, underlying_type):
        self.encoded_type = encoded_type
        self.underlying_type = underlying_type

    def size(self):
        return self.underlying_type.size()

    def decode(self, data_bytes):
        return self.underlying_type.decode(data_bytes)

    def write(self, file):
        write_big_endian_long(file, self.encoded_type)
        self.underlying_type.write(file)

    @classmethod
    def read(cls, file):
        encoded_type = read_big_endian_long(file)
        if encoded_type in SCALAR_STRUCT:
            return cls(encoded_type, DM3ScalarType(encoded_type))
        elif encoded_type == ENCODED_TYPES["STRUCT"]:
            return cls(encoded_type, DM3StructType.read(file))
        elif encoded_type == ENCODED_TYPES["STRING"]:
            return cls(encoded_type, DM3StringType.read(file))
        elif encoded_type == ENCODED_TYPES["ARRAY"]:
            return cls(encoded_type, DM3ArrayType.read(file))
        else:
            raise ValueError(f"unrecognized DM3 encoded type {encoded_type}")


class DM3ScalarType:
    """
    A simple DM3 scalar type, numerical or boolean.
    """

    def __init__(self, encoded_type):
        self.structure = SCALAR_STRUCT[encoded_type]

    def decode(self, data_bytes):
        return self.structure.unpack(data_bytes)[0]

    def size(self):
        return self.structure.size

    def write(self, file):
        pass


class DM3StructType:
    """
    A DM3 structure type with named and typed fields.
    """

    def __init__(self, struct_name_length, field_name_lengths, field_types):
        self.struct_name_length = struct_name_length
        self.field_name_lengths = field_name_lengths
        self.field_types = field_types

    def decode(self, data_bytes):
        raise NotImplementedError("dm3 struct decoding not implemented")

    def size(self):
        size = self.struct_name_length
        for field_name_length in self.field_name_lengths:
            size += field_name_length
        for field_type in self.field_types:
            size += field_type.size()
        return size

    def write(self, file):
        write_big_endian_long(file, self.struct_name_length)
        if len(self.field_name_lengths) != len(self.field_types):
            raise ValueError("struct field count not consistent")
        write_big_endian_long(file, len(self.field_types))
        for i, field_type in enumerate(self.field_types):
            write_big_endian_long(file, self.field_name_lengths[i])
            field_type.write(file)

    @classmethod
    def read(cls, file):
        struct_name_length = read_big_endian_long(file)
        struct_field_count = read_big_endian_long(file)
        field_name_lengths = []
        field_types = []
        for _ in range(struct_field_count):
            field_name_lengths.append(read_big_endian_long(file))
            field_types.append(DM3DataType.read(file))
        return cls(
            struct_name_length,
            field_name_lengths,
            field_types
        )


class DM3StringType:
    """
    A DM3 utf-16 encoded string type.
    """

    def __init__(self, string_length):
        self.string_length = string_length

    def decode(self, data_bytes):
        return data_bytes.decode("utf-16-le")

    def size(self):
        return 2 * self.string_length

    def write(self, file):
        write_big_endian_long(file, self.string_length)

    @classmethod
    def read(cls, file):
        string_length = read_big_endian_long(file)
        return cls(string_length)


class DM3ArrayType:
    """
    A DM3 array type. All array elements of the same type.
    """

    def __init__(self, array_type, array_length):
        self.array_type = array_type
        self.array_length = array_length

    def decode(self, data_bytes):
        if self.array_type.encoded_type in SCALAR_STRUCT:
            return np.frombuffer(
                data_bytes,
                SCALAR_NUMPY_TYPES[self.array_type.encoded_type]
            )
        else:
            raise NotImplementedError("non-scalar array decoding")

    def size(self):
        return self.array_length * self.array_type.size()

    def write(self, file):
        self.array_type.write(file)
        write_big_endian_long(file, self.array_length)

    @classmethod
    def read(cls, file):
        array_type = DM3DataType.read(file)
        array_length = read_big_endian_long(file)
        return cls(array_type, array_length)


def read_byte(file):
    """Reads a single byte from a file."""
    return Struct("B").unpack(file.read(1))[0]


def write_byte(file, n):
    """Writes a single byte from a file."""
    file.write(Struct("B").pack(n))


def read_big_endian_short(file):
    """Reads a two byte BE short from a file."""
    return Struct(">H").unpack(file.read(2))[0]


def write_big_endian_short(file, n):
    """Writes a two byte BE short from a file."""
    file.write(Struct(">H").pack(n))


def read_big_endian_long(file):
    """Reads a four byte BE long from a file."""
    return Struct(">I").unpack(file.read(4))[0]


def write_big_endian_long(file, n):
    """Writes a four byte BE long from a file."""
    file.write(Struct(">I").pack(n))


def read_label(file):
    """
    Reads a 1 character per byte string from a file.
    encoding: https://en.wikipedia.org/wiki/ISO/IEC_8859-1
    """
    length = read_big_endian_short(file)
    return file.read(length).decode("latin-1")


def write_label(file, string):
    """
    Reads a 1 character per byte string from a file.
    encoding: https://en.wikipedia.org/wiki/ISO/IEC_8859-1
    """
    write_big_endian_short(file, len(string))
    file.write(string.encode("latin-1"))
