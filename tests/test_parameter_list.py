"""
Unit tests for ParameterList class.
"""

import pytest
from avblocks import Library
from avblocks.parameter_list import ParameterList
from avblocks.media_buffer import MediaBuffer
from avblocks.video_stream_info import VideoStreamInfo
from avblocks.constants import StreamType, ColorFormat


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if Library.initialize():
        yield
        Library.shutdown()
    else:
        pytest.skip("Failed to initialize AVBlocks library")


class TestParameterListBasics:
    """Test basic ParameterList functionality."""
    
    def test_create_empty(self):
        """Test creating empty ParameterList."""
        params = ParameterList()
        assert len(params) == 0
        assert list(params) == []
    
    def test_add_basic_types(self):
        """Test adding basic types to ParameterList."""
        params = ParameterList()
        params["string"] = "test"
        params["int"] = 42
        params["float"] = 3.14
        params["bool"] = True
        
        assert len(params) == 4
        assert params["string"] == "test"
        assert params["int"] == 42
        assert params["float"] == 3.14
        assert params["bool"] is True
    
    def test_iterate(self):
        """Test iterating over ParameterList."""
        params = ParameterList()
        params["a"] = 1
        params["b"] = 2
        params["c"] = 3
        
        keys = [key for key in params]
        assert set(keys) == {"a", "b", "c"}
    
    def test_contains(self):
        """Test checking if key exists in ParameterList."""
        params = ParameterList()
        params["test"] = "value"
        
        assert "test" in params
        assert "missing" not in params
    
    def test_delete(self):
        """Test deleting parameter from ParameterList."""
        params = ParameterList()
        params["test"] = "value"
        
        del params["test"]
        assert "test" not in params
        assert len(params) == 0


class TestParameterListMediaBuffer:
    """Test ParameterList with MediaBuffer values."""
    
    def test_add_media_buffer(self, initialized_library):
        """Test adding MediaBuffer to ParameterList."""
        params = ParameterList()
        mb = MediaBuffer(data=b"Test buffer data")
        
        params["buffer"] = mb
        
        assert "buffer" in params
        assert isinstance(params["buffer"], MediaBuffer)
        assert params["buffer"] is mb
    
    def test_retrieve_media_buffer(self, initialized_library):
        """Test retrieving MediaBuffer from ParameterList."""
        test_data = b"MediaBuffer test data"
        mb = MediaBuffer(data=test_data)
        
        params = ParameterList()
        params["my_buffer"] = mb
        
        retrieved = params["my_buffer"]
        assert isinstance(retrieved, MediaBuffer)
        assert bytes(retrieved.data) == test_data
        assert retrieved.data_size == len(test_data)
    
    def test_multiple_media_buffers(self, initialized_library):
        """Test adding multiple MediaBuffer instances."""
        params = ParameterList()
        
        mb1 = MediaBuffer(data=b"First buffer")
        mb2 = MediaBuffer(data=b"Second buffer")
        mb3 = MediaBuffer(data=b"Third buffer")
        
        params["buffer1"] = mb1
        params["buffer2"] = mb2
        params["buffer3"] = mb3
        
        assert len(params) == 3
        assert bytes(params["buffer1"].data) == b"First buffer"
        assert bytes(params["buffer2"].data) == b"Second buffer"
        assert bytes(params["buffer3"].data) == b"Third buffer"
    
    def test_empty_media_buffer(self, initialized_library):
        """Test adding empty MediaBuffer."""
        params = ParameterList()
        mb = MediaBuffer()
        
        params["empty"] = mb
        
        assert "empty" in params
        assert isinstance(params["empty"], MediaBuffer)
        assert params["empty"].data_size == 0
    
    def test_large_media_buffer(self, initialized_library):
        """Test adding large MediaBuffer (1MB)."""
        large_data = b"X" * (1024 * 1024)
        mb = MediaBuffer(data=large_data)
        
        params = ParameterList()
        params["large_buffer"] = mb
        
        retrieved = params["large_buffer"]
        assert isinstance(retrieved, MediaBuffer)
        assert retrieved.data_size == len(large_data)
        assert bytes(retrieved.data) == large_data


