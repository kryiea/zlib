from typing import Dict, Type
from .base import BookPlatform
from .zlibrary import ZLibrary

class PlatformFactory:
    """Factory for creating book platform instances"""
    
    _platforms: Dict[str, Type[BookPlatform]] = {
        'zlibrary': ZLibrary
    }
    
    @classmethod
    def get_platform(cls, platform_name: str) -> BookPlatform:
        """
        Get platform instance by name
        Args:
            platform_name: Name of the platform
        Returns:
            Platform instance
        Raises:
            ValueError: If platform is not supported
        """
        platform_class = cls._platforms.get(platform_name.lower())
        if not platform_class:
            raise ValueError(f"Platform {platform_name} is not supported")
        return platform_class()
    
    @classmethod
    def register_platform(cls, name: str, platform_class: Type[BookPlatform]):
        """
        Register a new platform
        Args:
            name: Platform name
            platform_class: Platform class
        """
        cls._platforms[name.lower()] = platform_class 