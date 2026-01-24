import pytest
from avblocks import Library, StreamInfo, MediaBuffer
from avblocks.audio_stream_info import AudioStreamInfo
from avblocks.video_stream_info import VideoStreamInfo
from avblocks.data_stream_info import DataStreamInfo
from avblocks.constants import MediaType, StreamType, StreamSubType, BitrateMode


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if Library.initialize():
        yield
        Library.shutdown()
    else:
        pytest.skip("Failed to initialize AVBlocks library")


def assert_default(si: StreamInfo):
    """Assert that StreamInfo has default values."""
    assert si.duration == 0.0
    assert si.id == 0
    assert si.stream_type == StreamType.Unknown
    assert si.stream_sub_type == StreamSubType.Unknown
    assert si.bitrate == 0
    assert si.bitrate_mode == BitrateMode.Unknown
    assert si.program_number == 0
    assert si.config_data is None


def test_stream_info_media_type(initialized_library):
    """Test media_type property for different stream types."""
    asi = AudioStreamInfo()
    assert asi.media_type == MediaType.Audio
    
    vsi = VideoStreamInfo()
    assert vsi.media_type == MediaType.Video
    
    dsi = DataStreamInfo()
    assert dsi.media_type == MediaType.Data


def test_stream_info_set_properties(initialized_library):
    """Test setting StreamInfo properties."""
    si = AudioStreamInfo()
    
    si.duration = 120.5
    si.id = 42
    si.stream_type = StreamType.MPEG_Audio
    si.stream_sub_type = StreamSubType.MPEG_Audio_Layer3
    si.bitrate = 128000
    si.bitrate_mode = BitrateMode.CBR
    si.program_number = 1
    
    assert si.duration == 120.5
    assert si.id == 42
    assert si.stream_type == StreamType.MPEG_Audio
    assert si.stream_sub_type == StreamSubType.MPEG_Audio_Layer3
    assert si.bitrate == 128000
    assert si.bitrate_mode == BitrateMode.CBR
    assert si.program_number == 1


def test_stream_info_config_data_set_and_get(initialized_library):
    """Test config_data property set and get."""
    si = AudioStreamInfo()
    
    test_data = bytes([0x00, 0x01, 0x02, 0x03, 0x04])
    buffer = MediaBuffer(test_data)
    
    si.config_data = buffer
    
    assert si.config_data is not None
    assert si.config_data.data_size == 5


def test_stream_info_config_data_set_none(initialized_library):
    """Test setting config_data to None."""
    si = AudioStreamInfo()
    
    test_data = bytes([0x00, 0x01, 0x02])
    si.config_data = MediaBuffer(test_data)
    assert si.config_data is not None
    
    si.config_data = None
    assert si.config_data is None


def test_stream_info_clone_without_config_data(initialized_library):
    """Test cloning StreamInfo without config_data."""
    si = AudioStreamInfo()
    si.duration = 60.0
    si.id = 10
    si.stream_type = StreamType.AAC
    si.stream_sub_type = StreamSubType.AAC_MP4
    
    cloned = si.clone()
    
    assert cloned.duration == si.duration
    assert cloned.id == si.id
    assert cloned.stream_type == si.stream_type
    assert cloned.stream_sub_type == si.stream_sub_type
    assert cloned.media_type == si.media_type
    assert cloned.config_data is None


def test_stream_info_clone_with_config_data(initialized_library):
    """Test cloning StreamInfo with config_data."""
    si = AudioStreamInfo()
    si.duration = 60.0
    si.id = 10
    
    test_data = bytes([0xDE, 0xAD, 0xBE, 0xEF])
    si.config_data = MediaBuffer(test_data)
    
    cloned = si.clone()
    
    assert cloned.config_data is not None
    assert cloned.config_data.data_size == len(test_data)
    
    # Verify it's a deep copy - original and clone should be different objects
    assert si.config_data is not cloned.config_data


def test_stream_info_reset(initialized_library):
    """Test reset method."""
    si = AudioStreamInfo()
    si.duration = 120.5
    si.id = 42
    si.stream_type = StreamType.MPEG_Audio
    si.stream_sub_type = StreamSubType.MPEG_Audio_Layer3
    si.bitrate = 128000
    si.bitrate_mode = BitrateMode.CBR
    si.program_number = 1
    si.config_data = MediaBuffer(bytes([0x01, 0x02]))
    
    si.reset()
    
    assert si.duration == 0.0
    assert si.id == 0
    assert si.stream_type == StreamType.Unknown
    assert si.stream_sub_type == StreamSubType.Unknown
    assert si.bitrate == 0
    assert si.bitrate_mode == BitrateMode.Unknown
    assert si.program_number == 0
    assert si.config_data is None


