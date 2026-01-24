"""
DataStreamInfo class for AVBlocks Python bindings.
"""

import ctypes

from .stream_info import StreamInfo
from .constants import MediaType
from .native import get_native


class DataStreamInfo(StreamInfo):
    """
    Describes a generic data stream.
    
    The media type is always MediaType.Data and cannot be changed.
    """
    
    def __init__(self):
        super().__init__()
        self._media_type = MediaType.Data
    
    # pylint: disable=[protected-access]
    def _copy_to_native(self, native_si: ctypes.c_void_p) -> bool:
        """Copy properties to a native DataStreamInfo object."""
        if not native_si:
            return False
        
        lib = get_native().lib
        
        # Verify this is a data stream
        if MediaType(lib.StreamInfo_mediaType(native_si)) != MediaType.Data:
            return False
        
        # Copy all properties including bitrate info for data streams
        lib.StreamInfo_setDuration(native_si, self._duration)
        lib.StreamInfo_setID(native_si, self._id)
        lib.StreamInfo_setProgramNumber(native_si, self._program)
        lib.StreamInfo_setStreamType(native_si, self._stream_type.value)
        lib.StreamInfo_setStreamSubType(native_si, self._stream_sub_type.value)
        lib.StreamInfo_setBitrate(native_si, self._bitrate)
        lib.StreamInfo_setBitrateMode(native_si, self._bitrate_mode.value)
        
        # Copy config data to native
        if self._config_data is not None:
            native_config_data = self._config_data._to_native()
            lib.StreamInfo_setConfigData(native_si, native_config_data)
            lib.Reference_release(native_config_data)
        else:
            lib.StreamInfo_setConfigData(native_si, None)
        
        return True

    # pylint: disable=[protected-access]
    def clone(self) -> 'DataStreamInfo':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new DataStreamInfo object
        """
        cloned = DataStreamInfo()
        
        # Copy base StreamInfo properties
        cloned._media_type = self._media_type
        cloned._stream_type = self._stream_type
        cloned._stream_sub_type = self._stream_sub_type
        cloned._duration = self._duration
        cloned._id = self._id
        cloned._program = self._program
        cloned._bitrate = self._bitrate
        cloned._bitrate_mode = self._bitrate_mode
        
        # Deep copy config data
        if self._config_data is not None:
            cloned._config_data = self._config_data.clone()
        else:
            cloned._config_data = None
        
        # Cloned objects are always mutable
        cloned._immutable = False
        
        return cloned
