"""
Tests for ErrorInfo class.
"""

import pytest
from avblocks.error_info import ErrorInfo
from avblocks.constants import ErrorFacility


class TestErrorInfo:
    """Test suite for ErrorInfo class."""
    
    def test_default_constructor(self):
        """Test creating an ErrorInfo with default values."""
        error = ErrorInfo()
        
        assert error.code == 0
        assert error.facility == ErrorFacility.Success
        assert error.message == ""
        assert error.hint == ""
        assert error.block == ""
    
    def test_set_code(self):
        """Test setting error code."""
        error = ErrorInfo()
        error.code = 42
        
        assert error.code == 42
    
    def test_set_facility(self):
        """Test setting error facility."""
        error = ErrorInfo()
        error.facility = ErrorFacility.Codec
        
        assert error.facility == ErrorFacility.Codec
    
    def test_set_message(self):
        """Test setting error message."""
        error = ErrorInfo()
        error.message = "Test error message"
        
        assert error.message == "Test error message"
    
    def test_set_hint(self):
        """Test setting diagnostic hint."""
        error = ErrorInfo()
        error.hint = "Check the input file format"
        
        assert error.hint == "Check the input file format"
    
    def test_set_block(self):
        """Test setting block name."""
        error = ErrorInfo()
        error.block = "H264Encoder"
        
        assert error.block == "H264Encoder"
    
    def test_clone(self):
        """Test cloning an ErrorInfo object."""
        error = ErrorInfo()
        error.code = 100
        error.facility = ErrorFacility.Transcoder
        error.message = "Original message"
        error.hint = "Original hint"
        error.block = "TestBlock"
        
        cloned = error.clone()
        
        # Verify all properties are copied
        assert cloned.code == error.code
        assert cloned.facility == error.facility
        assert cloned.message == error.message
        assert cloned.hint == error.hint
        assert cloned.block == error.block
        
        # Verify it's a deep copy - modifying clone doesn't affect original
        cloned.code = 200
        cloned.message = "Modified message"
        
        assert error.code == 100
        assert error.message == "Original message"
    
    def test_str_representation(self):
        """Test string representation of ErrorInfo."""
        error = ErrorInfo()
        error.code = 404
        error.facility = ErrorFacility.AVBlocks
        error.message = "File not found"
        
        str_repr = str(error)
        
        assert "404" in str_repr
        assert "AVBlocks" in str_repr
        assert "File not found" in str_repr
    
    def test_str_with_all_fields(self):
        """Test string representation with all fields set."""
        error = ErrorInfo()
        error.code = 500
        error.facility = ErrorFacility.Transcoder
        error.message = "Internal error"
        error.hint = "Memory allocation failed"
        error.block = "MP4Muxer"
        
        str_repr = str(error)
        
        assert "500" in str_repr
        assert "Transcoder" in str_repr
        assert "Internal error" in str_repr
        assert "Memory allocation failed" in str_repr
        assert "MP4Muxer" in str_repr
    
    def test_str_minimal(self):
        """Test string representation with minimal fields."""
        error = ErrorInfo()
        error.code = 1
        error.facility = ErrorFacility.Success
        
        str_repr = str(error)
        
        assert "1" in str_repr
        assert "Success" in str_repr
    
    def test_repr(self):
        """Test repr equals str for ErrorInfo."""
        error = ErrorInfo()
        error.code = 123
        error.facility = ErrorFacility.Codec
        error.message = "Encoding failed"
        
        assert repr(error) == str(error)
    
    def test_multiple_properties(self):
        """Test setting multiple properties."""
        error = ErrorInfo()
        
        error.code = 999
        error.facility = ErrorFacility.AVBlocks
        error.message = "Unsupported format"
        error.hint = "Try converting to MP4"
        error.block = "FormatDetector"
        
        assert error.code == 999
        assert error.facility == ErrorFacility.AVBlocks
        assert error.message == "Unsupported format"
        assert error.hint == "Try converting to MP4"
        assert error.block == "FormatDetector"
    
    def test_facility_enum_values(self):
        """Test setting various ErrorFacility enum values."""
        error = ErrorInfo()
        
        facilities = [
            ErrorFacility.Success,
            ErrorFacility.SystemWindows,
            ErrorFacility.SystemMacOSStatus,
            ErrorFacility.SystemMacMach,
            ErrorFacility.SystemPosix,
            ErrorFacility.AVBlocks,
            ErrorFacility.Transcoder,
            ErrorFacility.Codec,
        ]
        
        for facility in facilities:
            error.facility = facility
            assert error.facility == facility
    
    def test_empty_strings(self):
        """Test setting empty strings."""
        error = ErrorInfo()
        error.message = ""
        error.hint = ""
        error.block = ""
        
        assert error.message == ""
        assert error.hint == ""
        assert error.block == ""
    
    def test_unicode_strings(self):
        """Test setting Unicode strings."""
        error = ErrorInfo()
        error.message = "Error: 文件未找到"
        error.hint = "Prüfen Sie die Datei"
        error.block = "Encodeur Français"
        
        assert error.message == "Error: 文件未找到"
        assert error.hint == "Prüfen Sie die Datei"
        assert error.block == "Encodeur Français"
    
    def test_negative_code(self):
        """Test setting negative error code."""
        error = ErrorInfo()
        error.code = -1
        
        assert error.code == -1
    
    def test_large_code(self):
        """Test setting large error code."""
        error = ErrorInfo()
        error.code = 2147483647  # Max int32
        
        assert error.code == 2147483647
