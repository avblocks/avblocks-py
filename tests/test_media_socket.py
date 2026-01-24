"""
Tests for MediaSocket class.
"""

import pytest
import tempfile
import io
from pathlib import Path

from avblocks import Library
from avblocks.media_socket import MediaSocket
from avblocks.constants import StreamType, StreamSubType, MediaType, ColorFormat
from avblocks.audio_stream_info import AudioStreamInfo
from avblocks.video_stream_info import VideoStreamInfo
from avblocks.media_pin import MediaPin
from avblocks.parameter_list import ParameterList
from avblocks.media_buffer import MediaBuffer
from avblocks.presets import Preset


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if Library.initialize():
        yield
        Library.shutdown()
    else:
        pytest.skip("Failed to initialize AVBlocks library")


@pytest.fixture
def temp_file():
    """Fixture to create a temporary file."""
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        temp_path = f.name
    yield temp_path
    # Cleanup
    try:
        Path(temp_path).unlink()
    except:
        pass


class TestMediaSocketCreation:
    """Test MediaSocket object creation and initialization."""
    
    def test_create_media_socket(self):
        """Test creating a MediaSocket object."""
        socket = MediaSocket()
        assert socket is not None
        assert socket.file is None
        assert socket.stream is None
        assert socket.stream_type == StreamType.Unknown
        assert socket.stream_sub_type == StreamSubType.Unknown
        assert socket.params is not None
        assert len(socket.params) == 0
        assert socket.pins is not None
        assert len(socket.pins) == 0
        assert socket.time_position == 0.0
        assert socket.metadata is None
        assert not socket.immutable
    
    def test_media_socket_default_collections(self):
        """Test that MediaSocket has empty collections by default."""
        socket = MediaSocket()
        assert isinstance(socket.params, ParameterList)
        assert len(socket.params) == 0
        assert len(socket.pins) == 0


class TestMediaSocketFile:
    """Test MediaSocket file property."""
    
    def test_set_file_path(self, temp_file):
        """Test setting file path."""
        socket = MediaSocket()
        socket.file = temp_file
        assert socket.file == temp_file
    
    def test_set_file_none(self):
        """Test setting file to None."""
        socket = MediaSocket()
        socket.file = "/path/to/file.mp4"
        assert socket.file is not None
        
        socket.file = None
        assert socket.file is None
    
    def test_file_immutable(self):
        """Test that file cannot be modified when socket is immutable."""
        socket = MediaSocket()
        socket.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.file = "/path/to/file.mp4"


class TestMediaSocketStream:
    """Test MediaSocket stream property."""
    
    def test_set_stream(self):
        """Test setting stream."""
        socket = MediaSocket()
        stream = io.BytesIO()
        socket.stream = stream
        assert socket.stream is stream
    
    def test_set_stream_none(self):
        """Test setting stream to None."""
        socket = MediaSocket()
        socket.stream = io.BytesIO()
        assert socket.stream is not None
        
        socket.stream = None
        assert socket.stream is None
    
    def test_stream_immutable(self):
        """Test that stream cannot be modified when socket is immutable."""
        socket = MediaSocket()
        socket.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.stream = io.BytesIO()


class TestMediaSocketStreamType:
    """Test MediaSocket stream type properties."""
    
    def test_set_stream_type(self):
        """Test setting stream type."""
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        assert socket.stream_type == StreamType.MP4
        
        socket.stream_type = StreamType.H264
        assert socket.stream_type == StreamType.H264
    
    def test_set_stream_sub_type(self):
        """Test setting stream sub type."""
        socket = MediaSocket()
        socket.stream_sub_type = StreamSubType.AVC1
        assert socket.stream_sub_type == StreamSubType.AVC1
    
    def test_stream_type_immutable(self):
        """Test that stream_type cannot be modified when socket is immutable."""
        socket = MediaSocket()
        socket.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.stream_type = StreamType.MP4
    
    def test_stream_sub_type_immutable(self):
        """Test that stream_sub_type cannot be modified when socket is immutable."""
        socket = MediaSocket()
        socket.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.stream_sub_type = StreamSubType.AVC1


