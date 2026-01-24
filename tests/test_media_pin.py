"""
Tests for MediaPin class.
"""

import pytest
from avblocks import Library
from avblocks.media_pin import MediaPin
from avblocks.constants import PinConnection, MediaType, StreamType, ColorFormat
from avblocks.audio_stream_info import AudioStreamInfo
from avblocks.video_stream_info import VideoStreamInfo
from avblocks.parameter_list import ParameterList
from avblocks.media_buffer import MediaBuffer


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if Library.initialize():
        yield
        Library.shutdown()
    else:
        pytest.skip("Failed to initialize AVBlocks library")


class TestMediaPinCreation:
    """Test MediaPin object creation and initialization."""
    
    def test_create_media_pin(self):
        """Test creating a MediaPin object."""
        pin = MediaPin()
        assert pin is not None
        assert pin.connection == PinConnection.Auto
        assert pin.stream_info is None
        assert pin.params is not None
        assert len(pin.params) == 0
        assert not pin.immutable
    
    def test_media_pin_default_params(self):
        """Test that MediaPin has an empty ParameterList by default."""
        pin = MediaPin()
        assert isinstance(pin.params, ParameterList)
        assert len(pin.params) == 0


class TestMediaPinConnection:
    """Test MediaPin connection property."""
    
    def test_set_connection_auto(self):
        """Test setting connection to Auto."""
        pin = MediaPin()
        pin.connection = PinConnection.Auto
        assert pin.connection == PinConnection.Auto
    
    def test_set_connection_disabled(self):
        """Test setting connection to Disabled."""
        pin = MediaPin()
        pin.connection = PinConnection.Disabled
        assert pin.connection == PinConnection.Disabled
    
    def test_set_connection_explicit(self):
        """Test setting an explicit connection ID."""
        pin = MediaPin()
        pin.connection = 1
        assert pin.connection == 1
        
        pin.connection = 100
        assert pin.connection == 100
    
    def test_connection_immutable(self):
        """Test that connection cannot be modified when pin is immutable."""
        pin = MediaPin()
        pin.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pin.connection = PinConnection.Disabled


class TestMediaPinStreamInfo:
    """Test MediaPin stream_info property."""
    
    def test_set_audio_stream_info(self, initialized_library):
        """Test setting audio stream info."""
        pin = MediaPin()
        asi = AudioStreamInfo()
        asi.stream_type = StreamType.LPCM
        asi.channels = 2
        asi.sample_rate = 44100
        asi.bits_per_sample = 16
        
        pin.stream_info = asi
        
        assert pin.stream_info is not None
        assert pin.stream_info.media_type == MediaType.Audio
        assert isinstance(pin.stream_info, AudioStreamInfo)
        assert pin.stream_info.channels == 2
        assert pin.stream_info.sample_rate == 44100
    
    def test_set_video_stream_info(self, initialized_library):
        """Test setting video stream info."""
        pin = MediaPin()
        vsi = VideoStreamInfo()
        vsi.stream_type = StreamType.H264
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        vsi.frame_rate = 30.0
        vsi.color_format = ColorFormat.YUV420
        
        pin.stream_info = vsi
        
        assert pin.stream_info is not None
        assert pin.stream_info.media_type == MediaType.Video
        assert isinstance(pin.stream_info, VideoStreamInfo)
        assert pin.stream_info.frame_width == 1920
        assert pin.stream_info.frame_height == 1080
    
    def test_stream_info_none(self):
        """Test setting stream_info to None."""
        pin = MediaPin()
        pin.stream_info = AudioStreamInfo()
        assert pin.stream_info is not None
        
        pin.stream_info = None
        assert pin.stream_info is None
    
    def test_stream_info_immutable(self):
        """Test that stream_info cannot be modified when pin is immutable."""
        pin = MediaPin()
        pin.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pin.stream_info = AudioStreamInfo()


