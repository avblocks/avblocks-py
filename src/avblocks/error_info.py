"""
ErrorInfo class for AVBlocks Python bindings.
"""

import ctypes
from typing import Optional

from .native import get_native
from .constants import ErrorFacility
from .string_util import decode_utf16le_string


class ErrorInfo:
    """
    Describes an AVBlocks error.
    """
    
    def __init__(self):
        """Creates an instance of ErrorInfo."""
        self._code: int = 0
        self._facility: ErrorFacility = ErrorFacility.Success
        self._message: str = ""
        self._hint: str = ""
        self._block: str = ""
    
    @property
    def code(self) -> int:
        """
        Error code. The value depends on the error facility.
        """
        return self._code
    
    @code.setter
    def code(self, value: int):
        """Set the error code."""
        self._code = value
    
    @property
    def facility(self) -> ErrorFacility:
        """
        Error facility. This is the AVBlocks subsystem that has generated the error.
        """
        return self._facility
    
    @facility.setter
    def facility(self, value: ErrorFacility):
        """Set the error facility."""
        self._facility = value
    
    @property
    def message(self) -> str:
        """
        Error message. This is a human-readable description of the error.
        """
        return self._message
    
    @message.setter
    def message(self, value: str):
        """Set the error message."""
        self._message = value
    
    @property
    def hint(self) -> str:
        """
        Diagnostic hint. This is an implementation specific diagnostics message,
        suitable for error logs or debugging.
        """
        return self._hint
    
    @hint.setter
    def hint(self, value: str):
        """Set the diagnostic hint."""
        self._hint = value
    
    @property
    def block(self) -> str:
        """
        The name of the component/block that has generated the error.
        This is useful only when facility is ErrorFacility.Block.
        """
        return self._block
    
    @block.setter
    def block(self, value: str):
        """Set the block name."""
        self._block = value

    # pylint: disable=[protected-access]
    def clone(self) -> 'ErrorInfo':
        """
        Creates a deep copy of the ErrorInfo object.
        
        Returns:
            A new ErrorInfo instance which is a deep copy of the current object.
        """
        e = ErrorInfo()
        e._code = self._code
        e._facility = self._facility
        e._hint = self._hint
        e._message = self._message
        e._block = self._block
        return e
    
    @staticmethod
    def _from_native(native_error: ctypes.c_void_p) -> Optional['ErrorInfo']:
        """
        Internal method to create an ErrorInfo from a native error pointer.
        
        Args:
            native_error: Native ErrorInfo pointer
            
        Returns:
            A new ErrorInfo object or None if native_error is null
        """
        if not native_error:
            return None
        
        lib = get_native().lib
        
        error_info = ErrorInfo()
        error_info._code = lib.ErrorInfo_code(native_error)
        error_info._facility = ErrorFacility(lib.ErrorInfo_facility(native_error))
        
        # Convert UTF-16LE strings from native pointers using string_util
        msg_ptr = lib.ErrorInfo_message(native_error)
        if msg_ptr:
            error_info._message = decode_utf16le_string(msg_ptr)
        
        hint_ptr = lib.ErrorInfo_hint(native_error)
        if hint_ptr:
            error_info._hint = decode_utf16le_string(hint_ptr)
        
        block_ptr = lib.ErrorInfo_block(native_error)
        if block_ptr:
            error_info._block = decode_utf16le_string(block_ptr)
        
        return error_info
    
    def __str__(self) -> str:
        """String representation of the error."""
        parts = [f"ErrorInfo(code={self._code}, facility={self._facility.name}"]
        if self._message:
            parts.append(f", message='{self._message}'")
        if self._hint:
            parts.append(f", hint='{self._hint}'")
        if self._block:
            parts.append(f", block='{self._block}'")
        parts.append(")")
        return "".join(parts)
    
    def __repr__(self) -> str:
        """Developer representation of the error."""
        return self.__str__()