class TestMediaSocketParams:
    """Test MediaSocket params property."""
    
    def test_add_string_parameter(self):
        """Test adding a string parameter."""
        socket = MediaSocket()
        socket.params["container"] = "mp4"
        
        assert len(socket.params) == 1
        assert "container" in socket.params
        assert socket.params["container"] == "mp4"
    
    def test_add_int_parameter(self):
        """Test adding an int parameter."""
        socket = MediaSocket()
        socket.params["duration"] = 300
        
        assert len(socket.params) == 1
        assert socket.params["duration"] == 300
    
    def test_add_multiple_parameters(self):
        """Test adding multiple parameters."""
        socket = MediaSocket()
        socket.params["format"] = "mov"
        socket.params["faststart"] = True
        socket.params["duration"] = 120
        
        assert len(socket.params) == 3
        assert socket.params["format"] == "mov"
        assert socket.params["faststart"] is True
        assert socket.params["duration"] == 120
    
    def test_replace_params(self):
        """Test replacing the entire params collection."""
        socket = MediaSocket()
        socket.params["param1"] = "value1"
        
        assert len(socket.params) == 1
        
        # Replace with new ParameterList
        new_params = ParameterList()
        new_params["param2"] = "value2"
        
        socket.params = new_params
        
        assert len(socket.params) == 1
        assert "param2" in socket.params
        assert "param1" not in socket.params
    
    def test_params_immutable(self):
        """Test that params cannot be modified when socket is immutable."""
        socket = MediaSocket()
        socket.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            new_params = ParameterList()
            socket.params = new_params


class TestMediaSocketPins:
    """Test MediaSocket pins property."""
    
    def test_add_audio_pin(self, initialized_library):
        """Test adding an audio pin."""
        socket = MediaSocket()
        
        pin = MediaPin()
        asi = AudioStreamInfo()
        asi.stream_type = StreamType.AAC
        asi.channels = 2
        asi.sample_rate = 44100
        pin.stream_info = asi
        
        socket.pins.add(pin)
        
        assert len(socket.pins) == 1
        assert socket.pins[0].stream_info.media_type == MediaType.Audio
        assert socket.pins[0].stream_info.channels == 2
    
    def test_add_video_pin(self, initialized_library):
        """Test adding a video pin."""
        socket = MediaSocket()
        
        pin = MediaPin()
        vsi = VideoStreamInfo()
        vsi.stream_type = StreamType.H264
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        pin.stream_info = vsi
        
        socket.pins.add(pin)
        
        assert len(socket.pins) == 1
        assert socket.pins[0].stream_info.media_type == MediaType.Video
        assert socket.pins[0].stream_info.frame_width == 1920
    
    def test_add_multiple_pins(self, initialized_library):
        """Test adding multiple pins."""
        socket = MediaSocket()
        
        # Add video pin
        video_pin = MediaPin()
        vsi = VideoStreamInfo()
        vsi.stream_type = StreamType.H264
        video_pin.stream_info = vsi
        socket.pins.add(video_pin)
        
        # Add audio pin
        audio_pin = MediaPin()
        asi = AudioStreamInfo()
        asi.stream_type = StreamType.AAC
        audio_pin.stream_info = asi
        socket.pins.add(audio_pin)
        
        assert len(socket.pins) == 2
        assert socket.pins[0].stream_info.media_type == MediaType.Video
        assert socket.pins[1].stream_info.media_type == MediaType.Audio
    
    def test_pins_immutable(self):
        """Test that pins cannot be modified when socket is immutable."""
        socket = MediaSocket()
        pin = MediaPin()
        socket.pins.add(pin)
        
        socket.immutable = True
        
        # Cannot add new pins
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.pins.add(MediaPin())