def test_stream_info_immutable_throws_on_modify(initialized_library):
    """Test that immutable StreamInfo raises on modification."""
    si = AudioStreamInfo()
    si.immutable = True
    
    with pytest.raises(RuntimeError):
        si.duration = 10.0
    with pytest.raises(RuntimeError):
        si.id = 1
    with pytest.raises(RuntimeError):
        si.stream_type = StreamType.AAC
    with pytest.raises(RuntimeError):
        si.stream_sub_type = StreamSubType.AAC_MP4
    with pytest.raises(RuntimeError):
        si.bitrate = 128000
    with pytest.raises(RuntimeError):
        si.bitrate_mode = BitrateMode.CBR
    with pytest.raises(RuntimeError):
        si.program_number = 1
    with pytest.raises(RuntimeError):
        si.config_data = MediaBuffer()
    with pytest.raises(RuntimeError):
        si.reset()


def test_stream_info_clone_is_mutable(initialized_library):
    """Test that cloned StreamInfo is mutable."""
    si = AudioStreamInfo()
    si.immutable = True
    
    cloned = si.clone()
    
    assert cloned.immutable == False
    # Should not raise
    cloned.duration = 10.0
    cloned.id = 1


def test_data_stream_info_default(initialized_library):
    """Test DataStreamInfo default values."""
    si = DataStreamInfo()
    assert_default(si)
    assert si.media_type == MediaType.Data


def test_stream_info_stream_type(initialized_library):
    """Test stream_type property."""
    asi = AudioStreamInfo()
    asi.stream_type = StreamType.AAC
    assert asi.stream_type == StreamType.AAC
    
    vsi = VideoStreamInfo()
    vsi.stream_type = StreamType.H264
    assert vsi.stream_type == StreamType.H264


def test_stream_info_stream_sub_type(initialized_library):
    """Test stream_sub_type property."""
    asi = AudioStreamInfo()
    asi.stream_sub_type = StreamSubType.AAC_ADTS
    assert asi.stream_sub_type == StreamSubType.AAC_ADTS
    
    vsi = VideoStreamInfo()
    vsi.stream_sub_type = StreamSubType.AVC_Annex_B
    assert vsi.stream_sub_type == StreamSubType.AVC_Annex_B


def test_stream_info_duration(initialized_library):
    """Test duration property."""
    asi = AudioStreamInfo()
    asi.duration = 10.5
    assert asi.duration == 10.5
    
    vsi = VideoStreamInfo()
    vsi.duration = 120.75
    assert vsi.duration == 120.75


def test_stream_info_id(initialized_library):
    """Test id property."""
    asi = AudioStreamInfo()
    asi.id = 1
    assert asi.id == 1
    
    vsi = VideoStreamInfo()
    vsi.id = 2
    assert vsi.id == 2


def test_stream_info_program_number(initialized_library):
    """Test program_number property."""
    asi = AudioStreamInfo()
    asi.program_number = 100
    assert asi.program_number == 100
    
    vsi = VideoStreamInfo()
    vsi.program_number = 200
    assert vsi.program_number == 200


def test_stream_info_bitrate(initialized_library):
    """Test bitrate property."""
    asi = AudioStreamInfo()
    asi.bitrate = 128000
    assert asi.bitrate == 128000
    
    vsi = VideoStreamInfo()
    vsi.bitrate = 5000000
    assert vsi.bitrate == 5000000


def test_stream_info_bitrate_mode(initialized_library):
    """Test bitrate_mode property."""
    asi = AudioStreamInfo()
    asi.bitrate_mode = BitrateMode.CBR
    assert asi.bitrate_mode == BitrateMode.CBR
    
    vsi = VideoStreamInfo()
    vsi.bitrate_mode = BitrateMode.VBR
    assert vsi.bitrate_mode == BitrateMode.VBR
    
    dsi = DataStreamInfo()
    dsi.bitrate_mode = BitrateMode.ABR
    assert dsi.bitrate_mode == BitrateMode.ABR


def test_stream_info_immutable(initialized_library):
    """Test immutable property."""
    asi = AudioStreamInfo()
    # New objects should not be immutable
    assert asi.immutable == False
    
    vsi = VideoStreamInfo()
    assert vsi.immutable == False
