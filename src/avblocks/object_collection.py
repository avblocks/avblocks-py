"""
ObjectCollection base class for AVBlocks Python bindings.
An ordered collection of items used in AVBlocks.
"""

from typing import TypeVar, Generic
from .immutable import IImmutable


T = TypeVar('T')


class ObjectCollection(list, IImmutable, Generic[T]):
    """
    An ordered collection of items used in AVBlocks.
    Implements the list interface with immutability support.
    """

    def __init__(self):
        super().__init__()
        self._immutable = False

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
        # Propagate to all items in the collection
        for item in self:
            if isinstance(item, IImmutable):
                item.immutable = value
        self._immutable = value

    def _check_item_immutable(self, item: T) -> bool:
        """Check if an item is immutable."""
        return isinstance(item, IImmutable) and item.immutable

    def add(self, item: T):
        """Add an item to the collection."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        if self._check_item_immutable(item):
            raise RuntimeError("Cannot add immutable object to collection")
        self.append(item)

    # Override list methods to enforce immutability
    def append(self, item: T):
        """Append an item to the end of the list."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        if self._check_item_immutable(item):
            raise RuntimeError("Cannot add immutable object to collection")
        super().append(item)

    def extend(self, iterable):
        """Extend the list by appending elements from the iterable."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        for item in iterable:
            if self._check_item_immutable(item):
                raise RuntimeError("Cannot add immutable object to collection")
        super().extend(iterable)

    def insert(self, index: int, item: T):
        """Insert an item at the specified index."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        if self._check_item_immutable(item):
            raise RuntimeError("Cannot add immutable object to collection")
        super().insert(index, item)

    def remove(self, item: T):
        """Remove the first occurrence of an item."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        super().remove(item)

    def pop(self, index: int = -1):
        """Remove and return an item at the specified index."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        return super().pop(index)

    def clear(self):
        """Remove all items from the list."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        super().clear()

    def __setitem__(self, index, item):
        """Set item at index."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        if self._check_item_immutable(item):
            raise RuntimeError("Cannot add immutable object to collection")
        super().__setitem__(index, item)

    def __delitem__(self, index):
        """Delete item at index."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        super().__delitem__(index)

    def __iadd__(self, other):
        """In-place addition (+=)."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        for item in other:
            if self._check_item_immutable(item):
                raise RuntimeError("Cannot add immutable object to collection")
        return super().__iadd__(other)

    def __imul__(self, other):
        """In-place multiplication (*=)."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        return super().__imul__(other)
