import os
import pytest
from avblocks import Library
from avblocks.constants import LicenseStatusFlags


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if Library.initialize():
        yield
        Library.shutdown()
    else:
        pytest.skip("Failed to initialize AVBlocks library. Make sure the library is available in the system path or set AVBLOCKS_CORE_PATH environment variable.")


def test_library_initialize():
    """Test library initialization."""
    result = Library.initialize()
    assert isinstance(result, bool)
    if result:
        Library.shutdown()


def test_library_version(initialized_library):
    """Test version methods."""
    major = Library.major_version()
    assert isinstance(major, int)
    assert major >= 0
    
    minor = Library.minor_version()
    assert isinstance(minor, int)
    assert minor >= 0
    
    patch = Library.patch_version()
    assert isinstance(patch, int)
    assert patch >= 0


def test_library_description(initialized_library):
    """Test library description."""
    desc = Library.description()
    assert isinstance(desc, str)
    assert len(desc) > 0
    assert 'AVBlocks' in desc


def test_library_license_status(initialized_library):
    """Test license status."""
    status = Library.license_status()
    assert isinstance(status, LicenseStatusFlags)
    # Should return ready
    assert status == LicenseStatusFlags.Ready


def test_library_set_license(initialized_library):
    """Test setting license."""
    # Test with None (should clear license)
    status = Library.set_license(None)
    assert isinstance(status, LicenseStatusFlags)
    
    # Test with empty string
    status = Library.set_license("")
    assert isinstance(status, LicenseStatusFlags)


def test_library_set_license_tls(initialized_library):
    """Test setting license TLS."""
    # Should not raise an exception
    Library.set_license_tls(True)
    Library.set_license_tls(False)


def test_library_is_licensed(initialized_library):
    """Test checking if licensed."""
    # Test with default product and feature
    result = Library.is_licensed()
    assert isinstance(result, bool)
    
    # Test with explicit product
    result = Library.is_licensed(product="AVBlocks")
    assert isinstance(result, bool)
    
    # Test with product and feature
    result = Library.is_licensed(product="avb", feature="pcm")
    assert isinstance(result, bool)


def test_library_version_consistency(initialized_library):
    """Test that version numbers are consistent."""
    major = Library.major_version()
    minor = Library.minor_version()
    patch = Library.patch_version()
    
    desc = Library.description()
    version_str = f"{major}.{minor}.{patch}"
    
    # The description should contain the version
    assert version_str in desc


def test_library_multiple_initialize():
    """Test multiple initialize/shutdown calls."""
    # First initialize
    result1 = Library.initialize()
    assert result1 is True
    
    # Second initialize (should still work)
    result2 = Library.initialize()
    assert isinstance(result2, bool)
    
    # Shutdown
    Library.shutdown()
    
    # Initialize again
    result3 = Library.initialize()
    assert result3 is True
    
    Library.shutdown()


def test_library_license_flags():
    """Test license status flags enum values."""
    assert LicenseStatusFlags.Ready == 0
    assert LicenseStatusFlags.ValidationInProgress == 1
    assert LicenseStatusFlags.DemoBuild == 2


def test_library():
    pass
