"""
MediaInfo class for AVBlocks Python bindings.
Analyzes a file or a stream and provides information about its type and properties.
"""

from typing import Optional, Tuple
import ctypes

from .block import Block
from .native import get_native
from .media_socket_list import MediaSocketList
from .media_socket import MediaSocket
from .media_sample import MediaSample
from .error_info import ErrorInfo

# pylint: disable=protected-access
class MediaInfo(Block):
    """
    Analyzes a file or a stream and provides information about its type and properties.
    """
    
    def __init__(self):
        """
        Creates a MediaInfo object in its default state.
        
        When the MediaInfo object is not needed anymore it should be disposed in order to 
        deterministically reclaim the allocated resources.
        """
        lib = get_native().lib
        self._native_media_info = lib.avb_create_media_info()
        self._native_sample: Optional[ctypes.c_void_p] = None
        
        self._inputs: MediaSocketList = MediaSocketList()
        self._outputs: MediaSocketList = MediaSocketList()
        
        # Copy from native
        self._copy_from_native_media_info()
    
    def __del__(self):
        """Finalizer to ensure resources are released."""
        self._dispose_native()
    
    def _dispose_native(self):
        """Dispose native resources."""
        if self._native_media_info:
            lib = get_native().lib
            lib.Reference_release(self._native_media_info)
            self._native_media_info = None
            self._dispose_native_sample()
    
    def _dispose_native_sample(self):
        """Dispose native sample."""
        if self._native_sample:
            lib = get_native().lib
            lib.Reference_release(self._native_sample)
            self._native_sample = None
    
    def _ensure_native_sample(self):
        """Ensure native sample is created."""
        if not self._native_sample:
            lib = get_native().lib
            self._native_sample = lib.avb_create_media_sample()
    
    def _check_disposed(self):
        """Check if object has been disposed."""
        if not self._native_media_info:
            raise RuntimeError("Object has been disposed")
    
    def _copy_to_native_sockets(self, sockets: MediaSocketList, native_sockets: ctypes.c_void_p):
        """Copy Python sockets to native socket list."""
        lib = get_native().lib
        lib.MediaSocketList_clear(native_sockets)
        
        for socket in sockets:
            native_socket = socket._to_native()
            lib.MediaSocketList_add(native_sockets, native_socket)
            lib.Reference_release(native_socket)
    
    def _copy_from_native_sockets(self, native_sockets: ctypes.c_void_p, sockets: MediaSocketList):
        """Copy native sockets to Python socket list."""
        lib = get_native().lib
        socket_count_native = lib.MediaSocketList_count(native_sockets)
        
        if socket_count_native != len(sockets):
            for i in range(socket_count_native):
                native_socket = lib.MediaSocketList_at(native_sockets, i)
                socket = MediaSocket._from_native(native_socket)
                if socket:
                    sockets.add(socket)
        else:
            for i in range(socket_count_native):
                native_socket = lib.MediaSocketList_at(native_sockets, i)
                socket_from_native = MediaSocket._from_native(native_socket)
                
                if socket_from_native:
                    # Keep the stream property
                    socket_from_native.stream = sockets[i].stream
                    sockets[i] = socket_from_native
    
    def _copy_from_native_media_info(self):
        """Copy data from native MediaInfo to Python object."""
        lib = get_native().lib
        self._outputs = MediaSocketList()
        
        native_inputs = lib.MediaInfo_inputs(self._native_media_info)
        native_outputs = lib.MediaInfo_outputs(self._native_media_info)
        
        self._copy_from_native_sockets(native_inputs, self._inputs)
        self._copy_from_native_sockets(native_outputs, self._outputs)
        
        # Copy the stream property from input to output
        if len(self._inputs) > 0 and len(self._outputs) > 0:
            self._outputs[0].stream = self._inputs[0].stream
        
        # Make outputs immutable
        self._outputs.immutable = True
    
    def dispose(self):
        """Disposes the MediaInfo and reclaims the resources used by the object."""
        self._dispose_native()
    
    @property
    def inputs(self) -> MediaSocketList:
        """
        A modifiable collection of MediaSocket objects which describe the input data of the MediaInfo.
        
        Each socket in the collection represents an input point - 
        it can be a container with one or more streams or just an elementary stream.
        
        The default value of this property is a collection with one element.
        """
        self._check_disposed()
        return self._inputs
    
    @property
    def outputs(self) -> MediaSocketList:
        """
        An immutable collection of MediaSocket objects describing the audio and video streams (tracks) 
        found in the input.
        
        The default value of this property is an empty collection.
        """
        self._check_disposed()
        return self._outputs
    
    @property
    def error(self) -> Optional[ErrorInfo]:
        """Error information for the last load operation."""
        self._check_disposed()
        lib = get_native().lib
        native_error = lib.MediaInfo_error(self._native_media_info)
        return ErrorInfo._from_native(native_error)
    
    @property
    def is_ready(self) -> bool:
        """
        Indicates whether stream info and metadata have been loaded and parsed.
        """
        self._check_disposed()
        lib = get_native().lib
        return lib.MediaInfo_isReady(self._native_media_info)
    
    # Block interface implementation
    
    def open(self) -> bool:
        """
        Analyzes the input specified by the inputs property.
        
        Returns:
            True if the input has been successfully analyzed, otherwise False.
            
        If this method succeeds the information about the detected media streams (tracks) 
        can be obtained from the outputs property.
        """
        self._check_disposed()
        
        lib = get_native().lib
        native_inputs = lib.MediaInfo_inputs(self._native_media_info)
        self._copy_to_native_sockets(self._inputs, native_inputs)
        
        result = lib.MediaInfo_open(self._native_media_info)
        
        if result:
            self._copy_from_native_media_info()
        
        return result
    
    def push(self, input_index: int, input_sample: Optional[MediaSample]) -> bool:
        """
        Pushes input data to the MediaInfo.
        
        Args:
            input_index: Specifies the index of the input socket whose data is pushed to the MediaInfo. 
                        Must be zero.
            input_sample: A MediaSample object that contains the input data in the buffer property.
            
        Returns:
            True when the MediaInfo has successfully processed the input data, otherwise False.
            
        In order to use this method the Inputs[0].stream_type must be set.
        
        Supported stream types:
        - StreamType.Mpeg1Video
        - StreamType.Mpeg2Video
        - StreamType.H264
        - StreamType.MpegTS
        """
        self._check_disposed()
        lib = get_native().lib
        
        if input_sample is not None:
            self._ensure_native_sample()
            
            # Copy properties to native sample
            input_sample._copy_props_to_native(self._native_sample)
            
            # Handle buffer if present
            if input_sample.buffer is not None and input_sample.buffer.data_size > 0:
                native_buffer = lib.avb_create_media_buffer(0)
                
                # Pin the buffer data
                buffer_data = input_sample.buffer.start
                buf_ptr = ctypes.cast(buffer_data, ctypes.c_void_p)
                
                lib.MediaBuffer_attach(native_buffer, 
                                      buf_ptr.value + input_sample.buffer.data_offset,
                                      input_sample.buffer.data_size, 
                                      True)
                
                lib.MediaSample_setBuffer(self._native_sample, native_buffer)
                lib.Reference_release(native_buffer)
            
            result = lib.MediaInfo_push(self._native_media_info, input_index, self._native_sample)
            
            if input_sample.buffer is not None:
                # Assumes that the whole buffer is consumed on MediaInfo.push
                input_sample.buffer.set_data(0, 0)
        else:
            result = lib.MediaInfo_push(self._native_media_info, input_index, None)
        
        if len(self._outputs) == 0 and self.is_ready:
            self._copy_from_native_media_info()
        
        return result
    
    def push_unmanaged(self, input_index: int, input_sample: Optional[MediaSample]) -> bool:
        """
        Pushes input data to the MediaInfo.
        
        Args:
            input_index: Specifies the index of the input socket whose data is pushed to the MediaInfo. 
                        Must be zero.
            input_sample: A MediaSample object that contains the input data in the unmanaged_buffer property.
            
        Returns:
            True when the MediaInfo has successfully processed the input data, otherwise False.
        """
        self._check_disposed()
        lib = get_native().lib
        
        if input_sample is not None:
            self._ensure_native_sample()
            
            input_sample._copy_props_to_native(self._native_sample)
            
            if input_sample.unmanaged_buffer is not None and input_sample.unmanaged_buffer.data_size > 0:
                native_buffer = input_sample.unmanaged_buffer.native_ref
                lib.MediaSample_setBuffer(self._native_sample, native_buffer)
            
            result = lib.MediaInfo_push(self._native_media_info, input_index, self._native_sample)
            
            if input_sample.unmanaged_buffer is not None:
                input_sample.unmanaged_buffer.clear()
        else:
            result = lib.MediaInfo_push(self._native_media_info, input_index, None)
        
        if len(self._outputs) == 0 and self.is_ready:
            self._copy_from_native_media_info()
        
        return result
    
    def pull(self, output_sample: MediaSample) -> Tuple[bool, int]:
        """
        The method is not implemented.
        
        Args:
            output_sample: Not used
            
        Returns:
            A tuple of (False, output_index)
        """
        self._check_disposed()
        lib = get_native().lib
        output_index = ctypes.c_int32(0)
        # Call native method just to set the errorInfo
        lib.MediaInfo_pull(self._native_media_info, ctypes.byref(output_index), None)
        return False, output_index.value
    
    def pull_unmanaged(self, output_sample: MediaSample) -> Tuple[bool, int]:
        """
        The method is not implemented.
        
        Args:
            output_sample: Not used
            
        Returns:
            A tuple of (False, output_index)
        """
        self._check_disposed()
        lib = get_native().lib
        output_index = ctypes.c_int32(0)
        # Call native method just to set the errorInfo
        lib.MediaInfo_pull(self._native_media_info, ctypes.byref(output_index), None)
        return False, output_index.value
    
    def close(self):
        """Closes the MediaInfo."""
        self._check_disposed()
        lib = get_native().lib
        lib.MediaInfo_close(self._native_media_info)
        self._dispose_native_sample()
    
    def flush(self) -> bool:
        """
        The method is not implemented.
        
        Returns:
            The result of the native flush call
        """
        self._check_disposed()
        lib = get_native().lib
        return lib.MediaInfo_flush(self._native_media_info)
    
    def end_of_stream(self, input_index: int) -> bool:
        """
        The method is not implemented.
        
        Args:
            input_index: Input index
            
        Returns:
            The result of the native end_of_stream call
        """
        self._check_disposed()
        lib = get_native().lib
        return lib.MediaInfo_endOfStream(self._native_media_info, input_index)
