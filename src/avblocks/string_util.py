"""
Utility functions for string operations.
"""

import ctypes


def decode_utf16le_string(str_ptr: ctypes.c_void_p) -> str:
    """
    Reads a null-terminated UTF-16-LE string from a pointer.
    
    Args:
        str_ptr: Pointer to the UTF-16-LE string.
        
    Returns:
        The decoded string.
    """
    if not str_ptr:
        return ""
    
    # Find null terminator in UTF-16-LE string
    size = 0
    while ctypes.c_uint16.from_address(str_ptr + size).value != 0:
        size += 2
    # Read and decode the string
    return ctypes.string_at(str_ptr, size).decode('utf-16-le')


def encode_utf16le_string(value: str) -> ctypes.c_void_p:
    """
    Encodes a string to UTF-16-LE without BOM and null-terminates it.
    
    Args:
        value: The string to encode.
        
    Returns:
        A void pointer to the encoded string buffer.
    """
    # Encode to UTF-16-LE without BOM and null-terminate
    encoded = value.encode('utf-16-le') + b'\x00\x00'
    # Create a buffer to keep the data alive
    str_buffer = ctypes.create_string_buffer(encoded)
    # Cast to void pointer
    return ctypes.cast(str_buffer, ctypes.c_void_p)