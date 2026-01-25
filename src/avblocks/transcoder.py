"""
Transcoder class for AVBlocks Python bindings.
Provides functionality for audio and video encoding, decoding and transforming.
"""

from typing import Optional, Tuple, Callable
import ctypes

from .constants import TranscoderStatus
from .block import Block
from .native import get_native
from .media_buffer import MediaBuffer
from .unmanaged_media_buffer import UnmanagedMediaBuffer
from .media_sample import MediaSample
from .media_socket_list import MediaSocketList
from .media_pin import MediaPin
from .error_info import ErrorInfo

# pylint: disable=protected-access
class TranscoderProgressEventArgs:
    """Contains the parameters of the on_progress event."""
    
    def __init__(self, current_time: float, total_time: float):
        """
        Initialize progress event arguments.
        
        Args:
            current_time: The duration of the media stream that has been processed so far (seconds)
            total_time: The total duration of the media stream that will be processed (seconds)
        """
        self.current_time = current_time
        self.total_time = total_time


class TranscoderStatusEventArgs:
    """Contains the parameters of the on_status event."""
    
    def __init__(self, status: TranscoderStatus):
        """
        Initialize status event arguments.
        
        Args:
            status: The current status
        """
        self.status = status


class TranscoderContinueEventArgs:
    """Contains the parameters of the on_continue event."""
    
    def __init__(self, current_time: float):
        """
        Initialize continue event arguments.
        
        Args:
            current_time: The duration of the media stream that has been processed so far (seconds)
        """
        self.current_time = current_time
        self.continue_transcoding = True


class TranscoderInputChangeEventArgs:
    """Contains the parameters of the on_input_change event."""
    
    def __init__(self, input_index: int):
        """
        Initialize input change event arguments.
        
        Args:
            input_index: The index of the input socket that has changed
        """
        self.input_index = input_index


