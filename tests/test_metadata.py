"""
Tests for Metadata class.
"""

import pytest
from avblocks.metadata import Metadata
from avblocks.meta_attribute import MetaAttribute
from avblocks.meta_picture import MetaPicture
from avblocks.constants import Meta, MetaPictureType, MimeType


class TestMetadata:
    """Test cases for Metadata class."""
    
    def test_create_default(self):
        """Test creating a default Metadata object."""
        metadata = Metadata()
        
        assert metadata is not None
        assert metadata.attributes is not None
        assert metadata.pictures is not None
        assert len(metadata.attributes) == 0
        assert len(metadata.pictures) == 0
        assert not metadata.immutable
    
    def test_add_attributes(self):
        """Test adding attributes to metadata."""
        metadata = Metadata()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "My Song"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist Name"
        
        metadata.attributes.add(attr1)
        metadata.attributes.add(attr2)
        
        assert len(metadata.attributes) == 2
        assert metadata.attributes[0].name == Meta.Title
        assert metadata.attributes[0].value == "My Song"
        assert metadata.attributes[1].name == Meta.AlbumArtist
        assert metadata.attributes[1].value == "Artist Name"
    
    def test_add_pictures(self):
        """Test adding pictures to metadata."""
        metadata = Metadata()
        
        pic1 = MetaPicture()
        pic1.mime_type = MimeType.Jpeg
        pic1.picture_type = MetaPictureType.FrontCover
        pic1.bytes = b'\xFF\xD8\xFF\xE0'
        
        pic2 = MetaPicture()
        pic2.mime_type = MimeType.Png
        pic2.picture_type = MetaPictureType.BackCover
        pic2.bytes = b'\x89PNG\r\n\x1a\n'
        
        metadata.pictures.add(pic1)
        metadata.pictures.add(pic2)
        
        assert len(metadata.pictures) == 2
        assert metadata.pictures[0].picture_type == MetaPictureType.FrontCover
        assert metadata.pictures[1].picture_type == MetaPictureType.BackCover
    
    def test_add_both_attributes_and_pictures(self):
        """Test adding both attributes and pictures."""
        metadata = Metadata()
        
        # Add attributes
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Album Title"
        metadata.attributes.add(attr)
        
        # Add picture
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.picture_type = MetaPictureType.FrontCover
        metadata.pictures.add(pic)
        
        assert len(metadata.attributes) == 1
        assert len(metadata.pictures) == 1
    
    def test_immutable_default(self):
        """Test that metadata is mutable by default."""
        metadata = Metadata()
        
        assert not metadata.immutable
        
        # Should be able to add
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Test"
        metadata.attributes.add(attr)
        
        assert len(metadata.attributes) == 1
    
    def test_immutable_set(self):
        """Test setting immutable state."""
        metadata = Metadata()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Test"
        metadata.attributes.add(attr)
        
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        metadata.pictures.add(pic)
        
        # Make immutable
        metadata.immutable = True
        assert metadata.immutable
        
        # Nested collections should also be immutable
        assert metadata.attributes.immutable
        assert metadata.pictures.immutable
        
        # Nested items should also be immutable
        assert metadata.attributes[0].immutable
        assert metadata.pictures[0].immutable
        
        # Should not be able to add more
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            metadata.attributes.add(attr2)
    
    def test_immutable_propagation(self):
        """Test that immutability propagates to all nested objects."""
        metadata = Metadata()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Title"
        metadata.attributes.add(attr)
        
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        metadata.pictures.add(pic)
        
        # Initially mutable
        assert not metadata.immutable
        assert not metadata.attributes.immutable
        assert not metadata.pictures.immutable
        assert not attr.immutable
        assert not pic.immutable
        
        # Make immutable
        metadata.immutable = True
        
        # Everything should be immutable
        assert metadata.immutable
        assert metadata.attributes.immutable
        assert metadata.pictures.immutable
        assert metadata.attributes[0].immutable
        assert metadata.pictures[0].immutable
        
        # Make mutable again
        metadata.immutable = False
        
        # Everything should be mutable
        assert not metadata.immutable
        assert not metadata.attributes.immutable
        assert not metadata.pictures.immutable
        assert not metadata.attributes[0].immutable
        assert not metadata.pictures[0].immutable
    
    def test_clone(self):
        """Test cloning a Metadata object."""
        meta1 = Metadata()
        
        # Add attributes
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Original Title"
        meta1.attributes.add(attr1)
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Original Artist"
        meta1.attributes.add(attr2)
        
        # Add pictures
        pic1 = MetaPicture()
        pic1.mime_type = MimeType.Jpeg
        pic1.picture_type = MetaPictureType.FrontCover
        pic1.bytes = b'\xFF\xD8\xFF\xE0'
        meta1.pictures.add(pic1)
        
        # Clone
        meta2 = meta1.clone()
        
        # Verify it's a different object
        assert meta2 is not meta1
        assert meta2.attributes is not meta1.attributes
        assert meta2.pictures is not meta1.pictures
        
        # Verify content is copied
        assert len(meta2.attributes) == 2
        assert len(meta2.pictures) == 1
        assert meta2.attributes[0].name == Meta.Title
        assert meta2.attributes[0].value == "Original Title"
        assert meta2.attributes[1].name == Meta.AlbumArtist
        assert meta2.pictures[0].picture_type == MetaPictureType.FrontCover
        
        # Verify deep copy - items are different objects
        assert meta2.attributes[0] is not meta1.attributes[0]
        assert meta2.pictures[0] is not meta1.pictures[0]
        
        # Verify clone is mutable
        assert not meta2.immutable
    
    def test_clone_immutable(self):
        """Test that cloning an immutable object produces a mutable clone."""
        meta1 = Metadata()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Title"
        meta1.attributes.add(attr)
        
        # Make immutable
        meta1.immutable = True
        assert meta1.immutable
        
        # Clone
        meta2 = meta1.clone()
        
        # Clone should be mutable
        assert not meta2.immutable
        assert not meta2.attributes.immutable
        assert not meta2.attributes[0].immutable
        
        # Should be able to modify clone
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist"
        meta2.attributes.add(attr2)
        
        assert len(meta2.attributes) == 2
    
    def test_modify_after_clone(self):
        """Test that modifying a clone doesn't affect the original."""
        meta1 = Metadata()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Original"
        meta1.attributes.add(attr)
        
        meta2 = meta1.clone()
        
        # Modify clone
        meta2.attributes[0].value = "Modified"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "New Artist"
        meta2.attributes.add(attr2)
        
        # Original should be unchanged
        assert len(meta1.attributes) == 1
        assert meta1.attributes[0].value == "Original"
        
        # Clone should be modified
        assert len(meta2.attributes) == 2
        assert meta2.attributes[0].value == "Modified"
    
    def test_common_audio_metadata(self):
        """Test creating common audio metadata."""
        metadata = Metadata()
        
        # Add common attributes
        common_tags = [
            (Meta.Title, "Song Title"),
            (Meta.AlbumArtist, "Artist Name"),
            (Meta.Album, "Album Name"),
            (Meta.Year, "2024"),
            (Meta.TrackNum, "5"),
            (Meta.Genre, "Rock"),
            (Meta.Comment, "Great song!"),
            (Meta.Copyright, "Copyright 2024"),
        ]
        
        for name, value in common_tags:
            attr = MetaAttribute()
            attr.name = name
            attr.value = value
            metadata.attributes.add(attr)
        
        # Add album artwork
        cover = MetaPicture()
        cover.mime_type = MimeType.Jpeg
        cover.picture_type = MetaPictureType.FrontCover
        cover.description = "Album Cover"
        cover.bytes = b'\xFF\xD8\xFF\xE0\x00\x10JFIF'
        metadata.pictures.add(cover)
        
        assert len(metadata.attributes) == 8
        assert len(metadata.pictures) == 1
        
        # Verify we can find attributes by name
        title = metadata.attributes.item_by_name(Meta.Title)
        assert title is not None
        assert title.value == "Song Title"
    
    def test_empty_metadata(self):
        """Test metadata with no attributes or pictures."""
        metadata = Metadata()
        
        assert len(metadata.attributes) == 0
        assert len(metadata.pictures) == 0
        
        # Clone empty metadata
        meta2 = metadata.clone()
        assert len(meta2.attributes) == 0
        assert len(meta2.pictures) == 0
    
    def test_attributes_collection_cannot_be_replaced(self):
        """Test that attributes collection reference cannot be replaced."""
        metadata = Metadata()
        
        # Get reference to attributes
        attrs1 = metadata.attributes
        
        # Add an attribute
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Test"
        attrs1.add(attr)
        
        # Verify it's the same collection
        assert metadata.attributes is attrs1
        assert len(metadata.attributes) == 1
    
    def test_pictures_collection_cannot_be_replaced(self):
        """Test that pictures collection reference cannot be replaced."""
        metadata = Metadata()
        
        # Get reference to pictures
        pics1 = metadata.pictures
        
        # Add a picture
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pics1.add(pic)
        
        # Verify it's the same collection
        assert metadata.pictures is pics1
        assert len(metadata.pictures) == 1
    
    def test_unicode_in_metadata(self):
        """Test metadata with Unicode characters."""
        metadata = Metadata()
        
        # Add Unicode attribute
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Песен - Song Title Здравей"
        metadata.attributes.add(attr)
        
        # Add Unicode picture description
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.description = "Песен Обложка"
        pic.bytes = b'\xFF\xD8\xFF\xE0'
        metadata.pictures.add(pic)
        
        assert metadata.attributes[0].value == "Песен - Song Title Здравей"
        assert metadata.pictures[0].description == "Песен Обложка"
    
    def test_multiple_pictures_same_type(self):
        """Test metadata with multiple pictures of the same type."""
        metadata = Metadata()
        
        # Add multiple artist photos
        for i in range(3):
            pic = MetaPicture()
            pic.mime_type = MimeType.Jpeg
            pic.picture_type = MetaPictureType.Artist
            pic.description = f"Artist Photo {i+1}"
            pic.bytes = bytes([i]) * 10
            metadata.pictures.add(pic)
        
        assert len(metadata.pictures) == 3
        for i in range(3):
            assert metadata.pictures[i].picture_type == MetaPictureType.Artist
    
    def test_clone_with_large_data(self):
        """Test cloning metadata with large picture data."""
        meta1 = Metadata()
        
        # Add picture with large data
        pic = MetaPicture()
        pic.mime_type = MimeType.Jpeg
        pic.bytes = bytes(range(256)) * 1024  # 256KB
        meta1.pictures.add(pic)
        
        # Clone
        meta2 = meta1.clone()
        
        # Verify data is copied
        assert len(meta2.pictures) == 1
        assert len(meta2.pictures[0].bytes) == len(pic.bytes)
        
        # Verify it's a different bytes object
        assert meta2.pictures[0].bytes is not meta1.pictures[0].bytes