class TestMediaPinParams:
    """Test MediaPin params property."""
    
    def test_add_string_parameter(self):
        """Test adding a string parameter."""
        pin = MediaPin()
        pin.params["test_string"] = "test_value"
        
        assert len(pin.params) == 1
        assert "test_string" in pin.params
        assert pin.params["test_string"] == "test_value"
    
    def test_add_int_parameter(self):
        """Test adding an int parameter."""
        pin = MediaPin()
        pin.params["test_int"] = 42
        
        assert len(pin.params) == 1
        assert pin.params["test_int"] == 42
    
    def test_add_float_parameter(self):
        """Test adding a float parameter."""
        pin = MediaPin()
        pin.params["test_float"] = 3.14
        
        assert len(pin.params) == 1
        assert pin.params["test_float"] == pytest.approx(3.14)
    
    def test_add_multiple_parameters(self):
        """Test adding multiple parameters."""
        pin = MediaPin()
        pin.params["str"] = "value"
        pin.params["int"] = 100
        pin.params["float"] = 2.5
        
        assert len(pin.params) == 3
        assert pin.params["str"] == "value"
        assert pin.params["int"] == 100
        assert pin.params["float"] == 2.5
    
    def test_add_media_buffer_parameter(self, initialized_library):
        """Test adding a MediaBuffer parameter."""
        pin = MediaPin()
        mb = MediaBuffer(data=b"test data")
        pin.params["buffer"] = mb
        
        assert len(pin.params) == 1
        assert "buffer" in pin.params
        assert isinstance(pin.params["buffer"], MediaBuffer)
    
    def test_replace_params(self):
        """Test replacing the entire params collection."""
        pin = MediaPin()
        pin.params["param1"] = "value1"
        
        assert len(pin.params) == 1
        
        # Replace with new ParameterList
        new_params = ParameterList()
        new_params["param2"] = "value2"
        
        pin.params = new_params
        
        assert len(pin.params) == 1
        assert "param2" in pin.params
        assert "param1" not in pin.params
    
    def test_params_immutable(self):
        """Test that params cannot be modified when pin is immutable."""
        pin = MediaPin()
        pin.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            new_params = ParameterList()
            pin.params = new_params


class TestMediaPinImmutability:
    """Test MediaPin immutability."""
    
    def test_default_not_immutable(self):
        """Test that MediaPin is mutable by default."""
        pin = MediaPin()
        assert not pin.immutable
    
    def test_set_immutable(self):
        """Test setting MediaPin to immutable."""
        pin = MediaPin()
        pin.immutable = True
        assert pin.immutable
    
    def test_immutability_propagates_to_stream_info(self, initialized_library):
        """Test that immutability propagates to stream_info."""
        pin = MediaPin()
        asi = AudioStreamInfo()
        pin.stream_info = asi
        
        assert not asi.immutable
        
        pin.immutable = True
        
        assert asi.immutable
    
    def test_immutability_propagates_to_params(self):
        """Test that immutability propagates to params."""
        pin = MediaPin()
        pin.params["test"] = "value"
        
        assert not pin.params.immutable
        
        pin.immutable = True
        
        assert pin.params.immutable
    
    def test_immutable_pin_modifications_fail(self, initialized_library):
        """Test that all modifications fail when pin is immutable."""
        pin = MediaPin()
        pin.connection = 1
        pin.stream_info = AudioStreamInfo()
        
        pin.immutable = True
        
        # All setters should raise RuntimeError
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pin.connection = 2
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pin.stream_info = VideoStreamInfo()
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pin.params = ParameterList()


