"""
Tests for MediaPinList class.
"""

import pytest
from avblocks.media_pin import MediaPin
from avblocks.media_pin_list import MediaPinList
from avblocks.audio_stream_info import AudioStreamInfo
from avblocks.video_stream_info import VideoStreamInfo
from avblocks.constants import PinConnection, StreamType, MediaType


class TestMediaPinList:
    """Test cases for MediaPinList class."""
    
    def test_create_default(self):
        """Test creating a default MediaPinList object."""
        pin_list = MediaPinList()
        
        assert pin_list is not None
        assert len(pin_list) == 0
        assert not pin_list.immutable
    
    def test_add_pin(self):
        """Test adding a pin to the list."""
        pin_list = MediaPinList()
        
        pin = MediaPin()
        pin.connection = PinConnection.Auto
        
        audio_info = AudioStreamInfo()
        audio_info.sample_rate = 44100
        audio_info.channels = 2
        pin.stream_info = audio_info
        
        pin_list.add(pin)
        
        assert len(pin_list) == 1
        assert pin_list[0].connection == PinConnection.Auto
        assert pin_list[0].stream_info.media_type == MediaType.Audio
    
    def test_add_multiple_pins(self):
        """Test adding multiple pins to the list."""
        pin_list = MediaPinList()
        
        # Add audio pin
        audio_pin = MediaPin()
        audio_pin.connection = 1
        audio_info = AudioStreamInfo()
        audio_info.sample_rate = 48000
        audio_pin.stream_info = audio_info
        pin_list.add(audio_pin)
        
        # Add video pin
        video_pin = MediaPin()
        video_pin.connection = 2
        video_info = VideoStreamInfo()
        video_info.frame_width = 1920
        video_info.frame_height = 1080
        video_pin.stream_info = video_info
        pin_list.add(video_pin)
        
        # Add another audio pin
        audio_pin2 = MediaPin()
        audio_pin2.connection = 3
        audio_info2 = AudioStreamInfo()
        audio_info2.sample_rate = 44100
        audio_pin2.stream_info = audio_info2
        pin_list.add(audio_pin2)
        
        assert len(pin_list) == 3
        assert pin_list[0].stream_info.media_type == MediaType.Audio
        assert pin_list[1].stream_info.media_type == MediaType.Video
        assert pin_list[2].stream_info.media_type == MediaType.Audio
    
    def test_immutable_default(self):
        """Test that lists are mutable by default."""
        pin_list = MediaPinList()
        
        assert not pin_list.immutable
        
        # Should be able to add
        pin = MediaPin()
        pin.connection = PinConnection.Auto
        pin_list.add(pin)
        
        assert len(pin_list) == 1
    
    def test_immutable_set(self):
        """Test setting immutable state."""
        pin_list = MediaPinList()
        
        pin = MediaPin()
        pin.connection = 1
        audio_info = AudioStreamInfo()
        audio_info.sample_rate = 44100
        pin.stream_info = audio_info
        pin_list.add(pin)
        
        # Make immutable
        pin_list.immutable = True
        assert pin_list.immutable
        
        # Pins should also be immutable
        assert pin_list[0].immutable
        
        # Should not be able to add more
        pin2 = MediaPin()
        pin2.connection = 2
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pin_list.add(pin2)
    
    def test_immutable_propagation(self):
        """Test that immutability propagates to nested pins."""
        pin_list = MediaPinList()
        
        pin1 = MediaPin()
        pin1.connection = 1
        
        pin2 = MediaPin()
        pin2.connection = 2
        
        pin_list.add(pin1)
        pin_list.add(pin2)
        
        # Initially mutable
        assert not pin1.immutable
        assert not pin2.immutable
        
        # Make list immutable
        pin_list.immutable = True
        
        # All pins should now be immutable
        assert pin1.immutable
        assert pin2.immutable
        
        # Make list mutable again
        pin_list.immutable = False
        
        # Pins should be mutable again
        assert not pin1.immutable
        assert not pin2.immutable
    
    def test_list_operations(self):
        """Test standard list operations."""
        pin_list = MediaPinList()
        
        pin1 = MediaPin()
        pin1.connection = 1
        
        pin2 = MediaPin()
        pin2.connection = 2
        
        # Add
        pin_list.add(pin1)
        pin_list.add(pin2)
        assert len(pin_list) == 2
        
        # Index access
        assert pin_list[0].connection == 1
        assert pin_list[1].connection == 2
        
        # Iteration
        connections = [pin.connection for pin in pin_list]
        assert connections == [1, 2]
    
    def test_clear_list(self):
        """Test clearing the list."""
        pin_list = MediaPinList()
        
        for i in range(3):
            pin = MediaPin()
            pin.connection = i + 1
            pin_list.add(pin)
        
        assert len(pin_list) == 3
        
        pin_list.clear()
        assert len(pin_list) == 0
    
    def test_remove_pin(self):
        """Test removing a pin from the list."""
        pin_list = MediaPinList()
        
        pin1 = MediaPin()
        pin1.connection = 1
        
        pin2 = MediaPin()
        pin2.connection = 2
        
        pin_list.add(pin1)
        pin_list.add(pin2)
        
        assert len(pin_list) == 2
        
        pin_list.remove(pin1)
        
        assert len(pin_list) == 1
        assert pin_list[0].connection == 2
    
    def test_pop_pin(self):
        """Test popping a pin from the list."""
        pin_list = MediaPinList()
        
        pin1 = MediaPin()
        pin1.connection = 1
        
        pin2 = MediaPin()
        pin2.connection = 2
        
        pin_list.add(pin1)
        pin_list.add(pin2)
        
        popped = pin_list.pop()
        
        assert popped.connection == 2
        assert len(pin_list) == 1
        assert pin_list[0].connection == 1
    
    def test_contains(self):
        """Test checking if a pin is in the list."""
        pin_list = MediaPinList()
        
        pin1 = MediaPin()
        pin1.connection = 1
        
        pin2 = MediaPin()
        pin2.connection = 2
        
        pin_list.add(pin1)
        
        assert pin1 in pin_list
        assert pin2 not in pin_list
    
    def test_empty_list_operations(self):
        """Test operations on an empty list."""
        pin_list = MediaPinList()
        
        assert len(pin_list) == 0
        assert list(pin_list) == []
    
    def test_audio_video_pins(self):
        """Test creating a list with both audio and video pins."""
        pin_list = MediaPinList()
        
        # Audio pin
        audio_pin = MediaPin()
        audio_pin.connection = 1
        audio_info = AudioStreamInfo()
        audio_info.stream_type = StreamType.MPEG_Audio
        audio_info.sample_rate = 44100
        audio_info.channels = 2
        audio_info.bits_per_sample = 16
        audio_pin.stream_info = audio_info
        pin_list.add(audio_pin)
        
        # Video pin
        video_pin = MediaPin()
        video_pin.connection = 2
        video_info = VideoStreamInfo()
        video_info.stream_type = StreamType.H264
        video_info.frame_width = 1920
        video_info.frame_height = 1080
        video_info.frame_rate = 30.0
        video_pin.stream_info = video_info
        pin_list.add(video_pin)
        
        assert len(pin_list) == 2
        
        # Verify audio pin
        assert pin_list[0].stream_info.media_type == MediaType.Audio
        assert isinstance(pin_list[0].stream_info, AudioStreamInfo)
        assert pin_list[0].stream_info.sample_rate == 44100
        
        # Verify video pin
        assert pin_list[1].stream_info.media_type == MediaType.Video
        assert isinstance(pin_list[1].stream_info, VideoStreamInfo)
        assert pin_list[1].stream_info.frame_width == 1920
    
    def test_multiple_lists_independent(self):
        """Test that multiple lists are independent."""
        list1 = MediaPinList()
        list2 = MediaPinList()
        
        pin1 = MediaPin()
        pin1.connection = 1
        
        pin2 = MediaPin()
        pin2.connection = 2
        
        list1.add(pin1)
        list2.add(pin2)
        
        assert len(list1) == 1
        assert len(list2) == 1
        assert list1[0].connection == 1
        assert list2[0].connection == 2
    
    def test_extend_list(self):
        """Test extending a list with another list."""
        list1 = MediaPinList()
        list2 = MediaPinList()
        
        pin1 = MediaPin()
        pin1.connection = 1
        
        pin2 = MediaPin()
        pin2.connection = 2
        
        list1.add(pin1)
        list2.add(pin2)
        
        list1.extend(list2)
        
        assert len(list1) == 2
        assert list1[0].connection == 1
        assert list1[1].connection == 2
    
    def test_pin_connection_types(self):
        """Test pins with different connection types."""
        pin_list = MediaPinList()
        
        # Auto connection
        auto_pin = MediaPin()
        auto_pin.connection = PinConnection.Auto
        pin_list.add(auto_pin)
        
        # Disabled connection
        disabled_pin = MediaPin()
        disabled_pin.connection = PinConnection.Disabled
        pin_list.add(disabled_pin)
        
        # Explicit connection ID
        explicit_pin = MediaPin()
        explicit_pin.connection = 100
        pin_list.add(explicit_pin)
        
        assert len(pin_list) == 3
        assert pin_list[0].connection == PinConnection.Auto
        assert pin_list[1].connection == PinConnection.Disabled
        assert pin_list[2].connection == 100
    
    def test_pins_with_params(self):
        """Test pins that have parameters."""
        pin_list = MediaPinList()
        
        pin = MediaPin()
        pin.connection = 1
        
        # Add some parameters (assuming ParameterList exists)
        # This is just to verify that pins with params can be added
        from avblocks.parameter_list import ParameterList
        pin.params = ParameterList()
        
        pin_list.add(pin)
        
        assert len(pin_list) == 1
        assert pin_list[0].params is not None
    
    def test_insert_pin(self):
        """Test inserting a pin at a specific position."""
        pin_list = MediaPinList()
        
        pin1 = MediaPin()
        pin1.connection = 1
        
        pin2 = MediaPin()
        pin2.connection = 2
        
        pin3 = MediaPin()
        pin3.connection = 3
        
        pin_list.add(pin1)
        pin_list.add(pin3)
        
        # Insert pin2 in the middle
        pin_list.insert(1, pin2)
        
        assert len(pin_list) == 3
        assert pin_list[0].connection == 1
        assert pin_list[1].connection == 2
        assert pin_list[2].connection == 3
    
    def test_index_access(self):
        """Test accessing pins by index."""
        pin_list = MediaPinList()
        
        for i in range(5):
            pin = MediaPin()
            pin.connection = i + 1
            pin_list.add(pin)
        
        assert pin_list[0].connection == 1
        assert pin_list[2].connection == 3
        assert pin_list[4].connection == 5
        assert pin_list[-1].connection == 5
        assert pin_list[-2].connection == 4
    
    def test_slice_access(self):
        """Test slice access on the list."""
        pin_list = MediaPinList()
        
        for i in range(5):
            pin = MediaPin()
            pin.connection = i + 1
            pin_list.add(pin)
        
        # Get slice
        subset = pin_list[1:3]
        assert len(subset) == 2
        assert subset[0].connection == 2
        assert subset[1].connection == 3
