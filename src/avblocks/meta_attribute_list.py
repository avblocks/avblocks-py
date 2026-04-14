"""
MetaAttributeList collection for AVBlocks Python bindings.
"""

from typing import Optional, Union
import ctypes

from .native import get_native
from .object_collection import ObjectCollection
from .meta_attribute import MetaAttribute


class MetaAttributeList(ObjectCollection[MetaAttribute]):
    """Collection of MetaAttribute objects."""

    def __getitem__(self, key: Union[int, str]):
        """
        Get an item by index or by attribute name.

        Args:
            key: An integer index to return the MetaAttribute at that position,
                 or a string attribute name (e.g. Meta.Title) to return the
                 value of the first matching attribute.

        Returns:
            MetaAttribute when key is an int; the attribute value string when
            key is a str.

        Raises:
            KeyError: When key is a string and no matching attribute is found.
        """
        if isinstance(key, str):
            attr = self.item_by_name(key)
            if attr is None:
                raise KeyError(key)
            return attr.value
        return super().__getitem__(key)

    def item_by_name(self, name: str) -> Optional[MetaAttribute]:
        """
        Find an attribute by name.
        
        Args:
            name: The attribute name to search for
            
        Returns:
            The MetaAttribute with the specified name, or None if not found
        """
        for attr in self:
            if attr.name == name:
                return attr
        return None

    # pylint: disable=protected-access
    def to_native(self, native_attrs: ctypes.c_void_p):
        """
        Add all attributes from this Python list to the provided native MetaAttributeList pointer.
        The native_attrs should be obtained via lib.Metadata_attributes(native_metadata).
        """
        if not native_attrs:
            return

        lib = get_native().lib
        for attr in self:
            native_attr = attr._to_native()
            lib.MetaAttributeList_add(native_attrs, native_attr)
            lib.Reference_release(native_attr)

    # pylint: disable=protected-access
    @staticmethod
    def from_native(native_attrs: ctypes.c_void_p) -> 'MetaAttributeList':
        """
        Create a Python MetaAttributeList from a native MetaAttributeList pointer.
        """
        attrs = MetaAttributeList()
        if not native_attrs:
            return attrs

        lib = get_native().lib
        count = lib.MetaAttributeList_count(native_attrs)
        for i in range(count):
            native_attr = lib.MetaAttributeList_at(native_attrs, i)
            attr = MetaAttribute._from_native(native_attr)
            if attr is not None:
                attrs.add(attr)

        return attrs