class TestParameterListVideoStreamInfo:
    """Test ParameterList with VideoStreamInfo values."""
    
    def test_add_video_stream_info(self, initialized_library):
        """Test adding VideoStreamInfo to ParameterList."""
        params = ParameterList()
        vsi = VideoStreamInfo()
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        
        params["video"] = vsi
        
        assert "video" in params
        assert isinstance(params["video"], VideoStreamInfo)
        assert params["video"] is vsi
    
    def test_retrieve_video_stream_info(self, initialized_library):
        """Test retrieving VideoStreamInfo from ParameterList."""
        vsi = VideoStreamInfo()
        vsi.frame_width = 1280
        vsi.frame_height = 720
        vsi.stream_type = StreamType.H264
        vsi.color_format = ColorFormat.YUV420
        vsi.frame_rate = 30.0
        
        params = ParameterList()
        params["stream_info"] = vsi
        
        retrieved = params["stream_info"]
        assert isinstance(retrieved, VideoStreamInfo)
        assert retrieved.frame_width == 1280
        assert retrieved.frame_height == 720
        assert retrieved.stream_type == StreamType.H264
        assert retrieved.color_format == ColorFormat.YUV420
        assert retrieved.frame_rate == 30.0
    
    def test_multiple_video_stream_infos(self, initialized_library):
        """Test adding multiple VideoStreamInfo instances."""
        params = ParameterList()
        
        vsi1 = VideoStreamInfo()
        vsi1.frame_width = 1920
        vsi1.frame_height = 1080
        
        vsi2 = VideoStreamInfo()
        vsi2.frame_width = 1280
        vsi2.frame_height = 720
        
        vsi3 = VideoStreamInfo()
        vsi3.frame_width = 640
        vsi3.frame_height = 480
        
        params["hd"] = vsi1
        params["hd_ready"] = vsi2
        params["sd"] = vsi3
        
        assert len(params) == 3
        assert params["hd"].frame_width == 1920
        assert params["hd_ready"].frame_width == 1280
        assert params["sd"].frame_width == 640
    
    def test_video_stream_info_with_all_properties(self, initialized_library):
        """Test VideoStreamInfo with all properties set."""
        vsi = VideoStreamInfo()
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        vsi.display_ratio_width = 16
        vsi.display_ratio_height = 9
        vsi.frame_rate = 29.97
        vsi.color_format = ColorFormat.YUV420
        vsi.stream_type = StreamType.H264
        vsi.bitrate = 5000000
        
        params = ParameterList()
        params["full_info"] = vsi
        
        retrieved = params["full_info"]
        assert retrieved.frame_width == 1920
        assert retrieved.frame_height == 1080
        assert retrieved.display_ratio_width == 16
        assert retrieved.display_ratio_height == 9
        assert abs(retrieved.frame_rate - 29.97) < 0.01
        assert retrieved.color_format == ColorFormat.YUV420
        assert retrieved.stream_type == StreamType.H264
        assert retrieved.bitrate == 5000000


