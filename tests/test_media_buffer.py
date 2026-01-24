"""
Unit tests for MediaBuffer class.
"""

import pytest
from avblocks.media_buffer import MediaBuffer


class TestMediaBufferConstruction:
    """Test MediaBuffer construction."""
    
    def test_default_construction(self):
        """Test creating MediaBuffer with no arguments."""
        mb = MediaBuffer()
        
        assert mb.start is None
        assert mb.data is None
        assert mb.data_offset == 0
        assert mb.data_size == 0
        assert mb.capacity == 0
        assert not mb.external
    
    def test_construction_with_buffer_size(self):
        """Test creating MediaBuffer with specified size."""
        mb = MediaBuffer(buffer_size=1024)
        
        assert mb.start is not None
        assert len(mb.start) == 1024
        assert mb.capacity == 1024
        assert mb.data_offset == 0
        assert mb.data_size == 0
        assert not mb.external
    
    def test_construction_with_bytes(self):
        """Test creating MediaBuffer with bytes data."""
        data = b"Hello, World!"
        mb = MediaBuffer(data=data)
        
        assert mb.start is not None
        assert len(mb.start) == len(data)
        assert mb.capacity == len(data)
        assert mb.data_size == len(data)
        assert mb.data_offset == 0
        assert mb.external
        assert bytes(mb.data) == data
    
    def test_construction_with_bytearray(self):
        """Test creating MediaBuffer with bytearray data."""
        data = bytearray(b"Hello, World!")
        mb = MediaBuffer(data=data)
        
        assert mb.start is data  # Should be same reference
        assert mb.capacity == len(data)
        assert mb.data_size == len(data)
        assert mb.external


class TestMediaBufferSetData:
    """Test MediaBuffer set_data method."""
    
    def test_set_data_valid(self):
        """Test setting valid data offset and size."""
        mb = MediaBuffer(buffer_size=100)
        
        assert mb.set_data(10, 50)
        assert mb.data_offset == 10
        assert mb.data_size == 50
    
    def test_set_data_zero_offset(self):
        """Test setting data with zero offset."""
        mb = MediaBuffer(buffer_size=100)
        
        assert mb.set_data(0, 100)
        assert mb.data_offset == 0
        assert mb.data_size == 100
    
    def test_set_data_invalid_offset_negative(self):
        """Test setting data with negative offset."""
        mb = MediaBuffer(buffer_size=100)
        
        assert not mb.set_data(-1, 50)
        assert mb.data_offset == 0
        assert mb.data_size == 0
    
    def test_set_data_invalid_offset_too_large(self):
        """Test setting data with offset beyond capacity."""
        mb = MediaBuffer(buffer_size=100)
        
        assert not mb.set_data(100, 10)
        assert mb.data_offset == 0
        assert mb.data_size == 0
    
    def test_set_data_invalid_size_negative(self):
        """Test setting data with negative size."""
        mb = MediaBuffer(buffer_size=100)
        
        assert not mb.set_data(0, -1)
        assert mb.data_offset == 0
        assert mb.data_size == 0
    
    def test_set_data_invalid_size_exceeds_capacity(self):
        """Test setting data with size that exceeds capacity."""
        mb = MediaBuffer(buffer_size=100)
        
        assert not mb.set_data(50, 60)
        assert mb.data_offset == 0
        assert mb.data_size == 0
    
    def test_set_data_no_buffer(self):
        """Test setting data when no buffer exists."""
        mb = MediaBuffer()
        
        assert not mb.set_data(0, 10)


class TestMediaBufferResetData:
    """Test MediaBuffer reset_data method."""
    
    def test_reset_data(self):
        """Test resetting data offset and size."""
        mb = MediaBuffer(buffer_size=100)
        mb.set_data(10, 50)
        
        mb.reset_data()
        
        assert mb.data_offset == 0
        assert mb.data_size == 0
        assert mb.capacity == 100  # Capacity unchanged


class TestMediaBufferAttach:
    """Test MediaBuffer attach method."""
    
    def test_attach_bytes(self):
        """Test attaching bytes buffer."""
        mb = MediaBuffer()
        data = b"Test data"
        
        assert mb.attach(data)
        assert mb.external
        assert mb.data_offset == 0
        assert mb.data_size == len(data)
        assert mb.capacity == len(data)
    
    def test_attach_bytearray(self):
        """Test attaching bytearray buffer."""
        mb = MediaBuffer()
        data = bytearray(b"Test data")
        
        assert mb.attach(data)
        assert mb.start is data  # Should be same reference
        assert mb.external
    
    def test_attach_without_set_data(self):
        """Test attaching buffer without setting data size."""
        mb = MediaBuffer()
        data = b"Test data"
        
        assert mb.attach(data, set_data=False)
        assert mb.external
        assert mb.data_offset == 0
        assert mb.data_size == 0
        assert mb.capacity == len(data)
    
    def test_attach_none(self):
        """Test attaching None buffer."""
        mb = MediaBuffer()
        
        assert not mb.attach(None)
        assert not mb.external
    
    def test_attach_replaces_existing(self):
        """Test that attach replaces existing buffer."""
        mb = MediaBuffer(buffer_size=100)
        old_buffer = mb.start
        new_data = b"New data"
        
        assert mb.attach(new_data)
        assert mb.start is not old_buffer
        assert mb.external


