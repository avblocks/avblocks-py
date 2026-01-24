"""
Tests for string_util module.
"""

import ctypes
import pytest
from avblocks.string_util import decode_utf16le_string, encode_utf16le_string


class TestDecodeUtf16leString:
    """Tests for decode_utf16le_string function."""
    
    def test_decode_empty_string(self):
        """Test decoding an empty UTF-16-LE string."""
        # Create a null-terminated empty string
        buffer = ctypes.create_string_buffer(b'\x00\x00')
        ptr = ctypes.addressof(buffer)
        
        result = decode_utf16le_string(ptr)
        assert result == ""
    
    def test_decode_null_pointer(self):
        """Test decoding a null pointer returns empty string."""
        result = decode_utf16le_string(None)
        assert result == ""
        
        result = decode_utf16le_string(0)
        assert result == ""
    
    def test_decode_ascii_string(self):
        """Test decoding ASCII characters in UTF-16-LE."""
        # "Hello" in UTF-16-LE with null terminator
        buffer = ctypes.create_string_buffer(b'H\x00e\x00l\x00l\x00o\x00\x00\x00')
        ptr = ctypes.addressof(buffer)
        
        result = decode_utf16le_string(ptr)
        assert result == "Hello"
    
    def test_decode_unicode_string(self):
        """Test decoding Unicode characters in UTF-16-LE."""
        # "Hello 世界" in UTF-16-LE
        test_string = "Hello 世界"
        encoded = test_string.encode('utf-16-le') + b'\x00\x00'
        buffer = ctypes.create_string_buffer(encoded)
        ptr = ctypes.addressof(buffer)
        
        result = decode_utf16le_string(ptr)
        assert result == test_string
    
    def test_decode_emoji(self):
        """Test decoding emoji characters in UTF-16-LE."""
        test_string = "Hello 👋🌍"
        encoded = test_string.encode('utf-16-le') + b'\x00\x00'
        buffer = ctypes.create_string_buffer(encoded)
        ptr = ctypes.addressof(buffer)
        
        result = decode_utf16le_string(ptr)
        assert result == test_string
    
    def test_decode_special_characters(self):
        """Test decoding strings with special characters."""
        test_string = "Test\nLine\tTab"
        encoded = test_string.encode('utf-16-le') + b'\x00\x00'
        buffer = ctypes.create_string_buffer(encoded)
        ptr = ctypes.addressof(buffer)
        
        result = decode_utf16le_string(ptr)
        assert result == test_string


class TestEncodeUtf16leString:
    """Tests for encode_utf16le_string function."""
    
    def test_encode_empty_string(self):
        """Test encoding an empty string."""
        ptr = encode_utf16le_string("")
        
        # Verify it's null-terminated
        assert ctypes.c_uint16.from_address(ptr.value).value == 0
    
    def test_encode_ascii_string(self):
        """Test encoding ASCII characters to UTF-16-LE."""
        test_string = "Hello"
        ptr = encode_utf16le_string(test_string)
        
        # Decode and verify
        result = decode_utf16le_string(ptr.value)
        assert result == test_string
    
    def test_encode_unicode_string(self):
        """Test encoding Unicode characters to UTF-16-LE."""
        test_string = "Hello 世界"
        ptr = encode_utf16le_string(test_string)
        
        # Decode and verify
        result = decode_utf16le_string(ptr.value)
        assert result == test_string
    
    def test_encode_emoji(self):
        """Test encoding emoji characters to UTF-16-LE."""
        test_string = "Hello 👋🌍"
        ptr = encode_utf16le_string(test_string)
        
        # Decode and verify
        result = decode_utf16le_string(ptr.value)
        assert result == test_string
    
    def test_encode_special_characters(self):
        """Test encoding strings with special characters."""
        test_string = "Test\nLine\tTab"
        ptr = encode_utf16le_string(test_string)
        
        # Decode and verify
        result = decode_utf16le_string(ptr.value)
        assert result == test_string
    
    def test_encode_null_termination(self):
        """Test that encoded strings are properly null-terminated."""
        test_string = "Test"
        ptr = encode_utf16le_string(test_string)
        
        # Calculate expected size (4 chars * 2 bytes + 2 bytes for null)
        expected_size = len(test_string) * 2
        
        # Check null terminator is present at the correct position
        null_pos = ptr.value + expected_size
        assert ctypes.c_uint16.from_address(null_pos).value == 0
    
    def test_encode_no_bom(self):
        """Test that encoding doesn't include BOM."""
        test_string = "Test"
        ptr = encode_utf16le_string(test_string)
        
        # First character should be 'T' (0x0054), not BOM (0xFEFF)
        first_char = ctypes.c_uint16.from_address(ptr.value).value
        assert first_char == ord('T')
        assert first_char != 0xFEFF


class TestRoundTrip:
    """Tests for encode/decode round-trip operations."""
    
    @pytest.mark.parametrize("test_string", [
        "",
        "Hello",
        "Hello World",
        "Hello 世界",
        "😀🎉🌟",
        "Test\nWith\tSpecial\rChars",
        "Путин хуйло",
        "مرحبا بالعالم",
        "こんにちは世界",
    ])
    def test_round_trip(self, test_string):
        """Test that encoding and decoding returns the original string."""
        ptr = encode_utf16le_string(test_string)
        result = decode_utf16le_string(ptr.value)
        assert result == test_string
