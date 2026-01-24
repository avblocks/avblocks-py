"""
ParameterList implementation for AVBlocks Python bindings.
A name-value collection used for passing parameters to different AVBlocks components.
"""

from typing import Dict, Any, Iterator, KeysView, ValuesView, ItemsView
from collections.abc import MutableMapping


class ParameterList(MutableMapping[str, Any]):
    """
    A name-value collection used for passing parameters to different AVBlocks components.
    
    This class implements a dictionary-like interface and supports immutability.
    An immutable object cannot be modified and all modifying methods will raise RuntimeError.
    """
    
    def __init__(self):
        self._dict: Dict[str, Any] = {}
        self._immutable: bool = False
    
    @property
    def immutable(self) -> bool:
        """
        Returns whether the object is immutable.
        An immutable object cannot be modified and all modifying methods fail to produce a result.
        
        Notes:
            - An immutable object can be modified by the AVBlocks library.
            - Object immutability spreads to all nested objects.
            - Therefore it is not possible to add/set an immutable object to a mutable object.
            - When cloned an immutable object becomes mutable.
        """
        return self._immutable
    
    @immutable.setter
    def immutable(self, value: bool):
        """Set the immutable flag."""
        self._immutable = value
    
    def __getitem__(self, key: str) -> Any:
        """Gets the element with the specified key."""
        return self._dict[key]
    
    def __setitem__(self, key: str, value: Any):
        """Sets the element with the specified key."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._dict[key] = value
    
    def __delitem__(self, key: str):
        """Removes the element with the specified key."""
        if self._immutable:
            raise RuntimeError("Object is immutable")
        del self._dict[key]
    
    def __iter__(self) -> Iterator[str]:
        """Returns an iterator over the keys."""
        return iter(self._dict)
    
    def __len__(self) -> int:
        """Gets the number of elements contained in the ParameterList."""
        return len(self._dict)
    
    def __contains__(self, key: object) -> bool:
        """Determines whether the ParameterList contains an element with the specified key."""
        return key in self._dict
    
    def keys(self) -> KeysView[str]:
        """Gets a collection containing the keys of the ParameterList."""
        return self._dict.keys()
    
    def values(self) -> ValuesView[Any]:
        """Gets a collection containing the values in the ParameterList."""
        return self._dict.values()
    
    def items(self) -> ItemsView[str, Any]:
        """Gets a collection containing the key-value pairs in the ParameterList."""
        return self._dict.items()
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Gets the value associated with the specified key.
        
        Args:
            key: The key whose value to get.
            default: The default value to return if key is not found.
            
        Returns:
            The value associated with the specified key, or default if key is not found.
        """
        return self._dict.get(key, default)
    
    def pop(self, key: str, *args) -> Any:
        """
        Removes the element with the specified key and returns its value.
        
        Args:
            key: The key of the element to remove.
            default: The default value to return if key is not found.
            
        Returns:
            The value that was removed, or default if key was not found.
            
        Raises:
            RuntimeError: If the object is immutable.
            KeyError: If key is not found and no default is provided.
        """
        if self._immutable:
            raise RuntimeError("Object is immutable")
        if len(args) > 1:
            raise TypeError(f"pop expected at most 2 arguments, got {len(args) + 1}")
        try:
            return self._dict.pop(key)
        except KeyError:
            if args:
                return args[0]
            raise
    
    def popitem(self):
        """
        Removes and returns an arbitrary (key, value) pair from the ParameterList.
        
        Raises:
            RuntimeError: If the object is immutable.
            KeyError: If the ParameterList is empty.
        """
        if self._immutable:
            raise RuntimeError("Object is immutable")
        return self._dict.popitem()
    
    def clear(self):
        """
        Removes all items from the ParameterList.
        
        Raises:
            RuntimeError: If the object is immutable.
        """
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._dict.clear()
    
    def update(self, other=(), /, **kwargs):
        """
        Updates the ParameterList with the key-value pairs from other mappings.
        
        Args:
            other: A mapping object or iterable of key-value pairs.
            **kwargs: Additional keyword arguments to add.
        
        Raises:
            RuntimeError: If the object is immutable.
        """
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._dict.update(other, **kwargs)
    
    def setdefault(self, key: str, default: Any = None) -> Any:
        """
        Returns the value of key if it exists, otherwise sets and returns default.
        
        Args:
            key: The key to look up.
            default: The default value to set and return if key is not found.
            
        Returns:
            The existing value or the default value that was set.
            
        Raises:
            RuntimeError: If the object is immutable and key is not found.
        """
        if key in self._dict:
            return self._dict[key]
        if self._immutable:
            raise RuntimeError("Object is immutable")
        self._dict[key] = default
        return default
    
    # pylint: disable=protected-access
    def copy(self) -> 'ParameterList':
        """
        Creates a shallow copy of the ParameterList.
        The copy is always mutable regardless of the source's immutability.
        """
        new_list = ParameterList()
        new_list._dict = self._dict.copy()
        return new_list
    
    def __repr__(self) -> str:
        """Returns a string representation of the ParameterList."""
        return f"ParameterList({dict(self._dict)})"
    
    def __str__(self) -> str:
        """Returns a string representation of the ParameterList."""
        return str(self._dict)