class TestMediaBufferDetach:
    """Test MediaBuffer detach method."""
    
    def test_detach_external_buffer(self):
        """Test detaching external buffer."""
        data = bytearray(b"Test data")
        mb = MediaBuffer(data=data)
        
        detached = mb.detach()
        
        assert detached is data
        assert mb.start is None
        assert not mb.external
        assert mb.data_offset == 0
        assert mb.data_size == 0
    
    def test_detach_non_external_buffer(self):
        """Test detaching non-external buffer returns None."""
        mb = MediaBuffer(buffer_size=100)
        
        detached = mb.detach()
        
        assert detached is None
        assert mb.start is not None  # Internal buffer unchanged
        assert not mb.external
    
    def test_detach_no_buffer(self):
        """Test detaching when no buffer exists."""
        mb = MediaBuffer()
        
        detached = mb.detach()
        
        assert detached is None
        assert not mb.external


class TestMediaBufferClone:
    """Test MediaBuffer clone method."""
    
    def test_clone_internal_buffer(self):
        """Test cloning MediaBuffer with internal buffer."""
        mb = MediaBuffer(buffer_size=100)
        mb.set_data(10, 50)
        mb.start[10:60] = b"X" * 50
        
        cloned = mb.clone()
        
        assert cloned is not mb
        assert cloned.start is not mb.start  # Deep copy
        assert cloned.data_offset == mb.data_offset
        assert cloned.data_size == mb.data_size
        assert cloned.capacity == mb.capacity
        assert not cloned.external
        assert bytes(cloned.start) == bytes(mb.start)
    
    def test_clone_external_buffer(self):
        """Test cloning MediaBuffer with external buffer."""
        data = bytearray(b"Test data")
        mb = MediaBuffer(data=data)
        
        cloned = mb.clone()
        
        assert cloned is not mb
        assert cloned.start is data  # Shallow copy for external
        assert cloned.data_offset == mb.data_offset
        assert cloned.data_size == mb.data_size
        assert cloned.external
    
    def test_clone_empty_buffer(self):
        """Test cloning empty MediaBuffer."""
        mb = MediaBuffer()
        
        cloned = mb.clone()
        
        assert cloned is not mb
        assert cloned.start is None
        assert cloned.data_offset == 0
        assert cloned.data_size == 0


class TestMediaBufferDataProperty:
    """Test MediaBuffer data property."""
    
    def test_data_property_with_offset(self):
        """Test data property returns correct view with offset."""
        mb = MediaBuffer(buffer_size=20)
        mb.start[5:15] = b"HelloWorld"
        mb.set_data(5, 10)
        
        data_view = mb.data
        
        assert len(data_view) == 10
        assert bytes(data_view) == b"HelloWorld"
    
    def test_data_property_no_offset(self):
        """Test data property with no offset."""
        mb = MediaBuffer(data=b"Hello")
        
        data_view = mb.data
        
        assert len(data_view) == 5
        assert bytes(data_view) == b"Hello"
    
    def test_data_property_no_buffer(self):
        """Test data property when no buffer exists."""
        mb = MediaBuffer()
        
        assert mb.data is None


class TestMediaBufferIntegration:
    """Integration tests for MediaBuffer."""
    
    def test_workflow_create_fill_read(self):
        """Test typical workflow: create, fill, read."""
        # Create buffer
        mb = MediaBuffer(buffer_size=100)
        
        # Fill with data
        test_data = b"Integration test data"
        mb.start[0:len(test_data)] = test_data
        mb.set_data(0, len(test_data))
        
        # Read data
        assert bytes(mb.data) == test_data
        assert mb.data_size == len(test_data)
    
    def test_workflow_attach_detach(self):
        """Test attach/detach workflow."""
        # Create buffer with external data
        external_data = bytearray(b"External buffer")
        mb = MediaBuffer()
        
        # Attach
        mb.attach(external_data)
        assert mb.external
        assert bytes(mb.data) == b"External buffer"
        
        # Modify
        external_data[0:8] = b"Modified"
        assert bytes(mb.data) == b"Modified buffer"
        
        # Detach
        detached = mb.detach()
        assert detached is external_data
        assert mb.start is None
    
    def test_workflow_clone_modify(self):
        """Test clone and modify workflow."""
        # Create and fill buffer
        mb = MediaBuffer(buffer_size=20)
        mb.start[0:5] = b"Hello"
        mb.set_data(0, 5)
        
        # Clone
        cloned = mb.clone()
        
        # Modify original
        mb.start[0:5] = b"World"
        
        # Verify clone is unchanged
        assert bytes(cloned.data) == b"Hello"
        assert bytes(mb.data) == b"World"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
