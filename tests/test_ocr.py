"""
Test Module for OCR and Medicine Scanner

This module provides tests for the OCR functionality and medicine detection.
"""

import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ocr_reader import OCRReader
from medicine_database import MedicineDatabase
from config_manager import ConfigManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_ocr_reader():
    """Test the OCR reader initialization and basic functionality."""
    print("\n" + "="*60)
    print("Testing OCR Reader")
    print("="*60)
    
    try:
        ocr = OCRReader(languages=['en'], confidence_threshold=0.5)
        print("✓ OCR Reader initialized successfully")
        
        # Test reading from a sample image (if available)
        print("\nNote: To test OCR reading, provide an image path and uncomment below:")
        # image_path = "path/to/test/image.jpg"
        # results = ocr.read_text_from_image(image_path)
        # print(f"Detected {len(results)} text items")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def test_medicine_database():
    """Test the medicine database functionality."""
    print("\n" + "="*60)
    print("Testing Medicine Database")
    print("="*60)
    
    try:
        config = ConfigManager()
        db_path = config.get_medicine_database_path()
        
        db = MedicineDatabase(str(db_path))
        print(f"✓ Database loaded with {db.count()} medicines")
        
        # Test exact match
        test_name = "Aspirin"
        result = db.search_medicine(test_name)
        print(f"\nExact search for '{test_name}': {result}")
        
        # Test fuzzy match
        test_name = "Ibuprofen"
        result = db.search_medicine(test_name, threshold=80)
        print(f"Fuzzy search for '{test_name}': {result}")
        
        # Test best matches
        test_name = "Asprin"  # Misspelled
        matches = db.get_best_matches(test_name, top_n=3)
        print(f"\nTop 3 matches for '{test_name}':")
        for medicine, score in matches:
            print(f"  - {medicine} (score: {score})")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def test_config_manager():
    """Test the configuration manager."""
    print("\n" + "="*60)
    print("Testing Configuration Manager")
    print("="*60)
    
    try:
        config = ConfigManager()
        print("✓ Configuration loaded successfully")
        
        print(f"\nConfiguration values:")
        print(f"  - OpenAI Model: {config.get_openai_model()}")
        print(f"  - Camera Index: {config.get_camera_index()}")
        print(f"  - Camera Resolution: {config.get_camera_resolution()}")
        print(f"  - OCR Languages: {config.get_ocr_languages()}")
        print(f"  - Scan Interval: {config.get_scan_interval()}s")
        
        # Test API key (without revealing it)
        try:
            api_key = config.get_openai_api_key()
            if api_key:
                print(f"  - OpenAI API Key: Set (length: {len(api_key)})")
            else:
                print(f"  - OpenAI API Key: Not set")
        except ValueError as e:
            print(f"  - OpenAI API Key: {e}")
        
    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run all tests."""
    print("\n" + "="*70)
    print(" PharmaSee Test Suite")
    print("="*70)
    
    test_config_manager()
    test_medicine_database()
    test_ocr_reader()
    
    print("\n" + "="*70)
    print("Tests Complete")
    print("="*70)
    print("\nNote: Some tests require additional resources:")
    print("  - Image files for OCR testing")
    print("  - OpenAI API key for LLM testing")
    print("  - Camera for live scanning")
    print()


if __name__ == "__main__":
    main()