class TestMediaPinClone:
    """Test MediaPin cloning."""
    
    def test_clone_empty_pin(self):
        """Test cloning an empty MediaPin."""
        pin = MediaPin()
        pin.connection = 5
        
        clone = pin.clone()
        
        assert clone is not None
        assert clone is not pin
        assert clone.connection == 5
        assert clone.stream_info is None
        assert len(clone.params) == 0
        assert not clone.immutable
    
    def test_clone_with_stream_info(self, initialized_library):
        """Test cloning MediaPin with stream info."""
        pin = MediaPin()
        asi = AudioStreamInfo()
        asi.channels = 2
        asi.sample_rate = 48000
        pin.stream_info = asi
        
        clone = pin.clone()
        
        assert clone.stream_info is not None
        assert clone.stream_info is not pin.stream_info
        assert clone.stream_info.channels == 2
        assert clone.stream_info.sample_rate == 48000
    
    def test_clone_with_params(self):
        """Test cloning MediaPin with parameters."""
        pin = MediaPin()
        pin.params["test"] = "value"
        pin.params["number"] = 42
        
        clone = pin.clone()
        
        assert len(clone.params) == 2
        assert "test" in clone.params
        assert clone.params is not pin.params
        assert clone.params["test"] == "value"
        assert clone.params["number"] == 42
    
    def test_clone_immutable_becomes_mutable(self):
        """Test that cloning an immutable pin creates a mutable clone."""
        pin = MediaPin()
        pin.connection = 10
        pin.immutable = True
        
        assert pin.immutable
        
        clone = pin.clone()
        
        assert not clone.immutable
        assert clone.connection == 10
        
        # Clone should be modifiable
        clone.connection = 20
        assert clone.connection == 20
    
    def test_clone_deep_copy(self, initialized_library):
        """Test that clone creates independent copies."""
        pin = MediaPin()
        pin.connection = 1
        
        asi = AudioStreamInfo()
        asi.channels = 2
        pin.stream_info = asi
        
        pin.params["bitrate"] = 128000
        
        clone = pin.clone()
        
        # Modify original
        pin.connection = 2
        pin.stream_info.channels = 6
        pin.params["bitrate"] = 256000
        
        # Clone should not be affected
        assert clone.connection == 1
        assert clone.stream_info.channels == 2
        assert clone.params["bitrate"] == 128000


class TestMediaPinIntegration:
    """Integration tests for MediaPin."""
    
    def test_complete_audio_pin_setup(self, initialized_library):
        """Test setting up a complete audio pin."""
        pin = MediaPin()
        pin.connection = PinConnection.Auto
        
        # Setup audio stream info
        asi = AudioStreamInfo()
        asi.stream_type = StreamType.AAC
        asi.channels = 2
        asi.sample_rate = 44100
        asi.bits_per_sample = 16
        pin.stream_info = asi
        
        # Add parameters
        pin.params["Bitrate"] = 128000
        pin.params["Quality"] = 5
        
        # Verify
        assert pin.connection == PinConnection.Auto
        assert pin.stream_info.media_type == MediaType.Audio
        assert pin.stream_info.channels == 2
        assert len(pin.params) == 2
        assert pin.params["Bitrate"] == 128000
        assert pin.params["Quality"] == 5
    
    def test_complete_video_pin_setup(self, initialized_library):
        """Test setting up a complete video pin."""
        pin = MediaPin()
        pin.connection = 1
        
        # Setup video stream info
        vsi = VideoStreamInfo()
        vsi.stream_type = StreamType.H264
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        vsi.frame_rate = 30.0
        vsi.color_format = ColorFormat.YUV420
        pin.stream_info = vsi
        
        # Add parameters
        pin.params["Bitrate"] = 5000000
        pin.params["Preset"] = "medium"
        pin.params["KeyframeInterval"] = 60
        
        # Verify
        assert pin.connection == 1
        assert pin.stream_info.media_type == MediaType.Video
        assert pin.stream_info.frame_width == 1920
        assert len(pin.params) == 3
        assert pin.params["Bitrate"] == 5000000
        assert pin.params["Preset"] == "medium"
        assert pin.params["KeyframeInterval"] == 60
    
    def test_pin_with_mixed_param_types(self, initialized_library):
        """Test pin with mixed parameter types."""
        pin = MediaPin()
        
        vsi = VideoStreamInfo()
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        pin.stream_info = vsi
        
        # Add various parameter types
        pin.params["codec"] = "h264"  # string
        pin.params["bitrate"] = 5000000  # int
        pin.params["quality"] = 23.5  # float
        pin.params["use_gpu"] = True  # bool
        
        mb = MediaBuffer(data=b"config data")
        pin.params["config_buffer"] = mb  # MediaBuffer
        
        # Verify
        assert len(pin.params) == 5
        assert isinstance(pin.params["codec"], str)
        assert isinstance(pin.params["bitrate"], int)
        assert isinstance(pin.params["quality"], float)
        assert isinstance(pin.params["use_gpu"], bool)
        assert isinstance(pin.params["config_buffer"], MediaBuffer)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
