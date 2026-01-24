"""
UnmanagedMediaBuffer class for AVBlocks Python bindings.
Provides direct access to native C memory without copying.
"""

from typing import Optional
import ctypes

from .native import get_native


class UnmanagedMediaBuffer:
    """
    Unmanaged buffer for media data that works directly with C memory.
    
    This class provides direct access to native memory without copying data to Python.
    It's useful for high-performance scenarios where you want to avoid memory copies.
    
    Unlike MediaBuffer, this class does not hold Python byte arrays. Instead, it manages
    native memory allocations through the C API.
    """
    
    def __init__(self, buffer_size: int = 0):
        """
        Creates an UnmanagedMediaBuffer and optionally allocates buffer storage.
        
        Args:
            buffer_size: Requested buffer size. If 0, the buffer is created without storage.
                        Buffer storage can be attached, explicitly allocated, or automatically
                        allocated when data is appended.
        """
        lib = get_native().lib
        self._native_ref = lib.avb_create_media_buffer(buffer_size)
        
        if not self._native_ref:
            raise MemoryError("Failed to create native MediaBuffer")
        
        # Keep reference count
        lib.Reference_retain(self._native_ref)
    
    def __del__(self):
        """Cleanup native resources."""
        if hasattr(self, '_native_ref') and self._native_ref:
            lib = get_native().lib
            lib.Reference_release(self._native_ref)
            self._native_ref = None
    
    @property
    def _native_ptr(self) -> ctypes.c_void_p:
        """Internal property to get the native pointer."""
        if not self._native_ref:
            raise RuntimeError("UnmanagedMediaBuffer has been disposed")
        return self._native_ref
    
    def alloc(self, size: int, keep_data: bool = False) -> bool:
        """
        Allocates internal buffer storage.
        
        Args:
            size: Requested buffer size. A buffer storage is allocated only if the
                 requested size exceeds the current buffer size (capacity).
            keep_data: Whether to keep existing data when the buffer is resized.
            
        Returns:
            True if allocation succeeded, False otherwise (out of memory).
            
        Remarks:
            If external storage is attached, it is automatically detached.
        """
        lib = get_native().lib
        return lib.MediaBuffer_alloc(self._native_ptr, size, keep_data)
    
    def free(self):
        """
        Frees internal buffer storage.
        
        Remarks:
            Does nothing if external storage is attached to the buffer.
        """
        lib = get_native().lib
        lib.MediaBuffer_free(self._native_ptr)
    
    def attach(self, buf_ptr: int, size: int, set_data: bool = True) -> bool:
        """
        Attaches an external buffer storage.
        
        Args:
            buf_ptr: Pointer to the buffer storage (as integer address).
            size: The buffer storage size.
            set_data: Whether to auto-set data with size equal to buffer size.
                     If True, DataSize equals Capacity. If False, DataSize is 0.
            
        Returns:
            True if buffer is attached successfully, False otherwise.
            
        Remarks:
            If internal storage is already allocated, it is automatically freed.
        """
        lib = get_native().lib
        ptr = ctypes.c_void_p(buf_ptr)
        return lib.MediaBuffer_attach(self._native_ptr, ptr, size, set_data)
    
    def detach(self) -> Optional[int]:
        """
        Detaches an external buffer storage.
        
        Returns:
            Pointer to the detached buffer storage (as integer), or None if no
            external storage has been attached.
        """
        lib = get_native().lib
        ptr = lib.MediaBuffer_detach(self._native_ptr)
        if ptr:
            return ctypes.cast(ptr, ctypes.c_void_p).value
        return None
    
    @property
    def external(self) -> bool:
        """Returns whether the buffer uses external storage."""
        lib = get_native().lib
        return lib.MediaBuffer_external(self._native_ptr)
    
    def clear(self):
        """
        Clears existing data.
        
        Remarks:
            Does not change buffer capacity.
        """
        lib = get_native().lib
        lib.MediaBuffer_clear(self._native_ptr)
    
    def normalize(self):
        """
        Moves existing data to the start of the buffer and maximizes free linear space.
        
        Remarks:
            Useful when new data is added through direct copying after existing data.
            Does not change buffer capacity.
        """
        lib = get_native().lib
        lib.MediaBuffer_normalize(self._native_ptr)
    
    def append(self, data_ptr: int, data_size: int) -> bool:
        """
        Appends data to the end of the buffer.
        
        Args:
            data_ptr: Pointer to the data that should be appended (as integer address).
            data_size: Number of bytes to append.
            
        Returns:
            True if operation is successful, False otherwise.
            
        Remarks:
            If buffer has internal storage, it will be increased if needed.
            If buffer has external storage and data cannot fit, operation fails.
        """
        lib = get_native().lib
        ptr = ctypes.c_void_p(data_ptr)
        return lib.MediaBuffer_append(self._native_ptr, ptr, data_size)
    
    def remove(self, data_size: int):
        """
        Removes data from the beginning of the buffer.
        
        Args:
            data_size: Number of bytes to remove from valid data.
            
        Remarks:
            Does not change buffer capacity.
        """
        lib = get_native().lib
        lib.MediaBuffer_remove(self._native_ptr, data_size)
    
    @property
    def buf_ptr(self) -> int:
        """
        Returns a pointer to the start of the buffer (as integer address).
        
        The pointer is guaranteed to be valid only when capacity > 0.
        """
        lib = get_native().lib
        ptr = lib.MediaBuffer_start(self._native_ptr)
        return ctypes.cast(ptr, ctypes.c_void_p).value
    
    @property
    def data_ptr(self) -> int:
        """
        Returns a pointer to the first byte of data (as integer address).
        
        This is effectively the same as buf_ptr + data_offset.
        """
        lib = get_native().lib
        ptr = lib.MediaBuffer_data(self._native_ptr)
        return ctypes.cast(ptr, ctypes.c_void_p).value
    
    @property
    def data_offset(self) -> int:
        """The offset at which valid data starts in the buffer (0 to capacity-1)."""
        lib = get_native().lib
        return lib.MediaBuffer_dataOffset(self._native_ptr)
    
    @property
    def data_size(self) -> int:
        """The size of the valid data in the buffer (0 to capacity)."""
        lib = get_native().lib
        return lib.MediaBuffer_dataSize(self._native_ptr)
    
    @property
    def capacity(self) -> int:
        """The size of the buffer in bytes. Can be zero."""
        lib = get_native().lib
        return lib.MediaBuffer_capacity(self._native_ptr)
    
    @property
    def free_linear_space(self) -> int:
        """
        The free linear space that can be used to append data without normalization.
        
        Remarks:
            Free linear space starts at data_offset + data_size.
            Its size equals capacity - data_size - data_offset.
            It is less than or equal to free_space.
        """
        lib = get_native().lib
        return lib.MediaBuffer_freeLinearSpace(self._native_ptr)
    
    @property
    def free_space(self) -> int:
        """
        The free space that can be used to append data without buffer reallocation.
        
        Remarks:
            Free space starts at data_offset + data_size.
            Its size is capacity - data_size.
            It is greater than or equal to free_linear_space.
        """
        lib = get_native().lib
        return lib.MediaBuffer_freeSpace(self._native_ptr)
    
    def set_data(self, data_offset: int, data_size: int) -> bool:
        """
        Sets the offset and size of valid data in the buffer.
        
        Args:
            data_offset: Offset where valid data starts (0 to capacity-1).
            data_size: Size of valid data in bytes (0 to capacity).
            
        Returns:
            True if data offset and size are successfully changed, False if invalid.
        """
        lib = get_native().lib
        return lib.MediaBuffer_setData(self._native_ptr, data_offset, data_size)
    
    # pylint: disable=protected-access
    def clone(self) -> 'UnmanagedMediaBuffer':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new UnmanagedMediaBuffer instance.
            
        Remarks:
            If buffer owns internal storage, it is copied.
            If buffer uses external storage, only the reference is copied.
        """
        lib = get_native().lib
        new_ref = lib.MediaBuffer_clone(self._native_ptr)
        
        if not new_ref:
            raise MemoryError("Failed to clone UnmanagedMediaBuffer")
        
        new_buffer = UnmanagedMediaBuffer.__new__(UnmanagedMediaBuffer)
        new_buffer._native_ref = new_ref
        lib.Reference_retain(new_ref)
        
        return new_buffer
    
    def to_bytes(self) -> bytes:
        """
        Copies the valid data portion to a Python bytes object.
        
        Returns:
            A bytes object containing a copy of the valid data.
        """
        if self.data_size == 0:
            return b''
        
        data_ptr = self.data_ptr
        buffer_array = (ctypes.c_uint8 * self.data_size).from_address(data_ptr)
        return bytes(buffer_array)
    
    def write_from_bytes(self, data: bytes, offset: int = 0) -> bool:
        """
        Writes Python bytes to the buffer at the specified offset.
        
        Args:
            data: Bytes to write to the buffer.
            offset: Offset in the buffer where to write the data.
            
        Returns:
            True if successful, False if data doesn't fit.
        """
        if offset + len(data) > self.capacity:
            return False
        
        buf_ptr = self.buf_ptr + offset
        ctypes.memmove(buf_ptr, data, len(data))
        return True
