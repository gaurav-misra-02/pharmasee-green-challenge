"""
Medicine Database Module

This module handles loading and searching the medicine database
from CSV files with fuzzy matching capabilities.
"""

import logging
from pathlib import Path
from typing import List, Optional, Tuple

import pandas as pd
from fuzzywuzzy import fuzz

logger = logging.getLogger(__name__)


class MedicineDatabase:
    """Manages the medicine database with search capabilities."""

    def __init__(self, database_path: str):
        """
        Initialize the medicine database.

        Args:
            database_path: Path to the CSV file containing medicine data.
        """
        self.database_path = Path(database_path)
        self.medicines: List[str] = []
        self._load_database()

    def _load_database(self) -> None:
        """Load the medicine database from CSV file."""
        try:
            if not self.database_path.exists():
                logger.warning(f"Database file not found: {self.database_path}")
                logger.info("Creating empty medicine database")
                self.medicines = []
                return

            df = pd.read_csv(self.database_path)
            
            # Expecting at least a 'name' column
            if 'name' not in df.columns:
                logger.error("CSV must contain a 'name' column")
                raise ValueError("Invalid CSV format: missing 'name' column")
            
            self.medicines = df['name'].dropna().str.strip().tolist()
            logger.info(f"Loaded {len(self.medicines)} medicines from database")

        except Exception as e:
            logger.error(f"Error loading medicine database: {e}")
            self.medicines = []

    def search_medicine(self, query: str, threshold: int = 80) -> Optional[str]:
        """
        Search for a medicine in the database using fuzzy matching.

        Args:
            query: Medicine name to search for.
            threshold: Minimum similarity score (0-100) to consider a match.

        Returns:
            Matched medicine name or None if no match found.
        """
        if not self.medicines:
            logger.warning("Medicine database is empty")
            return None

        query_lower = query.lower().strip()
        
        # First, try exact match
        for medicine in self.medicines:
            if medicine.lower() == query_lower:
                logger.info(f"Exact match found: {medicine}")
                return medicine

        # If no exact match, try fuzzy matching
        best_match = None
        best_score = 0

        for medicine in self.medicines:
            score = fuzz.ratio(query_lower, medicine.lower())
            if score > best_score:
                best_score = score
                best_match = medicine

        if best_score >= threshold:
            logger.info(f"Fuzzy match found: {best_match} (score: {best_score})")
            return best_match
        
        logger.debug(f"No match found for: {query} (best score: {best_score})")
        return None

    def get_best_matches(self, query: str, top_n: int = 5) -> List[Tuple[str, int]]:
        """
        Get the top N best matching medicines with their scores.

        Args:
            query: Medicine name to search for.
            top_n: Number of top matches to return.

        Returns:
            List of tuples (medicine_name, similarity_score) sorted by score.
        """
        if not self.medicines:
            return []

        query_lower = query.lower().strip()
        
        matches = [
            (medicine, fuzz.ratio(query_lower, medicine.lower()))
            for medicine in self.medicines
        ]
        
        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        
        return matches[:top_n]

    def is_valid_medicine(self, medicine_name: str, threshold: int = 80) -> bool:
        """
        Check if a medicine name exists in the database.

        Args:
            medicine_name: Name to validate.
            threshold: Minimum similarity score to consider valid.

        Returns:
            True if medicine is found, False otherwise.
        """
        return self.search_medicine(medicine_name, threshold) is not None

    def add_medicine(self, medicine_name: str) -> None:
        """
        Add a new medicine to the in-memory database.

        Note: This does not persist to the CSV file.

        Args:
            medicine_name: Name of the medicine to add.
        """
        medicine_name = medicine_name.strip()
        if medicine_name and medicine_name not in self.medicines:
            self.medicines.append(medicine_name)
            logger.info(f"Added medicine to database: {medicine_name}")

    def get_all_medicines(self) -> List[str]:
        """
        Get all medicines in the database.

        Returns:
            List of all medicine names.
        """
        return self.medicines.copy()

    def count(self) -> int:
        """
        Get the number of medicines in the database.

        Returns:
            Count of medicines.
        """
        return len(self.medicines)


