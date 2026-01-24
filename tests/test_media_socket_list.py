"""
Tests for MediaSocketList class.
"""

import pytest
from avblocks.media_socket import MediaSocket
from avblocks.media_socket_list import MediaSocketList
from avblocks.media_pin import MediaPin
from avblocks.audio_stream_info import AudioStreamInfo
from avblocks.video_stream_info import VideoStreamInfo
from avblocks.constants import StreamType, StreamSubType, MediaType


class TestMediaSocketList:
    """Test cases for MediaSocketList class."""
    
    def test_create_default(self):
        """Test creating a default MediaSocketList object."""
        socket_list = MediaSocketList()
        
        assert socket_list is not None
        assert len(socket_list) == 0
        assert not socket_list.immutable
    
    def test_add_socket(self):
        """Test adding a socket to the list."""
        socket_list = MediaSocketList()
        
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        socket.file = "output.mp4"
        
        socket_list.add(socket)
        
        assert len(socket_list) == 1
        assert socket_list[0].stream_type == StreamType.MP4
        assert socket_list[0].file == "output.mp4"
    
    def test_add_multiple_sockets(self):
        """Test adding multiple sockets to the list."""
        socket_list = MediaSocketList()
        
        # Add MP4 socket
        mp4_socket = MediaSocket()
        mp4_socket.stream_type = StreamType.MP4
        mp4_socket.file = "output.mp4"
        socket_list.add(mp4_socket)
        
        # Add WAV socket
        wav_socket = MediaSocket()
        wav_socket.stream_type = StreamType.WAVE
        wav_socket.file = "audio.wav"
        socket_list.add(wav_socket)
        
        # Add AVI socket
        avi_socket = MediaSocket()
        avi_socket.stream_type = StreamType.AVI
        avi_socket.file = "video.avi"
        socket_list.add(avi_socket)
        
        assert len(socket_list) == 3
        assert socket_list[0].stream_type == StreamType.MP4
        assert socket_list[1].stream_type == StreamType.WAVE
        assert socket_list[2].stream_type == StreamType.AVI
    
    def test_immutable_default(self):
        """Test that lists are mutable by default."""
        socket_list = MediaSocketList()
        
        assert not socket_list.immutable
        
        # Should be able to add
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        socket_list.add(socket)
        
        assert len(socket_list) == 1
    
    def test_immutable_set(self):
        """Test setting immutable state."""
        socket_list = MediaSocketList()
        
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        socket.file = "output.mp4"
        socket_list.add(socket)
        
        # Make immutable
        socket_list.immutable = True
        assert socket_list.immutable
        
        # Sockets should also be immutable
        assert socket_list[0].immutable
        
        # Should not be able to add more
        socket2 = MediaSocket()
        socket2.stream_type = StreamType.WAVE
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            socket_list.add(socket2)
    
    def test_immutable_propagation(self):
        """Test that immutability propagates to nested sockets."""
        socket_list = MediaSocketList()
        
        socket1 = MediaSocket()
        socket1.file = "file1.mp4"
        
        socket2 = MediaSocket()
        socket2.file = "file2.mp4"
        
        socket_list.add(socket1)
        socket_list.add(socket2)
        
        # Initially mutable
        assert not socket1.immutable
        assert not socket2.immutable
        
        # Make list immutable
        socket_list.immutable = True
        
        # All sockets should now be immutable
        assert socket1.immutable
        assert socket2.immutable
        
        # Make list mutable again
        socket_list.immutable = False
        
        # Sockets should be mutable again
        assert not socket1.immutable
        assert not socket2.immutable
    
    def test_list_operations(self):
        """Test standard list operations."""
        socket_list = MediaSocketList()
        
        socket1 = MediaSocket()
        socket1.file = "file1.mp4"
        
        socket2 = MediaSocket()
        socket2.file = "file2.mp4"
        
        # Add
        socket_list.add(socket1)
        socket_list.add(socket2)
        assert len(socket_list) == 2
        
        # Index access
        assert socket_list[0].file == "file1.mp4"
        assert socket_list[1].file == "file2.mp4"
        
        # Iteration
        files = [socket.file for socket in socket_list]
        assert files == ["file1.mp4", "file2.mp4"]
    
    def test_clear_list(self):
        """Test clearing the list."""
        socket_list = MediaSocketList()
        
        for i in range(3):
            socket = MediaSocket()
            socket.file = f"file{i}.mp4"
            socket_list.add(socket)
        
        assert len(socket_list) == 3
        
        socket_list.clear()
        assert len(socket_list) == 0
    
    def test_remove_socket(self):
        """Test removing a socket from the list."""
        socket_list = MediaSocketList()
        
        socket1 = MediaSocket()
        socket1.file = "file1.mp4"
        
        socket2 = MediaSocket()
        socket2.file = "file2.mp4"
        
        socket_list.add(socket1)
        socket_list.add(socket2)
        
        assert len(socket_list) == 2
        
        socket_list.remove(socket1)
        
        assert len(socket_list) == 1
        assert socket_list[0].file == "file2.mp4"
    
    def test_pop_socket(self):
        """Test popping a socket from the list."""
        socket_list = MediaSocketList()
        
        socket1 = MediaSocket()
        socket1.file = "file1.mp4"
        
        socket2 = MediaSocket()
        socket2.file = "file2.mp4"
        
        socket_list.add(socket1)
        socket_list.add(socket2)
        
        popped = socket_list.pop()
        
        assert popped.file == "file2.mp4"
        assert len(socket_list) == 1
        assert socket_list[0].file == "file1.mp4"
    
    def test_contains(self):
        """Test checking if a socket is in the list."""
        socket_list = MediaSocketList()
        
        socket1 = MediaSocket()
        socket1.file = "file1.mp4"
        
        socket2 = MediaSocket()
        socket2.file = "file2.mp4"
        
        socket_list.add(socket1)
        
        assert socket1 in socket_list
        assert socket2 not in socket_list
    
    def test_empty_list_operations(self):
        """Test operations on an empty list."""
        socket_list = MediaSocketList()
        
        assert len(socket_list) == 0
        assert list(socket_list) == []
    
    def test_sockets_with_pins(self):
        """Test sockets that contain pins."""
        socket_list = MediaSocketList()
        
        socket = MediaSocket()
        socket.stream_type = StreamType.MP4
        socket.file = "output.mp4"
        
        # Add audio pin
        audio_pin = MediaPin()
        audio_info = AudioStreamInfo()
        audio_info.sample_rate = 44100
        audio_info.channels = 2
        audio_pin.stream_info = audio_info
        socket.pins.add(audio_pin)
        
        # Add video pin
        video_pin = MediaPin()
        video_info = VideoStreamInfo()
        video_info.frame_width = 1920
        video_info.frame_height = 1080
        video_pin.stream_info = video_info
        socket.pins.add(video_pin)
        
        socket_list.add(socket)
        
        assert len(socket_list) == 1
        assert len(socket_list[0].pins) == 2
        assert socket_list[0].pins[0].stream_info.media_type == MediaType.Audio
        assert socket_list[0].pins[1].stream_info.media_type == MediaType.Video
    
    def test_multiple_lists_independent(self):
        """Test that multiple lists are independent."""
        list1 = MediaSocketList()
        list2 = MediaSocketList()
        
        socket1 = MediaSocket()
        socket1.file = "file1.mp4"
        
        socket2 = MediaSocket()
        socket2.file = "file2.mp4"
        
        list1.add(socket1)
        list2.add(socket2)
        
        assert len(list1) == 1
        assert len(list2) == 1
        assert list1[0].file == "file1.mp4"
        assert list2[0].file == "file2.mp4"
    
    def test_extend_list(self):
        """Test extending a list with another list."""
        list1 = MediaSocketList()
        list2 = MediaSocketList()
        
        socket1 = MediaSocket()
        socket1.file = "file1.mp4"
        
        socket2 = MediaSocket()
        socket2.file = "file2.mp4"
        
        list1.add(socket1)
        list2.add(socket2)
        
        list1.extend(list2)
        
        assert len(list1) == 2
        assert list1[0].file == "file1.mp4"
        assert list1[1].file == "file2.mp4"
    
    def test_different_stream_types(self):
        """Test sockets with different stream types."""
        socket_list = MediaSocketList()
        
        # MP4 socket
        mp4_socket = MediaSocket()
        mp4_socket.stream_type = StreamType.AAC
        mp4_socket.stream_sub_type = StreamSubType.AAC_ADTS
        socket_list.add(mp4_socket)
        
        # WAV socket
        wav_socket = MediaSocket()
        wav_socket.stream_type = StreamType.WAVE
        wav_socket.stream_sub_type = StreamSubType.Unknown
        socket_list.add(wav_socket)
        
        # H264 elementary stream
        h264_socket = MediaSocket()
        h264_socket.stream_type = StreamType.H264
        socket_list.add(h264_socket)
        
        assert len(socket_list) == 3
        assert socket_list[0].stream_type == StreamType.AAC
        assert socket_list[1].stream_type == StreamType.WAVE
        assert socket_list[2].stream_type == StreamType.H264
    
    def test_sockets_with_time_position(self):
        """Test sockets with time position set."""
        socket_list = MediaSocketList()
        
        socket = MediaSocket()
        socket.file = "input.mp4"
        socket.time_position = 10.5  # Start at 10.5 seconds
        
        socket_list.add(socket)
        
        assert len(socket_list) == 1
        assert socket_list[0].time_position == 10.5
    
    def test_insert_socket(self):
        """Test inserting a socket at a specific position."""
        socket_list = MediaSocketList()
        
        socket1 = MediaSocket()
        socket1.file = "file1.mp4"
        
        socket2 = MediaSocket()
        socket2.file = "file2.mp4"
        
        socket3 = MediaSocket()
        socket3.file = "file3.mp4"
        
        socket_list.add(socket1)
        socket_list.add(socket3)
        
        # Insert socket2 in the middle
        socket_list.insert(1, socket2)
        
        assert len(socket_list) == 3
        assert socket_list[0].file == "file1.mp4"
        assert socket_list[1].file == "file2.mp4"
        assert socket_list[2].file == "file3.mp4"
    
    def test_index_access(self):
        """Test accessing sockets by index."""
        socket_list = MediaSocketList()
        
        for i in range(5):
            socket = MediaSocket()
            socket.file = f"file{i}.mp4"
            socket_list.add(socket)
        
        assert socket_list[0].file == "file0.mp4"
        assert socket_list[2].file == "file2.mp4"
        assert socket_list[4].file == "file4.mp4"
        assert socket_list[-1].file == "file4.mp4"
        assert socket_list[-2].file == "file3.mp4"
    
    def test_slice_access(self):
        """Test slice access on the list."""
        socket_list = MediaSocketList()
        
        for i in range(5):
            socket = MediaSocket()
            socket.file = f"file{i}.mp4"
            socket_list.add(socket)
        
        # Get slice
        subset = socket_list[1:3]
        assert len(subset) == 2
        assert subset[0].file == "file1.mp4"
        assert subset[1].file == "file2.mp4"
    
    def test_sockets_with_metadata(self):
        """Test sockets with metadata."""
        from avblocks.metadata import Metadata
        from avblocks.meta_attribute import MetaAttribute
        
        socket_list = MediaSocketList()
        
        socket = MediaSocket()
        socket.file = "output.mp4"
        
        # Add metadata
        metadata = Metadata()
        attr = MetaAttribute()
        attr.name = "title"
        attr.value = "Test Video"
        metadata.attributes.add(attr)
        socket.metadata = metadata
        
        socket_list.add(socket)
        
        assert len(socket_list) == 1
        assert socket_list[0].metadata is not None
        assert len(socket_list[0].metadata.attributes) == 1
    
    def test_clone_independence(self):
        """Test that cloned sockets in the list are independent."""
        socket_list = MediaSocketList()
        
        socket = MediaSocket()
        socket.file = "original.mp4"
        socket_list.add(socket)
        
        # Clone the socket
        cloned = socket.clone()
        cloned.file = "cloned.mp4"
        socket_list.add(cloned)
        
        assert len(socket_list) == 2
        assert socket_list[0].file == "original.mp4"
        assert socket_list[1].file == "cloned.mp4"
        
        # Modifying cloned should not affect original
        socket_list[1].file = "modified.mp4"
        assert socket_list[0].file == "original.mp4"
        assert socket_list[1].file == "modified.mp4"
