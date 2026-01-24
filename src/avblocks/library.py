"""
AVBlocks module for handling audio and video processing tasks.
"""

from typing import Optional
from .native import get_native
from .constants import LicenseStatusFlags


class Library:
    """Initializes AVBlocks and manages license information."""
    
    @staticmethod
    def initialize() -> bool:
        """
        Initializes the AVBlocks library. Must be called once before the library is used,
        usually when the application starts.
        
        Returns:
            True if the library is successfully initialized, otherwise False.
        """
        native = get_native()
        return native.lib.avb_initialize()
    
    @staticmethod
    def shutdown() -> None:
        """
        Closes the AVBlocks library and frees the resources that are used (if any).
        Should be called when the library will not be used anymore, e.g. when the application ends.
        """
        native = get_native()
        native.lib.avb_shutdown()
    
    @staticmethod
    def set_license_tls(use_tls: bool) -> None:
        """
        Sets whether the license validation should use TLS (HTTPS) or not.
        
        Args:
            use_tls: If True the license validation will use TLS (HTTPS), 
                    otherwise it will use HTTP. The default is False.
        
        Note:
            This setting is used when the license validation is performed against a license server.
            Must be called before Library.set_license().
        """
        native = get_native()
        native.lib.avb_set_license_tls(use_tls)
    
    @staticmethod
    def set_license(license_string: Optional[str]) -> LicenseStatusFlags:
        """
        Sets a license string. The supplied license is appended to the library license state.
        
        Args:
            license_string: A string with license information. If None, the library 
                          license state is cleared.
        
        Returns:
            The status after the license is set. The returned value is a combination 
            of flags from the LicenseStatusFlags enum.
        
        Note:
            A Demo build of the library cannot be licensed and always returns 
            LicenseStatusFlags.DemoBuild.
        """
        native = get_native()
        license_bytes = license_string.encode('utf-8') if license_string else None
        status = native.lib.avb_set_license(license_bytes)
        return LicenseStatusFlags(status)
    
    @staticmethod
    def license_status() -> LicenseStatusFlags:
        """
        Returns the current license status.
        
        Returns:
            License status flags.
        
        Note:
            In the Demo build the license status is always LicenseStatusFlags.DemoBuild.
        """
        native = get_native()
        status = native.lib.avb_license_status()
        return LicenseStatusFlags(status)
    
    @staticmethod
    def is_licensed(product: Optional[str] = None, feature: Optional[str] = None) -> bool:
        """
        Checks whether a product feature is licensed.
        
        Args:
            product: The product id. If None, the AVBlocks product is implied.
            feature: The feature id. If None, the default AVBlocks product feature is implied.
        
        Returns:
            True if the specified product feature is licensed.
        
        Note:
            If a product is fully licensed then the function will always return True for 
            that product regardless of the feature parameter.
            
            If a product is licensed for a limited set of features then the function will 
            return True for that product only if the feature parameter specifies one of 
            the licensed features or is None.
        """
        native = get_native()
        product_bytes = product.encode('utf-8') if product else None
        feature_bytes = feature.encode('utf-8') if feature else None
        return native.lib.avb_is_licensed(product_bytes, feature_bytes)
    
    @staticmethod
    def description() -> str:
        """
        Returns library build description.
        
        Returns:
            String containing details about the build including full version, 
            architecture, configuration, license and platform.
        """
        native = get_native()
        core_desc = native.lib.avb_get_description().decode('utf-8')
        return f"AVBlocks.Python {Library.major_version()}.{Library.minor_version()}.{Library.patch_version()}, core: {core_desc}"
    
    @staticmethod
    def major_version() -> int:
        """Returns library major version."""
        native = get_native()
        return native.lib.avb_get_major_version()
    
    @staticmethod
    def minor_version() -> int:
        """Returns library minor version."""
        native = get_native()
        return native.lib.avb_get_minor_version()
    
    @staticmethod
    def patch_version() -> int:
        """
        Returns library patch version.
        
        Note:
            The patch version is used for bugfixes and small improvements that 
            do not involve API changes.
        """
        native = get_native()
        return native.lib.avb_get_patch_version()
   
