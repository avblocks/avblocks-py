"""
StreamInfo classes for AVBlocks Python bindings.
"""

from typing import Optional
import ctypes

from .native import get_native
from .constants import MediaType, StreamType, StreamSubType, BitrateMode
from .immutable import IImmutable
from .media_buffer import MediaBuffer

class StreamInfo(IImmutable):
    """
    Provides properties and operations that are common for all elementary streams.
    
    AudioStreamInfo and VideoStreamInfo inherit from this class.
    """
    
    def __init__(self):
        self._media_type: MediaType = MediaType.Unknown
        self._stream_type: StreamType = StreamType.Unknown
        self._stream_sub_type: StreamSubType = StreamSubType.Unknown
        self._duration: float = 0.0
        self._id: int = 0
        self._program: int = 0
        self._bitrate: int = 0
        self._bitrate_mode: BitrateMode = BitrateMode.Unknown
        self._config_data: Optional[MediaBuffer] = None
        self._immutable: bool = False
    
    @property
    def immutable(self) -> bool:
        """
        Returns whether the object is immutable.
        An immutable object cannot be modified and all modifying methods fail to produce a result.
        """
        return self._immutable
    
    @immutable.setter
    def immutable(self, value: bool):
        """Set the immutable state."""
        self._immutable = value
    
    @property
    def media_type(self) -> MediaType:
        """
        Media type. The media type of a StreamInfo object cannot be changed.
        """
        return self._media_type
    
    @property
    def stream_type(self) -> StreamType:
        """The stream type."""
        return self._stream_type
    
    @stream_type.setter
    def stream_type(self, value: StreamType):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._stream_type = value
    
    @property
    def stream_sub_type(self) -> StreamSubType:
        """The stream subtype."""
        return self._stream_sub_type
    
    @stream_sub_type.setter
    def stream_sub_type(self, value: StreamSubType):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._stream_sub_type = value
    
    @property
    def duration(self) -> float:
        """The stream duration in seconds."""
        return self._duration
    
    @duration.setter
    def duration(self, value: float):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._duration = value
    
    @property
    def id(self) -> int:
        """The ID of the elementary stream."""
        return self._id
    
    @id.setter
    def id(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._id = value
    
    @property
    def program_number(self) -> int:
        """
        The number of the program to which the elementary stream belongs.
        
        If the elementary stream is shared by 2 or more programs this property
        will return the last parsed program that uses this stream.
        """
        return self._program
    
    @program_number.setter
    def program_number(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._program = value
    
    @property
    def bitrate(self) -> int:
        """The stream bitrate expressed in bits per second."""
        return self._bitrate
    
    @bitrate.setter
    def bitrate(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._bitrate = value
    
    @property
    def bitrate_mode(self) -> BitrateMode:
        """The stream bitrate mode."""
        return self._bitrate_mode
    
    @bitrate_mode.setter
    def bitrate_mode(self, value: BitrateMode):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._bitrate_mode = value
    
    @property
    def config_data(self) -> Optional[MediaBuffer]:
        """
        Decoder specific configuration data.
        This data is typically obtained from a demuxer and is required for decoding certain stream types.
        """
        return self._config_data
    
    @config_data.setter
    def config_data(self, value: Optional[MediaBuffer]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._config_data = value
    
    # pylint: disable=[protected-access]
    def _copy_from_native(self, native_si: ctypes.c_void_p) -> bool:
        """Copy properties from a native StreamInfo object."""
        if not native_si:
            return False
        
        lib = get_native().lib
        
        # Get media type from native object
        media_type = MediaType(lib.StreamInfo_mediaType(native_si))
        self._media_type = media_type
        
        # Copy basic properties
        self._duration = lib.StreamInfo_duration(native_si)
        self._id = lib.StreamInfo_ID(native_si)
        self._program = lib.StreamInfo_programNumber(native_si)
        self._stream_type = StreamType(lib.StreamInfo_streamType(native_si))
        self._stream_sub_type = StreamSubType(lib.StreamInfo_streamSubType(native_si))
        self._bitrate = lib.StreamInfo_bitrate(native_si)
        self._bitrate_mode = BitrateMode(lib.StreamInfo_bitrateMode(native_si))
        
        # Copy config data from native (can be NULL)
        native_config_data = lib.StreamInfo_configData(native_si)
        if native_config_data:
            self._config_data = MediaBuffer._from_native(native_config_data)
        else:
            self._config_data = None
        
        return True
    
    # pylint: disable=[protected-access]
    def _copy_to_native(self, native_si: ctypes.c_void_p) -> bool:
        """Copy properties to a native StreamInfo object."""
        if not native_si:
            return False
        
        lib = get_native().lib
        
        # Verify media type matches
        native_media_type = MediaType(lib.StreamInfo_mediaType(native_si))
        if native_media_type != self._media_type:
            return False
        
        # Copy properties to native object
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
    def clone(self) -> 'StreamInfo':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new StreamInfo object that has the same dynamic type as the cloned object.
        """
        # Create a new instance of the same type
        cloned = self.__class__()
        
        # Copy all properties
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
    
    def reset(self):
        """
        Resets the stream information to its default state.
        
        The full underlying object is reset. The media type of the stream is not changed.
        """
        if self._immutable:
            raise RuntimeError("Object is immutable")
        
        self._stream_type = StreamType.Unknown
        self._stream_sub_type = StreamSubType.Unknown
        self._duration = 0.0
        self._id = 0
        self._program = 0
        self._bitrate = 0
        self._bitrate_mode = BitrateMode.Unknown
        self._config_data = None
    
    def _to_native(self) -> Optional[ctypes.c_void_p]:
        """Create a native StreamInfo object from this instance."""
        lib = get_native().lib
        native_si = None
        
        if self._media_type == MediaType.Audio:
            native_si = lib.avb_create_audio_stream_info()
        elif self._media_type == MediaType.Video:
            native_si = lib.avb_create_video_stream_info()
        elif self._media_type in (MediaType.Data, MediaType.Text):
            native_si = lib.avb_create_data_stream_info()
        
        if native_si:
            self._copy_to_native(native_si)
        
        return native_si
    
    # pylint: disable=[import-outside-toplevel]
    @staticmethod
    def create(media_type: MediaType) -> 'StreamInfo':
        """Create a StreamInfo object for the specified media type."""
        if media_type == MediaType.Audio:
            from .audio_stream_info import AudioStreamInfo
            return AudioStreamInfo()
        if media_type == MediaType.Video:
            from .video_stream_info import VideoStreamInfo
            return VideoStreamInfo()
        if media_type in (MediaType.Data, MediaType.Text):
            from .data_stream_info import DataStreamInfo
            return DataStreamInfo()
        raise ValueError(f"Unsupported media type: {media_type}")
    
    # pylint: disable=[W0212:protected-access]
    @staticmethod
    def from_native(native_si: ctypes.c_void_p) -> Optional['StreamInfo']:
        """Create a StreamInfo object from a native StreamInfo pointer."""
        if not native_si:
            return None
        
        lib = get_native().lib
        media_type = MediaType(lib.StreamInfo_mediaType(native_si))
        
        si = StreamInfo.create(media_type)
        if si._copy_from_native(native_si):
            return si
        
        return None