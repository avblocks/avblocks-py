"""
Tests for MetaPicture class.
"""

import pytest
from avblocks.meta_picture import MetaPicture
from avblocks.constants import MetaPictureType, MimeType


class TestMetaPicture:
    """Test cases for MetaPicture class."""
    
    def test_create_default(self):
        """Test creating a default MetaPicture object."""
        pic = MetaPicture()
        
        assert pic is not None
        assert pic.mime_type is None
        assert pic.picture_type == MetaPictureType.Other
        assert pic.description is None
        assert pic.bytes is None
        assert not pic.immutable
    
    def test_set_mime_type(self):
        """Test setting mime type."""
        pic = MetaPicture()
        
        pic.mime_type = MimeType.Jpeg
        assert pic.mime_type == MimeType.Jpeg
        
        pic.mime_type = MimeType.Png
        assert pic.mime_type == MimeType.Png
    
    def test_set_picture_type(self):
        """Test setting picture type."""
        pic = MetaPicture()
        
        pic.picture_type = MetaPictureType.FrontCover
        assert pic.picture_type == MetaPictureType.FrontCover
        
        pic.picture_type = MetaPictureType.BackCover
        assert pic.picture_type == MetaPictureType.BackCover
        
        pic.picture_type = MetaPictureType.Artist
        assert pic.picture_type == MetaPictureType.Artist
    
    def test_set_description(self):
        """Test setting description."""
        pic = MetaPicture()
        
        pic.description = "Album Cover"
        assert pic.description == "Album Cover"
        
        # Test Unicode description
        pic.description = "Album Art - България"
        assert pic.description == "Album Art - България"
    
    def test_set_bytes(self):
        """Test setting image bytes."""
        pic = MetaPicture()
        
        # Create some dummy image data
        image_data = b'\xFF\xD8\xFF\xE0\x00\x10JFIF'  # JPEG header
        pic.bytes = image_data
        
        assert pic.bytes == image_data
        assert len(pic.bytes) == len(image_data)
    
    def test_set_all_properties(self):
        """Test setting all properties together."""
        pic = MetaPicture()
        
        pic.mime_type = MimeType.Jpeg
        pic.picture_type = MetaPictureType.FrontCover
        pic.description = "Front Cover"
        pic.bytes = b'\xFF\xD8\xFF\xE0\x00\x10JFIF'
        
        assert pic.mime_type == MimeType.Jpeg
        assert pic.picture_type == MetaPictureType.FrontCover
        assert pic.description == "Front Cover"
        assert pic.bytes == b'\xFF\xD8\xFF\xE0\x00\x10JFIF'
    
    def test_immutable_default(self):
        """Test that objects are mutable by default."""
        pic = MetaPicture()
        
        assert not pic.immutable
        
        # Should be able to modify
        pic.mime_type = MimeType.Png
        assert pic.mime_type == MimeType.Png
    
    def test_immutable_set(self):
        """Test setting immutable state."""
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        
        # Make immutable
        pic.immutable = True
        assert pic.immutable
        
        # Should not be able to modify
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pic.mime_type = MimeType.Png
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pic.picture_type = MetaPictureType.BackCover
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pic.description = "New Description"
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pic.bytes = b'new data'
    
    def test_clone(self):
        """Test cloning a MetaPicture object."""
        pic1 = MetaPicture()
        pic1.mime_type = MimeType.Jpeg
        pic1.picture_type = MetaPictureType.FrontCover
        pic1.description = "Original Cover"
        pic1.bytes = b'\xFF\xD8\xFF\xE0'
        
        # Clone the object
        pic2 = pic1.clone()
        
        # Verify properties are copied
        assert pic2.mime_type == pic1.mime_type
        assert pic2.picture_type == pic1.picture_type
        assert pic2.description == pic1.description
        assert pic2.bytes == pic1.bytes
        
        # Verify it's a deep copy (different objects)
        assert pic2 is not pic1
        assert pic2.bytes is not pic1.bytes
        
        # Verify clone is mutable even if original is immutable
        pic1.immutable = True
        pic3 = pic1.clone()
        assert not pic3.immutable
        pic3.mime_type = MimeType.Png
        assert pic3.mime_type == MimeType.Png
    
    def test_clone_empty_bytes(self):
        """Test cloning when bytes is None."""
        pic1 = MetaPicture()
        pic1.mime_type = MimeType.Jpeg
        pic1.bytes = None
        
        pic2 = pic1.clone()
        
        assert pic2.mime_type == pic1.mime_type
        assert pic2.bytes is None
    
    def test_modify_after_clone(self):
        """Test that modifying a clone doesn't affect the original."""
        pic1 = MetaPicture()
        pic1.mime_type = MimeType.Jpeg
        pic1.description = "Original"
        pic1.bytes = b'original data'
        
        pic2 = pic1.clone()
        pic2.mime_type = MimeType.Png
        pic2.description = "Modified"
        pic2.bytes = b'modified data'
        
        # Original should be unchanged
        assert pic1.mime_type == MimeType.Jpeg
        assert pic1.description == "Original"
        assert pic1.bytes == b'original data'
        
        # Clone should be modified
        assert pic2.mime_type == MimeType.Png
        assert pic2.description == "Modified"
        assert pic2.bytes == b'modified data'
    
    def test_large_image_data(self):
        """Test with larger image data."""
        pic = MetaPicture()
        
        # Create a larger dummy image (1KB)
        large_data = bytes(range(256)) * 4
        pic.bytes = large_data
        
        assert pic.bytes == large_data
        assert len(pic.bytes) == 1024
    
    def test_empty_description(self):
        """Test with empty string description."""
        pic = MetaPicture()
        
        pic.description = ""
        assert pic.description == ""
    
    def test_none_values(self):
        """Test setting None values."""
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.description = "Cover"
        pic.bytes = b'data'
        
        # Set to None
        pic.mime_type = None
        pic.description = None
        pic.bytes = None
        
        assert pic.mime_type is None
        assert pic.description is None
        assert pic.bytes is None
    
    def test_picture_type_constants(self):
        """Test all picture type constants."""
        pic = MetaPicture()
        
        # Test various picture types
        types_to_test = [
            MetaPictureType.Other,
            MetaPictureType.FileIcon,
            MetaPictureType.FrontCover,
            MetaPictureType.BackCover,
            MetaPictureType.LeadArtist,
            MetaPictureType.Artist,
            MetaPictureType.Conductor,
            MetaPictureType.Band,
            MetaPictureType.Composer,
        ]
        
        for pic_type in types_to_test:
            pic.picture_type = pic_type
            assert pic.picture_type == pic_type
    
    def test_mime_type_constants(self):
        """Test all mime type constants."""
        pic = MetaPicture()
        
        # Test various MIME types
        mime_types_to_test = [
            MimeType.Jpeg,
            MimeType.Png,
            MimeType.Gif,
            MimeType.Tiff,
        ]
        
        for mime in mime_types_to_test:
            pic.mime_type = mime
            assert pic.mime_type == mime
