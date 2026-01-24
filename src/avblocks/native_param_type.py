"""
Native Parameter type enumeration.

The NativeParamType represents the type of the data stored in a Parameter.

Depending on this constant a Parameter interface can be cast to child interfaces such as
IntParameter, StringParameter, etc.
"""

from enum import IntEnum

class NativeParamType(IntEnum):
    """
    Enumeration of native parameter types in AVBlocks C API.
    
    The parameter type determines how the parameter value should be interpreted
    and which specific parameter interface should be used.
    """
    
    Float = 1
    """
    The parameter represents a 64-bit floating point number (double precision).
    """
    
    MediaBuffer = 3
    """
    The parameter represents a MediaBuffer object and can be cast to MediaBufferParameter.
    """
    
    VideoFrame = 4
    """
    The parameter represents a VideoStreamInfo object and can be cast to VideoStreamInfoParameter.
    """
    
    String = 5
    """
    The parameter represents a generic value which is stored in a char_t string.
    The parameter name constant documents how this value should be interpreted.
    
    The parameter can be cast to StringParameter.
    """
    
    Int = 6
    """
    The parameter represents a 64-bit Integer.
    """
