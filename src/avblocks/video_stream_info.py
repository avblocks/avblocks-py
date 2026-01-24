"""
VideoStreamInfo class for AVBlocks Python bindings.
"""

import ctypes

from .stream_info import StreamInfo
from .constants import MediaType, ColorFormat, ScanType
from .native import get_native


class VideoStreamInfo(StreamInfo):
    """
    Describes an elementary video stream.
    
    The media type is always MediaType.Video and cannot be changed.
    """
    
    def __init__(self):
        super().__init__()
        self._media_type = MediaType.Video
        self._frame_width: int = 0
        self._frame_height: int = 0
        self._display_ratio_width: int = 0
        self._display_ratio_height: int = 0
        self._frame_rate: float = 0.0
        self._color_format: ColorFormat = ColorFormat.Unknown
        self._scan_type: ScanType = ScanType.Unknown
        self._frame_bottom_up: bool = False
    
    @property
    def frame_width(self) -> int:
        """The video frame width."""
        return self._frame_width
    
    @frame_width.setter
    def frame_width(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._frame_width = value
    
    @property
    def frame_height(self) -> int:
        """The video frame height."""
        return self._frame_height
    
    @frame_height.setter
    def frame_height(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._frame_height = value
    
    @property
    def display_ratio_width(self) -> int:
        """The horizontal dimension of the display aspect ratio."""
        return self._display_ratio_width
    
    @display_ratio_width.setter
    def display_ratio_width(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._display_ratio_width = value
    
    @property
    def display_ratio_height(self) -> int:
        """The vertical dimension of the display aspect ratio."""
        return self._display_ratio_height
    
    @display_ratio_height.setter
    def display_ratio_height(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._display_ratio_height = value
    
    @property
    def frame_rate(self) -> float:
        """The video frame rate."""
        return self._frame_rate
    
    @frame_rate.setter
    def frame_rate(self, value: float):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._frame_rate = value
    
    @property
    def color_format(self) -> ColorFormat:
        """The video color format."""
        return self._color_format
    
    @color_format.setter
    def color_format(self, value: ColorFormat):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._color_format = value
    
    @property
    def scan_type(self) -> ScanType:
        """The interlace (scan) type of the video frame."""
        return self._scan_type
    
    @scan_type.setter
    def scan_type(self, value: ScanType):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._scan_type = value
    
    @property
    def frame_bottom_up(self) -> bool:
        """
        Specifies whether the video frame is stored upside down internally.
        
        When True the frame is stored upside down (vertically flipped) but logically 
        it should be displayed normally. This is typical for bitmaps.
        
        When False the frame is displayed as it is stored - top row is first in memory, 
        bottom row is last.
        """
        return self._frame_bottom_up
    
    @frame_bottom_up.setter
    def frame_bottom_up(self, value: bool):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._frame_bottom_up = value
    
    def _copy_from_native(self, native_si: ctypes.c_void_p) -> bool:
        """Copy properties from a native VideoStreamInfo object."""
        if not native_si:
            return False
        
        lib = get_native().lib
        
        # Verify this is a video stream
        if MediaType(lib.StreamInfo_mediaType(native_si)) != MediaType.Video:
            return False
        
        # Copy base properties
        if not super()._copy_from_native(native_si):
            return False
        
        # Copy video-specific properties
        self._frame_width = lib.VideoStreamInfo_frameWidth(native_si)
        self._frame_height = lib.VideoStreamInfo_frameHeight(native_si)
        self._display_ratio_width = lib.VideoStreamInfo_displayRatioWidth(native_si)
        self._display_ratio_height = lib.VideoStreamInfo_displayRatioHeight(native_si)
        self._frame_rate = lib.VideoStreamInfo_frameRate(native_si)
        self._color_format = ColorFormat(lib.VideoStreamInfo_colorFormat(native_si))
        self._scan_type = ScanType(lib.VideoStreamInfo_scanType(native_si))
        self._frame_bottom_up = lib.VideoStreamInfo_frameBottomUp(native_si)
        
        return True
    
    # pylint: disable=[protected-access]
    def _copy_to_native(self, native_si: ctypes.c_void_p) -> bool:
        """Copy properties to a native VideoStreamInfo object."""
        if not native_si:
            return False
        
        lib = get_native().lib
        
        # Verify this is a video stream
        if MediaType(lib.StreamInfo_mediaType(native_si)) != MediaType.Video:
            return False
        
        # Copy video-specific properties
        lib.VideoStreamInfo_setFrameWidth(native_si, self._frame_width)
        lib.VideoStreamInfo_setFrameHeight(native_si, self._frame_height)
        lib.VideoStreamInfo_setDisplayRatioWidth(native_si, self._display_ratio_width)
        lib.VideoStreamInfo_setDisplayRatioHeight(native_si, self._display_ratio_height)
        lib.VideoStreamInfo_setFrameRate(native_si, self._frame_rate)
        lib.VideoStreamInfo_setColorFormat(native_si, self._color_format.value)
        lib.VideoStreamInfo_setScanType(native_si, self._scan_type.value)
        lib.VideoStreamInfo_setFrameBottomUp(native_si, self._frame_bottom_up)
        
        # Copy base properties
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
    def clone(self) -> 'VideoStreamInfo':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new VideoStreamInfo object
        """
        cloned = VideoStreamInfo()
        
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
        
        # Copy VideoStreamInfo specific properties
        cloned._frame_width = self._frame_width
        cloned._frame_height = self._frame_height
        cloned._display_ratio_width = self._display_ratio_width
        cloned._display_ratio_height = self._display_ratio_height
        cloned._frame_rate = self._frame_rate
        cloned._color_format = self._color_format
        cloned._scan_type = self._scan_type
        cloned._frame_bottom_up = self._frame_bottom_up
        
        # Cloned objects are always mutable
        cloned._immutable = False
        
        return cloned
    
    def reset(self):
        """Resets the video stream information to its default state."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        
        # Reset base properties
        super().reset()
        
        # Reset video-specific properties
        self._frame_width = 0
        self._frame_height = 0
        self._display_ratio_width = 0
        self._display_ratio_height = 0
        self._frame_rate = 0.0
        self._color_format = ColorFormat.Unknown
        self._scan_type = ScanType.Unknown
        self._frame_bottom_up = False