class TestMediaSocketTimePosition:
    """Test MediaSocket time_position property."""
    
    def test_set_time_position(self):
        """Test setting time position."""
        socket = MediaSocket()
        socket.time_position = 10.5
        assert socket.time_position == 10.5
        
        socket.time_position = 0.0
        assert socket.time_position == 0.0
    
    def test_time_position_immutable(self):
        """Test that time_position cannot be modified when socket is immutable."""
        socket = MediaSocket()
        socket.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.time_position = 5.0


class TestMediaSocketImmutability:
    """Test MediaSocket immutability."""
    
    def test_default_not_immutable(self):
        """Test that MediaSocket is mutable by default."""
        socket = MediaSocket()
        assert not socket.immutable
    
    def test_set_immutable(self):
        """Test setting MediaSocket to immutable."""
        socket = MediaSocket()
        socket.immutable = True
        assert socket.immutable
    
    def test_immutability_propagates_to_pins(self, initialized_library):
        """Test that immutability propagates to pins."""
        socket = MediaSocket()
        pin = MediaPin()
        pin.stream_info = AudioStreamInfo()
        socket.pins.add(pin)
        
        assert not socket.pins.immutable
        assert not pin.immutable
        
        socket.immutable = True
        
        assert socket.pins.immutable
        assert pin.immutable
    
    def test_immutability_propagates_to_params(self):
        """Test that immutability propagates to params."""
        socket = MediaSocket()
        socket.params["test"] = "value"
        
        assert not socket.params.immutable
        
        socket.immutable = True
        
        assert socket.params.immutable
    
    def test_immutable_socket_modifications_fail(self, temp_file):
        """Test that all modifications fail when socket is immutable."""
        socket = MediaSocket()
        socket.file = temp_file
        socket.stream_type = StreamType.MP4
        
        socket.immutable = True
        
        # All setters should raise RuntimeError
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.file = "/other/path.mp4"
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.stream = io.BytesIO()
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.stream_type = StreamType.AVI
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.stream_sub_type = StreamSubType.AVC1
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.params = ParameterList()
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.time_position = 10.0


class TestMediaSocketClone:
    """Test MediaSocket cloning."""
    
    def test_clone_empty_socket(self):
        """Test cloning an empty MediaSocket."""
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        socket.time_position = 5.0
        
        clone = socket.clone()
        
        assert clone is not None
        assert clone is not socket
        assert clone.stream_type == StreamType.MP4
        assert clone.time_position == 5.0
        assert clone.file is None
        assert len(clone.pins) == 0
        assert len(clone.params) == 0
        assert not clone.immutable
    
    def test_clone_with_file(self, temp_file):
        """Test cloning MediaSocket with file."""
        socket = MediaSocket()
        socket.file = temp_file
        socket.stream_type = StreamType.MP4
        
        clone = socket.clone()
        
        assert clone.file == temp_file
        assert clone.stream_type == StreamType.MP4
    
    def test_clone_with_pins(self, initialized_library):
        """Test cloning MediaSocket with pins."""
        socket = MediaSocket()
        
        pin = MediaPin()
        asi = AudioStreamInfo()
        asi.channels = 2
        asi.sample_rate = 48000
        pin.stream_info = asi
        socket.pins.add(pin)
        
        clone = socket.clone()
        
        assert len(clone.pins) == 1
        assert clone.pins is not socket.pins
        assert clone.pins[0] is not socket.pins[0]
        assert clone.pins[0].stream_info.channels == 2
        assert clone.pins[0].stream_info.sample_rate == 48000
    
    def test_clone_with_params(self):
        """Test cloning MediaSocket with parameters."""
        socket = MediaSocket()
        socket.params["bitrate"] = 5000000
        socket.params["faststart"] = True
        
        clone = socket.clone()
        
        assert len(clone.params) == 2
        assert clone.params is not socket.params
        assert clone.params["bitrate"] == 5000000
        assert clone.params["faststart"] is True
    
    def test_clone_immutable_becomes_mutable(self):
        """Test that cloning an immutable socket creates a mutable clone."""
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        socket.immutable = True
        
        assert socket.immutable
        
        clone = socket.clone()
        
        assert not clone.immutable
        assert clone.stream_type == StreamType.MP4
        
        # Clone should be modifiable
        clone.stream_type = StreamType.AVI
        assert clone.stream_type == StreamType.AVI
    
    def test_clone_deep_copy(self, initialized_library):
        """Test that clone creates independent copies."""
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        socket.time_position = 10.0
        
        pin = MediaPin()
        asi = AudioStreamInfo()
        asi.channels = 2
        pin.stream_info = asi
        socket.pins.add(pin)
        
        socket.params["bitrate"] = 128000
        
        clone = socket.clone()
        
        # Modify original
        socket.stream_type = StreamType.AVI
        socket.time_position = 20.0
        socket.pins[0].stream_info.channels = 6
        socket.params["bitrate"] = 256000
        
        # Clone should not be affected
        assert clone.stream_type == StreamType.MP4
        assert clone.time_position == 10.0
        assert clone.pins[0].stream_info.channels == 2
        assert clone.params["bitrate"] == 128000
    
    def test_clone_stream_not_copied(self):
        """Test that stream object is not deep copied (streams can't be cloned)."""
        socket = MediaSocket()
        stream = io.BytesIO()
        socket.stream = stream
        
        clone = socket.clone()
        
        # Stream should be the same object (not deep copied)
        assert clone.stream is stream


