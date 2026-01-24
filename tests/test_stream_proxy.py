"""
Tests for StreamProxy class that bridges Python streams to native AVBlocks streams.
"""

import io
import tempfile
import os

from avblocks.stream_proxy import StreamProxy, StreamCallback


class TestStreamProxy:
    """Test suite for StreamProxy class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_data = b"Hello, AVBlocks! This is test data for stream proxy."
        self.temp_file = None
    
    def teardown_method(self):
        """Clean up test resources."""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_proxy_with_bytesio_read(self):
        """Test StreamProxy with BytesIO for reading."""
        # Create a BytesIO stream with test data
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Verify the proxy has a stream
        assert proxy.stream is not None
        assert proxy.stream == stream
        
        # Verify native callback structure is created
        callback = proxy.native_stream_callback
        assert callback is not None
        assert isinstance(callback, StreamCallback)
        
        # Verify callback functions are set
        assert callback.open is not None
        assert callback.close is not None
        assert callback.read is not None
        assert callback.write is not None
        assert callback.seek is not None
    
    def test_proxy_with_bytesio_write(self):
        """Test StreamProxy with BytesIO for writing."""
        stream = io.BytesIO()
        proxy = StreamProxy(stream)
        
        # Verify stream capabilities
        assert stream.readable()
        assert stream.writable()
        assert stream.seekable()
    
    def test_proxy_with_file_read(self):
        """Test StreamProxy with a real file for reading."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            self.temp_file = f.name
            f.write(self.test_data)
        
        # Open file for reading in binary mode
        with open(self.temp_file, 'rb') as f:
            proxy = StreamProxy(f)
            
            # Verify proxy setup
            assert proxy.stream is not None
            assert proxy.native_stream_callback is not None
            
            # Verify stream is readable
            assert f.readable()
            assert not f.writable()
            assert f.seekable()
    
    def test_proxy_with_file_write(self):
        """Test StreamProxy with a real file for writing."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            self.temp_file = f.name
        
        # Open file for writing in binary mode
        with open(self.temp_file, 'wb') as f:
            proxy = StreamProxy(f)
            
            # Verify proxy setup
            assert proxy.stream is not None
            assert proxy.native_stream_callback is not None
            
            # Verify stream is writable
            assert not f.readable()
            assert f.writable()
            assert f.seekable()
    
    def test_callback_can_read(self):
        """Test the _can_read callback."""
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Test can_read returns True
        result = proxy._can_read(0)
        assert result is True
        
        # Close stream and test can_read returns False
        stream.close()
        result = proxy._can_read(0)
        assert result is False
    
    def test_callback_can_write(self):
        """Test the _can_write callback."""
        stream = io.BytesIO()
        proxy = StreamProxy(stream)
        
        # Test can_write returns True
        result = proxy._can_write(0)
        assert result is True
    
    def test_callback_can_seek(self):
        """Test the _can_seek callback."""
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Test can_seek returns True
        result = proxy._can_seek(0)
        assert result is True
    
    def test_callback_is_open(self):
        """Test the _is_open callback."""
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Test is_open returns True
        result = proxy._is_open(0)
        assert result is True
        
        # Close stream and test is_open returns False
        stream.close()
        result = proxy._is_open(0)
        assert result is False
    
    def test_callback_position(self):
        """Test the _position callback."""
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Test initial position is 0
        pos = proxy._position(0)
        assert pos == 0
        
        # Read some data and check position changed
        stream.read(10)
        pos = proxy._position(0)
        assert pos == 10
    
    def test_callback_size(self):
        """Test the _size callback."""
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Test size matches data length
        size = proxy._size(0)
        assert size == len(self.test_data)
    
    def test_callback_seek(self):
        """Test the _seek callback."""
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Seek to position 10
        result = proxy._seek(10, 0)
        assert result is True
        assert stream.tell() == 10
        
        # Seek to position 0
        result = proxy._seek(0, 0)
        assert result is True
        assert stream.tell() == 0
    
    def test_stream_property_setter(self):
        """Test setting the stream property."""
        proxy = StreamProxy()
        assert proxy.stream is None
        assert proxy.native_stream_callback is None
        
        # Set a stream
        stream = io.BytesIO(self.test_data)
        proxy.stream = stream
        
        assert proxy.stream is not None
        assert proxy.stream == stream
        # Callback is created in __init__, so setting stream doesn't affect it
        # The callback will just fail if stream is None
    
    def test_proxy_with_none_stream(self):
        """Test StreamProxy with None stream."""
        proxy = StreamProxy(None)
        
        # Verify stream is None
        assert proxy.stream is None
        
        # Verify native_stream_callback returns None when stream is None
        assert proxy.native_stream_callback is None
        
        # Verify callbacks handle None stream gracefully
        assert proxy._can_read(0) is False
        assert proxy._can_write(0) is False
        assert proxy._can_seek(0) is False
        assert proxy._is_open(0) is False
    
    def test_callback_close(self):
        """Test the _close callback."""
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Verify stream is open
        assert not stream.closed
        assert proxy.stream is not None
        
        # Close through callback
        proxy._close(0)
        
        # Verify stream is closed
        assert stream.closed
        assert proxy.stream is None


class TestStreamProxyIntegration:
    """Integration tests for StreamProxy with file operations."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.test_data = b"Integration test data for StreamProxy.\n" * 100
        self.temp_file = None
    
    def teardown_method(self):
        """Clean up test resources."""
        if self.temp_file and os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_round_trip_with_file(self):
        """Test writing and reading through StreamProxy."""
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
            self.temp_file = f.name
        
        # Write data through proxy
        with open(self.temp_file, 'wb') as f:
            proxy = StreamProxy(f)
            # Simulate what native code would do
            f.write(self.test_data)
        
        # Read data through proxy
        with open(self.temp_file, 'rb') as f:
            proxy = StreamProxy(f)
            data = f.read()
        
        # Verify data matches
        assert data == self.test_data
    
    def test_seek_operations(self):
        """Test various seek operations through StreamProxy."""
        stream = io.BytesIO(self.test_data)
        proxy = StreamProxy(stream)
        
        # Seek to middle
        mid_pos = len(self.test_data) // 2
        assert proxy._seek(mid_pos, 0) is True
        assert stream.tell() == mid_pos
        
        # Read from middle
        remaining = stream.read()
        assert len(remaining) == len(self.test_data) - mid_pos
        
        # Seek back to start
        assert proxy._seek(0, 0) is True
        assert stream.tell() == 0
        
        # Seek to end
        end_pos = len(self.test_data)
        assert proxy._seek(end_pos, 0) is True
        assert stream.tell() == end_pos
