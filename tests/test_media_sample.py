"""
Unit tests for MediaSample class.
"""

import pytest
from avblocks.media_sample import MediaSample
from avblocks.media_buffer import MediaBuffer
from avblocks.unmanaged_media_buffer import UnmanagedMediaBuffer
from avblocks.constants import MediaSampleFlags, PictureType, FrameType, ColorFormat


class TestMediaSampleConstruction:
    """Test MediaSample construction."""
    
    def test_default_construction(self):
        """Test creating MediaSample with no arguments."""
        sample = MediaSample()
        
        assert sample.buffer is None
        assert sample.unmanaged_buffer is None
        assert sample.start_time == -1.0
        assert sample.end_time == -1.0
        assert sample.flags == MediaSampleFlags(0)
        assert sample.picture_type == PictureType.None_
        assert sample.frame_type == FrameType.None_


class TestMediaSampleBuffer:
    """Test MediaSample buffer property."""
    
    def test_set_buffer(self):
        """Test setting buffer property."""
        sample = MediaSample()
        buffer = MediaBuffer(buffer_size=1024)
        
        sample.buffer = buffer
        
        assert sample.buffer is buffer
        assert sample.buffer.capacity == 1024
    
    def test_set_buffer_none(self):
        """Test setting buffer to None."""
        sample = MediaSample()
        buffer = MediaBuffer(buffer_size=1024)
        sample.buffer = buffer
        
        sample.buffer = None
        
        assert sample.buffer is None


class TestMediaSampleUnmanagedBuffer:
    """Test MediaSample unmanaged_buffer property."""
    
    def test_set_unmanaged_buffer(self):
        """Test setting unmanaged_buffer property."""
        sample = MediaSample()
        buffer = UnmanagedMediaBuffer(buffer_size=1024)
        
        sample.unmanaged_buffer = buffer
        
        assert sample.unmanaged_buffer is buffer
        assert sample.unmanaged_buffer.capacity == 1024
    
    def test_set_unmanaged_buffer_none(self):
        """Test setting unmanaged_buffer to None."""
        sample = MediaSample()
        buffer = UnmanagedMediaBuffer(buffer_size=1024)
        sample.unmanaged_buffer = buffer
        
        sample.unmanaged_buffer = None
        
        assert sample.unmanaged_buffer is None


class TestMediaSampleTiming:
    """Test MediaSample timing properties."""
    
    def test_start_time_default(self):
        """Test default start_time value."""
        sample = MediaSample()
        assert sample.start_time == -1.0
    
    def test_set_start_time(self):
        """Test setting start_time."""
        sample = MediaSample()
        
        sample.start_time = 5.5
        
        assert sample.start_time == 5.5
    
    def test_set_start_time_zero(self):
        """Test setting start_time to zero."""
        sample = MediaSample()
        
        sample.start_time = 0.0
        
        assert sample.start_time == 0.0
    
    def test_end_time_default(self):
        """Test default end_time value."""
        sample = MediaSample()
        assert sample.end_time == -1.0
    
    def test_set_end_time(self):
        """Test setting end_time."""
        sample = MediaSample()
        
        sample.end_time = 10.5
        
        assert sample.end_time == 10.5
    
    def test_set_timing_range(self):
        """Test setting valid timing range."""
        sample = MediaSample()
        
        sample.start_time = 2.0
        sample.end_time = 5.0
        
        assert sample.start_time == 2.0
        assert sample.end_time == 5.0
        assert sample.end_time > sample.start_time


