"""
Configuration Manager Module

This module handles loading and accessing application configuration
from JSON files and environment variables.
"""

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configuration from JSON files and environment variables."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.

        Args:
            config_path: Path to the configuration JSON file.
                        If None, uses default path.
        """
        if config_path is None:
            # Default to config/config.json in project root
            project_root = Path(__file__).parent.parent
            config_path = project_root / "config" / "config.json"
        
        self.config_path = Path(config_path)
        self.config: Dict[str, Any] = {}
        self._load_config()
        self._override_from_env()

    def _load_config(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as config_file:
                self.config = json.load(config_file)
            logger.info(f"Configuration loaded from {self.config_path}")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise

    def _override_from_env(self) -> None:
        """Override configuration values from environment variables."""
        # Override OpenAI API key from environment if available
        env_api_key = os.getenv('OPENAI_API_KEY')
        if env_api_key:
            self.config['openai']['api_key'] = env_api_key
            logger.info("OpenAI API key loaded from environment variable")

    def get(self, *keys: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.

        Args:
            *keys: Keys to traverse the config dictionary.
            default: Default value if key path doesn't exist.

        Returns:
            The configuration value or default.

        Example:
            config.get('openai', 'api_key')
            config.get('camera', 'device_index', default=0)
        """
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default

    def get_openai_api_key(self) -> str:
        """Get OpenAI API key from configuration."""
        api_key = self.get('openai', 'api_key', default='')
        if not api_key:
            raise ValueError(
                "OpenAI API key not found. Please set it in config/config.json "
                "or set the OPENAI_API_KEY environment variable."
            )
        return api_key

    def get_openai_model(self) -> str:
        """Get OpenAI model name from configuration."""
        return self.get('openai', 'model', default='gpt-3.5-turbo')

    def get_openai_temperature(self) -> float:
        """Get OpenAI temperature setting from configuration."""
        return self.get('openai', 'temperature', default=0.3)

    def get_openai_max_tokens(self) -> int:
        """Get OpenAI max tokens setting from configuration."""
        return self.get('openai', 'max_tokens', default=200)

    def get_camera_index(self) -> int:
        """Get camera device index from configuration."""
        return self.get('camera', 'device_index', default=0)

    def get_camera_resolution(self) -> tuple:
        """Get camera resolution from configuration."""
        width = self.get('camera', 'frame_width', default=1280)
        height = self.get('camera', 'frame_height', default=720)
        return (width, height)

    def get_ocr_languages(self) -> list:
        """Get OCR languages from configuration."""
        return self.get('ocr', 'languages', default=['en'])

    def get_ocr_confidence_threshold(self) -> float:
        """Get OCR confidence threshold from configuration."""
        return self.get('ocr', 'confidence_threshold', default=0.5)

    def get_medicine_database_path(self) -> Path:
        """Get path to medicine database CSV file."""
        project_root = Path(__file__).parent.parent
        relative_path = self.get('paths', 'medicine_database', default='data/medicines.csv')
        return project_root / relative_path

    def get_scan_interval(self) -> float:
        """Get scan interval in seconds from configuration."""
        return self.get('scanner', 'scan_interval_seconds', default=2.0)


