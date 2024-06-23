"""
LLM Analyzer Module

This module uses OpenAI's GPT-3.5 to analyze medicine names and determine
their type, usage, and other relevant information.
"""

import logging
from typing import Dict, Optional

from openai import OpenAI

logger = logging.getLogger(__name__)


class MedicineLLMAnalyzer:
    """Uses Large Language Models to analyze and classify medicines."""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", 
                 temperature: float = 0.3, max_tokens: int = 200):
        """
        Initialize the LLM analyzer.

        Args:
            api_key: OpenAI API key.
            model: Model name to use (default: gpt-3.5-turbo).
            temperature: Model temperature for response variability.
            max_tokens: Maximum tokens in response.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        logger.info(f"Initialized LLM Analyzer with model: {model}")

    def _create_medicine_analysis_prompt(self, medicine_name: str) -> str:
        """
        Create a prompt for analyzing medicine information.

        Args:
            medicine_name: Name of the medicine to analyze.

        Returns:
            Formatted prompt string.
        """
        prompt = f"""You are a pharmaceutical expert assistant. Analyze the following medicine name and provide structured information.

Medicine Name: {medicine_name}

Please provide the following information in a structured format:
1. Medicine Type: (e.g., Antibiotic, Analgesic, Antacid, Antihistamine, etc.)
2. Primary Use: (Brief description of what it's used for)
3. Drug Class: (Pharmacological classification)
4. Common Form: (Tablet, Capsule, Cream, Syrup, etc.)

Format your response as follows:
Type: [medicine type]
Use: [primary use]
Class: [drug class]
Form: [common form]

If you don't recognize the medicine name or it doesn't appear to be a valid medicine, respond with:
Type: Unknown
Use: Unable to determine - please verify medicine name
Class: Unknown
Form: Unknown"""

        return prompt

    def analyze_medicine(self, medicine_name: str) -> Dict[str, str]:
        """
        Analyze a medicine using the LLM and extract key information.

        Args:
            medicine_name: Name of the medicine to analyze.

        Returns:
            Dictionary containing medicine information with keys:
            - type: Medicine type/category
            - use: Primary medical use
            - drug_class: Pharmacological class
            - form: Physical form (tablet, cream, etc.)

        Raises:
            Exception: If LLM API call fails.
        """
        logger.info(f"Analyzing medicine: {medicine_name}")

        try:
            prompt = self._create_medicine_analysis_prompt(medicine_name)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a pharmaceutical expert providing accurate medicine information."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            # Extract the response text
            response_text = response.choices[0].message.content.strip()
            logger.debug(f"LLM Response: {response_text}")

            # Parse the structured response
            medicine_info = self._parse_llm_response(response_text)
            
            logger.info(f"Successfully analyzed medicine: {medicine_name} - Type: {medicine_info.get('type', 'Unknown')}")
            return medicine_info

        except Exception as e:
            logger.error(f"Error analyzing medicine with LLM: {e}")
            return {
                'type': 'Error',
                'use': f'Failed to analyze: {str(e)}',
                'drug_class': 'Unknown',
                'form': 'Unknown'
            }

    def _parse_llm_response(self, response_text: str) -> Dict[str, str]:
        """
        Parse the structured response from the LLM.

        Args:
            response_text: Raw response text from LLM.

        Returns:
            Dictionary with parsed medicine information.
        """
        info = {
            'type': 'Unknown',
            'use': 'Unknown',
            'drug_class': 'Unknown',
            'form': 'Unknown'
        }

        # Parse the structured response
        lines = response_text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()

                if key == 'type':
                    info['type'] = value
                elif key == 'use':
                    info['use'] = value
                elif key == 'class':
                    info['drug_class'] = value
                elif key == 'form':
                    info['form'] = value

        return info

    def get_medicine_type(self, medicine_name: str) -> str:
        """
        Get just the medicine type using LLM analysis.

        Args:
            medicine_name: Name of the medicine.

        Returns:
            Medicine type as a string.
        """
        analysis = self.analyze_medicine(medicine_name)
        return analysis.get('type', 'Unknown')

    def get_detailed_info(self, medicine_name: str) -> str:
        """
        Get a formatted detailed information string about the medicine.

        Args:
            medicine_name: Name of the medicine.

        Returns:
            Formatted string with medicine details.
        """
        analysis = self.analyze_medicine(medicine_name)
        
        info_string = f"""
Medicine: {medicine_name}
Type: {analysis['type']}
Primary Use: {analysis['use']}
Drug Class: {analysis['drug_class']}
Common Form: {analysis['form']}
        """.strip()
        
        return info_string


