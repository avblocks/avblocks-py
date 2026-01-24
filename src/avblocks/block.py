"""
Block class for AVBlocks Python bindings.
"""

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from .media_socket_list import MediaSocketList
from .media_sample import MediaSample
from .error_info import ErrorInfo


class Block(ABC):
    """
    Provides functionality for audio and video encoding, decoding and transforming.
    
    This is an abstract base class. See Transcoder for a concrete implementation.
    """
    
    @abstractmethod
    def dispose(self):
        """
        Disposes the Block and reclaims the resources used by the object.
        """
    
    @property
    @abstractmethod
    def inputs(self) -> MediaSocketList:
        """
        A modifiable collection of MediaSocket objects which describe the input data of the Block.
        """
    
    @property
    @abstractmethod
    def outputs(self) -> MediaSocketList:
        """
        A modifiable collection of MediaSocket objects which describe the output data of the Block.
        """
    
    @abstractmethod
    def open(self) -> bool:
        """
        Initializes the Block based on the specified input and desired output.
        
        Returns:
            True if the Block is successfully initialized and is ready to process data; otherwise False.
        """
    
    @abstractmethod
    def push(self, input_index: int, input_sample: MediaSample) -> bool:
        """
        Pushes input data to the Block.
        
        Args:
            input_index: Specifies the index of the input socket whose data is pushed to the Block.
            input_sample: A MediaSample object that contains the input data in the buffer property.
            
        Returns:
            True when the Block has successfully processed the input data, otherwise False.
        """
    
    @abstractmethod
    def push_unmanaged(self, input_index: int, input_sample: MediaSample) -> bool:
        """
        Pushes input data to the Block.
        
        Args:
            input_index: Specifies the index of the input socket whose data is pushed to the Block.
            input_sample: A MediaSample object that contains the input data in the unmanaged_buffer property.
            
        Returns:
            True when the Block has successfully processed the input data, otherwise False.
        """
    
    @abstractmethod
    def pull(self, output_sample: MediaSample) -> Tuple[bool, int]:
        """
        Pulls output data from the Block.
        
        Args:
            output_sample: The MediaSample object receives the output data in the buffer property.
            
        Returns:
            A tuple of (success, output_index) where:
            - success: True if the Block has successfully generated output, otherwise False.
            - output_index: The index of the output socket to which the data belongs.
        """
    
    @abstractmethod
    def pull_unmanaged(self, output_sample: MediaSample) -> Tuple[bool, int]:
        """
        Pulls output data from the Block.
        
        Args:
            output_sample: The MediaSample object receives the output data in the unmanaged_buffer property.
            
        Returns:
            A tuple of (success, output_index) where:
            - success: True if the Block has successfully generated output, otherwise False.
            - output_index: The index of the output socket to which the data belongs.
        """
    
    @abstractmethod
    def close(self):
        """
        Closes the Block. When closed it can neither accept, nor deliver data.
        """
    
    @abstractmethod
    def flush(self) -> bool:
        """
        Flushes the data buffered in the Block to the output.
        
        Returns:
            True if the buffered data is successfully flushed; otherwise False.
        """
    
    @abstractmethod
    def end_of_stream(self, input_index: int) -> bool:
        """
        Tells the Block that there's no more data for the specified input socket.
        
        Args:
            input_index: Specifies the index of the input socket for which there's no more data.
            
        Returns:
            True if the operation is successful; otherwise False.
        """
    
    @property
    @abstractmethod
    def error(self) -> Optional[ErrorInfo]:
        """
        The error information for the last block operation.
        """
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures dispose is called."""
        self.dispose()
        return False
