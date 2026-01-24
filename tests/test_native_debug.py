import pytest
from avblocks import Library
from avblocks.native import get_native


@pytest.fixture(scope="module")
def initialized_library():
    """Fixture to initialize and shutdown the library."""
    if not Library.initialize():
        pytest.skip("Failed to initialize AVBlocks library")
    yield
    Library.shutdown()


def test_native_library_loaded(initialized_library):
    """Test that the native library is loaded."""
    native = get_native()
    assert native is not None
    assert native.lib is not None


def test_native_functions_exist(initialized_library):
    """Test that required native functions exist."""
    native = get_native()
    
    # Check if the function exists
    assert hasattr(native.lib, 'avb_create_audio_stream_info'), \
        "avb_create_audio_stream_info function not found in native library"
    
    assert hasattr(native.lib, 'avb_create_video_stream_info'), \
        "avb_create_video_stream_info function not found in native library"
    
    assert hasattr(native.lib, 'avb_create_data_stream_info'), \
        "avb_create_data_stream_info function not found in native library"


def test_native_function_call(initialized_library):
    """Test calling a native function directly."""
    native = get_native()
    
    # Try to call the function directly
    try:
        handle = native.lib.avb_create_audio_stream_info()
        if handle:
            # Clean up
            native.lib.Reference_release(handle)
            assert True
        else:
            pytest.fail("avb_create_audio_stream_info returned NULL")
    except Exception as e:
        pytest.fail(f"Failed to call avb_create_audio_stream_info: {e}")