class TestParameterListMixedTypes:
    """Test ParameterList with mixed types including MediaBuffer and VideoStreamInfo."""
    
    def test_mixed_basic_and_complex_types(self, initialized_library):
        """Test mixing basic types with MediaBuffer and VideoStreamInfo."""
        params = ParameterList()
        
        # Basic types
        params["title"] = "My Video"
        params["frame_count"] = 300
        params["fps"] = 30.0
        params["enabled"] = True
        
        # MediaBuffer
        mb = MediaBuffer(data=b"Video frame data")
        params["frame_buffer"] = mb
        
        # VideoStreamInfo
        vsi = VideoStreamInfo()
        vsi.frame_width = 1920
        vsi.frame_height = 1080
        params["stream_config"] = vsi
        
        # Verify all types
        assert len(params) == 6
        assert params["title"] == "My Video"
        assert params["frame_count"] == 300
        assert params["fps"] == 30.0
        assert params["enabled"] is True
        assert isinstance(params["frame_buffer"], MediaBuffer)
        assert isinstance(params["stream_config"], VideoStreamInfo)
    
    def test_multiple_buffers_and_stream_infos(self, initialized_library):
        """Test multiple MediaBuffers and VideoStreamInfos together."""
        params = ParameterList()
        
        # Multiple buffers
        params["video_buffer"] = MediaBuffer(data=b"Video data")
        params["audio_buffer"] = MediaBuffer(data=b"Audio data")
        params["metadata_buffer"] = MediaBuffer(data=b"Metadata")
        
        # Multiple stream infos
        video_si = VideoStreamInfo()
        video_si.frame_width = 1920
        video_si.frame_height = 1080
        params["video_stream"] = video_si
        
        thumbnail_si = VideoStreamInfo()
        thumbnail_si.frame_width = 320
        thumbnail_si.frame_height = 240
        params["thumbnail_stream"] = thumbnail_si
        
        # Basic metadata
        params["duration"] = 120.5
        params["codec"] = "h264"
        
        assert len(params) == 7
        assert all(isinstance(params[k], MediaBuffer) for k in ["video_buffer", "audio_buffer", "metadata_buffer"])
        assert all(isinstance(params[k], VideoStreamInfo) for k in ["video_stream", "thumbnail_stream"])
    
    def test_overwrite_with_different_types(self, initialized_library):
        """Test overwriting parameter with different type."""
        params = ParameterList()
        
        # Start with string
        params["data"] = "initial string"
        assert isinstance(params["data"], str)
        
        # Overwrite with MediaBuffer
        params["data"] = MediaBuffer(data=b"buffer data")
        assert isinstance(params["data"], MediaBuffer)
        
        # Overwrite with VideoStreamInfo
        vsi = VideoStreamInfo()
        params["data"] = vsi
        assert isinstance(params["data"], VideoStreamInfo)
        
        # Overwrite with int
        params["data"] = 42
        assert isinstance(params["data"], int)


class TestParameterListCopy:
    """Test copying ParameterList with complex types."""
    
    def test_copy_with_media_buffer(self, initialized_library):
        """Test copying ParameterList containing MediaBuffer."""
        params = ParameterList()
        mb = MediaBuffer(data=b"Test data")
        params["buffer"] = mb
        params["name"] = "test"
        
        copied = params.copy()
        
        assert copied is not params
        assert copied["name"] == "test"
        assert "buffer" in copied
        assert isinstance(copied["buffer"], MediaBuffer)
        # Reference should be copied (shallow copy)
        assert copied["buffer"] is params["buffer"]
    
    def test_copy_with_video_stream_info(self, initialized_library):
        """Test copying ParameterList containing VideoStreamInfo."""
        params = ParameterList()
        vsi = VideoStreamInfo()
        vsi.frame_width = 1920
        params["stream"] = vsi
        params["codec"] = "h264"
        
        copied = params.copy()
        
        assert copied is not params
        assert copied["codec"] == "h264"
        assert "stream" in copied
        assert isinstance(copied["stream"], VideoStreamInfo)
        # Reference should be copied (shallow copy)
        assert copied["stream"] is params["stream"]
    
    def test_copy_with_mixed_types(self, initialized_library):
        """Test copying ParameterList with mixed types."""
        params = ParameterList()
        params["string"] = "value"
        params["int"] = 42
        params["buffer"] = MediaBuffer(data=b"data")
        params["stream"] = VideoStreamInfo()
        
        copied = params.copy()
        
        assert len(copied) == 4
        assert copied["string"] == "value"
        assert copied["int"] == 42
        assert isinstance(copied["buffer"], MediaBuffer)
        assert isinstance(copied["stream"], VideoStreamInfo)


