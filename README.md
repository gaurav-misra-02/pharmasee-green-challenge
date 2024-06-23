# PharmaSee - AI-Powered Medicine Scanner

PharmaSee is an intelligent medicine identification system that uses computer vision (OCR) and Large Language Models (LLMs) to identify medications and provide detailed information about their type, usage, and classification.

## Features

- **Real-time Medicine Detection**: Uses camera and OCR to detect medicine names from packaging
- **AI-Powered Analysis**: Leverages OpenAI's GPT-3.5 to determine medicine type, usage, and classification
- **Lightning Fast**: Produces complete analysis results in less than 1 second
- **Fuzzy Matching**: Smart medicine name matching even with partial or misspelled text
- **User-Friendly Interface**: Clean OpenCV-based GUI with real-time results display
- **Configurable**: Easy configuration through JSON files
- **Comprehensive Logging**: Detailed logging for debugging and monitoring

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam/Camera
- OpenAI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pharmasee-green-challenge
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**
   
   Copy the example configuration:
   ```bash
   cp config/config.example.json config/config.json
   ```
   
   Edit `config/config.json` and add your OpenAI API key:
   ```json
   {
     "openai": {
       "api_key": "your-actual-api-key-here"
     }
   }
   ```
   
   Alternatively, set the API key as an environment variable:
   ```bash
   export OPENAI_API_KEY="your-actual-api-key-here"
   ```

4. **Run the application**
   ```bash
   cd src
   python medicine_scanner.py
   ```

## Usage

### Controls

- **S** - Manually trigger a scan
- **R** - Reset the current detection
- **Q** - Quit the application

### How It Works

1. Point your camera at medicine packaging with clear text
2. Press 'S' to scan or wait for auto-scan (every 2 seconds by default)
3. The system will:
   - Extract text using OCR
   - Match against the medicine database
   - Analyze using GPT-3.5 to determine type and usage
   - Display results on screen

## Project Structure

```
pharmasee-green-challenge/
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── .gitignore                 # Git ignore rules
├── config/
│   ├── config.json            # Main configuration (add your API key here)
│   └── config.example.json    # Example configuration template
├── data/
│   └── medicines.csv          # Medicine database (names only)
├── src/
│   ├── __init__.py
│   ├── medicine_scanner.py    # Main application
│   ├── llm_analyzer.py        # LLM integration for medicine analysis
│   ├── ocr_reader.py          # OCR wrapper
│   ├── medicine_database.py   # Database management
│   └── config_manager.py      # Configuration management
├── tests/
│   └── test_ocr.py            # Test suite
└── docs/
    ├── abstract.pdf
    ├── Green Challenge Presentation.pptx
    └── Green Challenge Model.stl
```

## Configuration

The `config/config.json` file allows you to customize:

- **OpenAI Settings**: API key, model, temperature, max tokens
- **Camera Settings**: Device index, resolution
- **OCR Settings**: Languages, confidence threshold
- **Scanner Settings**: Scan interval, display duration

Example configuration:

```json
{
  "openai": {
    "api_key": "your-api-key",
    "model": "gpt-3.5-turbo",
    "temperature": 0.3,
    "max_tokens": 200
  },
  "camera": {
    "device_index": 0,
    "frame_width": 1280,
    "frame_height": 720
  },
  "ocr": {
    "languages": ["en"],
    "confidence_threshold": 0.5
  }
}
```

## Medicine Database

The medicine database (`data/medicines.csv`) contains known medicine names for validation. Format:

```csv
name
Aspirin
Ibuprofen
Paracetamol
...
```

You can add more medicines to this file. The system will still analyze medicines not in the database using the LLM.

## Testing

Run the test suite to verify installation:

```bash
cd tests
python test_ocr.py
```

This will test:
- Configuration loading
- Medicine database functionality
- OCR reader initialization

## Troubleshooting

### Camera Not Opening
- Check if another application is using the camera
- Try changing `device_index` in config (0, 1, 2, etc.)
- Verify camera permissions on your system

### OpenAI API Errors
- Verify your API key is correct
- Check your OpenAI account has available credits
- Ensure you have internet connectivity

### OCR Not Detecting Text
- Ensure good lighting conditions
- Hold medicine packaging steady and close to camera
- Make sure text is clear and in focus
- Adjust `confidence_threshold` in config (lower for more detections)

### Installation Issues
- Make sure you're using Python 3.8+
- Try installing dependencies one by one if bulk install fails
- On Windows, you may need Visual C++ Build Tools for some packages

## Contributing

This project was created for the Green Challenge. Contributions and improvements are welcome!

## License

This project is part of the PharmaSee Green Challenge submission.

## Acknowledgments

- EasyOCR for text detection
- OpenAI for GPT-3.5 API
- OpenCV for image processing
- The Green Challenge organizers

## Support

For issues and questions, please check the troubleshooting section or review the logs in the console output.

---