class TestMediaSampleFlags:
    """Test MediaSample flags property."""
    
    def test_flags_default(self):
        """Test default flags value."""
        sample = MediaSample()
        assert sample.flags == MediaSampleFlags(0)
    
    def test_set_flags_single(self):
        """Test setting a single flag."""
        sample = MediaSample()
        
        sample.flags = MediaSampleFlags.KeyFrame
        
        assert sample.flags == MediaSampleFlags.KeyFrame
    
    def test_set_flags_combined(self):
        """Test setting combined flags."""
        sample = MediaSample()
        
        sample.flags = MediaSampleFlags.KeyFrame | MediaSampleFlags.Bos
        
        assert (sample.flags & MediaSampleFlags.KeyFrame) != 0
        assert (sample.flags & MediaSampleFlags.Bos) != 0


class TestMediaSamplePictureType:
    """Test MediaSample picture_type property."""
    
    def test_picture_type_default(self):
        """Test default picture_type value."""
        sample = MediaSample()
        assert sample.picture_type == PictureType.None_
    
    def test_set_picture_type_i_frame(self):
        """Test setting I-frame picture type."""
        sample = MediaSample()
        
        sample.picture_type = PictureType.I
        
        assert sample.picture_type == PictureType.I
    
    def test_set_picture_type_p_frame(self):
        """Test setting P-frame picture type."""
        sample = MediaSample()
        
        sample.picture_type = PictureType.P
        
        assert sample.picture_type == PictureType.P
    
    def test_set_picture_type_b_frame(self):
        """Test setting B-frame picture type."""
        sample = MediaSample()
        
        sample.picture_type = PictureType.B
        
        assert sample.picture_type == PictureType.B


class TestMediaSampleFrameType:
    """Test MediaSample frame_type property."""
    
    def test_frame_type_default(self):
        """Test default frame_type value."""
        sample = MediaSample()
        assert sample.frame_type == FrameType.None_
    
    def test_set_frame_type(self):
        """Test setting frame_type."""
        sample = MediaSample()
        
        sample.frame_type = FrameType.G711VoiceFrame
        
        assert sample.frame_type == FrameType.G711VoiceFrame


class TestMediaSampleVideoBufferSize:
    """Test MediaSample.video_buffer_size_in_bytes static method."""
    
    def test_video_buffer_size_hd(self):
        """Test calculating buffer size for HD video."""
        size = MediaSample.video_buffer_size_in_bytes(
            1920, 1080, ColorFormat.YUV420
        )
        
        # YUV420 should be exactly width * height * 1.5
        expected = 1920 * 1080 * 3 // 2
        assert size == expected
    
    def test_video_buffer_size_sd(self):
        """Test calculating buffer size for SD video."""
        size = MediaSample.video_buffer_size_in_bytes(
            720, 576, ColorFormat.YUV420
        )
        
        # YUV420 should be exactly width * height * 1.5
        expected = 720 * 576 * 3 // 2
        assert size == expected
    
    def test_video_buffer_size_invalid(self):
        """Test calculating buffer size with invalid parameters."""
        size = MediaSample.video_buffer_size_in_bytes(
            0, 0, ColorFormat.Unknown
        )
        
        assert size == 0


