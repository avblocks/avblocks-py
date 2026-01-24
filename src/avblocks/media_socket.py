"""
MediaSocket class for AVBlocks Python bindings.
"""

from typing import Optional, TYPE_CHECKING
import ctypes

from io import RawIOBase

from .native import get_native
from .constants import StreamType, StreamSubType
from .immutable import IImmutable
from .media_pin import MediaPin
from .parameter_list import ParameterList
from .param_util import ParamUtil
from .stream_proxy import StreamProxy
from .media_pin_list import MediaPinList
from .metadata import Metadata
from .string_util import encode_utf16le_string, decode_utf16le_string

# Import TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from .media_info import MediaInfo


class MediaSocket(IImmutable):
    """
    An input or output point of the Transcoder.
    
    A MediaSocket object describes either a container (WAV, AVI, MP4, etc.) with one or more streams or 
    simply an elementary stream (MP3, M2V, etc.)
    
    When MediaSocket describes a container the child collection of media pins can contain one or more items 
    (for each contained stream). The socket stream type designates the container type.
    
    When MediaSocket describes an elementary stream the child collection of media pins contains a single item 
    which is the elementary stream itself. The socket stream type is the same as the pin stream type.
    """
    
    def __init__(self):
        """Creates a MediaSocket object."""
        self._file: Optional[str] = None
        self._stream: Optional[RawIOBase] = None
        self._stream_proxy: Optional[StreamProxy] = None
        self._stream_type: int = StreamType.Unknown
        self._stream_sub_type: int = StreamSubType.Unknown
        self._params: ParameterList = ParameterList()
        self._pins: MediaPinList = MediaPinList()
        self._time_position: float = 0.0
        self._metadata: Optional[Metadata] = None
        self._immutable: bool = False
    
    @property
    def immutable(self) -> bool:
        """
        Returns whether the object is immutable.
        An immutable object cannot be modified and all modifying methods fail to produce a result.
        
        An immutable object can be modified by the AVBlocks library.
        Object immutability spreads to all nested objects.
        Therefore it is not possible to add/set an immutable object to a mutable object.
        When cloned an immutable object becomes mutable.
        """
        return self._immutable
    
    @immutable.setter
    def immutable(self, value: bool):
        """Set the immutable state and propagate to nested objects."""
        if self._metadata is not None:
            self._metadata.immutable = value
        
        self._pins.immutable = value
        self._params.immutable = value
        self._immutable = value
    
    @property
    def file(self) -> Optional[str]:
        """
        The file associated with the media socket.
        The default value is None.
        """
        return self._file
    
    @file.setter
    def file(self, value: Optional[str]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._file = value
    
    @property
    def stream(self) -> Optional[RawIOBase]:
        """
        The user stream associated with the media socket.
        The default value of this property is None.
        
        This is an alternative to the file property.
        When both a file and a user stream are associated with a socket the Transcoder prefers the user stream.
        """
        return self._stream
    
    @stream.setter
    def stream(self, value: Optional[RawIOBase]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._stream = value
        # Reset stream proxy when stream changes
        self._stream_proxy = None
    
    @property
    def stream_type(self) -> int:
        """
        Specifies explicitly the format of the associated file or stream.
        The default value of this property is StreamType.Unknown.
        """
        return self._stream_type
    
    @stream_type.setter
    def stream_type(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._stream_type = value
    
    @property
    def stream_sub_type(self) -> int:
        """
        Specifies explicitly the subtype of the associated file or stream.
        The default value of this property is StreamSubType.Unknown.
        """
        return self._stream_sub_type
    
    @stream_sub_type.setter
    def stream_sub_type(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._stream_sub_type = value
    
    @property
    def params(self) -> ParameterList:
        """
        A collection of socket parameters.
        These parameters are used when demuxing the input or multiplexing the output defined by this media socket.
        The default value of this property is an empty list.
        """
        return self._params
    
    @params.setter
    def params(self, value: ParameterList):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._params = value if value is not None else ParameterList()
    
    @property
    def pins(self) -> MediaPinList:
        """
        A modifiable collection with all the pins (elementary streams) that are defined for this socket.
        
        The default value of this property is an empty collection which can be modified but it cannot be replaced.
        """
        return self._pins
    
    @property
    def time_position(self) -> float:
        """
        Specifies the position within file / stream (in seconds).
        
        The transcoder tries to seek to the time position before the transcoding operation starts.
        Seeking is not possible while transcoder is open. The Transcoder needs to be closed before 
        setting a new time position with this property.
        """
        return self._time_position
    
    @time_position.setter
    def time_position(self, value: float):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._time_position = value
    
    @property
    def metadata(self) -> Optional[Metadata]:
        """
        The socket metadata.
        Can be None if the socket has no metadata.
        """
        return self._metadata
    
    @metadata.setter
    def metadata(self, value: Optional[Metadata]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._metadata = value
    
    # pylint: disable=[protected-access]
    def clone(self) -> 'MediaSocket':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new MediaSocket object
        """
        socket = MediaSocket()
        socket._file = self._file
        socket._stream = self._stream
        socket._stream_proxy = None  # Don't copy the proxy
        socket._stream_type = self._stream_type
        socket._stream_sub_type = self._stream_sub_type
        socket._time_position = self._time_position
        socket._immutable = False
        
        # Deep copy params
        socket._params = self._params.copy()
        
        # Deep copy pins
        socket._pins = MediaPinList()
        for pin in self._pins:
            socket._pins.add(pin.clone())
        
        # Deep copy metadata
        if self._metadata is not None:
            socket._metadata = self._metadata.clone()
        
        return socket
    
    @staticmethod
    def from_media_info(media_info: 'MediaInfo') -> Optional['MediaSocket']:
        """
        Creates a media socket from a MediaInfo object.
        
        Args:
            media_info: A MediaInfo object with audio/video information. The object may or may not be 
                       loaded before calling this function. This object is not needed after the method returns.
        
        Returns:
            A new MediaSocket object or None.
            The MediaSocket object contains the information supplied by the media_info parameter.
            When from_media_info fails, it returns None. In that case use the MediaInfo.error property 
            to get error information.
        
        This method is meant to help in setting correctly the inputs of a Transcoder.
        The intended usage is as follows:
        1. Use MediaInfo to load information for a file or user stream.
        2. Create a media socket from the MediaInfo object (MediaSocket.from_media_info(media_info))
        3. Add the newly created socket to the inputs of a Transcoder (transcoder.inputs.add(socket))
        """
        if media_info is None:
            return None
        
        if not media_info.is_ready:
            if not media_info.open():
                return None
        
        socket = MediaSocket()
        
        # If there are multiple MediaInfo outputs then the implementation has to be revised.
        assert len(media_info.outputs) <= 1
        
        if len(media_info.outputs) > 0:
            mi_output_socket = media_info.outputs[0]
            
            # Copy pins
            for mi_pin in mi_output_socket.pins:
                stream_info = mi_pin.stream_info
                pin = MediaPin()
                pin.connection = mi_pin.connection
                pin.stream_info = stream_info.clone() if stream_info is not None else None
                socket.pins.add(pin)
            
            socket._stream_type = mi_output_socket.stream_type
            socket._file = mi_output_socket.file
            socket._stream = mi_output_socket.stream
            socket._metadata = mi_output_socket.metadata
        
        return socket
    
    @staticmethod
    def from_preset(preset: str) -> Optional['MediaSocket']:
        """
        Creates a media socket from an AVBlocks Preset.
        
        Args:
            preset: A constant from the Preset enum
            
        Returns:
            A new MediaSocket object which is configured for the specified preset,
            or None if the preset is invalid.
            
        This method is meant to help in setting correctly the outputs of the Transcoder.
        The intended usage is as follows:
        1. Create a media socket from a Preset (MediaSocket.from_preset(preset))
        2. Add the newly created socket to the outputs of the Transcoder (transcoder.outputs.add(socket))
        """
        lib = get_native().lib
        native_socket = lib.avb_create_media_socket_from_preset(preset.encode('utf-8'))
        
        if not native_socket:
            return None
        
        socket = MediaSocket._from_native(native_socket)
        lib.Reference_release(native_socket)
        
        return socket
    
    def _to_native(self) -> ctypes.c_void_p:
        """Create a native MediaSocket object from this instance."""
        lib = get_native().lib
        native_socket = lib.avb_create_media_socket()
        
        # Set file
        if self._file is not None:
            lib.MediaSocket_setFile(native_socket, encode_utf16le_string(self._file))
        
        # Set stream callback - reuse existing proxy if available
        if self._stream is not None:
            if self._stream_proxy is None:
                self._stream_proxy = StreamProxy(self._stream)
            callback = self._stream_proxy.native_stream_callback
            if callback is not None:
                lib.MediaSocket_setStreamCallback(native_socket, ctypes.byref(callback))
        
        # Set stream type and subtype
        lib.MediaSocket_setStreamType(native_socket, self._stream_type)
        lib.MediaSocket_setStreamSubType(native_socket, self._stream_sub_type)
        
        # Set params
        if len(self._params) > 0:
            native_params = ParamUtil.to_native_param_list(self._params)
            lib.MediaSocket_setParams(native_socket, native_params)
            lib.Reference_release(native_params)
        
        # Add pins using MediaPinList.to_native
        native_pins = lib.MediaSocket_pins(native_socket)
        self._pins.to_native(native_pins)
        
        # Set metadata
        if self._metadata is not None:
            native_metadata = self._metadata._to_native()
            lib.MediaSocket_setMetadata(native_socket, native_metadata)
            lib.Reference_release(native_metadata)
        
        # Set time position
        lib.MediaSocket_setTimePosition(native_socket, self._time_position)
        
        return native_socket
    
    @staticmethod
    def _from_native(native_socket: ctypes.c_void_p) -> Optional['MediaSocket']:
        """Create a MediaSocket object from a native MediaSocket pointer."""
        if not native_socket:
            return None
        
        lib = get_native().lib
        socket = MediaSocket()
        
        # Get file
        file_ptr = lib.MediaSocket_file(native_socket)
        if file_ptr:
            socket._file = decode_utf16le_string(file_ptr)
        
        # Note: We probably don't need to construct a Python Stream from native Stream interface
        
        # Get stream type and subtype
        socket._stream_type = lib.MediaSocket_streamType(native_socket)
        socket._stream_sub_type = lib.MediaSocket_streamSubType(native_socket)
        
        # Get params
        native_params = lib.MediaSocket_params(native_socket)
        if native_params:
            socket._params = ParamUtil.from_native_parameter_list(native_params)
        
        # Get pins - add to existing _pins list, don't replace it
        native_pins = lib.MediaSocket_pins(native_socket)
        if native_pins:
            pin_count = lib.MediaPinList_count(native_pins)
            for i in range(pin_count):
                native_pin = lib.MediaPinList_at(native_pins, i)
                pin = MediaPin._from_native(native_pin)
                if pin is not None:
                    socket._pins.add(pin)
        
        # Get metadata
        native_metadata = lib.MediaSocket_metadata(native_socket)
        if native_metadata:
            socket._metadata = Metadata._from_native(native_metadata)
        
        # Get time position
        socket._time_position = lib.MediaSocket_timePosition(native_socket)
        
        return socket