class Transcoder(Block):
    """
    Provides functionality for audio and video encoding, decoding and transforming.
    """
    
    def __init__(self):
        """
        Creates a Transcoder object in its default state.
        
        When the Transcoder object is not needed anymore it should be disposed in order to 
        deterministically reclaim the allocated resources.
        """
        lib = get_native().lib
        self._native_ref = lib.avb_create_transcoder()
        self._native_sample: Optional[ctypes.c_void_p] = None
        
        self._inputs: MediaSocketList = MediaSocketList()
        self._outputs: MediaSocketList = MediaSocketList()
        
        # Event handlers
        self.on_progress: Optional[Callable[[TranscoderProgressEventArgs], None]] = None
        self.on_status: Optional[Callable[[TranscoderStatusEventArgs], None]] = None
        self.on_continue: Optional[Callable[[TranscoderContinueEventArgs], None]] = None
        self.on_input_change: Optional[Callable[[TranscoderInputChangeEventArgs], None]] = None
        
        # Native callback references (must be kept alive)
        self._native_progress_callback = None
        self._native_continue_callback = None
        self._native_status_callback = None
        self._native_input_change_callback = None
        
        self._setup_callbacks()
    
    def __del__(self):
        """Finalizer to ensure resources are released."""
        self._dispose_native()
    
    # pylint: disable=[unused-argument, not-callable]
    def _setup_callbacks(self):
        """Setup native callbacks."""
        lib = get_native().lib
        
        # Progress callback
        @ctypes.CFUNCTYPE(None, ctypes.c_double, ctypes.c_double, ctypes.c_void_p)
        def native_progress_callback(current_time, total_time, callback_param):
            if self.on_progress:
                args = TranscoderProgressEventArgs(current_time, total_time)
                self.on_progress(args)
        
        self._native_progress_callback = native_progress_callback
        lib.Transcoder_setProgressCallback(self._native_ref, native_progress_callback, None)
        
        # Continue callback
        @ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_double, ctypes.c_void_p)
        def native_continue_callback(current_time, callback_param):
            if self.on_continue:
                args = TranscoderContinueEventArgs(current_time)
                self.on_continue(args)
                return 1 if args.continue_transcoding else 0
            return 1
        
        self._native_continue_callback = native_continue_callback
        lib.Transcoder_setContinueCallback(self._native_ref, native_continue_callback, None)
        
        # Status callback
        @ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_void_p)
        def native_status_callback(status, callback_param):
            if self.on_status:
                args = TranscoderStatusEventArgs(TranscoderStatus(status))
                self.on_status(args)
        
        self._native_status_callback = native_status_callback
        lib.Transcoder_setStatusCallback(self._native_ref, native_status_callback, None)
        
        # Input change callback
        @ctypes.CFUNCTYPE(None, ctypes.c_int32, ctypes.c_void_p)
        def native_input_change_callback(input_index, callback_param):
            if self.on_input_change:
                args = TranscoderInputChangeEventArgs(input_index)
                self.on_input_change(args)
        
        self._native_input_change_callback = native_input_change_callback
        lib.Transcoder_setInputChangeCallback(self._native_ref, native_input_change_callback, None)
    
    def _dispose_native(self):
        """Dispose native resources."""
        if self._native_ref:
            lib = get_native().lib
            lib.Reference_release(self._native_ref)
            self._native_ref = None
            self._dispose_native_sample()
            
            # Clear callback references
            self._native_progress_callback = None
            self._native_continue_callback = None
            self._native_status_callback = None
            self._native_input_change_callback = None
    
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
        if not self._native_ref:
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
        
        assert socket_count_native == len(sockets)
        
        for i in range(socket_count_native):
            native_socket = lib.MediaSocketList_at(native_sockets, i)
            native_pins = lib.MediaSocket_pins(native_socket)
            pin_count_native = lib.MediaPinList_count(native_pins)
            
            if len(sockets[i].pins) == pin_count_native:
                for j in range(pin_count_native):
                    native_pin = lib.MediaPinList_at(native_pins, j)
                    sockets[i].pins[j]._copy_from_native(native_pin)
            else:
                sockets[i].pins.clear()
                for j in range(pin_count_native):
                    native_pin = lib.MediaPinList_at(native_pins, j)
                    pin = MediaPin._from_native(native_pin)
                    if pin:
                        sockets[i].pins.add(pin)
    
    def dispose(self):
        """Disposes the Transcoder and reclaims the resources used by the object."""
        self._dispose_native()
    
    @property
    def inputs(self) -> MediaSocketList:
        """
        A modifiable collection of MediaSocket objects which describe the input data of the Transcoder.
        
        Each socket in the collection represents an input point - 
        it can be a container with one or more streams or just an elementary stream.
        
        The default value of this property is an empty collection which can be modified but it cannot be replaced.
        """
        self._check_disposed()
        return self._inputs
    
    @property
    def outputs(self) -> MediaSocketList:
        """
        A modifiable collection of MediaSocket objects which describe the output data of the Transcoder.
        
        Each socket in the collection describes an output point - 
        it can be a container with one or more streams or just an elementary stream.
        
        The default value of this property is an empty collection which can be modified but it cannot be replaced.
        """
        self._check_disposed()
        return self._outputs
    
    @property
    def auto_connect(self) -> bool:
        """
        Specifies whether the Transcoder automatically connects input to output pins when opened.
        
        Only pins that have their connection property equal to PinConnection.Auto
        participate in the automatic connection.
        """
        self._check_disposed()
        lib = get_native().lib
        return lib.Transcoder_autoConnect(self._native_ref)
    
    @auto_connect.setter
    def auto_connect(self, value: bool):
        self._check_disposed()
        lib = get_native().lib
        lib.Transcoder_setAutoConnect(self._native_ref, value)
    
    @property
    def allow_demo_mode(self) -> bool:
        """
        Specifies whether the Transcoder allows demo mode (unlicensed transcoding).
        
        If True a demo watermark is applied when a required feature (codec/format) is not licensed.
        If False the Transcoder returns an error instead of applying the demo watermark.
        """
        self._check_disposed()
        lib = get_native().lib
        return lib.Transcoder_allowDemoMode(self._native_ref)
    
    @allow_demo_mode.setter
    def allow_demo_mode(self, value: bool):
        self._check_disposed()
        lib = get_native().lib
        lib.Transcoder_setAllowDemoMode(self._native_ref, value)
    
    @property
    def error(self) -> Optional[ErrorInfo]:
        """The error information for the last transcoder operation."""
        self._check_disposed()
        lib = get_native().lib
        native_error = lib.Transcoder_error(self._native_ref)
        return ErrorInfo._from_native(native_error)
    
    def open(self) -> bool:
        """
        Initializes the Transcoder based on the specified input and desired output.
        
        Returns:
            True if the Transcoder is successfully initialized and is ready to process data; otherwise False.
        """
        self._check_disposed()
        
        lib = get_native().lib
        native_inputs = lib.Transcoder_inputs(self._native_ref)
        native_outputs = lib.Transcoder_outputs(self._native_ref)
        
        self._copy_to_native_sockets(self._inputs, native_inputs)
        self._copy_to_native_sockets(self._outputs, native_outputs)
        
        result = lib.Transcoder_open(self._native_ref)
        
        self._copy_from_native_sockets(native_inputs, self._inputs)
        self._copy_from_native_sockets(native_outputs, self._outputs)
        
        return result
    
    def run(self) -> bool:
        """
        Runs an automatic transcoding.
        
        Returns:
            True when the transcoding has succeeded.
            False when there's a transcoding error or the run() method cannot be used with the specified inputs and outputs.
        """
        self._check_disposed()
        lib = get_native().lib
        return lib.Transcoder_run(self._native_ref)
    
    def push(self, input_index: int, input_sample: Optional[MediaSample]) -> bool:
        """
        Pushes input data to the Transcoder.
        
        Args:
            input_index: Specifies the index of the input socket whose data is pushed to the Transcoder.
            input_sample: A MediaSample object that contains the input data in the buffer property.
            
        Returns:
            True when the Transcoder has successfully processed some or all of the input data, otherwise False.
        """
        self._check_disposed()
        lib = get_native().lib
        
        if input_sample is not None:
            self._ensure_native_sample()
            
            input_sample._copy_props_to_native(self._native_sample)
            
            if input_sample.buffer is not None:
                if input_sample.buffer.start is None:
                    native_buffer = lib.avb_create_media_buffer(0)
                    lib.MediaSample_setBuffer(self._native_sample, native_buffer)
                    lib.Reference_release(native_buffer)
                else:
                    native_buffer = lib.avb_create_media_buffer(0)
                    
                    # Get buffer data and convert to ctypes pointer
                    buffer_data = input_sample.buffer.start
                    
                    # Create a ctypes array from the bytearray/bytes
                    if isinstance(buffer_data, bytearray):
                        # For bytearray, create array from buffer
                        c_array = (ctypes.c_uint8 * len(buffer_data)).from_buffer(buffer_data)
                        buf_ptr = ctypes.addressof(c_array)
                    elif isinstance(buffer_data, bytes):
                        # For bytes, we need to copy to a mutable buffer first
                        c_array = (ctypes.c_uint8 * len(buffer_data)).from_buffer_copy(buffer_data)
                        buf_ptr = ctypes.addressof(c_array)
                    else:
                        # Fallback for other types
                        buf_ptr = ctypes.cast(buffer_data, ctypes.c_void_p).value
                    
                    lib.MediaBuffer_attach(native_buffer,
                                          buf_ptr + input_sample.buffer.data_offset,
                                          input_sample.buffer.data_size,
                                          True)
                    
                    lib.MediaSample_setBuffer(self._native_sample, native_buffer)
                    lib.Reference_release(native_buffer)
            else:
                lib.MediaSample_setBuffer(self._native_sample, None)
            
            result = lib.Transcoder_push(self._native_ref, input_index, self._native_sample)
            
            if input_sample.buffer is not None:
                native_buffer = lib.MediaSample_buffer(self._native_sample)
                new_data_size = lib.MediaBuffer_dataSize(native_buffer)
                
                if new_data_size == 0:
                    input_sample.buffer.reset_data()
                elif new_data_size < input_sample.buffer.data_size:
                    native_data_offset = lib.MediaBuffer_dataOffset(native_buffer)
                    input_sample.buffer.set_data(
                        input_sample.buffer.data_offset + native_data_offset,
                        new_data_size
                    )
        else:
            result = lib.Transcoder_push(self._native_ref, input_index, None)
        
        return result
    
    def push_unmanaged(self, input_index: int, input_sample: Optional[MediaSample]) -> bool:
        """
        Pushes input data to the Transcoder.
        
        Args:
            input_index: Specifies the index of the input socket whose data is pushed to the Transcoder.
            input_sample: A MediaSample object that contains the input data in the unmanaged_buffer property.
            
        Returns:
            True when the Transcoder has successfully processed some or all of the input data, otherwise False.
        """
        self._check_disposed()
        lib = get_native().lib
        
        if input_sample is not None:
            self._ensure_native_sample()
            
            input_sample._copy_props_to_native(self._native_sample)
            
            if input_sample.unmanaged_buffer is not None and input_sample.unmanaged_buffer.data_size > 0:
                native_buffer = input_sample.unmanaged_buffer._native_ref
                lib.MediaSample_setBuffer(self._native_sample, native_buffer)
            
            result = lib.Transcoder_push(self._native_ref, input_index, self._native_sample)
        else:
            result = lib.Transcoder_push(self._native_ref, input_index, None)
        
        return result
    
    def pull(self, output_sample: MediaSample) -> Tuple[bool, int]:
        """
        Pulls output data from the Transcoder.
        
        Args:
            output_sample: The MediaSample object receives the output data in the buffer property.
            
        Returns:
            A tuple of (success, output_index) where:
            - success: True if the Transcoder has successfully generated output, otherwise False.
            - output_index: The index of the output socket to which the data belongs.
        """
        self._check_disposed()
        lib = get_native().lib
        
        self._ensure_native_sample()
        
        output_index = ctypes.c_int32(0)
        result = lib.Transcoder_pull(self._native_ref, ctypes.byref(output_index), self._native_sample)
        
        if result and output_sample is not None:
            output_sample._copy_props_from_native(self._native_sample)
            output_sample.buffer = MediaBuffer._from_native(lib.MediaSample_buffer(self._native_sample))
        
        return result, output_index.value
    
    def pull_unmanaged(self, output_sample: MediaSample) -> Tuple[bool, int]:
        """
        Pulls output data from the Transcoder.
        
        Args:
            output_sample: The MediaSample object receives the output data in the unmanaged_buffer property.
            
        Returns:
            A tuple of (success, output_index) where:
            - success: True if the Transcoder has successfully generated output, otherwise False.
            - output_index: The index of the output socket to which the data belongs.
        """
        self._check_disposed()
        lib = get_native().lib
        
        self._ensure_native_sample()
        
        output_index = ctypes.c_int32(0)
        result = lib.Transcoder_pull(self._native_ref, ctypes.byref(output_index), self._native_sample)
        
        if result and output_sample is not None:
            output_sample._copy_props_from_native(self._native_sample)
            
            if output_sample.unmanaged_buffer is not None:
                output_sample.unmanaged_buffer.release()
            
            native_buffer = lib.MediaSample_buffer(self._native_sample)
            
            if native_buffer:
                output_sample.unmanaged_buffer = UnmanagedMediaBuffer(native_buffer)
            else:
                output_sample.unmanaged_buffer = None
        
        lib.MediaSample_setBuffer(self._native_sample, None)
        
        return result, output_index.value
    
    def close(self):
        """
        Closes the Transcoder. When closed it can neither accept, nor deliver data.
        
        inputs and outputs are not modified.
        """
        self._check_disposed()
        lib = get_native().lib
        lib.Transcoder_close(self._native_ref)
        self._dispose_native_sample()
    
    def flush(self) -> bool:
        """
        Flushes the data buffered in the Transcoder to the output.
        
        Returns:
            True if the buffered data is successfully flushed; otherwise False.
        """
        self._check_disposed()
        lib = get_native().lib
        return lib.Transcoder_flush(self._native_ref)
    
    def end_of_stream(self, input_index: int) -> bool:
        """
        Tells the Transcoder that there's no more data for the specified input socket.
        
        Args:
            input_index: Specifies the index of the input socket for which there's no more data.
            
        Returns:
            True if the operation is successful; otherwise False.
        """
        self._check_disposed()
        lib = get_native().lib
        return lib.Transcoder_endOfStream(self._native_ref, input_index)
