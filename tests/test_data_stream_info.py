import pytest
from avblocks import Library
from avblocks.data_stream_info import DataStreamInfo
from avblocks.constants import MediaType, StreamType, BitrateMode


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if Library.initialize():
        yield
        Library.shutdown()
    else:
        pytest.skip("Failed to initialize AVBlocks library")


def test_data_stream_info_creation(initialized_library):
    """Test creating a DataStreamInfo object."""
    dsi = DataStreamInfo()
    assert dsi is not None
    assert dsi.media_type == MediaType.Data


def test_data_stream_info_media_type_immutable(initialized_library):
    """Test that media type for DataStreamInfo is always Data."""
    dsi = DataStreamInfo()
    assert dsi.media_type == MediaType.Data
    # Media type should always be Data for DataStreamInfo


def test_data_stream_info_inherited_properties(initialized_library):
    """Test that DataStreamInfo properly inherits base StreamInfo properties."""
    dsi = DataStreamInfo()
    
    # Test stream type
    dsi.stream_type = StreamType.Teletext
    assert dsi.stream_type == StreamType.Teletext
    
    # Test bitrate
    dsi.bitrate = 1000000
    assert dsi.bitrate == 1000000
    
    # Test bitrate mode
    dsi.bitrate_mode = BitrateMode.CBR
    assert dsi.bitrate_mode == BitrateMode.CBR
    
    # Test duration
    dsi.duration = 30.0
    assert dsi.duration == 30.0
    
    # Test id
    dsi.id = 3
    assert dsi.id == 3
    
    # Test program number
    dsi.program_number = 300
    assert dsi.program_number == 300


def test_data_stream_info_clone(initialized_library):
    """Test cloning DataStreamInfo."""
    dsi = DataStreamInfo()
    dsi.stream_type = StreamType.Teletext
    dsi.bitrate = 1000000
    dsi.bitrate_mode = BitrateMode.CBR
    dsi.duration = 15.0
    dsi.id = 5
    
    cloned = dsi.clone()
    assert cloned is not None
    assert isinstance(cloned, DataStreamInfo)
    assert cloned.media_type == MediaType.Data
    assert cloned.stream_type == dsi.stream_type
    assert cloned.bitrate == dsi.bitrate
    assert cloned.bitrate_mode == dsi.bitrate_mode
    assert cloned.duration == dsi.duration
    assert cloned.id == dsi.id


def test_data_stream_info_clone_independence(initialized_library):
    """Test that cloned DataStreamInfo is independent from original."""
    dsi = DataStreamInfo()
    dsi.stream_type = StreamType.Teletext
    dsi.bitrate = 1000000
    
    cloned = dsi.clone()
    
    # Modify original
    dsi.stream_type = StreamType.MPEG_PSI_PACKETS
    dsi.bitrate = 2000000
    
    # Cloned should remain unchanged
    assert cloned.stream_type == StreamType.Teletext
    assert cloned.bitrate == 1000000


def test_data_stream_info_reset(initialized_library):
    """Test reset method for DataStreamInfo."""
    dsi = DataStreamInfo()
    dsi.stream_type = StreamType.Teletext
    dsi.bitrate = 1000000
    dsi.duration = 20.0
    
    dsi.reset()
    
    # After reset, values should return to defaults
    assert dsi.media_type == MediaType.Data  # Should remain Data
    assert dsi.stream_type == StreamType.Unknown
    assert dsi.bitrate == 0
    assert dsi.duration == 0.0


def test_data_stream_info_immutable_property(initialized_library):
    """Test immutable property for DataStreamInfo."""
    dsi = DataStreamInfo()
    # New objects should not be immutable
    assert dsi.immutable == False