class TestMediaSampleClone:
    """Test MediaSample clone method."""
    
    def test_clone_empty_sample(self):
        """Test cloning empty MediaSample."""
        sample = MediaSample()
        
        cloned = sample.clone()
        
        assert cloned is not sample
        assert cloned.buffer is None
        assert cloned.unmanaged_buffer is None
        assert cloned.start_time == sample.start_time
        assert cloned.end_time == sample.end_time
        assert cloned.flags == sample.flags
        assert cloned.picture_type == sample.picture_type
        assert cloned.frame_type == sample.frame_type
    
    def test_clone_with_properties(self):
        """Test cloning MediaSample with properties set."""
        sample = MediaSample()
        sample.start_time = 1.5
        sample.end_time = 3.0
        sample.flags = MediaSampleFlags.KeyFrame
        sample.picture_type = PictureType.I
        sample.frame_type = FrameType.G711VoiceFrame
        
        cloned = sample.clone()
        
        assert cloned is not sample
        assert cloned.start_time == 1.5
        assert cloned.end_time == 3.0
        assert cloned.flags == MediaSampleFlags.KeyFrame
        assert cloned.picture_type == PictureType.I
        assert cloned.frame_type == FrameType.G711VoiceFrame
    
    def test_clone_with_buffer(self):
        """Test cloning MediaSample with buffer."""
        sample = MediaSample()
        buffer = MediaBuffer(buffer_size=1024)
        buffer.start[0:5] = b"Hello"
        buffer.set_data(0, 5)
        sample.buffer = buffer
        
        cloned = sample.clone()
        
        assert cloned is not sample
        assert cloned.buffer is not sample.buffer
        assert cloned.buffer.capacity == sample.buffer.capacity
        assert bytes(cloned.buffer.data) == bytes(sample.buffer.data)
    
    def test_clone_with_unmanaged_buffer(self):
        """Test cloning MediaSample with unmanaged buffer."""
        sample = MediaSample()
        buffer = UnmanagedMediaBuffer(buffer_size=1024)
        sample.unmanaged_buffer = buffer
        
        cloned = sample.clone()
        
        assert cloned is not sample
        assert cloned.unmanaged_buffer is not sample.unmanaged_buffer
        assert cloned.unmanaged_buffer.capacity == sample.unmanaged_buffer.capacity
    
    def test_clone_independence(self):
        """Test that cloned sample is independent."""
        sample = MediaSample()
        sample.start_time = 1.0
        sample.flags = MediaSampleFlags.KeyFrame
        
        cloned = sample.clone()
        
        # Modify original
        sample.start_time = 5.0
        sample.flags = MediaSampleFlags.Eos
        
        # Verify clone is unchanged
        assert cloned.start_time == 1.0
        assert cloned.flags == MediaSampleFlags.KeyFrame


class TestMediaSampleIntegration:
    """Integration tests for MediaSample."""
    
    def test_complete_sample_setup(self):
        """Test setting up a complete media sample."""
        # Create sample
        sample = MediaSample()
        
        # Set timing
        sample.start_time = 0.0
        sample.end_time = 0.04  # 40ms for 25fps
        
        # Set flags
        sample.flags = MediaSampleFlags.KeyFrame
        sample.picture_type = PictureType.I
        
        # Create and attach buffer
        buffer = MediaBuffer(buffer_size=1920 * 1080 * 3 // 2)
        sample.buffer = buffer
        
        # Verify all properties
        assert sample.start_time == 0.0
        assert sample.end_time == 0.04
        assert sample.flags == MediaSampleFlags.KeyFrame
        assert sample.picture_type == PictureType.I
        assert sample.buffer is not None
        assert sample.buffer.capacity > 0
    
    def test_sample_with_data(self):
        """Test sample with actual data."""
        # Create sample with data
        sample = MediaSample()
        test_data = b"Sample media data"
        buffer = MediaBuffer(data=test_data)
        sample.buffer = buffer
        sample.start_time = 1.0
        sample.end_time = 2.0
        
        # Verify data is accessible
        assert bytes(sample.buffer.data) == test_data
        assert sample.buffer.data_size == len(test_data)
    
    def test_sample_sequence(self):
        """Test creating a sequence of samples."""
        samples = []
        frame_duration = 1.0 / 30.0  # 30fps
        
        for i in range(5):
            sample = MediaSample()
            sample.start_time = i * frame_duration
            sample.end_time = (i + 1) * frame_duration
            sample.flags = MediaSampleFlags.KeyFrame if i == 0 else MediaSampleFlags(0)
            sample.picture_type = PictureType.I if i == 0 else PictureType.P
            samples.append(sample)
        
        # Verify sequence
        assert len(samples) == 5
        assert samples[0].flags == MediaSampleFlags.KeyFrame
        assert samples[0].picture_type == PictureType.I
        for i in range(1, 5):
            assert samples[i].start_time == samples[i-1].end_time
            assert samples[i].picture_type == PictureType.P
