"""
MediaPin class for AVBlocks Python bindings.
"""

from typing import Optional
import ctypes

from .native import get_native
from .constants import PinConnection
from .immutable import IImmutable
from .stream_info import StreamInfo
from .parameter_list import ParameterList
from .param_util import ParamUtil


class MediaPin(IImmutable):
    """
    MediaPin represents an elementary media stream.
    
    MediaPin object can exist for audio, video or any other type of stream. 
    However, AVBlocks can process only the audio and video streams.
    MediaPin objects are used as inputs and outputs of Transcoder.
    """
    
    def __init__(self):
        """Creates a MediaPin object."""
        self._connection: int = PinConnection.Auto
        self._stream_info: Optional[StreamInfo] = None
        self._params: ParameterList = ParameterList()
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
        if self._stream_info is not None:
            self._stream_info.immutable = value
        
        self._params.immutable = value
        self._immutable = value
    
    @property
    def connection(self) -> int:
        """
        Connection ID. This should not be confused with the stream ID that is
        defined for certain stream types.

        A Transcoder object matches and connects input and output pins by their
        connection ID. The Transcoder processes the connected pins and ignores
        the unconnected pins.

        Pins are connected to one another according to the following rules:

        - Input pins with connection ID greater than PinConnection.Auto are connected
          to output pins with the same connection ID.
        - Input and output pins with connection ID equal to PinConnection.Auto are
          connected automatically based on their media type (audio or video).
        - Input and output pins with connection ID equal to PinConnection.Disabled
          are ignored.
        """
        return self._connection
    
    @connection.setter
    def connection(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._connection = value
    
    @property
    def stream_info(self) -> Optional[StreamInfo]:
        """
        Information about the elementary stream represented by this pin.
        
        The Transcoder ignores pins that are not audio or video elementary streams.
        If the value of StreamInfo.media_type is MediaType.Audio, it is safe to cast 
        this property to AudioStreamInfo.
        If the media type is MediaType.Video, it is safe to cast this property to 
        VideoStreamInfo.
        """
        return self._stream_info
    
    @stream_info.setter
    def stream_info(self, value: Optional[StreamInfo]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._stream_info = value
    
    @property
    def params(self) -> ParameterList:
        """
        A collection of pin parameters.
        
        These parameters affect the processing of the elementary stream represented 
        by this pin. The default value of this property is an empty ParameterList.
        """
        return self._params
    
    @params.setter
    def params(self, value: ParameterList):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._params = value if value is not None else ParameterList()
    
    # pylint: disable=[protected-access]
    def clone(self) -> 'MediaPin':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new MediaPin object
        """
        pin = MediaPin()
        pin._connection = self._connection
        pin._immutable = False
        
        # Deep copy stream_info
        if self._stream_info is not None:
            pin._stream_info = self._stream_info.clone()
        
        # Deep copy params
        pin._params = self._params.copy()
        
        return pin
    
    def _to_native(self) -> ctypes.c_void_p:
        """Create a native MediaPin object from this instance."""
        
        lib = get_native().lib
        native_pin = lib.avb_create_media_pin()
        
        lib.MediaPin_setConnection(native_pin, self._connection)
        
        if len(self._params) > 0:
            native_params = ParamUtil.to_native_param_list(self._params)
            lib.MediaPin_setParams(native_pin, native_params)
            lib.Reference_release(native_params)
        
        if self._stream_info is not None:
            native_stream_info = self._stream_info._to_native()
            lib.MediaPin_setStreamInfo(native_pin, native_stream_info)
        
        return native_pin
    
    def _copy_from_native(self, native_pin: ctypes.c_void_p):
        """Copy properties from a native MediaPin object."""
        if not native_pin:
            return
        
        lib = get_native().lib
        
        self._connection = lib.MediaPin_connection(native_pin)
        
        # Get params
        native_params = lib.MediaPin_params(native_pin)
        if native_params:
            self._params = ParamUtil.from_native_parameter_list(native_params)
        
        # Get stream info
        native_stream_info = lib.MediaPin_streamInfo(native_pin)
        if native_stream_info:
            self._stream_info = StreamInfo.from_native(native_stream_info)
    
    @staticmethod
    def _from_native(native: ctypes.c_void_p) -> Optional['MediaPin']:
        """Create a MediaPin object from a native MediaPin pointer."""
        if not native:
            return None
        
        pin = MediaPin()
        pin._copy_from_native(native)
        return pin
