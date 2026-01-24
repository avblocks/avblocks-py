"""
Native C API bindings for AVBlocks.
"""

import os
import sys
import ctypes
from ctypes import c_bool, c_int32, c_char_p, c_void_p, c_double
from pathlib import Path
from typing import Optional

class NativeLibrary:
    """Wrapper for the native AVBlocks library."""
    
    _instance: Optional['NativeLibrary'] = None
    _lib = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._lib is None:
            self._load_library()
            self._setup_functions()
    
    def _load_library(self):
        """Load the native library from the path specified in environment variable."""
        lib_path = os.environ.get('AVBLOCKS_LIBRARY_PATH')
        
        if not lib_path:
            # Try default locations based on platform
            if sys.platform == 'darwin':
                lib_name = 'libAVBlocks.dylib'
            elif sys.platform == 'linux':
                lib_name = 'libAVBlocks64.so'
            elif sys.platform == 'win32':
                lib_name = 'AVBlocks64.dll'
            else:
                raise RuntimeError(f"Unsupported platform: {sys.platform}")
            
            # Look in common locations
            search_paths = [
                Path(__file__).parent.parent.parent / 'sdk' / 'lib' / 'x64',
                Path('/usr/local/lib'),
                Path('/usr/lib'),
            ]
            
            for path in search_paths:
                candidate = path / lib_name
                if candidate.exists():
                    lib_path = str(candidate)
                    break
        
        if not lib_path or not Path(lib_path).exists():
            raise RuntimeError(
                "AVBlocks library not found. Please set AVBLOCKS_LIBRARY_PATH "
                "environment variable to point to the library file."
            )
        
        try:
            self._lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise RuntimeError(f"Failed to load AVBlocks library from {lib_path}: {e}") from e
    
    def _setup_functions(self):
        """Set up function signatures for the native library."""
        lib = self._lib
        
        # Library initialization
        lib.avb_initialize.argtypes = []
        lib.avb_initialize.restype = c_bool
        
        lib.avb_shutdown.argtypes = []
        lib.avb_shutdown.restype = None
        
        lib.avb_get_major_version.argtypes = []
        lib.avb_get_major_version.restype = c_int32
        
        lib.avb_get_minor_version.argtypes = []
        lib.avb_get_minor_version.restype = c_int32
        
        lib.avb_get_patch_version.argtypes = []
        lib.avb_get_patch_version.restype = c_int32
        
        lib.avb_get_description.argtypes = []
        lib.avb_get_description.restype = c_char_p
        
        lib.avb_set_license_tls.argtypes = [c_bool]
        lib.avb_set_license_tls.restype = None
        
        lib.avb_set_license.argtypes = [c_char_p]
        lib.avb_set_license.restype = c_int32
        
        lib.avb_license_status.argtypes = []
        lib.avb_license_status.restype = c_int32
        
        lib.avb_is_licensed.argtypes = [c_char_p, c_char_p]
        lib.avb_is_licensed.restype = c_bool
        
        # MediaInfo methods
        lib.avb_create_media_info.argtypes = []
        lib.avb_create_media_info.restype = c_void_p
        
        lib.MediaInfo_error.argtypes = [c_void_p]
        lib.MediaInfo_error.restype = c_void_p
        
        lib.MediaInfo_isReady.argtypes = [c_void_p]
        lib.MediaInfo_isReady.restype = c_bool
        
        lib.MediaInfo_push.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MediaInfo_push.restype = c_bool
        
        lib.MediaInfo_pull.argtypes = [c_void_p, ctypes.POINTER(c_int32), c_void_p]
        lib.MediaInfo_pull.restype = c_bool
        
        lib.MediaInfo_inputs.argtypes = [c_void_p]
        lib.MediaInfo_inputs.restype = c_void_p
        
        lib.MediaInfo_outputs.argtypes = [c_void_p]
        lib.MediaInfo_outputs.restype = c_void_p
        
        lib.MediaInfo_open.argtypes = [c_void_p]
        lib.MediaInfo_open.restype = c_bool
        
        lib.MediaInfo_close.argtypes = [c_void_p]
        lib.MediaInfo_close.restype = None
        
        lib.MediaInfo_flush.argtypes = [c_void_p]
        lib.MediaInfo_flush.restype = c_bool
        
        lib.MediaInfo_endOfStream.argtypes = [c_void_p, c_int32]
        lib.MediaInfo_endOfStream.restype = c_bool
        
        # Reference counting
        lib.Reference_retain.argtypes = [c_void_p]
        lib.Reference_retain.restype = c_int32
        
        lib.Reference_release.argtypes = [c_void_p]
        lib.Reference_release.restype = c_int32
        
        lib.Reference_count.argtypes = [c_void_p]
        lib.Reference_count.restype = c_int32
        
        # ErrorInfo methods
        lib.ErrorInfo_code.argtypes = [c_void_p]
        lib.ErrorInfo_code.restype = c_int32
        
        lib.ErrorInfo_facility.argtypes = [c_void_p]
        lib.ErrorInfo_facility.restype = c_int32
        
        lib.ErrorInfo_message.argtypes = [c_void_p]
        lib.ErrorInfo_message.restype = c_void_p  # char_t* (utf-16-le)
        
        lib.ErrorInfo_hint.argtypes = [c_void_p]
        lib.ErrorInfo_hint.restype = c_void_p  # char_t* (utf-16-le)
        
        lib.ErrorInfo_block.argtypes = [c_void_p]
        lib.ErrorInfo_block.restype = c_void_p  # char_t* (utf-16-le)
        
        lib.ErrorInfo_clone.argtypes = [c_void_p]
        lib.ErrorInfo_clone.restype = c_void_p
        
        # Create stream info objects
        lib.avb_create_audio_stream_info.argtypes = []
        lib.avb_create_audio_stream_info.restype = c_void_p
        
        lib.avb_create_video_stream_info.argtypes = []
        lib.avb_create_video_stream_info.restype = c_void_p
        
        lib.avb_create_data_stream_info.argtypes = []
        lib.avb_create_data_stream_info.restype = c_void_p
        
        # StreamInfo methods
        lib.StreamInfo_mediaType.argtypes = [c_void_p]
        lib.StreamInfo_mediaType.restype = c_int32
        
        lib.StreamInfo_streamType.argtypes = [c_void_p]
        lib.StreamInfo_streamType.restype = c_int32
        
        lib.StreamInfo_setStreamType.argtypes = [c_void_p, c_int32]
        lib.StreamInfo_setStreamType.restype = c_bool
        
        lib.StreamInfo_streamSubType.argtypes = [c_void_p]
        lib.StreamInfo_streamSubType.restype = c_int32
        
        lib.StreamInfo_setStreamSubType.argtypes = [c_void_p, c_int32]
        lib.StreamInfo_setStreamSubType.restype = c_bool
        
        lib.StreamInfo_duration.argtypes = [c_void_p]
        lib.StreamInfo_duration.restype = c_double
        
        lib.StreamInfo_setDuration.argtypes = [c_void_p, c_double]
        lib.StreamInfo_setDuration.restype = c_bool
        
        lib.StreamInfo_ID.argtypes = [c_void_p]
        lib.StreamInfo_ID.restype = c_int32
        
        lib.StreamInfo_setID.argtypes = [c_void_p, c_int32]
        lib.StreamInfo_setID.restype = c_bool
        
        lib.StreamInfo_programNumber.argtypes = [c_void_p]
        lib.StreamInfo_programNumber.restype = c_int32
        
        lib.StreamInfo_setProgramNumber.argtypes = [c_void_p, c_int32]
        lib.StreamInfo_setProgramNumber.restype = c_bool
        
        lib.StreamInfo_bitrate.argtypes = [c_void_p]
        lib.StreamInfo_bitrate.restype = c_int32
        
        lib.StreamInfo_setBitrate.argtypes = [c_void_p, c_int32]
        lib.StreamInfo_setBitrate.restype = c_bool
        
        lib.StreamInfo_bitrateMode.argtypes = [c_void_p]
        lib.StreamInfo_bitrateMode.restype = c_int32
        
        lib.StreamInfo_setBitrateMode.argtypes = [c_void_p, c_int32]
        lib.StreamInfo_setBitrateMode.restype = c_bool
        
        lib.StreamInfo_immutable.argtypes = [c_void_p]
        lib.StreamInfo_immutable.restype = c_bool
        
        lib.StreamInfo_clone.argtypes = [c_void_p]
        lib.StreamInfo_clone.restype = c_void_p
        
        lib.StreamInfo_reset.argtypes = [c_void_p]
        lib.StreamInfo_reset.restype = c_bool
        
        lib.StreamInfo_configData.argtypes = [c_void_p]
        lib.StreamInfo_configData.restype = c_void_p
        
        lib.StreamInfo_setConfigData.argtypes = [c_void_p, c_void_p]
        lib.StreamInfo_setConfigData.restype = None
        
        # AudioStreamInfo methods
        lib.AudioStreamInfo_pcmFlags.argtypes = [c_void_p]
        lib.AudioStreamInfo_pcmFlags.restype = c_int32
        
        lib.AudioStreamInfo_setPcmFlags.argtypes = [c_void_p, c_int32]
        lib.AudioStreamInfo_setPcmFlags.restype = c_bool
        
        lib.AudioStreamInfo_channels.argtypes = [c_void_p]
        lib.AudioStreamInfo_channels.restype = c_int32
        
        lib.AudioStreamInfo_setChannels.argtypes = [c_void_p, c_int32]
        lib.AudioStreamInfo_setChannels.restype = c_bool
        
        lib.AudioStreamInfo_channelLayout.argtypes = [c_void_p]
        lib.AudioStreamInfo_channelLayout.restype = c_int32
        
        lib.AudioStreamInfo_setChannelLayout.argtypes = [c_void_p, c_int32]
        lib.AudioStreamInfo_setChannelLayout.restype = c_bool
        
        lib.AudioStreamInfo_sampleRate.argtypes = [c_void_p]
        lib.AudioStreamInfo_sampleRate.restype = c_int32
        
        lib.AudioStreamInfo_setSampleRate.argtypes = [c_void_p, c_int32]
        lib.AudioStreamInfo_setSampleRate.restype = c_bool
        
        lib.AudioStreamInfo_bitsPerSample.argtypes = [c_void_p]
        lib.AudioStreamInfo_bitsPerSample.restype = c_int32
        
        lib.AudioStreamInfo_setBitsPerSample.argtypes = [c_void_p, c_int32]
        lib.AudioStreamInfo_setBitsPerSample.restype = c_bool
        
        lib.AudioStreamInfo_bytesPerFrame.argtypes = [c_void_p]
        lib.AudioStreamInfo_bytesPerFrame.restype = c_int32
        
        lib.AudioStreamInfo_setBytesPerFrame.argtypes = [c_void_p, c_int32]
        lib.AudioStreamInfo_setBytesPerFrame.restype = c_bool
        
        lib.AudioStreamInfo_clone.argtypes = [c_void_p]
        lib.AudioStreamInfo_clone.restype = c_void_p
        
        # VideoStreamInfo methods
        lib.VideoStreamInfo_frameWidth.argtypes = [c_void_p]
        lib.VideoStreamInfo_frameWidth.restype = c_int32
        
        lib.VideoStreamInfo_setFrameWidth.argtypes = [c_void_p, c_int32]
        lib.VideoStreamInfo_setFrameWidth.restype = c_bool
        
        lib.VideoStreamInfo_frameHeight.argtypes = [c_void_p]
        lib.VideoStreamInfo_frameHeight.restype = c_int32
        
        lib.VideoStreamInfo_setFrameHeight.argtypes = [c_void_p, c_int32]
        lib.VideoStreamInfo_setFrameHeight.restype = c_bool
        
        lib.VideoStreamInfo_displayRatioWidth.argtypes = [c_void_p]
        lib.VideoStreamInfo_displayRatioWidth.restype = c_int32
        
        lib.VideoStreamInfo_setDisplayRatioWidth.argtypes = [c_void_p, c_int32]
        lib.VideoStreamInfo_setDisplayRatioWidth.restype = c_bool
        
        lib.VideoStreamInfo_displayRatioHeight.argtypes = [c_void_p]
        lib.VideoStreamInfo_displayRatioHeight.restype = c_int32
        
        lib.VideoStreamInfo_setDisplayRatioHeight.argtypes = [c_void_p, c_int32]
        lib.VideoStreamInfo_setDisplayRatioHeight.restype = c_bool
        
        lib.VideoStreamInfo_frameRate.argtypes = [c_void_p]
        lib.VideoStreamInfo_frameRate.restype = c_double
        
        lib.VideoStreamInfo_setFrameRate.argtypes = [c_void_p, c_double]
        lib.VideoStreamInfo_setFrameRate.restype = c_bool
        
        lib.VideoStreamInfo_colorFormat.argtypes = [c_void_p]
        lib.VideoStreamInfo_colorFormat.restype = c_int32
        
        lib.VideoStreamInfo_setColorFormat.argtypes = [c_void_p, c_int32]
        lib.VideoStreamInfo_setColorFormat.restype = c_bool
        
        lib.VideoStreamInfo_scanType.argtypes = [c_void_p]
        lib.VideoStreamInfo_scanType.restype = c_int32
        
        lib.VideoStreamInfo_setScanType.argtypes = [c_void_p, c_int32]
        lib.VideoStreamInfo_setScanType.restype = c_bool
        
        lib.VideoStreamInfo_frameBottomUp.argtypes = [c_void_p]
        lib.VideoStreamInfo_frameBottomUp.restype = c_bool
        
        lib.VideoStreamInfo_setFrameBottomUp.argtypes = [c_void_p, c_bool]
        lib.VideoStreamInfo_setFrameBottomUp.restype = c_bool
        
        lib.VideoStreamInfo_clone.argtypes = [c_void_p]
        lib.VideoStreamInfo_clone.restype = c_void_p
        
        # VideoStreamInfo parameter methods
        lib.avb_create_video_stream_info_parameter.argtypes = []
        lib.avb_create_video_stream_info_parameter.restype = c_void_p
        
        lib.VideoStreamInfoParameter_videoStreamInfo.argtypes = [c_void_p]
        lib.VideoStreamInfoParameter_videoStreamInfo.restype = c_void_p
        
        lib.VideoStreamInfoParameter_setVideoStreamInfo.argtypes = [c_void_p, c_void_p]
        lib.VideoStreamInfoParameter_setVideoStreamInfo.restype = None
        
        # Parameter list creation and manipulation
        lib.avb_create_parameter_list.argtypes = []
        lib.avb_create_parameter_list.restype = c_void_p
        
        lib.ParameterList_count.argtypes = [c_void_p]
        lib.ParameterList_count.restype = c_int32
        
        lib.ParameterList_at.argtypes = [c_void_p, c_int32]
        lib.ParameterList_at.restype = c_void_p
        
        lib.ParameterList_add.argtypes = [c_void_p, c_void_p]
        lib.ParameterList_add.restype = c_bool
        
        # Parameter creation functions
        lib.avb_create_string_parameter.argtypes = []
        lib.avb_create_string_parameter.restype = c_void_p
        
        lib.avb_create_int_parameter.argtypes = []
        lib.avb_create_int_parameter.restype = c_void_p
        
        lib.avb_create_float_parameter.argtypes = []
        lib.avb_create_float_parameter.restype = c_void_p
        
        lib.avb_create_media_buffer_parameter.argtypes = []
        lib.avb_create_media_buffer_parameter.restype = c_void_p
        
        # Parameter methods
        lib.Parameter_name.argtypes = [c_void_p]
        lib.Parameter_name.restype = c_char_p
        lib.Parameter_setName.argtypes = [c_void_p, c_char_p]
        lib.Parameter_setName.restype = None
        
        lib.Parameter_type.argtypes = [c_void_p]
        lib.Parameter_type.restype = c_int32
        
        # MediaBufferParameter methods
        lib.MediaBufferParameter_buffer.argtypes = [c_void_p]
        lib.MediaBufferParameter_buffer.restype = c_void_p
        
        lib.MediaBufferParameter_setBuffer.argtypes = [c_void_p, c_void_p]
        lib.MediaBufferParameter_setBuffer.restype = None
        
        # String parameter methods
        lib.StringParameter_value.argtypes = [c_void_p]
        lib.StringParameter_value.restype = ctypes.c_void_p # C API returns char_t* (utf-16-le)
        
        lib.StringParameter_setValue.argtypes = [c_void_p, ctypes.c_void_p] # C API accepts char_t* (utf-16-le)
        lib.StringParameter_setValue.restype = None
        
        # Int parameter methods
        lib.IntParameter_value.argtypes = [c_void_p]
        lib.IntParameter_value.restype = ctypes.c_int64
        
        lib.IntParameter_setValue.argtypes = [c_void_p, ctypes.c_int64]
        lib.IntParameter_setValue.restype = None
        
        # Float parameter methods
        lib.FloatParameter_value.argtypes = [c_void_p]
        lib.FloatParameter_value.restype = c_double
        
        lib.FloatParameter_setValue.argtypes = [c_void_p, c_double]
        lib.FloatParameter_setValue.restype = None
        
        # MediaBuffer methods
        lib.avb_create_media_buffer.argtypes = [c_int32]
        lib.avb_create_media_buffer.restype = c_void_p
        
        lib.MediaBuffer_start.argtypes = [c_void_p]
        lib.MediaBuffer_start.restype = ctypes.POINTER(ctypes.c_uint8)
        
        lib.MediaBuffer_data.argtypes = [c_void_p]
        lib.MediaBuffer_data.restype = ctypes.POINTER(ctypes.c_uint8)
        
        lib.MediaBuffer_capacity.argtypes = [c_void_p]
        lib.MediaBuffer_capacity.restype = c_int32
        
        lib.MediaBuffer_dataSize.argtypes = [c_void_p]
        lib.MediaBuffer_dataSize.restype = c_int32
        
        lib.MediaBuffer_dataOffset.argtypes = [c_void_p]
        lib.MediaBuffer_dataOffset.restype = c_int32
        
        lib.MediaBuffer_setData.argtypes = [c_void_p, c_int32, c_int32]
        lib.MediaBuffer_setData.restype = c_bool
        
        lib.MediaBuffer_alloc.argtypes = [c_void_p, c_int32, c_bool]
        lib.MediaBuffer_alloc.restype = c_bool
        
        lib.MediaBuffer_free.argtypes = [c_void_p]
        lib.MediaBuffer_free.restype = None
        
        lib.MediaBuffer_attach.argtypes = [c_void_p, c_void_p, c_int32, c_bool]
        lib.MediaBuffer_attach.restype = c_bool
        
        lib.MediaBuffer_detach.argtypes = [c_void_p]
        lib.MediaBuffer_detach.restype = ctypes.POINTER(ctypes.c_uint8)
        
        lib.MediaBuffer_external.argtypes = [c_void_p]
        lib.MediaBuffer_external.restype = c_bool
        
        lib.MediaBuffer_clear.argtypes = [c_void_p]
        lib.MediaBuffer_clear.restype = None
        
        lib.MediaBuffer_append.argtypes = [c_void_p, c_void_p, c_int32]
        lib.MediaBuffer_append.restype = c_bool
        
        lib.MediaBuffer_remove.argtypes = [c_void_p, c_int32]
        lib.MediaBuffer_remove.restype = None
        
        lib.MediaBuffer_normalize.argtypes = [c_void_p]
        lib.MediaBuffer_normalize.restype = None
        
        lib.MediaBuffer_freeLinearSpace.argtypes = [c_void_p]
        lib.MediaBuffer_freeLinearSpace.restype = c_int32
        
        lib.MediaBuffer_freeSpace.argtypes = [c_void_p]
        lib.MediaBuffer_freeSpace.restype = c_int32
        
        lib.MediaBuffer_clone.argtypes = [c_void_p]
        lib.MediaBuffer_clone.restype = c_void_p
        
        # MediaPin methods
        lib.avb_create_media_pin.argtypes = []
        lib.avb_create_media_pin.restype = c_void_p
        
        lib.MediaPin_connection.argtypes = [c_void_p]
        lib.MediaPin_connection.restype = c_int32
        
        lib.MediaPin_setConnection.argtypes = [c_void_p, c_int32]
        lib.MediaPin_setConnection.restype = c_bool
        
        lib.MediaPin_streamInfo.argtypes = [c_void_p]
        lib.MediaPin_streamInfo.restype = c_void_p
        
        lib.MediaPin_setStreamInfo.argtypes = [c_void_p, c_void_p]
        lib.MediaPin_setStreamInfo.restype = c_bool
        
        lib.MediaPin_params.argtypes = [c_void_p]
        lib.MediaPin_params.restype = c_void_p
        
        lib.MediaPin_setParams.argtypes = [c_void_p, c_void_p]
        lib.MediaPin_setParams.restype = c_bool
        
        lib.MediaPin_clone.argtypes = [c_void_p]
        lib.MediaPin_clone.restype = c_void_p
        
        lib.MediaPin_immutable.argtypes = [c_void_p]
        lib.MediaPin_immutable.restype = c_bool
        
        # MediaSocket methods
        lib.avb_create_media_socket.argtypes = []
        lib.avb_create_media_socket.restype = c_void_p
        
        lib.MediaSocket_setFile.argtypes = [c_void_p, ctypes.c_void_p]
        lib.MediaSocket_setFile.restype = c_bool
        
        lib.MediaSocket_file.argtypes = [c_void_p]
        lib.MediaSocket_file.restype = ctypes.c_void_p
        
        lib.MediaSocket_setStreamCallback.argtypes = [c_void_p, c_void_p]
        lib.MediaSocket_setStreamCallback.restype = None
        
        lib.MediaSocket_streamCallback.argtypes = [c_void_p]
        lib.MediaSocket_streamCallback.restype = c_void_p
        
        lib.MediaSocket_setStreamType.argtypes = [c_void_p, c_int32]
        lib.MediaSocket_setStreamType.restype = c_bool
        
        lib.MediaSocket_streamType.argtypes = [c_void_p]
        lib.MediaSocket_streamType.restype = c_int32
        
        lib.MediaSocket_setStreamSubType.argtypes = [c_void_p, c_int32]
        lib.MediaSocket_setStreamSubType.restype = c_bool
        
        lib.MediaSocket_streamSubType.argtypes = [c_void_p]
        lib.MediaSocket_streamSubType.restype = c_int32
        
        lib.MediaSocket_setParams.argtypes = [c_void_p, c_void_p]
        lib.MediaSocket_setParams.restype = c_bool
        
        lib.MediaSocket_params.argtypes = [c_void_p]
        lib.MediaSocket_params.restype = c_void_p
        
        lib.MediaSocket_pins.argtypes = [c_void_p]
        lib.MediaSocket_pins.restype = c_void_p
        
        lib.MediaSocket_setMetadata.argtypes = [c_void_p, c_void_p]
        lib.MediaSocket_setMetadata.restype = c_bool
        
        lib.MediaSocket_metadata.argtypes = [c_void_p]
        lib.MediaSocket_metadata.restype = c_void_p
        
        lib.MediaSocket_setTimePosition.argtypes = [c_void_p, c_double]
        lib.MediaSocket_setTimePosition.restype = c_bool
        
        lib.MediaSocket_timePosition.argtypes = [c_void_p]
        lib.MediaSocket_timePosition.restype = c_double
        
        lib.MediaSocket_immutable.argtypes = [c_void_p]
        lib.MediaSocket_immutable.restype = c_bool
        
        # MediaSocketList methods
        lib.MediaSocketList_add.argtypes = [c_void_p, c_void_p]
        lib.MediaSocketList_add.restype = c_bool
        
        lib.MediaSocketList_remove.argtypes = [c_void_p, c_int32]
        lib.MediaSocketList_remove.restype = c_bool
        
        lib.MediaSocketList_clear.argtypes = [c_void_p]
        lib.MediaSocketList_clear.restype = c_bool
        
        lib.MediaSocketList_count.argtypes = [c_void_p]
        lib.MediaSocketList_count.restype = c_int32
        
        lib.MediaSocketList_at.argtypes = [c_void_p, c_int32]
        lib.MediaSocketList_at.restype = c_void_p
        
        lib.MediaSocketList_setAt.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MediaSocketList_setAt.restype = c_bool
        
        lib.MediaSocketList_insert.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MediaSocketList_insert.restype = c_bool
        
        lib.MediaSocketList_immutable.argtypes = [c_void_p]
        lib.MediaSocketList_immutable.restype = c_bool
        
        # MediaPinList methods
        lib.MediaPinList_add.argtypes = [c_void_p, c_void_p]
        lib.MediaPinList_add.restype = c_bool
        
        lib.MediaPinList_remove.argtypes = [c_void_p, c_int32]
        lib.MediaPinList_remove.restype = c_bool
        
        lib.MediaPinList_clear.argtypes = [c_void_p]
        lib.MediaPinList_clear.restype = c_bool
        
        lib.MediaPinList_count.argtypes = [c_void_p]
        lib.MediaPinList_count.restype = c_int32
        
        lib.MediaPinList_at.argtypes = [c_void_p, c_int32]
        lib.MediaPinList_at.restype = c_void_p
        
        lib.MediaPinList_setAt.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MediaPinList_setAt.restype = c_bool
        
        lib.MediaPinList_insert.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MediaPinList_insert.restype = c_bool
        
        lib.MediaPinList_immutable.argtypes = [c_void_p]
        lib.MediaPinList_immutable.restype = c_bool
        
        # MediaSocket preset creation
        lib.avb_create_media_socket_from_preset.argtypes = [c_char_p]
        lib.avb_create_media_socket_from_preset.restype = c_void_p

        # MetaPicture methods
        lib.avb_create_meta_picture.argtypes = []
        lib.avb_create_meta_picture.restype = c_void_p
        
        lib.MetaPicture_mimeType.argtypes = [c_void_p]
        lib.MetaPicture_mimeType.restype = c_char_p
        
        lib.MetaPicture_setMimeType.argtypes = [c_void_p, c_char_p]
        lib.MetaPicture_setMimeType.restype = c_bool
        
        lib.MetaPicture_description.argtypes = [c_void_p]
        lib.MetaPicture_description.restype = ctypes.c_void_p  # char_t* (utf-16-le)
        
        lib.MetaPicture_setDescription.argtypes = [c_void_p, ctypes.c_void_p]  # char_t* (utf-16-le)
        lib.MetaPicture_setDescription.restype = c_bool
        
        lib.MetaPicture_pictureType.argtypes = [c_void_p]
        lib.MetaPicture_pictureType.restype = c_int32
        
        lib.MetaPicture_setPictureType.argtypes = [c_void_p, c_int32]
        lib.MetaPicture_setPictureType.restype = c_bool
        
        lib.MetaPicture_data.argtypes = [c_void_p]
        lib.MetaPicture_data.restype = ctypes.POINTER(ctypes.c_uint8)
        
        lib.MetaPicture_dataSize.argtypes = [c_void_p]
        lib.MetaPicture_dataSize.restype = c_int32
        
        lib.MetaPicture_setData.argtypes = [c_void_p, c_void_p, c_int32]
        lib.MetaPicture_setData.restype = c_bool
        
        lib.MetaPicture_immutable.argtypes = [c_void_p]
        lib.MetaPicture_immutable.restype = c_bool
        
        # MetaPictureList methods
        lib.MetaPictureList_add.argtypes = [c_void_p, c_void_p]
        lib.MetaPictureList_add.restype = c_bool
        
        lib.MetaPictureList_remove.argtypes = [c_void_p, c_int32]
        lib.MetaPictureList_remove.restype = c_bool
        
        lib.MetaPictureList_clear.argtypes = [c_void_p]
        lib.MetaPictureList_clear.restype = c_bool
        
        lib.MetaPictureList_count.argtypes = [c_void_p]
        lib.MetaPictureList_count.restype = c_int32
        
        lib.MetaPictureList_at.argtypes = [c_void_p, c_int32]
        lib.MetaPictureList_at.restype = c_void_p
        
        lib.MetaPictureList_setAt.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MetaPictureList_setAt.restype = c_bool
        
        lib.MetaPictureList_insert.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MetaPictureList_insert.restype = c_bool
        
        lib.MetaPictureList_immutable.argtypes = [c_void_p]
        lib.MetaPictureList_immutable.restype = c_bool
        
        # MetaAttribute methods
        lib.avb_create_meta_attribute.argtypes = []
        lib.avb_create_meta_attribute.restype = c_void_p
        
        lib.MetaAttribute_name.argtypes = [c_void_p]
        lib.MetaAttribute_name.restype = c_char_p
        
        lib.MetaAttribute_setName.argtypes = [c_void_p, c_char_p]
        lib.MetaAttribute_setName.restype = c_bool
        
        lib.MetaAttribute_value.argtypes = [c_void_p]
        lib.MetaAttribute_value.restype = ctypes.c_void_p  # char_t* (utf-16-le)
        
        lib.MetaAttribute_setValue.argtypes = [c_void_p, ctypes.c_void_p]  # char_t* (utf-16-le)
        lib.MetaAttribute_setValue.restype = c_bool
        
        lib.MetaAttribute_immutable.argtypes = [c_void_p]
        lib.MetaAttribute_immutable.restype = c_bool
        
        # MetaAttributeList methods
        lib.MetaAttributeList_add.argtypes = [c_void_p, c_void_p]
        lib.MetaAttributeList_add.restype = c_bool
        
        lib.MetaAttributeList_remove.argtypes = [c_void_p, c_int32]
        lib.MetaAttributeList_remove.restype = c_bool
        
        lib.MetaAttributeList_clear.argtypes = [c_void_p]
        lib.MetaAttributeList_clear.restype = c_bool
        
        lib.MetaAttributeList_count.argtypes = [c_void_p]
        lib.MetaAttributeList_count.restype = c_int32
        
        lib.MetaAttributeList_at.argtypes = [c_void_p, c_int32]
        lib.MetaAttributeList_at.restype = c_void_p
        
        lib.MetaAttributeList_setAt.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MetaAttributeList_setAt.restype = c_bool
        
        lib.MetaAttributeList_insert.argtypes = [c_void_p, c_int32, c_void_p]
        lib.MetaAttributeList_insert.restype = c_bool
        
        lib.MetaAttributeList_itemByName.argtypes = [c_void_p, c_char_p]
        lib.MetaAttributeList_itemByName.restype = c_void_p
        
        lib.MetaAttributeList_immutable.argtypes = [c_void_p]
        lib.MetaAttributeList_immutable.restype = c_bool
        
        # Metadata methods
        lib.avb_create_metadata.argtypes = []
        lib.avb_create_metadata.restype = c_void_p
        
        lib.Metadata_attributes.argtypes = [c_void_p]
        lib.Metadata_attributes.restype = c_void_p
        
        lib.Metadata_pictures.argtypes = [c_void_p]
        lib.Metadata_pictures.restype = c_void_p
        
        lib.Metadata_immutable.argtypes = [c_void_p]
        lib.Metadata_immutable.restype = c_bool
        
        # MediaSample methods
        lib.avb_create_media_sample.argtypes = []
        lib.avb_create_media_sample.restype = c_void_p
        
        lib.MediaSample_buffer.argtypes = [c_void_p]
        lib.MediaSample_buffer.restype = c_void_p
        
        lib.MediaSample_setBuffer.argtypes = [c_void_p, c_void_p]
        lib.MediaSample_setBuffer.restype = None
        
        lib.MediaSample_startTime.argtypes = [c_void_p]
        lib.MediaSample_startTime.restype = c_double
        
        lib.MediaSample_setStartTime.argtypes = [c_void_p, c_double]
        lib.MediaSample_setStartTime.restype = None
        
        lib.MediaSample_endTime.argtypes = [c_void_p]
        lib.MediaSample_endTime.restype = c_double
        
        lib.MediaSample_setEndTime.argtypes = [c_void_p, c_double]
        lib.MediaSample_setEndTime.restype = None
        
        lib.MediaSample_flags.argtypes = [c_void_p]
        lib.MediaSample_flags.restype = c_int32
        
        lib.MediaSample_setFlags.argtypes = [c_void_p, c_int32]
        lib.MediaSample_setFlags.restype = None
        
        lib.MediaSample_pictureType.argtypes = [c_void_p]
        lib.MediaSample_pictureType.restype = c_int32
        
        lib.MediaSample_setPictureType.argtypes = [c_void_p, c_int32]
        lib.MediaSample_setPictureType.restype = None
        
        lib.MediaSample_frameType.argtypes = [c_void_p]
        lib.MediaSample_frameType.restype = c_int32
        
        lib.MediaSample_setFrameType.argtypes = [c_void_p, c_int32]
        lib.MediaSample_setFrameType.restype = None
        
        lib.MediaSample_reset.argtypes = [c_void_p]
        lib.MediaSample_reset.restype = None
        
        lib.MediaSample_videoBufferSizeInBytes.argtypes = [c_void_p, c_int32, c_int32, c_int32]
        lib.MediaSample_videoBufferSizeInBytes.restype = c_int32
        
        # Transcoder methods
        lib.avb_create_transcoder.argtypes = []
        lib.avb_create_transcoder.restype = c_void_p
        
        lib.Transcoder_inputs.argtypes = [c_void_p]
        lib.Transcoder_inputs.restype = c_void_p
        
        lib.Transcoder_outputs.argtypes = [c_void_p]
        lib.Transcoder_outputs.restype = c_void_p
        
        lib.Transcoder_autoConnect.argtypes = [c_void_p]
        lib.Transcoder_autoConnect.restype = c_bool
        
        lib.Transcoder_setAutoConnect.argtypes = [c_void_p, c_bool]
        lib.Transcoder_setAutoConnect.restype = None
        
        lib.Transcoder_allowDemoMode.argtypes = [c_void_p]
        lib.Transcoder_allowDemoMode.restype = c_bool
        
        lib.Transcoder_setAllowDemoMode.argtypes = [c_void_p, c_bool]
        lib.Transcoder_setAllowDemoMode.restype = None
        
        lib.Transcoder_error.argtypes = [c_void_p]
        lib.Transcoder_error.restype = c_void_p
        
        lib.Transcoder_open.argtypes = [c_void_p]
        lib.Transcoder_open.restype = c_bool
        
        lib.Transcoder_run.argtypes = [c_void_p]
        lib.Transcoder_run.restype = c_bool
        
        lib.Transcoder_push.argtypes = [c_void_p, c_int32, c_void_p]
        lib.Transcoder_push.restype = c_bool
        
        lib.Transcoder_pull.argtypes = [c_void_p, ctypes.POINTER(c_int32), c_void_p]
        lib.Transcoder_pull.restype = c_bool
        
        lib.Transcoder_close.argtypes = [c_void_p]
        lib.Transcoder_close.restype = None
        
        lib.Transcoder_flush.argtypes = [c_void_p]
        lib.Transcoder_flush.restype = c_bool
        
        lib.Transcoder_endOfStream.argtypes = [c_void_p, c_int32]
        lib.Transcoder_endOfStream.restype = c_bool
        
        # Transcoder callback types
        TranscoderProgressCallback = ctypes.CFUNCTYPE(None, c_double, c_double, c_void_p)
        TranscoderContinueCallback = ctypes.CFUNCTYPE(c_bool, c_double, c_void_p)
        TranscoderStatusCallback = ctypes.CFUNCTYPE(None, c_int32, c_void_p)
        TranscoderInputChangeCallback = ctypes.CFUNCTYPE(None, c_int32, c_void_p)
        
        lib.Transcoder_setProgressCallback.argtypes = [c_void_p, TranscoderProgressCallback, c_void_p]
        lib.Transcoder_setProgressCallback.restype = None
        
        lib.Transcoder_setContinueCallback.argtypes = [c_void_p, TranscoderContinueCallback, c_void_p]
        lib.Transcoder_setContinueCallback.restype = None
        
        lib.Transcoder_setStatusCallback.argtypes = [c_void_p, TranscoderStatusCallback, c_void_p]
        lib.Transcoder_setStatusCallback.restype = None
        
        lib.Transcoder_setInputChangeCallback.argtypes = [c_void_p, TranscoderInputChangeCallback, c_void_p]
        lib.Transcoder_setInputChangeCallback.restype = None
    
    @property
    def lib(self):
        """Get the ctypes library object."""
        return self._lib


class _NativeSingleton:
    """Singleton holder for the native library instance."""
    _instance: Optional[NativeLibrary] = None

    @classmethod
    def get(cls) -> NativeLibrary:
        if cls._instance is None:
            cls._instance = NativeLibrary()
        return cls._instance

def get_native() -> NativeLibrary:
    """Get the singleton native library instance."""
    return _NativeSingleton.get()
