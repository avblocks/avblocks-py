"""
MediaBuffer class for AVBlocks Python bindings.
"""

from typing import Optional, Union
import ctypes

from .native import get_native


class MediaBuffer:
    """
    A buffer for media data.
    
    MediaBuffer has a capacity which is the size of the buffer and data size which is 
    the size of the actual data in the buffer. The buffer is a continuous block of memory.
    The valid data is also a continuous block. The data can start at any offset in the buffer.
    """
    
    def __init__(self, data: Optional[Union[bytes, bytearray]] = None, buffer_size: Optional[int] = None):
        """
        Creates a MediaBuffer object.
        
        Args:
            data: Optional byte array to use as external data buffer
            buffer_size: Optional size to allocate for internal buffer
        """
        self._buffer: Optional[Union[bytes, bytearray]] = None
        self._data_offset: int = 0
        self._data_size: int = 0
        self._external: bool = False
        
        if data is not None:
            # Attach external data (keep reference)
            self._buffer = data
            self._external = True
            self._data_size = len(self._buffer)
        elif buffer_size is not None and buffer_size > 0:
            # Create internal buffer (use bytearray for mutability)
            self._buffer = bytearray(buffer_size)
            self._data_size = 0  # No valid data yet
    
    @property
    def external(self) -> bool:
        """Indicates that MediaBuffer uses an external data buffer."""
        return self._external
    
    @property
    def start(self) -> Optional[Union[bytes, bytearray]]:
        """Data buffer."""
        return self._buffer
    
    @property
    def data(self) -> Optional[memoryview]:
        """
        Returns a view of the valid data portion of the buffer.
        This is effectively the same as start[data_offset:data_offset+data_size]
        """
        if self._buffer is None:
            return None
        
        return memoryview(self._buffer)[self._data_offset:self._data_offset + self._data_size]
    
    @property
    def data_offset(self) -> int:
        """The offset at which valid data starts in the data buffer."""
        return self._data_offset
    
    @property
    def data_size(self) -> int:
        """The size of the data that is still valid in the data buffer."""
        return self._data_size
    
    @property
    def capacity(self) -> int:
        """The total capacity of the buffer."""
        if self._buffer is None:
            return 0
        return len(self._buffer)
    
    def set_data(self, data_offset: int, data_size: int) -> bool:
        """
        This is a convenience method that sets buffer data offset and size at once.
        
        Args:
            data_offset: The offset in the buffer where valid data starts
            data_size: The size in bytes of the valid data in the buffer
            
        Returns:
            True if data_offset and data_size are accepted and valid data is set,
            False otherwise
        """
        if self._buffer is None:
            return False
        
        if data_offset < 0 or data_offset >= len(self._buffer):
            return False
        
        if data_size < 0 or (data_offset + data_size > len(self._buffer)):
            return False
        
        self._data_offset = data_offset
        self._data_size = data_size
        return True
    
    def reset_data(self):
        """Reset data offset and size to zero."""
        self._data_offset = 0
        self._data_size = 0
    
    def attach(self, buffer: Union[bytes, bytearray], set_data: bool = True) -> bool:
        """
        Attaches an external buffer storage.
        
        Args:
            buffer: A byte array that should be used as external storage
            set_data: Specifies whether to auto set data with a size equal to the buffer size.
                     If True, the data size is set to the buffer size.
                     If False, data size is 0.
                     
        Returns:
            True if the buffer is attached successfully, False otherwise
        """
        if buffer is None:
            return False
        
        # Store reference to external buffer (don't copy)
        self._buffer = buffer
        self._data_offset = 0
        self._data_size = len(self._buffer) if set_data else 0
        self._external = True
        return True
    
    def detach(self) -> Optional[Union[bytes, bytearray]]:
        """
        Detaches an external data buffer.
        
        Returns:
            A reference to the detached buffer or None if no external buffer has been attached
        """
        if not self._external:
            return None
        
        # Return reference to the buffer (don't copy)
        external_buffer = self._buffer
        self._buffer = None
        self._data_offset = 0
        self._data_size = 0
        self._external = False
        return external_buffer
    
    # pylint: disable=[protected-access]
    def clone(self) -> 'MediaBuffer':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new MediaBuffer object
            
        Remarks:
            Only the reference to the external buffer is copied when MediaBuffer does not 
            own its data buffer (uses external/attached data). When MediaBuffer owns its data,
            a new copy of the data is created.
        """
        mb = MediaBuffer()
        mb._data_offset = self._data_offset
        mb._data_size = self._data_size
        mb._external = self._external
        
        if not self._external and self._buffer is not None:
            # Deep copy the buffer data
            if isinstance(self._buffer, bytearray):
                mb._buffer = bytearray(self._buffer)
            else:
                mb._buffer = bytes(self._buffer)
        else:
            # Shallow copy for external buffer
            mb._buffer = self._buffer
        
        return mb
    
    def _to_native(self) -> Optional[ctypes.c_void_p]:
        """Create a native MediaBuffer object from this instance."""
        if self._buffer is None:
            return None
        
        lib = get_native().lib
        native_buffer = lib.avb_create_media_buffer(self._data_size)
        
        if self._data_size > 0:
            native_buffer_ptr = lib.MediaBuffer_start(native_buffer)
            # Copy data from Python buffer to native buffer
            # Convert to bytes-like for ctypes if needed
            buffer_data = self._buffer[self._data_offset:self._data_offset + self._data_size]
            ctypes.memmove(
                native_buffer_ptr,
                bytes(buffer_data),
                self._data_size
            )
            lib.MediaBuffer_setData(native_buffer, 0, self._data_size)
        
        return native_buffer
    
    @staticmethod
    def _from_native(native: ctypes.c_void_p) -> Optional['MediaBuffer']:
        """Create a MediaBuffer object from a native MediaBuffer pointer."""
        if not native:
            return None
        
        lib = get_native().lib
        data_size = lib.MediaBuffer_dataSize(native)
        data_ptr = lib.MediaBuffer_data(native)
        
        if data_size <= 0:
            return MediaBuffer()
        
        # Create mutable buffer and copy data from native
        mb = MediaBuffer(buffer_size=data_size)
        ctypes.memmove(
            (ctypes.c_uint8 * data_size).from_buffer(mb._buffer),
            data_ptr,
            data_size
        )
        mb.set_data(0, data_size)
        return mb
