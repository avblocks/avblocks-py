"""
MetaAttribute class for AVBlocks Python bindings.
"""

from typing import Optional
import ctypes

from .native import get_native
from .immutable import IImmutable
from .string_util import decode_utf16le_string, encode_utf16le_string


class MetaAttribute(IImmutable):
    """
    MetaAttribute describes a metadata attribute (tag) that is part of an audio or video file.
    """
    
    def __init__(self):
        """Creates a MetaAttribute object."""
        self._name: Optional[str] = None
        self._value: Optional[str] = None
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
        """Set the immutable state."""
        self._immutable = value
    
    @property
    def name(self) -> Optional[str]:
        """
        Attribute name (tag).
        
        See the Meta class for common attribute names.
        """
        return self._name
    
    @name.setter
    def name(self, value: Optional[str]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._name = value
    
    @property
    def value(self) -> Optional[str]:
        """
        Attribute value as a free text.
        """
        return self._value
    
    @value.setter
    def value(self, val: Optional[str]):
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._value = val
    
    # pylint: disable=[protected-access]
    def clone(self) -> 'MetaAttribute':
        """
        Creates a deep copy of this object.
        
        Returns:
            A new MetaAttribute object
        """
        attribute = MetaAttribute()
        attribute._name = self._name
        attribute._value = self._value
        attribute._immutable = False
        
        return attribute
    
    def _to_native(self) -> ctypes.c_void_p:
        """Create a native MetaAttribute object from this instance."""
        
        lib = get_native().lib
        native_attr = lib.avb_create_meta_attribute()
        
        if self._name:
            lib.MetaAttribute_setName(native_attr, self._name.encode('utf-8'))
        
        if self._value:
            # Use the existing string utility for UTF-16-LE encoding
            value_ptr = encode_utf16le_string(self._value)
            lib.MetaAttribute_setValue(native_attr, value_ptr)
        
        return native_attr
    
    def _copy_from_native(self, native_attr: ctypes.c_void_p):
        """Copy properties from a native MetaAttribute object."""
        if not native_attr:
            return
        
        lib = get_native().lib
        
        # Get name (UTF-8)
        name_ptr = lib.MetaAttribute_name(native_attr)
        if name_ptr:
            self._name = ctypes.string_at(name_ptr).decode('utf-8')
        
        # Get value (UTF-16-LE) - use existing string utility
        value_ptr = lib.MetaAttribute_value(native_attr)
        if value_ptr:
            self._value = decode_utf16le_string(value_ptr)
    
    @staticmethod
    def _from_native(native: ctypes.c_void_p) -> Optional['MetaAttribute']:
        """Create a MetaAttribute object from a native MetaAttribute pointer."""
        if not native:
            return None
        
        attribute = MetaAttribute()
        attribute._copy_from_native(native)
        return attribute
