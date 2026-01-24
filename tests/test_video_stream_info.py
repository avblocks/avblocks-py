import pytest
from avblocks import Library
from avblocks.video_stream_info import VideoStreamInfo
from avblocks.constants import MediaType, StreamType, BitrateMode, ColorFormat, ScanType


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if Library.initialize():
        yield
        Library.shutdown()
    else:
        pytest.skip("Failed to initialize AVBlocks library")


def test_video_stream_info_creation(initialized_library):
    """Test creating a VideoStreamInfo object."""
    vsi = VideoStreamInfo()
    assert vsi is not None
    assert vsi.media_type == MediaType.Video


def test_video_stream_info_frame_width(initialized_library):
    """Test frame_width property."""
    vsi = VideoStreamInfo()
    
    # Test common resolutions
    vsi.frame_width = 1920
    assert vsi.frame_width == 1920
    
    vsi.frame_width = 1280
    assert vsi.frame_width == 1280
    
    vsi.frame_width = 640
    assert vsi.frame_width == 640


def test_video_stream_info_frame_height(initialized_library):
    """Test frame_height property."""
    vsi = VideoStreamInfo()
    
    # Test common resolutions
    vsi.frame_height = 1080
    assert vsi.frame_height == 1080
    
    vsi.frame_height = 720
    assert vsi.frame_height == 720
    
    vsi.frame_height = 480
    assert vsi.frame_height == 480


def test_video_stream_info_display_ratio_width(initialized_library):
    """Test display_ratio_width property."""
    vsi = VideoStreamInfo()
    
    # Test 16:9 aspect ratio
    vsi.display_ratio_width = 16
    assert vsi.display_ratio_width == 16
    
    # Test 4:3 aspect ratio
    vsi.display_ratio_width = 4
    assert vsi.display_ratio_width == 4


def test_video_stream_info_display_ratio_height(initialized_library):
    """Test display_ratio_height property."""
    vsi = VideoStreamInfo()
    
    # Test 16:9 aspect ratio
    vsi.display_ratio_height = 9
    assert vsi.display_ratio_height == 9
    
    # Test 4:3 aspect ratio
    vsi.display_ratio_height = 3
    assert vsi.display_ratio_height == 3


def test_video_stream_info_frame_rate(initialized_library):
    """Test frame_rate property."""
    vsi = VideoStreamInfo()
    
    # Test common frame rates
    vsi.frame_rate = 29.97
    assert abs(vsi.frame_rate - 29.97) < 0.01
    
    vsi.frame_rate = 30.0
    assert abs(vsi.frame_rate - 30.0) < 0.01
    
    vsi.frame_rate = 23.976
    assert abs(vsi.frame_rate - 23.976) < 0.01
    
    vsi.frame_rate = 25.0
    assert abs(vsi.frame_rate - 25.0) < 0.01
    
    vsi.frame_rate = 60.0
    assert abs(vsi.frame_rate - 60.0) < 0.01


def test_video_stream_info_color_format(initialized_library):
    """Test color_format property."""
    vsi = VideoStreamInfo()
    
    # Test common color formats
    vsi.color_format = ColorFormat.YUV420
    assert vsi.color_format == ColorFormat.YUV420
    
    vsi.color_format = ColorFormat.YV12
    assert vsi.color_format == ColorFormat.YV12
    
    vsi.color_format = ColorFormat.NV12
    assert vsi.color_format == ColorFormat.NV12
    
    vsi.color_format = ColorFormat.BGR24
    assert vsi.color_format == ColorFormat.BGR24


def test_video_stream_info_scan_type(initialized_library):
    """Test scan_type property."""
    vsi = VideoStreamInfo()
    
    # Test scan types
    vsi.scan_type = ScanType.Progressive
    assert vsi.scan_type == ScanType.Progressive
    
    vsi.scan_type = ScanType.TopFieldFirst
    assert vsi.scan_type == ScanType.TopFieldFirst
    
    vsi.scan_type = ScanType.BottomFieldFirst
    assert vsi.scan_type == ScanType.BottomFieldFirst


def test_video_stream_info_frame_bottom_up(initialized_library):
    """Test frame_bottom_up property."""
    vsi = VideoStreamInfo()
    
    vsi.frame_bottom_up = True
    assert vsi.frame_bottom_up == True
    
    vsi.frame_bottom_up = False
    assert vsi.frame_bottom_up == False


def test_video_stream_info_inherited_properties(initialized_library):
    """Test that VideoStreamInfo properly inherits base StreamInfo properties."""
    vsi = VideoStreamInfo()
    
    # Test stream type
    vsi.stream_type = StreamType.H264
    assert vsi.stream_type == StreamType.H264
    
    # Test bitrate
    vsi.bitrate = 5000000
    assert vsi.bitrate == 5000000
    
    # Test bitrate mode
    vsi.bitrate_mode = BitrateMode.VBR
    assert vsi.bitrate_mode == BitrateMode.VBR
    
    # Test duration
    vsi.duration = 120.5
    assert vsi.duration == 120.5
    
    # Test id
    vsi.id = 2
    assert vsi.id == 2
    
    # Test program number
    vsi.program_number = 200
    assert vsi.program_number == 200


def test_video_stream_info_clone(initialized_library):
    """Test cloning VideoStreamInfo."""
    vsi = VideoStreamInfo()
    vsi.frame_width = 1280
    vsi.frame_height = 720
    vsi.frame_rate = 30.0
    vsi.color_format = ColorFormat.YUV420
    vsi.scan_type = ScanType.Progressive
    vsi.frame_bottom_up = False
    vsi.stream_type = StreamType.H264
    vsi.bitrate = 2500000
    vsi.duration = 60.0
    
    cloned = vsi.clone()
    assert cloned is not None
    assert isinstance(cloned, VideoStreamInfo)
    assert cloned.frame_width == vsi.frame_width
    assert cloned.frame_height == vsi.frame_height
    assert cloned.frame_rate == vsi.frame_rate
    assert cloned.color_format == vsi.color_format
    assert cloned.scan_type == vsi.scan_type
    assert cloned.frame_bottom_up == vsi.frame_bottom_up
    assert cloned.stream_type == vsi.stream_type
    assert cloned.bitrate == vsi.bitrate
    assert cloned.duration == vsi.duration


def test_video_stream_info_clone_independence(initialized_library):
    """Test that cloned VideoStreamInfo is independent from original."""
    vsi = VideoStreamInfo()
    vsi.frame_width = 1920
    vsi.frame_height = 1080
    vsi.frame_rate = 30.0
    
    cloned = vsi.clone()
    
    # Modify original
    vsi.frame_width = 1280
    vsi.frame_height = 720
    vsi.frame_rate = 25.0
    
    # Cloned should remain unchanged
    assert cloned.frame_width == 1920
    assert cloned.frame_height == 1080
    assert abs(cloned.frame_rate - 30.0) < 0.01


def test_video_stream_info_reset(initialized_library):
    """Test reset method for VideoStreamInfo."""
    vsi = VideoStreamInfo()
    vsi.frame_width = 1920
    vsi.frame_height = 1080
    vsi.frame_rate = 30.0
    vsi.stream_type = StreamType.H264
    vsi.bitrate = 5000000
    
    vsi.reset()
    
    # After reset, values should return to defaults
    assert vsi.frame_width == 0
    assert vsi.frame_height == 0
    assert vsi.frame_rate == 0.0
    assert vsi.stream_type == StreamType.Unknown
    assert vsi.bitrate == 0
