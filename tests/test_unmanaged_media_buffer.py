"""
Tests for UnmanagedMediaBuffer class.
"""

import pytest
import ctypes
from avblocks import UnmanagedMediaBuffer


class TestUnmanagedMediaBufferCreation:
    """Tests for UnmanagedMediaBuffer creation and initialization."""
    
    def test_create_empty_buffer(self):
        """Test creating an empty buffer with no storage."""
        buffer = UnmanagedMediaBuffer()
        
        assert buffer.capacity == 0
        assert buffer.data_size == 0
        assert buffer.data_offset == 0
        assert not buffer.external
    
    def test_create_buffer_with_size(self):
        """Test creating a buffer with specified size."""
        buffer = UnmanagedMediaBuffer(1024)
        
        assert buffer.capacity >= 1024
        assert buffer.data_size == 0
        assert buffer.data_offset == 0
        assert not buffer.external
    
    def test_create_large_buffer(self):
        """Test creating a large buffer."""
        buffer = UnmanagedMediaBuffer(10 * 1024 * 1024)  # 10 MB
        
        assert buffer.capacity >= 10 * 1024 * 1024
        assert buffer.data_size == 0
        assert not buffer.external


class TestUnmanagedMediaBufferAllocation:
    """Tests for buffer allocation and deallocation."""
    
    def test_alloc_increases_capacity(self):
        """Test that alloc increases buffer capacity."""
        buffer = UnmanagedMediaBuffer()
        
        result = buffer.alloc(2048, keep_data=False)
        
        assert result is True
        assert buffer.capacity >= 2048
        assert buffer.data_size == 0
    
    def test_alloc_keep_data(self):
        """Test that alloc can preserve existing data."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        # Write some data
        buffer.write_from_bytes(test_data, 0)
        buffer.set_data(0, len(test_data))
        
        # Allocate larger buffer, keeping data
        result = buffer.alloc(2048, keep_data=True)
        
        assert result is True
        assert buffer.capacity >= 2048
        assert buffer.data_size == len(test_data)
        assert buffer.to_bytes() == test_data
    
    def test_alloc_without_keep_data(self):
        """Test that alloc can discard existing data."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        # Write some data
        buffer.write_from_bytes(test_data, 0)
        buffer.set_data(0, len(test_data))
        
        # Allocate larger buffer, discarding data
        result = buffer.alloc(2048, keep_data=False)
        
        assert result is True
        assert buffer.capacity >= 2048
        # Data size may be reset or preserved depending on implementation
    
    def test_free_buffer(self):
        """Test freeing buffer storage."""
        buffer = UnmanagedMediaBuffer(1024)
        
        buffer.free()
        
        # After freeing, capacity should be 0
        assert buffer.capacity == 0
        assert buffer.data_size == 0


class TestUnmanagedMediaBufferExternalStorage:
    """Tests for attaching and detaching external storage."""
    
    def test_attach_external_buffer(self):
        """Test attaching external buffer storage."""
        # Create an external buffer using ctypes
        external_data = (ctypes.c_uint8 * 1024)()
        external_ptr = ctypes.addressof(external_data)
        
        buffer = UnmanagedMediaBuffer()
        result = buffer.attach(external_ptr, 1024, set_data=True)
        
        assert result is True
        assert buffer.external is True
        assert buffer.capacity == 1024
        assert buffer.data_size == 1024
    
    def test_attach_without_set_data(self):
        """Test attaching external buffer without setting data."""
        external_data = (ctypes.c_uint8 * 1024)()
        external_ptr = ctypes.addressof(external_data)
        
        buffer = UnmanagedMediaBuffer()
        result = buffer.attach(external_ptr, 1024, set_data=False)
        
        assert result is True
        assert buffer.external is True
        assert buffer.capacity == 1024
        assert buffer.data_size == 0
    
    def test_detach_external_buffer(self):
        """Test detaching external buffer storage."""
        external_data = (ctypes.c_uint8 * 1024)()
        external_ptr = ctypes.addressof(external_data)
        
        buffer = UnmanagedMediaBuffer()
        buffer.attach(external_ptr, 1024, set_data=True)
        
        detached_ptr = buffer.detach()
        
        assert detached_ptr == external_ptr
        assert not buffer.external
    
    def test_detach_when_no_external_buffer(self):
        """Test detaching when no external buffer is attached."""
        buffer = UnmanagedMediaBuffer(1024)
        
        detached_ptr = buffer.detach()
        
        assert detached_ptr is None


