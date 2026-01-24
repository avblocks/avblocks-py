"""
MediaSample class for AVBlocks Python bindings.
"""

from typing import Optional
import ctypes

from .media_buffer import MediaBuffer
from .unmanaged_media_buffer import UnmanagedMediaBuffer
from .native import get_native
from .constants import MediaSampleFlags, PictureType, FrameType, ColorFormat


class MediaSample:
    """
    Represents one or more samples of media data.
    """
    
    def __init__(self):
        """Creates an empty sample."""
        self._buffer: Optional[MediaBuffer] = None
        self._unmanaged_buffer: Optional[UnmanagedMediaBuffer] = None
        self._start_time: float = -1.0
        self._end_time: float = -1.0
        self._flags: MediaSampleFlags = MediaSampleFlags(0)
        self._picture_type: PictureType = PictureType.None_
        self._frame_type: FrameType = FrameType.None_
    
    @property
    def buffer(self) -> Optional[MediaBuffer]:
        """The buffer storage."""
        return self._buffer
    
    @buffer.setter
    def buffer(self, value: Optional[MediaBuffer]):
        """Set the buffer storage."""
        self._buffer = value
    
    @property
    def unmanaged_buffer(self) -> Optional[UnmanagedMediaBuffer]:
        """
        Used to push and pull unmanaged data to/from Transcoder.
        """
        return self._unmanaged_buffer
    
    @unmanaged_buffer.setter
    def unmanaged_buffer(self, value: Optional[UnmanagedMediaBuffer]):
        """Set the unmanaged buffer."""
        self._unmanaged_buffer = value
    
    @property
    def start_time(self) -> float:
        """
        Presentation timestamp.
        
        The StartTime is valid if it is 0 or greater than 0.
        The default value is -1.0
        """
        return self._start_time
    
    @start_time.setter
    def start_time(self, value: float):
        """Set the start time."""
        self._start_time = value
    
    @property
    def end_time(self) -> float:
        """
        The time when the media sample should end.
        
        The EndTime is valid only if it is positive and greater than the StartTime.
        The default value is -1.0
        """
        return self._end_time
    
    @end_time.setter
    def end_time(self, value: float):
        """Set the end time."""
        self._end_time = value
    
    @property
    def flags(self) -> MediaSampleFlags:
        """Various properties of the media sample (MediaSampleFlags)."""
        return self._flags
    
    @flags.setter
    def flags(self, value: MediaSampleFlags):
        """Set the flags."""
        self._flags = value
    
    @property
    def picture_type(self) -> PictureType:
        """
        The picture type (I/P/B/etc.) of a demuxed, decoded or encoded frame.
        
        Currently this is returned only by the MPEG-2 encoder and is ignored by all encoders.
        """
        return self._picture_type
    
    @picture_type.setter
    def picture_type(self, value: PictureType):
        """Set the picture type."""
        self._picture_type = value
    
    @property
    def frame_type(self) -> FrameType:
        """
        The frame type of demuxed, decoded, or encoded frame.
        Added in version 3.2
        
        Currently this is used only by G.711 a-law and u-law codecs.
        """
        return self._frame_type
    
    @frame_type.setter
    def frame_type(self, value: FrameType):
        """Set the frame type."""
        self._frame_type = value
    
    @staticmethod
    def video_buffer_size_in_bytes(frame_width: int, frame_height: int, color_format: ColorFormat) -> int:
        """
        Calculates the exact number of bytes that are needed
        for a video frame with the specified properties.
        
        Args:
            frame_width: Frame width in pixels.
            frame_height: Frame height in pixels.
            color_format: The color format represents how colors are coded in the video frame.
            
        Returns:
            The number of bytes needed to store a video frame with the specified properties.
            Zero if it is not possible to calculate the video frame buffer size from the supplied arguments.
        """
        lib = get_native().lib
        native_sample = lib.avb_create_media_sample()
        buffer_size = lib.MediaSample_videoBufferSizeInBytes(
            native_sample,
            frame_width,
            frame_height,
            color_format.value
        )
        lib.Reference_release(native_sample)
        return buffer_size
    
    def _copy_props_to_native(self, native_sample: ctypes.c_void_p):
        """
        Internal method to copy properties to a native MediaSample.
        
        Args:
            native_sample: Native MediaSample pointer
        """
        lib = get_native().lib
        lib.MediaSample_setStartTime(native_sample, self._start_time)
        lib.MediaSample_setEndTime(native_sample, self._end_time)
        lib.MediaSample_setFlags(native_sample, self._flags.value)
        lib.MediaSample_setPictureType(native_sample, self._picture_type.value)
        lib.MediaSample_setFrameType(native_sample, self._frame_type.value)
    
    def _copy_props_from_native(self, native_sample: ctypes.c_void_p):
        """
        Internal method to copy properties from a native MediaSample.
        
        Args:
            native_sample: Native MediaSample pointer
        """
        lib = get_native().lib
        self._start_time = lib.MediaSample_startTime(native_sample)
        self._end_time = lib.MediaSample_endTime(native_sample)
        self._flags = MediaSampleFlags(lib.MediaSample_flags(native_sample))
        self._picture_type = PictureType(lib.MediaSample_pictureType(native_sample))
        self._frame_type = FrameType(lib.MediaSample_frameType(native_sample))
    
    # pylint: disable=protected-access
    def clone(self) -> 'MediaSample':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new MediaSample object.
            
        Raises:
            MemoryError: If the object cannot be cloned because there's not enough memory.
        """
        ms = MediaSample()
        ms._start_time = self._start_time
        ms._end_time = self._end_time
        ms._flags = self._flags
        ms._picture_type = self._picture_type
        ms._frame_type = self._frame_type
        
        if self._buffer is not None:
            ms._buffer = self._buffer.clone()
        
        if self._unmanaged_buffer is not None:
            ms._unmanaged_buffer = self._unmanaged_buffer.clone()
        
        return ms
