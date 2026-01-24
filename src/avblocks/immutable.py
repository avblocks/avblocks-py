"""
IImmutable interface for AVBlocks Python bindings.
"""

from abc import ABC, abstractmethod


class IImmutable(ABC):
    """
    Interface for objects that support immutability.
    
    An immutable object cannot be modified and all modifying methods fail to produce a result.
    An immutable object can be modified by the AVBlocks library.
    Object immutability spreads to all nested objects.
    Therefore it is not possible to add/set an immutable object to a mutable object.
    When cloned an immutable object becomes mutable.
    """
    
    @property
    @abstractmethod
    def immutable(self) -> bool:
        """
        Returns whether the object is immutable.
        """
    
    @immutable.setter
    @abstractmethod
    def immutable(self, value: bool):
        """
        Set the immutable state.
        
        Args:
            value: True to make the object immutable, False to make it mutable
        """