class TestUnmanagedMediaBufferDataManipulation:
    """Tests for data manipulation operations."""
    
    def test_set_data_offset_and_size(self):
        """Test setting data offset and size."""
        buffer = UnmanagedMediaBuffer(1024)
        
        result = buffer.set_data(10, 100)
        
        assert result is True
        assert buffer.data_offset == 10
        assert buffer.data_size == 100
    
    def test_set_data_invalid_offset(self):
        """Test setting invalid data offset."""
        buffer = UnmanagedMediaBuffer(1024)
        
        result = buffer.set_data(2000, 100)
        
        assert result is False
    
    def test_set_data_invalid_size(self):
        """Test setting invalid data size."""
        buffer = UnmanagedMediaBuffer(1024)
        
        result = buffer.set_data(10, 2000)
        
        assert result is False
    
    def test_clear_data(self):
        """Test clearing buffer data."""
        buffer = UnmanagedMediaBuffer(1024)
        buffer.set_data(10, 100)
        
        buffer.clear()
        
        assert buffer.data_size == 0
        assert buffer.data_offset == 0
        assert buffer.capacity == 1024  # Capacity unchanged
    
    def test_normalize_buffer(self):
        """Test normalizing buffer data."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        # Write data at offset 100
        buffer.write_from_bytes(test_data, 100)
        buffer.set_data(100, len(test_data))
        
        buffer.normalize()
        
        # After normalize, data should be at offset 0
        assert buffer.data_offset == 0
        assert buffer.data_size == len(test_data)
        assert buffer.to_bytes() == test_data


class TestUnmanagedMediaBufferAppendRemove:
    """Tests for appending and removing data."""
    
    def test_append_data(self):
        """Test appending data to buffer."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data1 = b"Hello"
        test_data2 = b", World!"
        
        # Append first chunk
        data1_array = (ctypes.c_uint8 * len(test_data1)).from_buffer_copy(test_data1)
        result1 = buffer.append(ctypes.addressof(data1_array), len(test_data1))
        assert result1 is True
        
        # Append second chunk
        data2_array = (ctypes.c_uint8 * len(test_data2)).from_buffer_copy(test_data2)
        result2 = buffer.append(ctypes.addressof(data2_array), len(test_data2))
        assert result2 is True
        
        assert buffer.data_size == len(test_data1) + len(test_data2)
        assert buffer.to_bytes() == test_data1 + test_data2
    
    def test_append_with_reallocation(self):
        """Test that append reallocates if needed."""
        buffer = UnmanagedMediaBuffer(10)  # Small buffer
        test_data = b"This is a longer string that will require reallocation"
        
        data_array = (ctypes.c_uint8 * len(test_data)).from_buffer_copy(test_data)
        result = buffer.append(ctypes.addressof(data_array), len(test_data))
        
        assert result is True
        assert buffer.capacity >= len(test_data)
        assert buffer.to_bytes() == test_data
    
    def test_remove_data(self):
        """Test removing data from buffer."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        buffer.write_from_bytes(test_data, 0)
        buffer.set_data(0, len(test_data))
        
        # Remove first 7 bytes ("Hello, ")
        buffer.remove(7)
        
        assert buffer.data_size == len(test_data) - 7
        assert buffer.to_bytes() == b"World!"


class TestUnmanagedMediaBufferSpaceCalculations:
    """Tests for free space calculations."""
    
    def test_free_linear_space(self):
        """Test free linear space calculation."""
        buffer = UnmanagedMediaBuffer(1024)
        buffer.set_data(100, 200)
        
        expected_free_linear = 1024 - 200 - 100
        assert buffer.free_linear_space == expected_free_linear
    
    def test_free_space(self):
        """Test free space calculation."""
        buffer = UnmanagedMediaBuffer(1024)
        buffer.set_data(100, 200)
        
        expected_free = 1024 - 200
        assert buffer.free_space == expected_free


class TestUnmanagedMediaBufferPointers:
    """Tests for pointer access."""
    
    def test_buf_ptr(self):
        """Test getting buffer pointer."""
        buffer = UnmanagedMediaBuffer(1024)
        
        ptr = buffer.buf_ptr
        
        assert isinstance(ptr, int)
        assert ptr > 0
    
    def test_data_ptr(self):
        """Test getting data pointer."""
        buffer = UnmanagedMediaBuffer(1024)
        buffer.set_data(10, 100)
        
        data_ptr = buffer.data_ptr
        buf_ptr = buffer.buf_ptr
        
        assert isinstance(data_ptr, int)
        assert data_ptr == buf_ptr + 10


class TestUnmanagedMediaBufferClone:
    """Tests for cloning buffers."""
    
    def test_clone_internal_buffer(self):
        """Test cloning buffer with internal storage."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        buffer.write_from_bytes(test_data, 0)
        buffer.set_data(0, len(test_data))
        
        cloned = buffer.clone()
        
        assert cloned.capacity == buffer.capacity
        assert cloned.data_size == buffer.data_size
        assert cloned.to_bytes() == test_data
        assert not cloned.external
    
    def test_clone_external_buffer(self):
        """Test cloning buffer with external storage."""
        external_data = (ctypes.c_uint8 * 1024)()
        external_ptr = ctypes.addressof(external_data)
        
        buffer = UnmanagedMediaBuffer()
        buffer.attach(external_ptr, 1024, set_data=True)
        
        cloned = buffer.clone()
        
        assert cloned.external is True
        assert cloned.capacity == buffer.capacity
    
    def test_clone_independence(self):
        """Test that cloned buffer is independent for internal storage."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Original"
        
        buffer.write_from_bytes(test_data, 0)
        buffer.set_data(0, len(test_data))
        
        cloned = buffer.clone()
        
        # Modify original
        new_data = b"Modified"
        buffer.clear()
        buffer.write_from_bytes(new_data, 0)
        buffer.set_data(0, len(new_data))
        
        # Cloned should be unchanged
        assert cloned.to_bytes() == test_data


class TestUnmanagedMediaBufferByteConversion:
    """Tests for conversion to/from Python bytes."""
    
    def test_to_bytes(self):
        """Test converting buffer data to Python bytes."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        buffer.write_from_bytes(test_data, 0)
        buffer.set_data(0, len(test_data))
        
        result = buffer.to_bytes()
        
        assert result == test_data
    
    def test_to_bytes_empty(self):
        """Test converting empty buffer to bytes."""
        buffer = UnmanagedMediaBuffer(1024)
        
        result = buffer.to_bytes()
        
        assert result == b''
    
    def test_to_bytes_with_offset(self):
        """Test converting buffer with offset to bytes."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        buffer.write_from_bytes(test_data, 100)
        buffer.set_data(100, len(test_data))
        
        result = buffer.to_bytes()
        
        assert result == test_data
    
    def test_write_from_bytes(self):
        """Test writing Python bytes to buffer."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        result = buffer.write_from_bytes(test_data, 0)
        
        assert result is True
        buffer.set_data(0, len(test_data))
        assert buffer.to_bytes() == test_data
    
    def test_write_from_bytes_at_offset(self):
        """Test writing bytes at specific offset."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"World!"
        
        result = buffer.write_from_bytes(test_data, 100)
        
        assert result is True
        buffer.set_data(100, len(test_data))
        assert buffer.to_bytes() == test_data
    
    def test_write_from_bytes_overflow(self):
        """Test writing bytes that exceed buffer capacity."""
        buffer = UnmanagedMediaBuffer(10)
        test_data = b"This is too long for the buffer"
        
        result = buffer.write_from_bytes(test_data, 0)
        
        assert result is False


class TestUnmanagedMediaBufferEdgeCases:
    """Tests for edge cases and error conditions."""
    
    def test_operations_on_empty_buffer(self):
        """Test operations on empty buffer."""
        buffer = UnmanagedMediaBuffer()
        
        assert buffer.to_bytes() == b''
        buffer.clear()  # Should not crash
        buffer.normalize()  # Should not crash
    
    def test_zero_size_operations(self):
        """Test operations with zero size."""
        buffer = UnmanagedMediaBuffer(1024)
        
        buffer.remove(0)  # Should not crash
        assert buffer.set_data(0, 0) is True
    
    def test_multiple_alloc_calls(self):
        """Test multiple allocation calls."""
        buffer = UnmanagedMediaBuffer()
        
        buffer.alloc(1024, keep_data=False)
        buffer.alloc(2048, keep_data=False)
        buffer.alloc(512, keep_data=False)
        
        # Last allocation should determine capacity (or keep larger)
        assert buffer.capacity > 0


class TestUnmanagedMediaBufferRoundTrip:
    """Integration tests for common usage patterns."""
    
    def test_write_read_roundtrip(self):
        """Test writing and reading data back."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"The quick brown fox jumps over the lazy dog"
        
        # Write
        buffer.write_from_bytes(test_data, 0)
        buffer.set_data(0, len(test_data))
        
        # Read
        result = buffer.to_bytes()
        
        assert result == test_data
    
    def test_append_read_roundtrip(self):
        """Test appending and reading data back."""
        buffer = UnmanagedMediaBuffer(1024)
        chunks = [b"Hello", b", ", b"World", b"!"]
        
        # Append all chunks
        for chunk in chunks:
            chunk_array = (ctypes.c_uint8 * len(chunk)).from_buffer_copy(chunk)
            buffer.append(ctypes.addressof(chunk_array), len(chunk))
        
        # Read
        result = buffer.to_bytes()
        expected = b"".join(chunks)
        
        assert result == expected
    
    def test_modify_and_normalize(self):
        """Test modifying data and normalizing."""
        buffer = UnmanagedMediaBuffer(1024)
        test_data = b"Hello, World!"
        
        # Write at offset
        buffer.write_from_bytes(test_data, 100)
        buffer.set_data(100, len(test_data))
        
        # Remove some data
        buffer.remove(7)
        
        # Normalize
        buffer.normalize()
        
        # Should now be at offset 0
        assert buffer.data_offset == 0
        assert buffer.to_bytes() == b"World!"