class TestMediaSocketFromPreset:
    """Test MediaSocket.from_preset static method."""
    
    def test_from_preset_generic_mp4_h264_720p(self, initialized_library):
        """Test creating socket from generic MP4 H.264 720p preset."""
        socket = MediaSocket.from_preset(Preset.Video.Generic.MP4.H264_720p)
        
        assert socket is not None
        # The preset should configure the socket appropriately
        # Exact validation depends on AVBlocks implementation
    
    def test_from_preset_generic_mp4_h264_1080p(self, initialized_library):
        """Test creating socket from generic MP4 H.264 1080p preset."""
        socket = MediaSocket.from_preset(Preset.Video.Generic.MP4.H264_1080p)
        
        assert socket is not None
    
    def test_from_preset_audio_mp3_cd(self, initialized_library):
        """Test creating socket from MP3 CD preset."""
        socket = MediaSocket.from_preset(Preset.Audio.Generic.MP3.CD)
        
        assert socket is not None
    
    def test_from_preset_audio_aac_m4a(self, initialized_library):
        """Test creating socket from M4A AAC preset."""
        socket = MediaSocket.from_preset(Preset.Audio.Generic.M4A.CBR_128kbps)
        
        assert socket is not None
    
    def test_from_preset_ipad_720p(self, initialized_library):
        """Test creating socket from iPad 720p preset."""
        socket = MediaSocket.from_preset(Preset.Video.iPad.H264_720p)
        
        assert socket is not None
    
    def test_from_preset_invalid(self, initialized_library):
        """Test creating socket from invalid preset."""
        socket = MediaSocket.from_preset("invalid.preset.name")
        
        assert socket is None


