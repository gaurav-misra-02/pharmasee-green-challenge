"""
Medicine Scanner Application

Main application for real-time medicine identification using OCR and LLM analysis.
"""

import logging
import time
from pathlib import Path
from typing import Optional, Tuple

import cv2 as cv
import numpy as np

from config_manager import ConfigManager
from llm_analyzer import MedicineLLMAnalyzer
from medicine_database import MedicineDatabase
from ocr_reader import OCRReader

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MedicineScanner:
    """Real-time medicine scanner using camera, OCR, and LLM analysis."""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the medicine scanner.

        Args:
            config_path: Path to configuration file (optional).
        """
        logger.info("Initializing Medicine Scanner...")
        
        # Load configuration
        self.config = ConfigManager(config_path)
        
        # Initialize components
        self._initialize_ocr()
        self._initialize_llm()
        self._initialize_database()
        self._initialize_camera()
        
        # Scanner state
        self.last_scan_time = 0
        self.scan_interval = self.config.get_scan_interval()
        self.last_detected_medicine = None
        self.last_analysis = None
        
        logger.info("Medicine Scanner initialized successfully")

    def _initialize_ocr(self) -> None:
        """Initialize the OCR reader."""
        languages = self.config.get_ocr_languages()
        confidence_threshold = self.config.get_ocr_confidence_threshold()
        
        self.ocr_reader = OCRReader(
            languages=languages,
            confidence_threshold=confidence_threshold
        )

    def _initialize_llm(self) -> None:
        """Initialize the LLM analyzer."""
        api_key = self.config.get_openai_api_key()
        model = self.config.get_openai_model()
        temperature = self.config.get_openai_temperature()
        max_tokens = self.config.get_openai_max_tokens()
        
        self.llm_analyzer = MedicineLLMAnalyzer(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

    def _initialize_database(self) -> None:
        """Initialize the medicine database."""
        db_path = self.config.get_medicine_database_path()
        self.medicine_db = MedicineDatabase(str(db_path))
        logger.info(f"Loaded {self.medicine_db.count()} medicines from database")

    def _initialize_camera(self) -> None:
        """Initialize the camera capture."""
        camera_index = self.config.get_camera_index()
        self.camera_capture = cv.VideoCapture(camera_index)
        
        if not self.camera_capture.isOpened():
            logger.error(f"Failed to open camera at index {camera_index}")
            raise RuntimeError(f"Could not open camera at index {camera_index}")
        
        # Set camera resolution
        width, height = self.config.get_camera_resolution()
        self.camera_capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
        self.camera_capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)
        
        logger.info(f"Camera initialized: {width}x{height}")

    def _should_scan(self) -> bool:
        """
        Check if enough time has passed since last scan.

        Returns:
            True if should scan now, False otherwise.
        """
        current_time = time.time()
        return (current_time - self.last_scan_time) >= self.scan_interval

    def _detect_medicine_from_frame(self, frame: np.ndarray) -> Optional[str]:
        """
        Detect medicine name from a video frame using OCR.

        Args:
            frame: Video frame as numpy array.

        Returns:
            Detected medicine name or None.
        """
        # Extract text from frame
        text_results = self.ocr_reader.read_text_from_frame(frame)
        
        if not text_results:
            return None
        
        # Try to match each detected text with medicine database
        for text, confidence in text_results:
            logger.debug(f"Detected text: '{text}' (confidence: {confidence:.2f})")
            
            # Clean the text
            text_cleaned = text.strip()
            
            # Try to find in database
            matched_medicine = self.medicine_db.search_medicine(text_cleaned)
            
            if matched_medicine:
                return matched_medicine
            
            # If not in database but has high confidence, might be a medicine
            if confidence > 0.7 and len(text_cleaned) > 3:
                return text_cleaned
        
        return None

    def _analyze_medicine_with_llm(self, medicine_name: str) -> dict:
        """
        Analyze medicine using LLM.

        Args:
            medicine_name: Name of the medicine to analyze.

        Returns:
            Dictionary with medicine analysis.
        """
        return self.llm_analyzer.analyze_medicine(medicine_name)

    def _draw_ui_elements(self, frame: np.ndarray, 
                          medicine_name: Optional[str],
                          analysis: Optional[dict]) -> np.ndarray:
        """
        Draw UI elements on the frame.

        Args:
            frame: Video frame to draw on.
            medicine_name: Detected medicine name (if any).
            analysis: LLM analysis results (if any).

        Returns:
            Frame with UI elements drawn.
        """
        frame_copy = frame.copy()
        height, width = frame_copy.shape[:2]
        
        # Draw title bar
        cv.rectangle(frame_copy, (0, 0), (width, 60), (50, 50, 50), -1)
        cv.putText(frame_copy, "PharmaSee - Medicine Scanner", 
                   (10, 40), cv.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        # Draw instructions
        instructions = "Press 'S' to scan | 'Q' to quit | 'R' to reset"
        cv.putText(frame_copy, instructions, 
                   (10, height - 20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        # Draw results panel if medicine detected
        if medicine_name and analysis:
            self._draw_results_panel(frame_copy, medicine_name, analysis)
        
        return frame_copy

    def _draw_results_panel(self, frame: np.ndarray, 
                           medicine_name: str, 
                           analysis: dict) -> None:
        """
        Draw the results panel on the frame.

        Args:
            frame: Video frame to draw on.
            medicine_name: Detected medicine name.
            analysis: LLM analysis results.
        """
        height, width = frame.shape[:2]
        
        # Panel dimensions
        panel_width = 500
        panel_height = 280
        panel_x = width - panel_width - 20
        panel_y = 80
        
        # Draw semi-transparent panel
        overlay = frame.copy()
        cv.rectangle(overlay, (panel_x, panel_y), 
                    (panel_x + panel_width, panel_y + panel_height),
                    (40, 40, 40), -1)
        cv.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
        
        # Draw border
        cv.rectangle(frame, (panel_x, panel_y), 
                    (panel_x + panel_width, panel_y + panel_height),
                    (0, 255, 0), 2)
        
        # Draw title
        cv.putText(frame, "MEDICINE DETECTED", 
                   (panel_x + 10, panel_y + 30),
                   cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        # Draw medicine information
        y_offset = panel_y + 70
        line_height = 35
        
        info_lines = [
            f"Name: {medicine_name}",
            f"Type: {analysis.get('type', 'Unknown')}",
            f"Use: {analysis.get('use', 'Unknown')[:40]}...",
            f"Class: {analysis.get('drug_class', 'Unknown')}",
            f"Form: {analysis.get('form', 'Unknown')}"
        ]
        
        for i, line in enumerate(info_lines):
            cv.putText(frame, line, 
                      (panel_x + 15, y_offset + i * line_height),
                      cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

    def run(self) -> None:
        """Run the medicine scanner application."""
        logger.info("Starting medicine scanner...")
        print("\n" + "="*60)
        print("PharmaSee - Medicine Scanner")
        print("="*60)
        print("Controls:")
        print("  S - Scan for medicine")
        print("  R - Reset detection")
        print("  Q - Quit application")
        print("="*60 + "\n")
        
        try:
            while True:
                # Read frame from camera
                frame_read_success, frame = self.camera_capture.read()
                
                if not frame_read_success:
                    logger.error("Failed to read frame from camera")
                    break
                
                # Draw UI elements
                display_frame = self._draw_ui_elements(
                    frame, 
                    self.last_detected_medicine,
                    self.last_analysis
                )
                
                # Display the frame
                cv.imshow("PharmaSee - Medicine Scanner", display_frame)
                
                # Handle keyboard input
                key = cv.waitKey(1) & 0xFF
                
                if key == ord('q') or key == ord('Q'):
                    logger.info("Quit requested by user")
                    break
                
                elif key == ord('s') or key == ord('S'):
                    logger.info("Manual scan triggered")
                    self._perform_scan(frame)
                
                elif key == ord('r') or key == ord('R'):
                    logger.info("Reset detection")
                    self.last_detected_medicine = None
                    self.last_analysis = None
                
                # Auto-scan at intervals
                elif self._should_scan():
                    self._perform_scan(frame)
        
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        
        except Exception as e:
            logger.error(f"Error in scanner loop: {e}", exc_info=True)
        
        finally:
            self._cleanup()

    def _perform_scan(self, frame: np.ndarray) -> None:
        """
        Perform medicine detection and analysis on a frame.

        Args:
            frame: Video frame to scan.
        """
        self.last_scan_time = time.time()
        
        logger.info("Scanning for medicine...")
        print("\n🔍 Scanning for medicine...")
        
        # Detect medicine from frame
        medicine_name = self._detect_medicine_from_frame(frame)
        
        if medicine_name:
            logger.info(f"Medicine detected: {medicine_name}")
            print(f"✓ Medicine detected: {medicine_name}")
            print("🤖 Analyzing with AI...")
            
            # Analyze with LLM
            analysis = self._analyze_medicine_with_llm(medicine_name)
            
            # Store results
            self.last_detected_medicine = medicine_name
            self.last_analysis = analysis
            
            # Print results to console
            print("\n" + "─"*50)
            print(f"Medicine Name: {medicine_name}")
            print(f"Type: {analysis.get('type', 'Unknown')}")
            print(f"Primary Use: {analysis.get('use', 'Unknown')}")
            print(f"Drug Class: {analysis.get('drug_class', 'Unknown')}")
            print(f"Common Form: {analysis.get('form', 'Unknown')}")
            print("─"*50 + "\n")
        else:
            logger.info("No medicine detected in frame")
            print("✗ No medicine detected. Please try again.\n")

    def _cleanup(self) -> None:
        """Clean up resources."""
        logger.info("Cleaning up resources...")
        
        if hasattr(self, 'camera_capture') and self.camera_capture is not None:
            self.camera_capture.release()
        
        cv.destroyAllWindows()
        
        logger.info("Cleanup complete")


def main():
    """Main entry point for the application."""
    try:
        scanner = MedicineScanner()
        scanner.run()
    except Exception as e:
        logger.error(f"Failed to start scanner: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        print("\nPlease check:")
        print("  1. OpenAI API key is set in config/config.json or OPENAI_API_KEY env variable")
        print("  2. Camera is connected and accessible")
        print("  3. All required packages are installed (run: pip install -r requirements.txt)")


if __name__ == "__main__":
    main()


