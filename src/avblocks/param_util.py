"""
Utility functions for converting between Python and native parameter lists.
"""

import ctypes
from typing import Dict, Any, Optional

from .native import get_native
from .string_util import decode_utf16le_string, encode_utf16le_string
from .parameter_list import ParameterList
from .native_param_type import NativeParamType

class ParamUtil:
    """Utility class for parameter list conversions between Python and native code."""
    
    @staticmethod
    def clone_parameters(param_list: ParameterList) -> ParameterList:
        """
        Creates a deep copy of a ParameterList, cloning any cloneable values.
        
        Args:
            param_list: The ParameterList to clone.
            
        Returns:
            A new ParameterList with cloned values where possible.
        """
        clone = ParameterList()
        
        for key, value in param_list.items():
            # Check if the value has a clone method
            if hasattr(value, 'clone') and callable(getattr(value, 'clone')):
                clone[key] = value.clone()
            # Check if the value has a copy method
            elif hasattr(value, 'copy') and callable(getattr(value, 'copy')):
                clone[key] = value.copy()
            else:
                # For basic types, just copy the reference
                clone[key] = value
        
        return clone

    # pylint: disable=import-outside-toplevel
    # pylint: disable=protected-access
    @staticmethod
    def from_native_parameter_list(native_list: ctypes.c_void_p) -> Optional[ParameterList]:
        """
        Converts a native parameter list to a Python ParameterList.
        
        Args:
            native_list: Pointer to the native parameter list.
            
        Returns:
            A new ParameterList with values from the native list, or None if native_list is null.
        """
        from .media_buffer import MediaBuffer

        if not native_list:
            return None
        
        native = get_native()
        param_list = ParameterList()
        
        param_count = native.lib.ParameterList_count(native_list)
        
        for i in range(param_count):
            native_param = native.lib.ParameterList_at(native_list, i)
            if not native_param:
                continue
            
            # Get parameter name first
            name_ptr = native.lib.Parameter_name(native_param)
            if not name_ptr:
                continue

            param_name = ctypes.string_at(name_ptr).decode('ascii')
            
            # Get parameter type and value
            param_type = native.lib.Parameter_type(native_param)
            param_value = None
            
            # Convert based on parameter type
            if param_type == NativeParamType.Float:
                param_value = native.lib.FloatParameter_value(native_param)
            elif param_type == NativeParamType.String:
                str_ptr = native.lib.StringParameter_value(native_param)
                if str_ptr:
                    param_value = decode_utf16le_string(str_ptr)
            elif param_type == NativeParamType.Int:
                param_value = native.lib.IntParameter_value(native_param)
            elif param_type == NativeParamType.MediaBuffer:
                native_buffer = native.lib.MediaBufferParameter_buffer(native_param)
                if native_buffer:
                    param_value = MediaBuffer._from_native(native_buffer)
            
            # TODO: Add support for VideoStreamInfo
            
            if param_value is not None:
                param_list[param_name] = param_value
    
        return param_list

    # pylint: disable=import-outside-toplevel
    # pylint: disable=protected-access
    @staticmethod
    def to_native_param_list(param_list: Optional[Dict[str, Any]]) -> ctypes.c_void_p:
        """
        Converts a Python parameter dictionary to a native parameter list.
        
        Args:
            param_list: Dictionary of parameters to convert, or None.
            
        Returns:
            Pointer to the native parameter list, or null pointer if param_list is None.
        """
        from .media_buffer import MediaBuffer
        from .video_stream_info import VideoStreamInfo

        if param_list is None:
            return ctypes.c_void_p(0)
        
        native = get_native()
        
        try:
            native_list = native.lib.avb_create_parameter_list()
            if not native_list:
                return ctypes.c_void_p(0)
            
            for key, value in param_list.items():
                native_param = ctypes.c_void_p(0)
                try:
                    if value is None:
                        native_param = native.lib.avb_create_int_parameter()
                        if native_param:
                            native.lib.IntParameter_setValue(native_param, 0)

                    elif isinstance(value, str):
                        native_param = native.lib.avb_create_string_parameter()
                        if native_param:
                            str_ptr = encode_utf16le_string(value)
                            native.lib.StringParameter_setValue(native_param, str_ptr)

                    elif isinstance(value, bool):
                        native_param = native.lib.avb_create_int_parameter()
                        if native_param:
                            native.lib.IntParameter_setValue(native_param, 1 if value else 0)
                    
                    elif ParamUtil._is_integer(value):
                        native_param = native.lib.avb_create_int_parameter()
                        if native_param:
                            native.lib.IntParameter_setValue(native_param, int(value))
                    
                    elif ParamUtil._is_float(value):
                        native_param = native.lib.avb_create_float_parameter()
                        if native_param:
                            native.lib.FloatParameter_setValue(native_param, float(value))
                    
                    # Handle MediaBuffer
                    elif isinstance(value, MediaBuffer):
                        native_param = native.lib.avb_create_media_buffer_parameter()
                        if native_param:
                            native_buffer = value._to_native()
                            if native_buffer:
                                native.lib.MediaBufferParameter_setBuffer(native_param, native_buffer)
                                native.lib.Reference_release(native_buffer)

                    # Handle VideoStreamInfo
                    elif isinstance(value, VideoStreamInfo):
                        native_param = native.lib.avb_create_video_stream_info_parameter()
                        if native_param:
                            # Create native VideoStreamInfo and copy data
                            native_vsi = native.lib.avb_create_video_stream_info()
                            if native_vsi:
                                value._copy_to_native(native_vsi)
                                native.lib.VideoStreamInfoParameter_setVideoStreamInfo(native_param, native_vsi)
                                native.lib.Reference_release(native_vsi)
                    
                    if native_param:
                        # Set parameter name (ASCII for parameter names)
                        key_bytes = key.encode('ascii') + b'\0'
                        name_buffer = ctypes.create_string_buffer(key_bytes)
                        native.lib.Parameter_setName(native_param, name_buffer)
                        
                        # Add to list
                        if native.lib.ParameterList_add(native_list, native_param):
                            # Release our reference only if add succeeded
                            native.lib.Reference_release(native_param)
                        else:
                            # If add failed, still need to release
                            native.lib.Reference_release(native_param)
                
                except Exception:
                    if native_param:
                        native.lib.Reference_release(native_param)
                    continue
            
            return native_list
        
        except Exception:
            return ctypes.c_void_p(0)
    
    @staticmethod
    def _is_integer(value: Any) -> bool:
        """
        Checks if a value can be converted to an integer.
        
        Args:
            value: The value to check.
            
        Returns:
            True if the value can be converted to integer, False otherwise.
        """
        try:
            if isinstance(value, bool):
                return True
            if isinstance(value, int):
                return True
            # Explicitly exclude float types
            if isinstance(value, float):
                return False
            # Check if it's a numeric type that can be converted to int
            if hasattr(value, '__int__'):
                int(value)
                return True
            return False
        except (ValueError, TypeError, OverflowError):
            return False
    
    @staticmethod
    def _is_float(value: Any) -> bool:
        """
        Checks if a value can be converted to a float.
        
        Args:
            value: The value to check.
            
        Returns:
            True if the value can be converted to float, False otherwise.
        """
        try:
            if isinstance(value, float):
                return True
            if isinstance(value, int):
                return False  # Integers should be handled as integers, not floats
            # Check if it's a numeric type that can be converted to float
            if hasattr(value, '__float__'):
                float(value)
                return True
            return False
        except (ValueError, TypeError, OverflowError):
            return False