class TestMediaSocketIntegration:
    """Integration tests for MediaSocket."""
    
    def test_complete_output_socket_setup(self, initialized_library, temp_file):
        """Test setting up a complete output socket."""
        socket = MediaSocket()
        socket.file = temp_file
        socket.stream_type = StreamType.MP4
        
        # Setup video pin
        video_pin = MediaPin()
        vsi = VideoStreamInfo()
        vsi.stream_type = StreamType.H264
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        vsi.frame_rate = 30.0
        vsi.color_format = ColorFormat.YUV420
        video_pin.stream_info = vsi
        video_pin.params["Bitrate"] = 5000000
        socket.pins.add(video_pin)
        
        # Setup audio pin
        audio_pin = MediaPin()
        asi = AudioStreamInfo()
        asi.stream_type = StreamType.AAC
        asi.channels = 2
        asi.sample_rate = 44100
        asi.bits_per_sample = 16
        audio_pin.stream_info = asi
        audio_pin.params["Bitrate"] = 128000
        socket.pins.add(audio_pin)
        
        # Socket parameters
        socket.params["FastStart"] = True
        
        # Verify
        assert socket.file == temp_file
        assert socket.stream_type == StreamType.MP4
        assert len(socket.pins) == 2
        assert socket.pins[0].stream_info.media_type == MediaType.Video
        assert socket.pins[1].stream_info.media_type == MediaType.Audio
        assert len(socket.params) == 1
        assert socket.params["FastStart"] is True
    
    def test_complete_input_socket_setup(self, initialized_library, temp_file):
        """Test setting up a complete input socket."""
        socket = MediaSocket()
        socket.file = temp_file
        socket.time_position = 5.0
        
        # Input sockets typically don't need pins configured
        # (they are discovered by the transcoder)
        
        # Verify
        assert socket.file == temp_file
        assert socket.time_position == 5.0
    
    def test_socket_with_stream(self, initialized_library):
        """Test setting up socket with stream instead of file."""
        socket = MediaSocket()
        stream = io.BytesIO()
        socket.stream = stream
        socket.stream_type = StreamType.MP4
        
        # Setup video pin
        video_pin = MediaPin()
        vsi = VideoStreamInfo()
        vsi.stream_type = StreamType.H264
        vsi.frame_width = 1280
        vsi.frame_height = 720
        vsi.frame_rate = 30.0
        video_pin.stream_info = vsi
        socket.pins.add(video_pin)
        
        # Verify
        assert socket.stream is stream
        assert socket.stream_type == StreamType.MP4
        assert len(socket.pins) == 1
    
    def test_socket_from_preset_with_modifications(self, initialized_library):
        """Test creating socket from preset and modifying it."""
        socket = MediaSocket.from_preset(Preset.Video.Generic.MP4.H264_720p)
        
        assert socket is not None
        
        # Modify the preset-created socket
        socket.params["CustomParam"] = "custom_value"
        
        # Should be able to modify
        assert "CustomParam" in socket.params
        assert socket.params["CustomParam"] == "custom_value"
    
    def test_multiple_pins_with_different_types(self, initialized_library):
        """Test socket with multiple pins of different stream types."""
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        
        # Video pin - H.264
        video_pin1 = MediaPin()
        vsi1 = VideoStreamInfo()
        vsi1.stream_type = StreamType.H264
        vsi1.frame_width = 1920
        vsi1.frame_height = 1080
        video_pin1.stream_info = vsi1
        socket.pins.add(video_pin1)
        
        # Audio pin - AAC
        audio_pin1 = MediaPin()
        asi1 = AudioStreamInfo()
        asi1.stream_type = StreamType.AAC
        asi1.channels = 2
        audio_pin1.stream_info = asi1
        socket.pins.add(audio_pin1)
        
        # Audio pin - MP3 (for testing multiple audio tracks)
        audio_pin2 = MediaPin()
        asi2 = AudioStreamInfo()
        asi2.stream_type = StreamType.MPEG_Audio
        asi2.channels = 2
        audio_pin2.stream_info = asi2
        socket.pins.add(audio_pin2)
        
        # Verify
        assert len(socket.pins) == 3
        assert socket.pins[0].stream_info.media_type == MediaType.Video
        assert socket.pins[1].stream_info.media_type == MediaType.Audio
        assert socket.pins[2].stream_info.media_type == MediaType.Audio
        assert socket.pins[1].stream_info.stream_type == StreamType.AAC
        assert socket.pins[2].stream_info.stream_type == StreamType.MPEG_Audio


