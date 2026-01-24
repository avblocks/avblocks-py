"""
AudioStreamInfo class for AVBlocks Python bindings.
"""

import ctypes

from .stream_info import StreamInfo
from .constants import MediaType, PcmFlags, AudioChannelFlags
from .native import get_native


class AudioStreamInfo(StreamInfo):
    """
    Describes an elementary audio stream.
    
    The media type is always MediaType.Audio and cannot be changed.
    """
    
    def __init__(self):
        super().__init__()
        self._media_type = MediaType.Audio
        self._pcm_flags: PcmFlags = PcmFlags.None_
        self._channels: int = 0
        self._channel_layout: AudioChannelFlags = AudioChannelFlags.None_
        self._sample_rate: int = 0
        self._bits_per_sample: int = 0
        self._bytes_per_frame: int = 0
    
    @property
    def pcm_flags(self) -> PcmFlags:
        """Various properties of the audio stream."""
        return self._pcm_flags
    
    @pcm_flags.setter
    def pcm_flags(self, value: PcmFlags):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._pcm_flags = value
    
    @property
    def channels(self) -> int:
        """The number of audio channels in the stream."""
        return self._channels
    
    @channels.setter
    def channels(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._channels = value
    
    @property
    def channel_layout(self) -> AudioChannelFlags:
        """The channel layout defines the mapping between channels and speakers."""
        return self._channel_layout
    
    @channel_layout.setter
    def channel_layout(self, value: AudioChannelFlags):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._channel_layout = value
    
    @property
    def sample_rate(self) -> int:
        """The audio sample rate in Hz."""
        return self._sample_rate
    
    @sample_rate.setter
    def sample_rate(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._sample_rate = value
    
    @property
    def bits_per_sample(self) -> int:
        """
        The number of valid bits per sample (sample resolution).
        
        Common values are 8, 16, 20, 24 and 32.
        
        Normally BitsPerSample is defined only for uncompressed audio streams. 
        For compressed audio it is not defined and is 0.
        However it is possible for a compressed audio stream to return a positive 
        value as an indication of audio quality.
        It can also designate the bits per sample of the LPCM stream once the 
        compressed stream is decoded.
        """
        return self._bits_per_sample
    
    @bits_per_sample.setter
    def bits_per_sample(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._bits_per_sample = value
    
    @property
    def bytes_per_frame(self) -> int:
        """
        The number of bytes occupied by an audio frame (smallest discrete unit).
        
        A frame is the smallest discrete unit in an audio stream. It may contain 
        one or more samples. Depending on the audio stream type the frame may 
        contain fixed or variable number of samples.
        
        For compressed streams the frame size is variable even if there are fixed 
        number of samples in each frame. In this case BytesPerFrame is 0.
        
        For an LPCM stream the frame size is constant. In this case BytesPerFrame 
        is greater than 0. Normally for interleaved LPCM streams the following is true:
        - BytesPerFrame / ChannelCount == SampleSize
        - The valid bits in a sample are given by BitsPerSample and they are 
          aligned towards the hi-order byte.
        """
        return self._bytes_per_frame
    
    @bytes_per_frame.setter
    def bytes_per_frame(self, value: int):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._bytes_per_frame = value
    
    def _copy_from_native(self, native_si: ctypes.c_void_p) -> bool:
        """Copy properties from a native AudioStreamInfo object."""
        if not native_si:
            return False
        
        lib = get_native().lib
        
        # Verify this is an audio stream
        if MediaType(lib.StreamInfo_mediaType(native_si)) != MediaType.Audio:
            return False
        
        # Copy base properties
        if not super()._copy_from_native(native_si):
            return False
        
        # Copy audio-specific properties
        self._bits_per_sample = lib.AudioStreamInfo_bitsPerSample(native_si)
        self._bytes_per_frame = lib.AudioStreamInfo_bytesPerFrame(native_si)
        self._channel_layout = AudioChannelFlags(lib.AudioStreamInfo_channelLayout(native_si))
        self._channels = lib.AudioStreamInfo_channels(native_si)
        self._pcm_flags = PcmFlags(lib.AudioStreamInfo_pcmFlags(native_si))
        self._sample_rate = lib.AudioStreamInfo_sampleRate(native_si)
        
        return True
    
    # pylint: disable=[protected-access]
    def _copy_to_native(self, native_si: ctypes.c_void_p) -> bool:
        """Copy properties to a native AudioStreamInfo object."""
        if not native_si:
            return False
        
        lib = get_native().lib
        
        # Verify this is an audio stream
        if MediaType(lib.StreamInfo_mediaType(native_si)) != MediaType.Audio:
            return False
        
        # Copy audio-specific properties
        lib.AudioStreamInfo_setBitsPerSample(native_si, self._bits_per_sample)
        lib.AudioStreamInfo_setBytesPerFrame(native_si, self._bytes_per_frame)
        lib.AudioStreamInfo_setChannelLayout(native_si, self._channel_layout.value)
        lib.AudioStreamInfo_setChannels(native_si, self._channels)
        lib.AudioStreamInfo_setPcmFlags(native_si, self._pcm_flags.value)
        lib.AudioStreamInfo_setSampleRate(native_si, self._sample_rate)
        
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
    def clone(self) -> 'AudioStreamInfo':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new AudioStreamInfo object
        """
        cloned = AudioStreamInfo()
        
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
        
        # Copy AudioStreamInfo specific properties
        cloned._pcm_flags = self._pcm_flags
        cloned._channels = self._channels
        cloned._channel_layout = self._channel_layout
        cloned._sample_rate = self._sample_rate
        cloned._bits_per_sample = self._bits_per_sample
        cloned._bytes_per_frame = self._bytes_per_frame
        
        # Cloned objects are always mutable
        cloned._immutable = False
        
        return cloned
    
    def reset(self):
        """Resets the audio stream information to its default state."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        
        # Reset base properties
        super().reset()
        
        # Reset audio-specific properties
        self._channels = 0
        self._channel_layout = AudioChannelFlags.None_
        self._sample_rate = 0
        self._bits_per_sample = 0
        self._bytes_per_frame = 0
        self._pcm_flags = PcmFlags.None_
