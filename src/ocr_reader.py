"""
OCR Reader Module

This module provides a wrapper around EasyOCR for text extraction
from images with proper error handling and filtering.
"""

import logging
from typing import List, Tuple, Optional

import easyocr
import numpy as np

logger = logging.getLogger(__name__)


class OCRReader:
    """Wrapper for EasyOCR with enhanced functionality."""

    def __init__(self, languages: List[str] = None, confidence_threshold: float = 0.5):
        """
        Initialize the OCR reader.

        Args:
            languages: List of language codes for OCR (default: ['en']).
            confidence_threshold: Minimum confidence score for accepting text.
        """
        if languages is None:
            languages = ['en']
        
        self.languages = languages
        self.confidence_threshold = confidence_threshold
        
        logger.info(f"Initializing OCR Reader with languages: {languages}")
        try:
            self.reader = easyocr.Reader(languages, gpu=False)
            logger.info("OCR Reader initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize OCR Reader: {e}")
            raise

    def read_text_from_image(self, image_path: str) -> List[Tuple[str, float]]:
        """
        Extract text from an image file.

        Args:
            image_path: Path to the image file.

        Returns:
            List of tuples containing (text, confidence_score).
        """
        try:
            results = self.reader.readtext(image_path)
            
            # Filter results by confidence threshold and extract text
            filtered_results = [
                (text, confidence)
                for (_, text, confidence) in results
                if confidence >= self.confidence_threshold
            ]
            
            logger.debug(f"Extracted {len(filtered_results)} text items from image")
            return filtered_results

        except Exception as e:
            logger.error(f"Error reading text from image: {e}")
            return []

    def read_text_from_frame(self, frame: np.ndarray) -> List[Tuple[str, float]]:
        """
        Extract text from a video frame (numpy array).

        Args:
            frame: Video frame as numpy array.

        Returns:
            List of tuples containing (text, confidence_score).
        """
        try:
            results = self.reader.readtext(frame)
            
            # Filter results by confidence threshold and extract text
            filtered_results = [
                (text, confidence)
                for (_, text, confidence) in results
                if confidence >= self.confidence_threshold
            ]
            
            logger.debug(f"Extracted {len(filtered_results)} text items from frame")
            return filtered_results

        except Exception as e:
            logger.error(f"Error reading text from frame: {e}")
            return []

    def get_all_text(self, image_path: str, separator: str = " ") -> str:
        """
        Get all extracted text as a single string.

        Args:
            image_path: Path to the image file.
            separator: String to separate multiple text items.

        Returns:
            Combined text string.
        """
        results = self.read_text_from_image(image_path)
        text_items = [text for text, _ in results]
        return separator.join(text_items)

    def get_all_text_from_frame(self, frame: np.ndarray, separator: str = " ") -> str:
        """
        Get all extracted text from a frame as a single string.

        Args:
            frame: Video frame as numpy array.
            separator: String to separate multiple text items.

        Returns:
            Combined text string.
        """
        results = self.read_text_from_frame(frame)
        text_items = [text for text, _ in results]
        return separator.join(text_items)

    def get_highest_confidence_text(self, image_path: str) -> Optional[Tuple[str, float]]:
        """
        Get the text item with the highest confidence score.

        Args:
            image_path: Path to the image file.

        Returns:
            Tuple of (text, confidence) with highest confidence, or None if no text found.
        """
        results = self.read_text_from_image(image_path)
        
        if not results:
            return None
        
        return max(results, key=lambda x: x[1])

    def get_highest_confidence_text_from_frame(self, frame: np.ndarray) -> Optional[Tuple[str, float]]:
        """
        Get the text item with the highest confidence score from a frame.

        Args:
            frame: Video frame as numpy array.

        Returns:
            Tuple of (text, confidence) with highest confidence, or None if no text found.
        """
        results = self.read_text_from_frame(frame)
        
        if not results:
            return None
        
        return max(results, key=lambda x: x[1])