class TestMediaSocketMetadata:
    """Test MediaSocket metadata property."""
    
    def test_metadata_default_none(self):
        """Test that metadata is None by default."""
        socket = MediaSocket()
        assert socket.metadata is None
    
    def test_set_metadata(self, initialized_library):
        """Test setting metadata."""
        from avblocks.metadata import Metadata
        from avblocks.meta_attribute import MetaAttribute
        from avblocks.constants import Meta
        
        socket = MediaSocket()
        metadata = Metadata()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Test Title"
        metadata.attributes.add(attr)
        
        socket.metadata = metadata
        
        assert socket.metadata is not None
        assert len(socket.metadata.attributes) == 1
        assert socket.metadata.attributes[0].name == Meta.Title
        assert socket.metadata.attributes[0].value == "Test Title"
    
    def test_set_metadata_none(self, initialized_library):
        """Test setting metadata to None."""
        from avblocks.metadata import Metadata
        
        socket = MediaSocket()
        socket.metadata = Metadata()
        assert socket.metadata is not None
        
        socket.metadata = None
        assert socket.metadata is None
    
    def test_metadata_with_attributes(self, initialized_library):
        """Test metadata with multiple attributes."""
        from avblocks.metadata import Metadata
        from avblocks.meta_attribute import MetaAttribute
        from avblocks.constants import Meta
        
        socket = MediaSocket()
        metadata = Metadata()
        
        # Add multiple attributes
        attributes_data = [
            (Meta.Title, "My Song"),
            (Meta.AlbumArtist, "Artist Name"),
            (Meta.Album, "Album Name"),
            (Meta.Year, "2024"),
            (Meta.Genre, "Rock"),
        ]
        
        for name, value in attributes_data:
            attr = MetaAttribute()
            attr.name = name
            attr.value = value
            metadata.attributes.add(attr)
        
        socket.metadata = metadata
        
        assert len(socket.metadata.attributes) == 5
        assert socket.metadata.attributes[0].value == "My Song"
        assert socket.metadata.attributes[1].value == "Artist Name"
    
    def test_metadata_with_pictures(self, initialized_library):
        """Test metadata with pictures."""
        from avblocks.metadata import Metadata
        from avblocks.meta_picture import MetaPicture
        from avblocks.constants import MetaPictureType, MimeType
        
        socket = MediaSocket()
        metadata = Metadata()
        
        # Add a picture
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.picture_type = MetaPictureType.FrontCover
        pic.description = "Album Cover"
        pic.bytes = b'\xFF\xD8\xFF\xE0\x00\x10JFIF'
        metadata.pictures.add(pic)
        
        socket.metadata = metadata
        
        assert len(socket.metadata.pictures) == 1
        assert socket.metadata.pictures[0].picture_type == MetaPictureType.FrontCover
        assert socket.metadata.pictures[0].mime_type == MimeType.Jpeg
    
    def test_metadata_with_both_attributes_and_pictures(self, initialized_library):
        """Test metadata with both attributes and pictures."""
        from avblocks.metadata import Metadata
        from avblocks.meta_attribute import MetaAttribute
        from avblocks.meta_picture import MetaPicture
        from avblocks.constants import Meta, MetaPictureType, MimeType
        
        socket = MediaSocket()
        metadata = Metadata()
        
        # Add attributes
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Song Title"
        metadata.attributes.add(attr)
        
        # Add picture
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.picture_type = MetaPictureType.FrontCover
        pic.bytes = b'\xFF\xD8\xFF\xE0'
        metadata.pictures.add(pic)
        
        socket.metadata = metadata
        
        assert len(socket.metadata.attributes) == 1
        assert len(socket.metadata.pictures) == 1
    
    def test_metadata_immutable(self, initialized_library):
        """Test that metadata cannot be modified when socket is immutable."""
        from avblocks.metadata import Metadata
        
        socket = MediaSocket()
        socket.metadata = Metadata()
        socket.immutable = True
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket.metadata = Metadata()
    
    def test_metadata_immutability_propagates(self, initialized_library):
        """Test that immutability propagates to metadata."""
        from avblocks.metadata import Metadata
        from avblocks.meta_attribute import MetaAttribute
        from avblocks.constants import Meta
        
        socket = MediaSocket()
        metadata = Metadata()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Title"
        metadata.attributes.add(attr)
        
        socket.metadata = metadata
        
        assert not socket.metadata.immutable
        assert not metadata.immutable
        
        socket.immutable = True
        
        assert socket.metadata.immutable
        assert metadata.immutable
    
    def test_clone_with_metadata(self, initialized_library):
        """Test cloning MediaSocket with metadata."""
        from avblocks.metadata import Metadata
        from avblocks.meta_attribute import MetaAttribute
        from avblocks.constants import Meta
        
        socket = MediaSocket()
        metadata = Metadata()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Original Title"
        metadata.attributes.add(attr)
        
        socket.metadata = metadata
        
        clone = socket.clone()
        
        assert clone.metadata is not None
        assert clone.metadata is not socket.metadata
        assert len(clone.metadata.attributes) == 1
        assert clone.metadata.attributes[0].value == "Original Title"
        
        # Modify clone's metadata
        clone.metadata.attributes[0].value = "Modified Title"
        
        # Original should be unchanged
        assert socket.metadata.attributes[0].value == "Original Title"
    
    def test_clone_with_empty_metadata(self, initialized_library):
        """Test cloning MediaSocket with empty metadata."""
        from avblocks.metadata import Metadata
        
        socket = MediaSocket()
        socket.metadata = Metadata()
        
        clone = socket.clone()
        
        assert clone.metadata is not None
        assert clone.metadata is not socket.metadata
        assert len(clone.metadata.attributes) == 0
        assert len(clone.metadata.pictures) == 0
    
    def test_clone_without_metadata(self):
        """Test cloning MediaSocket without metadata."""
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        
        clone = socket.clone()
        
        assert clone.metadata is None
        assert socket.metadata is None
    
    def test_metadata_in_complete_socket(self, initialized_library, temp_file):
        """Test metadata in a complete socket setup."""
        from avblocks.metadata import Metadata
        from avblocks.meta_attribute import MetaAttribute
        from avblocks.meta_picture import MetaPicture
        from avblocks.constants import Meta, MetaPictureType, MimeType
        
        socket = MediaSocket()
        socket.file = temp_file
        socket.stream_type = StreamType.MP4
        
        # Setup video pin
        video_pin = MediaPin()
        vsi = VideoStreamInfo()
        vsi.stream_type = StreamType.H264
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        video_pin.stream_info = vsi
        socket.pins.add(video_pin)
        
        # Setup metadata
        metadata = Metadata()
        
        # Add title
        title = MetaAttribute()
        title.name = Meta.Title
        title.value = "Video Title"
        metadata.attributes.add(title)
        
        # Add copyright
        copyright_attr = MetaAttribute()
        copyright_attr.name = Meta.Copyright
        copyright_attr.value = "Copyright 2024"
        metadata.attributes.add(copyright_attr)
        
        # Add cover art
        cover = MetaPicture()
        cover.mime_type = MimeType.Jpeg
        cover.picture_type = MetaPictureType.FrontCover
        cover.description = "Video Thumbnail"
        cover.bytes = b'\xFF\xD8\xFF\xE0\x00\x10JFIF'
        metadata.pictures.add(cover)
        
        socket.metadata = metadata
        
        # Verify complete setup
        assert socket.file == temp_file
        assert len(socket.pins) == 1
        assert socket.metadata is not None
        assert len(socket.metadata.attributes) == 2
        assert len(socket.metadata.pictures) == 1
        assert socket.metadata.attributes[0].value == "Video Title"
        assert socket.metadata.pictures[0].picture_type == MetaPictureType.FrontCover
    
    def test_replace_metadata(self, initialized_library):
        """Test replacing metadata."""
        from avblocks.metadata import Metadata
        from avblocks.meta_attribute import MetaAttribute
        from avblocks.constants import Meta
        
        socket = MediaSocket()
        
        # Set first metadata
        metadata1 = Metadata()
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "First Title"
        metadata1.attributes.add(attr1)
        socket.metadata = metadata1
        
        assert socket.metadata.attributes[0].value == "First Title"
        
        # Replace with new metadata
        metadata2 = Metadata()
        attr2 = MetaAttribute()
        attr2.name = Meta.Title
        attr2.value = "Second Title"
        metadata2.attributes.add(attr2)
        socket.metadata = metadata2
        
        assert socket.metadata.attributes[0].value == "Second Title"
        assert len(socket.metadata.attributes) == 1

