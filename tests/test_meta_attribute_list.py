"""
Tests for MetaAttributeList class.
"""

import pytest
from avblocks.meta_attribute import MetaAttribute
from avblocks.meta_attribute_list import MetaAttributeList
from avblocks.constants import Meta


class TestMetaAttributeList:
    """Test cases for MetaAttributeList class."""
    
    def test_create_default(self):
        """Test creating a default MetaAttributeList object."""
        attr_list = MetaAttributeList()
        
        assert attr_list is not None
        assert len(attr_list) == 0
        assert not attr_list.immutable
    
    def test_add_attribute(self):
        """Test adding an attribute to the list."""
        attr_list = MetaAttributeList()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Test Title"
        
        attr_list.add(attr)
        
        assert len(attr_list) == 1
        assert attr_list[0].name == Meta.Title
        assert attr_list[0].value == "Test Title"
    
    def test_add_multiple_attributes(self):
        """Test adding multiple attributes to the list."""
        attr_list = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Song Title"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist Name"
        
        attr3 = MetaAttribute()
        attr3.name = Meta.Album
        attr3.value = "Album Name"
        
        attr_list.add(attr1)
        attr_list.add(attr2)
        attr_list.add(attr3)
        
        assert len(attr_list) == 3
        assert attr_list[0].name == Meta.Title
        assert attr_list[1].name == Meta.AlbumArtist
        assert attr_list[2].name == Meta.Album
    
    def test_item_by_name(self):
        """Test finding an attribute by name."""
        attr_list = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Song Title"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist Name"
        
        attr_list.add(attr1)
        attr_list.add(attr2)
        
        # Find existing attribute
        found = attr_list.item_by_name(Meta.Title)
        assert found is not None
        assert found.name == Meta.Title
        assert found.value == "Song Title"
        
        # Find another existing attribute
        found = attr_list.item_by_name(Meta.AlbumArtist)
        assert found is not None
        assert found.name == Meta.AlbumArtist
        assert found.value == "Artist Name"
        
        # Try to find non-existent attribute
        found = attr_list.item_by_name(Meta.Genre)
        assert found is None
    
    def test_item_by_name_empty_list(self):
        """Test finding an attribute by name in an empty list."""
        attr_list = MetaAttributeList()
        
        found = attr_list.item_by_name(Meta.Title)
        assert found is None
    
    def test_item_by_name_first_match(self):
        """Test that item_by_name returns the first matching attribute."""
        attr_list = MetaAttributeList()
        
        # Add two attributes with the same name
        attr1 = MetaAttribute()
        attr1.name = Meta.Comment
        attr1.value = "First Comment"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.Comment
        attr2.value = "Second Comment"
        
        attr_list.add(attr1)
        attr_list.add(attr2)
        
        # Should return the first one
        found = attr_list.item_by_name(Meta.Comment)
        assert found is not None
        assert found.value == "First Comment"
    
    def test_immutable_default(self):
        """Test that lists are mutable by default."""
        attr_list = MetaAttributeList()
        
        assert not attr_list.immutable
        
        # Should be able to add
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Test"
        attr_list.add(attr)
        
        assert len(attr_list) == 1
    
    def test_immutable_set(self):
        """Test setting immutable state."""
        attr_list = MetaAttributeList()
        
        attr = MetaAttribute()
        attr.name = Meta.Title
        attr.value = "Test"
        attr_list.add(attr)
        
        # Make immutable
        attr_list.immutable = True
        assert attr_list.immutable
        
        # Attributes should also be immutable
        assert attr_list[0].immutable
        
        # Should not be able to add more
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist"
        
        with pytest.raises(RuntimeError, match="Object is immutable"):
            attr_list.add(attr2)
    
    def test_immutable_propagation(self):
        """Test that immutability propagates to nested attributes."""
        attr_list = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Title"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist"
        
        attr_list.add(attr1)
        attr_list.add(attr2)
        
        # Initially mutable
        assert not attr1.immutable
        assert not attr2.immutable
        
        # Make list immutable
        attr_list.immutable = True
        
        # All attributes should now be immutable
        assert attr1.immutable
        assert attr2.immutable
        
        # Make list mutable again
        attr_list.immutable = False
        
        # Attributes should be mutable again
        assert not attr1.immutable
        assert not attr2.immutable
    
    def test_list_operations(self):
        """Test standard list operations."""
        attr_list = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Title 1"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist 1"
        
        # Add
        attr_list.add(attr1)
        attr_list.add(attr2)
        assert len(attr_list) == 2
        
        # Index access
        assert attr_list[0].name == Meta.Title
        assert attr_list[1].name == Meta.AlbumArtist
        
        # Iteration
        names = [attr.name for attr in attr_list]
        assert names == [Meta.Title, Meta.AlbumArtist]
    
    def test_clear_list(self):
        """Test clearing the list."""
        attr_list = MetaAttributeList()
        
        for i in range(3):
            attr = MetaAttribute()
            attr.name = Meta.Title
            attr.value = f"Title {i}"
            attr_list.add(attr)
        
        assert len(attr_list) == 3
        
        attr_list.clear()
        assert len(attr_list) == 0
    
    def test_remove_attribute(self):
        """Test removing an attribute from the list."""
        attr_list = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Title 1"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist 1"
        
        attr_list.add(attr1)
        attr_list.add(attr2)
        
        assert len(attr_list) == 2
        
        attr_list.remove(attr1)
        
        assert len(attr_list) == 1
        assert attr_list[0].name == Meta.AlbumArtist
    
    def test_pop_attribute(self):
        """Test popping an attribute from the list."""
        attr_list = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Title 1"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist 1"
        
        attr_list.add(attr1)
        attr_list.add(attr2)
        
        popped = attr_list.pop()
        
        assert popped.name == Meta.AlbumArtist
        assert len(attr_list) == 1
        assert attr_list[0].name == Meta.Title
    
    def test_contains(self):
        """Test checking if an attribute is in the list."""
        attr_list = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Title 1"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist 1"
        
        attr_list.add(attr1)
        
        assert attr1 in attr_list
        assert attr2 not in attr_list
    
    def test_empty_list_operations(self):
        """Test operations on an empty list."""
        attr_list = MetaAttributeList()
        
        assert len(attr_list) == 0
        assert list(attr_list) == []
        
        found = attr_list.item_by_name(Meta.Title)
        assert found is None
    
    def test_common_metadata_set(self):
        """Test creating a common set of metadata attributes."""
        attr_list = MetaAttributeList()
        
        metadata = [
            (Meta.Title, "My Song"),
            (Meta.AlbumArtist, "John Doe"),
            (Meta.Album, "Greatest Hits"),
            (Meta.Year, "2024"),
            (Meta.TrackNum, "5"),
            (Meta.Genre, "Rock"),
            (Meta.Comment, "Great song!"),
        ]
        
        for name, value in metadata:
            attr = MetaAttribute()
            attr.name = name
            attr.value = value
            attr_list.add(attr)
        
        assert len(attr_list) == 7
        
        # Verify we can find each one
        for name, value in metadata:
            found = attr_list.item_by_name(name)
            assert found is not None
            assert found.value == value
    
    def test_multiple_lists_independent(self):
        """Test that multiple lists are independent."""
        list1 = MetaAttributeList()
        list2 = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Title 1"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist 1"
        
        list1.add(attr1)
        list2.add(attr2)
        
        assert len(list1) == 1
        assert len(list2) == 1
        assert list1[0].name == Meta.Title
        assert list2[0].name == Meta.AlbumArtist
    
    def test_extend_list(self):
        """Test extending a list with another list."""
        list1 = MetaAttributeList()
        list2 = MetaAttributeList()
        
        attr1 = MetaAttribute()
        attr1.name = Meta.Title
        attr1.value = "Title 1"
        
        attr2 = MetaAttribute()
        attr2.name = Meta.AlbumArtist
        attr2.value = "Artist 1"
        
        list1.add(attr1)
        list2.add(attr2)
        
        list1.extend(list2)
        
        assert len(list1) == 2
        assert list1[0].name == Meta.Title
        assert list1[1].name == Meta.AlbumArtist
