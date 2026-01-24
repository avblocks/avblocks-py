"""
Tests for MetaPictureList class.
"""

import pytest
from avblocks.meta_picture import MetaPicture
from avblocks.meta_picture_list import MetaPictureList
from avblocks.constants import MetaPictureType, MimeType


class TestMetaPictureList:
    """Test cases for MetaPictureList class."""
    
    def test_create_default(self):
        """Test creating a default MetaPictureList object."""
        pic_list = MetaPictureList()
        
        assert pic_list is not None
        assert len(pic_list) == 0
        assert not pic_list.immutable
    
    def test_add_picture(self):
        """Test adding a picture to the list."""
        pic_list = MetaPictureList()
        
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.picture_type = MetaPictureType.FrontCover
        pic.description = "Album Cover"
        pic.bytes = b'\xFF\xD8\xFF\xE0'
        
        pic_list.add(pic)
        
        assert len(pic_list) == 1
        assert pic_list[0].mime_type == MimeType.Jpeg
        assert pic_list[0].picture_type == MetaPictureType.FrontCover
        assert pic_list[0].description == "Album Cover"
    
    def test_add_multiple_pictures(self):
        """Test adding multiple pictures to the list."""
        pic_list = MetaPictureList()
        
        pic1 = MetaPicture()
        pic1.mime_type = MimeType.Jpeg
        pic1.picture_type = MetaPictureType.FrontCover
        pic1.bytes = b'\xFF\xD8\xFF\xE0'
        
        pic2 = MetaPicture()
        pic2.mime_type = MimeType.Png
        pic2.picture_type = MetaPictureType.BackCover
        pic2.bytes = b'\x89PNG\r\n\x1a\n'
        
        pic3 = MetaPicture()
        pic3.mime_type = MimeType.Jpeg
        pic3.picture_type = MetaPictureType.Artist
        pic3.bytes = b'\xFF\xD8\xFF\xE1'
        
        pic_list.add(pic1)
        pic_list.add(pic2)
        pic_list.add(pic3)
        
        assert len(pic_list) == 3
        assert pic_list[0].picture_type == MetaPictureType.FrontCover
        assert pic_list[1].picture_type == MetaPictureType.BackCover
        assert pic_list[2].picture_type == MetaPictureType.Artist
    
    def test_immutable_default(self):
        """Test that lists are mutable by default."""
        pic_list = MetaPictureList()
        
        assert not pic_list.immutable
        
        # Should be able to add
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic_list.add(pic)
        
        assert len(pic_list) == 1
    
    def test_immutable_set(self):
        """Test setting immutable state."""
        pic_list = MetaPictureList()
        
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.picture_type = MetaPictureType.FrontCover
        pic_list.add(pic)
        
        # Make immutable
        pic_list.immutable = True
        assert pic_list.immutable
        
        # Pictures should also be immutable
        assert pic_list[0].immutable
        
        # Should not be able to add more
        pic2 = MetaPicture()
        pic2.mime_type = MimeType.Png
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            pic_list.add(pic2)
    
    def test_immutable_propagation(self):
        """Test that immutability propagates to nested pictures."""
        pic_list = MetaPictureList()
        
        pic1 = MetaPicture()
        pic1.mime_type = MimeType.Jpeg
        
        pic2 = MetaPicture()
        pic2.mime_type = MimeType.Png
        
        pic_list.add(pic1)
        pic_list.add(pic2)
        
        # Initially mutable
        assert not pic1.immutable
        assert not pic2.immutable
        
        # Make list immutable
        pic_list.immutable = True
        
        # All pictures should now be immutable
        assert pic1.immutable
        assert pic2.immutable
        
        # Make list mutable again
        pic_list.immutable = False
        
        # Pictures should be mutable again
        assert not pic1.immutable
        assert not pic2.immutable
    
    def test_list_operations(self):
        """Test standard list operations."""
        pic_list = MetaPictureList()
        
        pic1 = MetaPicture()
        pic1.picture_type = MetaPictureType.FrontCover
        
        pic2 = MetaPicture()
        pic2.picture_type = MetaPictureType.BackCover
        
        # Add
        pic_list.add(pic1)
        pic_list.add(pic2)
        assert len(pic_list) == 2
        
        # Index access
        assert pic_list[0].picture_type == MetaPictureType.FrontCover
        assert pic_list[1].picture_type == MetaPictureType.BackCover
        
        # Iteration
        types = [pic.picture_type for pic in pic_list]
        assert types == [MetaPictureType.FrontCover, MetaPictureType.BackCover]
    
    def test_clear_list(self):
        """Test clearing the list."""
        pic_list = MetaPictureList()
        
        for i in range(3):
            pic = MetaPicture()
            pic.mime_type = MimeType.Jpeg
            pic.bytes = bytes([i] * 10)
            pic_list.add(pic)
        
        assert len(pic_list) == 3
        
        pic_list.clear()
        assert len(pic_list) == 0
    
    def test_remove_picture(self):
        """Test removing a picture from the list."""
        pic_list = MetaPictureList()
        
        pic1 = MetaPicture()
        pic1.picture_type = MetaPictureType.FrontCover
        
        pic2 = MetaPicture()
        pic2.picture_type = MetaPictureType.BackCover
        
        pic_list.add(pic1)
        pic_list.add(pic2)
        
        assert len(pic_list) == 2
        
        pic_list.remove(pic1)
        
        assert len(pic_list) == 1
        assert pic_list[0].picture_type == MetaPictureType.BackCover
    
    def test_pop_picture(self):
        """Test popping a picture from the list."""
        pic_list = MetaPictureList()
        
        pic1 = MetaPicture()
        pic1.picture_type = MetaPictureType.FrontCover
        
        pic2 = MetaPicture()
        pic2.picture_type = MetaPictureType.BackCover
        
        pic_list.add(pic1)
        pic_list.add(pic2)
        
        popped = pic_list.pop()
        
        assert popped.picture_type == MetaPictureType.BackCover
        assert len(pic_list) == 1
        assert pic_list[0].picture_type == MetaPictureType.FrontCover
    
    def test_contains(self):
        """Test checking if a picture is in the list."""
        pic_list = MetaPictureList()
        
        pic1 = MetaPicture()
        pic1.picture_type = MetaPictureType.FrontCover
        
        pic2 = MetaPicture()
        pic2.picture_type = MetaPictureType.BackCover
        
        pic_list.add(pic1)
        
        assert pic1 in pic_list
        assert pic2 not in pic_list
    
    def test_empty_list_operations(self):
        """Test operations on an empty list."""
        pic_list = MetaPictureList()
        
        assert len(pic_list) == 0
        assert list(pic_list) == []
    
    def test_common_album_artwork(self):
        """Test creating a common set of album artwork."""
        pic_list = MetaPictureList()
        
        # Front cover
        front = MetaPicture()
        front.mime_type = MimeType.Jpeg
        front.picture_type = MetaPictureType.FrontCover
        front.description = "Front Cover"
        front.bytes = b'\xFF\xD8\xFF\xE0\x00\x10JFIF'
        pic_list.add(front)
        
        # Back cover
        back = MetaPicture()
        back.mime_type = MimeType.Jpeg
        back.picture_type = MetaPictureType.BackCover
        back.description = "Back Cover"
        back.bytes = b'\xFF\xD8\xFF\xE0\x00\x11JFIF'
        pic_list.add(back)
        
        # Artist
        artist = MetaPicture()
        artist.mime_type = MimeType.Png
        artist.picture_type = MetaPictureType.Artist
        artist.description = "Artist Photo"
        artist.bytes = b'\x89PNG\r\n\x1a\n'
        pic_list.add(artist)
        
        assert len(pic_list) == 3
        
        # Verify each picture
        assert pic_list[0].picture_type == MetaPictureType.FrontCover
        assert pic_list[0].mime_type == MimeType.Jpeg
        assert pic_list[1].picture_type == MetaPictureType.BackCover
        assert pic_list[1].mime_type == MimeType.Jpeg
        assert pic_list[2].picture_type == MetaPictureType.Artist
        assert pic_list[2].mime_type == MimeType.Png
    
    def test_multiple_lists_independent(self):
        """Test that multiple lists are independent."""
        list1 = MetaPictureList()
        list2 = MetaPictureList()
        
        pic1 = MetaPicture()
        pic1.picture_type = MetaPictureType.FrontCover
        
        pic2 = MetaPicture()
        pic2.picture_type = MetaPictureType.BackCover
        
        list1.add(pic1)
        list2.add(pic2)
        
        assert len(list1) == 1
        assert len(list2) == 1
        assert list1[0].picture_type == MetaPictureType.FrontCover
        assert list2[0].picture_type == MetaPictureType.BackCover
    
    def test_extend_list(self):
        """Test extending a list with another list."""
        list1 = MetaPictureList()
        list2 = MetaPictureList()
        
        pic1 = MetaPicture()
        pic1.picture_type = MetaPictureType.FrontCover
        
        pic2 = MetaPicture()
        pic2.picture_type = MetaPictureType.BackCover
        
        list1.add(pic1)
        list2.add(pic2)
        
        list1.extend(list2)
        
        assert len(list1) == 2
        assert list1[0].picture_type == MetaPictureType.FrontCover
        assert list1[1].picture_type == MetaPictureType.BackCover
    
    def test_different_image_formats(self):
        """Test pictures with different image formats."""
        pic_list = MetaPictureList()
        
        # JPEG
        jpeg_pic = MetaPicture()
        jpeg_pic.mime_type = MimeType.Jpeg
        jpeg_pic.bytes = b'\xFF\xD8\xFF\xE0'
        pic_list.add(jpeg_pic)
        
        # PNG
        png_pic = MetaPicture()
        png_pic.mime_type = MimeType.Png
        png_pic.bytes = b'\x89PNG\r\n\x1a\n'
        pic_list.add(png_pic)
        
        # GIF
        gif_pic = MetaPicture()
        gif_pic.mime_type = MimeType.Gif
        gif_pic.bytes = b'GIF89a'
        pic_list.add(gif_pic)
        
        # TIFF
        tiff_pic = MetaPicture()
        tiff_pic.mime_type = MimeType.Tiff
        tiff_pic.bytes = b'II*\x00'
        pic_list.add(tiff_pic)
        
        assert len(pic_list) == 4
        assert pic_list[0].mime_type == MimeType.Jpeg
        assert pic_list[1].mime_type == MimeType.Png
        assert pic_list[2].mime_type == MimeType.Gif
        assert pic_list[3].mime_type == MimeType.Tiff
    
    def test_large_image_data(self):
        """Test with larger image data."""
        pic_list = MetaPictureList()
        
        # Create a picture with 1MB of data
        large_data = bytes(range(256)) * 4096  # 1MB
        
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.picture_type = MetaPictureType.FrontCover
        pic.bytes = large_data
        
        pic_list.add(pic)
        
        assert len(pic_list) == 1
        assert len(pic_list[0].bytes) == len(large_data)
    
    def test_all_picture_types(self):
        """Test creating pictures for all picture types."""
        pic_list = MetaPictureList()
        
        picture_types = [
            MetaPictureType.Other,
            MetaPictureType.FileIcon,
            MetaPictureType.FrontCover,
            MetaPictureType.BackCover,
            MetaPictureType.LeafletPage,
            MetaPictureType.Media,
            MetaPictureType.LeadArtist,
            MetaPictureType.Artist,
            MetaPictureType.Conductor,
            MetaPictureType.Band,
            MetaPictureType.Composer,
        ]
        
        for pic_type in picture_types:
            pic = MetaPicture()
            pic.mime_type = MimeType.Jpeg
            pic.picture_type = pic_type
            pic.bytes = bytes([pic_type]) * 10
            pic_list.add(pic)
        
        assert len(pic_list) == len(picture_types)
        
        for i, pic_type in enumerate(picture_types):
            assert pic_list[i].picture_type == pic_type
