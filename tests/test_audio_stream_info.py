import pytest
from avblocks import Library
from avblocks.audio_stream_info import AudioStreamInfo
from avblocks.constants import MediaType, StreamType, BitrateMode, PcmFlags
from avblocks.native import get_native


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if not Library.initialize():
        pytest.skip("Failed to initialize AVBlocks library")
    yield
    Library.shutdown()


def test_library_is_initialized(initialized_library):
    """Verify that the library is properly initialized before running tests."""
    native = get_native()
    assert native is not None
    assert native.lib is not None


def test_audio_stream_info_creation(initialized_library):
    """Test creating an AudioStreamInfo object."""
    try:
        # First check if we can call the native function directly
        native = get_native()
        handle = native.lib.avb_create_audio_stream_info()
        assert handle is not None, "Native function returned NULL"
        assert handle != 0, "Native function returned NULL (0)"
        
        # Now try through the Python wrapper
        asi = AudioStreamInfo()
        assert asi is not None
        
        # Try to get media type
        mt = asi.media_type
        assert mt == MediaType.Audio
    except Exception as e:
        pytest.fail(f"Failed to create AudioStreamInfo: {e}")


def test_audio_stream_info_pcm_flags(initialized_library):
    """Test pcm_flags property."""
    asi = AudioStreamInfo()
    asi.pcm_flags = PcmFlags.Unsigned
    assert asi.pcm_flags == PcmFlags.Unsigned


def test_audio_stream_info_channels(initialized_library):
    """Test channels property."""
    asi = AudioStreamInfo()
    
    # Test mono
    asi.channels = 1
    assert asi.channels == 1
    
    # Test stereo
    asi.channels = 2
    assert asi.channels == 2
    
    # Test 5.1
    asi.channels = 6
    assert asi.channels == 6


def test_audio_stream_info_channel_layout(initialized_library):
    """Test channel_layout property."""
    asi = AudioStreamInfo()
    asi.channel_layout = 0x03  # Left | Right (Stereo)
    assert asi.channel_layout == 0x03


def test_audio_stream_info_sample_rate(initialized_library):
    """Test sample_rate property."""
    asi = AudioStreamInfo()
    
    # Test common sample rates
    asi.sample_rate = 44100
    assert asi.sample_rate == 44100
    
    asi.sample_rate = 48000
    assert asi.sample_rate == 48000
    
    asi.sample_rate = 96000
    assert asi.sample_rate == 96000


def test_audio_stream_info_bits_per_sample(initialized_library):
    """Test bits_per_sample property."""
    asi = AudioStreamInfo()
    
    # Test common bit depths
    asi.bits_per_sample = 16
    assert asi.bits_per_sample == 16
    
    asi.bits_per_sample = 24
    assert asi.bits_per_sample == 24
    
    asi.bits_per_sample = 32
    assert asi.bits_per_sample == 32


def test_audio_stream_info_bytes_per_frame(initialized_library):
    """Test bytes_per_frame property."""
    asi = AudioStreamInfo()
    
    # For stereo 16-bit: 2 channels * 2 bytes = 4 bytes per frame
    asi.bytes_per_frame = 4
    assert asi.bytes_per_frame == 4
    
    # For stereo 24-bit: 2 channels * 3 bytes = 6 bytes per frame
    asi.bytes_per_frame = 6
    assert asi.bytes_per_frame == 6


def test_audio_stream_info_inherited_properties(initialized_library):
    """Test that AudioStreamInfo properly inherits base StreamInfo properties."""
    asi = AudioStreamInfo()
    
    # Test stream type
    asi.stream_type = StreamType.AAC
    assert asi.stream_type == StreamType.AAC
    
    # Test bitrate
    asi.bitrate = 128000
    assert asi.bitrate == 128000
    
    # Test bitrate mode
    asi.bitrate_mode = BitrateMode.CBR
    assert asi.bitrate_mode == BitrateMode.CBR
    
    # Test duration
    asi.duration = 10.5
    assert asi.duration == 10.5
    
    # Test id
    asi.id = 1
    assert asi.id == 1
    
    # Test program number
    asi.program_number = 100
    assert asi.program_number == 100


def test_audio_stream_info_clone(initialized_library):
    """Test cloning AudioStreamInfo."""
    asi = AudioStreamInfo()
    asi.channels = 2
    asi.sample_rate = 44100
    asi.bits_per_sample = 16
    asi.bytes_per_frame = 4
    asi.stream_type = StreamType.AAC
    asi.bitrate = 128000
    asi.duration = 5.0
    
    cloned = asi.clone()
    assert cloned is not None
    assert isinstance(cloned, AudioStreamInfo)
    assert cloned.channels == asi.channels
    assert cloned.sample_rate == asi.sample_rate
    assert cloned.bits_per_sample == asi.bits_per_sample
    assert cloned.bytes_per_frame == asi.bytes_per_frame
    assert cloned.stream_type == asi.stream_type
    assert cloned.bitrate == asi.bitrate
    assert cloned.duration == asi.duration


def test_audio_stream_info_clone_independence(initialized_library):
    """Test that cloned AudioStreamInfo is independent from original."""
    asi = AudioStreamInfo()
    asi.channels = 2
    asi.sample_rate = 44100
    
    cloned = asi.clone()
    
    # Modify original
    asi.channels = 6
    asi.sample_rate = 48000
    
    # Cloned should remain unchanged
    assert cloned.channels == 2
    assert cloned.sample_rate == 44100


def test_audio_stream_info_reset(initialized_library):
    """Test reset method for AudioStreamInfo."""
    asi = AudioStreamInfo()
    asi.channels = 2
    asi.sample_rate = 44100
    asi.bits_per_sample = 16
    asi.stream_type = StreamType.AAC
    asi.bitrate = 128000
    
    asi.reset()
    
    # After reset, values should return to defaults
    assert asi.channels == 0
    assert asi.sample_rate == 0
    assert asi.bits_per_sample == 0
    assert asi.stream_type == StreamType.Unknown
    assert asi.bitrate == 0