class TestParameterListEdgeCases:
    """Test edge cases for ParameterList with complex types."""
    
    def test_none_values(self, initialized_library):
        """Test setting None values."""
        params = ParameterList()
        params["null_value"] = None
        params["buffer"] = MediaBuffer(data=b"data")
        params["another_null"] = None
        
        assert params["null_value"] is None
        assert params["another_null"] is None
        assert isinstance(params["buffer"], MediaBuffer)
    
    def test_replace_complex_with_basic(self, initialized_library):
        """Test replacing complex type with basic type."""
        params = ParameterList()
        
        mb = MediaBuffer(data=b"original")
        params["value"] = mb
        
        # Replace with string
        params["value"] = "replaced"
        
        assert params["value"] == "replaced"
        assert not isinstance(params["value"], MediaBuffer)
    
    def test_empty_key_string(self, initialized_library):
        """Test using empty string as key."""
        params = ParameterList()
        mb = MediaBuffer(data=b"test")
        
        params[""] = mb
        
        assert "" in params
        assert isinstance(params[""], MediaBuffer)
    
    def test_unicode_keys(self, initialized_library):
        """Test using unicode characters in keys."""
        params = ParameterList()
        
        vsi = VideoStreamInfo()
        vsi.frame_width = 1920
        
        params["браво"] = vsi
        params["résolution"] = "1920x1080"
        
        assert "браво" in params
        assert isinstance(params["браво"], VideoStreamInfo)
        assert params["résolution"] == "1920x1080"


class TestParameterListIntegration:
    """Integration tests for ParameterList."""
    
    def test_workflow_video_encoding_params(self, initialized_library):
        """Test realistic video encoding parameter workflow."""
        # Setup encoding parameters
        params = ParameterList()
        
        # Input stream info
        input_vsi = VideoStreamInfo()
        input_vsi.frame_width = 1920
        input_vsi.frame_height = 1080
        input_vsi.frame_rate = 30.0
        input_vsi.color_format = ColorFormat.YUV420
        params["input_video"] = input_vsi
        
        # Output stream info
        output_vsi = VideoStreamInfo()
        output_vsi.frame_width = 1280
        output_vsi.frame_height = 720
        output_vsi.frame_rate = 30.0
        output_vsi.stream_type = StreamType.H264
        output_vsi.bitrate = 2500000
        params["output_video"] = output_vsi
        
        # Frame buffer
        params["frame_buffer"] = MediaBuffer(buffer_size=1920*1080*3)
        
        # Encoding parameters
        params["codec"] = "h264"
        params["preset"] = "medium"
        params["quality"] = 23
        params["keyframe_interval"] = 60
        
        # Verify all parameters
        assert len(params) == 7
        assert params["input_video"].frame_width == 1920
        assert params["output_video"].frame_width == 1280
        assert params["frame_buffer"].capacity == 1920*1080*3
        assert params["codec"] == "h264"
        assert params["quality"] == 23
    
    def test_workflow_multi_stream_setup(self, initialized_library):
        """Test multi-stream configuration workflow."""
        params = ParameterList()
        
        # Video stream
        video_stream = VideoStreamInfo()
        video_stream.frame_width = 1920
        video_stream.frame_height = 1080
        video_stream.stream_type = StreamType.H264
        params["video_stream"] = video_stream
        
        # Thumbnail stream
        thumb_stream = VideoStreamInfo()
        thumb_stream.frame_width = 320
        thumb_stream.frame_height = 240
        params["thumbnail_stream"] = thumb_stream
        
        # Buffers for each stream
        params["video_buffer"] = MediaBuffer(data=b"V" * 100000)
        params["thumb_buffer"] = MediaBuffer(data=b"T" * 10000)
        params["metadata_buffer"] = MediaBuffer(data=b"Metadata info")
        
        # Stream identifiers
        params["video_id"] = 1
        params["thumb_id"] = 2
        params["title"] = "Multi-stream video"
        
        # Verify configuration
        assert len(params) == 8
        assert params["video_stream"].frame_width == 1920
        assert params["thumbnail_stream"].frame_width == 320
        assert params["video_buffer"].data_size == 100000
        assert params["thumb_buffer"].data_size == 10000
        assert params["video_id"] == 1
        assert params["thumb_id"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
