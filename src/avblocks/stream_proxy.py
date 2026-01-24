"""
StreamProxy class for bridging Python RawIOBase to native AVBlocks streams.
"""

import os
import ctypes
from typing import Optional
from io import RawIOBase


# Define callback function types matching the native stream interface
StreamOpenCallback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)
StreamCloseCallback = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
StreamIsOpenCallback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)
StreamCanReadCallback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)
StreamCanWriteCallback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)
StreamCanSeekCallback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_void_p)
StreamReadCallback = ctypes.CFUNCTYPE(
    ctypes.c_bool, 
    ctypes.c_void_p,  # buffer
    ctypes.c_int32,   # buffer_size
    ctypes.POINTER(ctypes.c_int32),  # total_read
    ctypes.c_void_p   # context
)
StreamWriteCallback = ctypes.CFUNCTYPE(
    ctypes.c_bool,
    ctypes.c_void_p,  # buffer
    ctypes.c_int32,   # data_size
    ctypes.c_void_p   # context
)
StreamSizeCallback = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)
StreamPositionCallback = ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.c_void_p)
StreamSeekCallback = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_int64, ctypes.c_void_p)


class StreamCallback(ctypes.Structure):
    """Native stream callback structure."""
    _pack_ = 1
    _fields_ = [
        ("context", ctypes.c_void_p),
        ("open", StreamOpenCallback),
        ("close", StreamCloseCallback),
        ("is_open", StreamIsOpenCallback),
        ("can_read", StreamCanReadCallback),
        ("can_write", StreamCanWriteCallback),
        ("can_seek", StreamCanSeekCallback),
        ("read", StreamReadCallback),
        ("write", StreamWriteCallback),
        ("size", StreamSizeCallback),
        ("position", StreamPositionCallback),
        ("seek", StreamSeekCallback),
    ]

# pylint:disable=unused-argument
class StreamProxy:
    """
    Proxy class that bridges Python RawIOBase streams to native AVBlocks streams.
    
    This class wraps a Python stream object and provides callback functions
    that match the native stream interface expected by AVBlocks.
    """
    
    def __init__(self, stream: Optional[RawIOBase] = None):
        """
        Initialize the stream proxy.
        
        Args:
            stream: A Python RawIOBase stream object (e.g., file opened in binary mode)
        """
        self._stream = stream
        self._native_callback = StreamCallback()
        
        # Set up callbacks - store references to prevent garbage collection
        self._open_callback = StreamOpenCallback(self._open)
        self._close_callback = StreamCloseCallback(self._close)
        self._is_open_callback = StreamIsOpenCallback(self._is_open)
        self._can_read_callback = StreamCanReadCallback(self._can_read)
        self._can_write_callback = StreamCanWriteCallback(self._can_write)
        self._can_seek_callback = StreamCanSeekCallback(self._can_seek)
        self._read_callback = StreamReadCallback(self._read)
        self._write_callback = StreamWriteCallback(self._write)
        self._size_callback = StreamSizeCallback(self._size)
        self._position_callback = StreamPositionCallback(self._position)
        self._seek_callback = StreamSeekCallback(self._seek)
        
        # Populate the native callback structure
        self._native_callback.context = ctypes.c_void_p(0)
        self._native_callback.open = self._open_callback
        self._native_callback.close = self._close_callback
        self._native_callback.is_open = self._is_open_callback
        self._native_callback.can_read = self._can_read_callback
        self._native_callback.can_write = self._can_write_callback
        self._native_callback.can_seek = self._can_seek_callback
        self._native_callback.read = self._read_callback
        self._native_callback.write = self._write_callback
        self._native_callback.size = self._size_callback
        self._native_callback.position = self._position_callback
        self._native_callback.seek = self._seek_callback
    
    @property
    def stream(self) -> Optional[RawIOBase]:
        """Get the wrapped Python stream."""
        return self._stream
    
    @stream.setter
    def stream(self, value: Optional[RawIOBase]):
        """Set the wrapped Python stream."""
        self._stream = value
    
    @property
    def native_stream_callback(self) -> Optional[StreamCallback]:
        """Get the native stream callback structure."""
        return self._native_callback if self._stream is not None else None
    
    def _open(self, context: ctypes.c_void_p) -> bool:
        """Callback for opening the stream."""
        if self._stream is None:
            return False
        # Stream is always considered open in Python
        return True
    
    def _close(self, context: ctypes.c_void_p):
        """Callback for closing the stream."""
        if self._stream is not None:
            try:
                self._stream.close()
            except Exception:
                pass
            self._stream = None
    
    def _is_open(self, context: int) -> bool:
        """Callback for checking if stream is open."""
        if self._stream is None:
            return False
        
        try:
            return not self._stream.closed
        except (ValueError, AttributeError):
            return False
    
    def _can_read(self, context: int) -> bool:
        """Callback for checking if stream can be read."""
        if self._stream is None:
            return False
        
        try:
            return self._stream.readable()
        except (ValueError, IOError):
            return False
    
    def _can_write(self, context: int) -> bool:
        """Callback for checking if stream can be written."""
        if self._stream is None:
            return False
        
        try:
            return self._stream.writable()
        except (ValueError, IOError):
            return False
    
    def _can_seek(self, context: int) -> bool:
        """Callback for checking if stream can be seeked."""
        if self._stream is None:
            return False
        
        try:
            return self._stream.seekable()
        except (ValueError, IOError):
            return False
    
    def _read(
        self, 
        native_buffer: ctypes.c_void_p, 
        buffer_size: ctypes.c_int32,
        total_read: 'ctypes._Pointer[ctypes.c_int32]',
        context: ctypes.c_void_p
    ) -> bool:
        """Callback for reading from the stream."""
        if self._stream is None or buffer_size < 0:
            return False
        
        try:
            # Read from Python stream
            data = self._stream.read(buffer_size)
            if data is None:
                total_read[0] = 0
                return True
            
            bytes_read = len(data)
            total_read[0] = bytes_read
            
            # Copy data to native buffer
            if bytes_read > 0:
                ctypes.memmove(native_buffer, data, bytes_read)
            
            return True
        except Exception:
            return False
    
    def _write(
        self,
        native_buffer: ctypes.c_void_p,
        data_size: ctypes.c_int32,
        context: ctypes.c_void_p
    ) -> bool:
        """Callback for writing to the stream."""
        if self._stream is None or data_size < 0:
            return False
        
        try:
            # Copy data from native buffer
            if data_size > 0:
                buffer = (ctypes.c_uint8 * data_size).from_address(native_buffer)
                data = bytes(buffer)
            else:
                data = b''
            
            # Write to Python stream
            self._stream.write(data)
            return True
        except Exception:
            return False
    
    def _size(self, context: int) -> int:
        """Callback for getting stream size."""
        if self._stream is None:
            return 0
        
        try:
            current_pos = self._stream.tell()
            self._stream.seek(0, os.SEEK_END)  # Seek to end
            size = self._stream.tell()
            self._stream.seek(current_pos, os.SEEK_SET)  # Restore position
            return size
        except (ValueError, IOError, OSError):
            return 0
    
    def _position(self, context: int) -> int:
        """Callback for getting current stream position."""
        if self._stream is None:
            return -1
        
        try:
            return self._stream.tell()
        except (ValueError, IOError, OSError):
            return -1
    
    def _seek(self, position: int, context: int) -> bool:
        """Callback for seeking in stream."""
        if self._stream is None:
            return False
        
        try:
            new_pos = self._stream.seek(position, os.SEEK_SET)
            return new_pos == position
        except (ValueError, IOError, OSError):
            return False
