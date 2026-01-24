"""
Metadata class for AVBlocks Python bindings.
"""

from typing import Optional
import ctypes

from .native import get_native
from .immutable import IImmutable
from .meta_attribute_list import MetaAttributeList
from .meta_picture_list import MetaPictureList


class Metadata(IImmutable):
    """
    Metadata describes meta information that is part of an audio or video file.
    
    It can hold various textual information and images.
    """
    
    def __init__(self):
        """Creates a Metadata object."""
        self._attributes: MetaAttributeList = MetaAttributeList()
        self._pictures: MetaPictureList = MetaPictureList()
        self._immutable: bool = False
    
    @property
    def immutable(self) -> bool:
        """
        Returns whether the object is immutable.
        An immutable object cannot be modified and all modifying methods fail to produce a result.
        
        An immutable object can be modified by the AVBlocks library.
        Object immutability spreads to all nested objects.
        Therefore it is not possible to add/set an immutable object to a mutable object.
        When cloned an immutable object becomes mutable.
        """
        return self._immutable
    
    @immutable.setter
    def immutable(self, value: bool):
        """Set the immutable state and propagate to nested objects."""
        self._attributes.immutable = value
        self._pictures.immutable = value
        self._immutable = value
    
    @property
    def attributes(self) -> MetaAttributeList:
        """
        A modifiable collection with all metadata attributes.
        
        The default value of this property is an empty collection which can be modified 
        but it cannot be replaced.
        """
        return self._attributes
    
    @property
    def pictures(self) -> MetaPictureList:
        """
        A modifiable collection with all metadata pictures.
        
        The default value of this property is an empty collection which can be modified 
        but it cannot be replaced.
        """
        return self._pictures
    
    # pylint: disable=[protected-access]
    def clone(self) -> 'Metadata':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new Metadata object
        """
        metadata = Metadata()
        metadata._immutable = False
        
        # Deep copy attributes
        for attr in self._attributes:
            metadata._attributes.add(attr.clone())
        
        # Deep copy pictures
        for pic in self._pictures:
            metadata._pictures.add(pic.clone())
        
        return metadata
    
    def _to_native(self) -> ctypes.c_void_p:
        """Create a native Metadata object from this instance."""
        
        lib = get_native().lib
        native_meta = lib.avb_create_metadata()
        
        # Get native attribute and picture lists
        native_attrib_list = lib.Metadata_attributes(native_meta)
        native_picture_list = lib.Metadata_pictures(native_meta)
        
        # Populate attributes
        self._attributes.to_native(native_attrib_list)
        
        # Populate pictures
        self._pictures.to_native(native_picture_list)
        
        return native_meta
    
    @staticmethod
    def _from_native(native_meta: ctypes.c_void_p) -> Optional['Metadata']:
        """Create a Metadata object from a native Metadata pointer."""
        if not native_meta:
            return None
        
        lib = get_native().lib
        metadata = Metadata()
        
        # Get attributes
        native_attrib_list = lib.Metadata_attributes(native_meta)
        if native_attrib_list:
            metadata._attributes = MetaAttributeList.from_native(native_attrib_list)
        
        # Get pictures
        native_picture_list = lib.Metadata_pictures(native_meta)
        if native_picture_list:
            metadata._pictures = MetaPictureList.from_native(native_picture_list)
        
        return metadata
