"""
Tests for MetaAttribute class.
"""

import pytest
from avblocks.meta_attribute import MetaAttribute
from avblocks.constants import Meta


class TestMetaAttribute:
    """Test cases for MetaAttribute class."""
    
    def test_create_default(self):
        """Test creating a default MetaAttribute object."""
        attr = MetaAttribute()
        
        assert attr is not None
        assert attr.name is None
        assert attr.value is None
        assert not attr.immutable
    
    def test_set_name(self):
        """Test setting attribute name."""
        attr = MetaAttribute()
        
        attr.name = Meta.Title
        assert attr.name == Meta.Title
        
        attr.name = Meta.AlbumArtist
        assert attr.name == Meta.AlbumArtist
    
    def test_set_value(self):
        """Test setting attribute value."""
        attr = MetaAttribute()
        
        attr.value = "My Song Title"
        assert attr.value == "My Song Title"
        
        # Test Unicode value
        attr.value = "歌曲标题 - Song Title"
        assert attr.value == "歌曲标题 - Song Title"
    
    def test_set_name_and_value(self):
        """Test setting both name and value."""
        attr = MetaAttribute()
        
        attr.name = Meta.Title
        attr.value = "Amazing Song"
        
        assert attr.name == Meta.Title
        assert attr.value == "Amazing Song"
    
    def test_common_metadata_attributes(self):
        """Test setting various common metadata attributes."""
        test_cases = [
            (Meta.Title, "Song Title"),
            (Meta.AlbumArtist, "Artist Name"),
            (Meta.Album, "Album Name"),
            (Meta.Genre, "Rock"),
            (Meta.Year, "2024"),
            (Meta.TrackNum, "5"),
            (Meta.Comment, "Great song!"),
            (Meta.Copyright, "Copyright 2024"),
            (Meta.Composer, "John Doe"),
            (Meta.Publisher, "Music Publisher Inc."),
        ]
        
        for name, value in test_cases:
            attr = MetaAttribute()
            attr.name = name
            attr.value = value
            
            assert attr.name == name
            assert attr.value == value
    
    def test_immutable_default(self):
        """Test that objects are mutable by default."""
        attr = MetaAttribute()
        
        assert not attr.immutable
        
        # Should be able to modify
        attr.name = Meta.Title
        attr.value = "Test"
        assert attr.name == Meta.Title
        assert attr.value == "Test"
    
    def test_immutable_set(self):
        """Test setting immutable state."""
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Original"
        
        # Make immutable
        attr.immutable = True
        assert attr.immutable
        
        # Should not be able to modify name
        with pytest.raises(RuntimeError, match="Object is immutable"):
            attr.name = Meta.AlbumArtist
        
        # Should not be able to modify value
        with pytest.raises(RuntimeError, match="Object is immutable"):
            attr.value = "Modified"
        
        # Original values should remain
        assert attr.name == Meta.Title
        assert attr.value == "Original"
    
    def test_clone(self):
        """Test cloning a MetaAttribute object."""
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Original Title"
        
        # Clone the object
        attr2 = attr1.clone()
        
        # Verify properties are copied
        assert attr2.name == attr1.name
        assert attr2.value == attr1.value
        
        # Verify it's a different object
        assert attr2 is not attr1
        
        # Verify clone is mutable even if original is immutable
        attr1.immutable = True
        attr3 = attr1.clone()
        assert not attr3.immutable
        attr3.name = Meta.AlbumArtist
        attr3.value = "New Artist"
        assert attr3.name == Meta.AlbumArtist
        assert attr3.value == "New Artist"
    
    def test_clone_empty_values(self):
        """Test cloning when values are None."""
        attr1 = MetaAttribute()
        attr1.name = None
        attr1.value = None
        
        attr2 = attr1.clone()
        
        assert attr2.name is None
        assert attr2.value is None
    
    def test_modify_after_clone(self):
        """Test that modifying a clone doesn't affect the original."""
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Original"
        
        attr2 = attr1.clone()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Modified"
        
        # Original should be unchanged
        assert attr1.name == Meta.Title
        assert attr1.value == "Original"
        
        # Clone should be modified
        assert attr2.name == Meta.AlbumArtist
        assert attr2.value == "Modified"
    
    def test_empty_string_name(self):
        """Test with empty string name."""
        attr = MetaAttribute()
        
        attr.name = ""
        assert attr.name == ""
    
    def test_empty_string_value(self):
        """Test with empty string value."""
        attr = MetaAttribute()
        
        attr.value = ""
        assert attr.value == ""
    
    def test_none_values(self):
        """Test setting None values."""
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Title"
        
        # Set to None
        attr.name = None
        attr.value = None
        
        assert attr.name is None
        assert attr.value is None
    
    def test_long_value(self):
        """Test with a long value string."""
        attr = MetaAttribute()
        
        long_value = "A" * 1000
        attr.value = long_value
        
        assert attr.value == long_value
        assert len(attr.value) == 1000
    
    def test_unicode_name_and_value(self):
        """Test with Unicode characters in both name and value."""
        attr = MetaAttribute()
        
        # Unicode name (custom attribute)
        attr.name = "title123"
        attr.value = "Здравей - Bulgarian Song Title"
        
        assert attr.name == "title123"
        assert attr.value == "Здравей - Bulgarian Song Title"
    
    def test_special_characters_in_value(self):
        """Test with special characters in value."""
        attr = MetaAttribute()
        attr.name = Meta.Comment
        
        special_chars = "Test with <special> & 'characters' \"quoted\" \n\t\r"
        attr.value = special_chars
        
        assert attr.value == special_chars
    
    def test_multiple_attributes(self):
        """Test creating multiple independent attributes."""
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Title 1"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist 1"
        
        attr3 = MetaAttribute()
        attr3.name = Meta.Album
        attr3.value = "Album 1"
        
        # Verify they are independent
        assert attr1.name == Meta.Title
        assert attr1.value == "Title 1"
        assert attr2.name == Meta.AlbumArtist
        assert attr2.value == "Artist 1"
        assert attr3.name == Meta.Album
        assert attr3.value == "Album 1"
    
    def test_url_attributes(self):
        """Test URL-type metadata attributes."""
        test_cases = [
            (Meta.UrlArtist, "https://artist.example.com"),
            (Meta.UrlPublisher, "https://publisher.example.com"),
            (Meta.UrlCommercialInfo, "https://buy.example.com"),
            (Meta.UrlCopyright, "https://copyright.example.com"),
        ]
        
        for name, value in test_cases:
            attr = MetaAttribute()
            attr.name = name
            attr.value = value
            
            assert attr.name == name
            assert attr.value == value
    
    def test_numeric_string_values(self):
        """Test with numeric values stored as strings."""
        test_cases = [
            (Meta.Year, "2024"),
            (Meta.TrackNum, "12"),
            (Meta.DiscNum, "2"),
            (Meta.BeatsPerMinute, "120"),
        ]
        
        for name, value in test_cases:
            attr = MetaAttribute()
            attr.name = name
            attr.value = value
            
            assert attr.name == name
            assert attr.value == value
