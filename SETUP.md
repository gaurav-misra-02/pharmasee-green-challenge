# PharmaSee Setup Guide

This guide will help you set up and run PharmaSee on your system.

## Step-by-Step Setup

### 1. Prerequisites

Make sure you have:
- Python 3.8 or higher
- A webcam/camera
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `opencv-python` - For camera and image processing
- `easyocr` - For text extraction from images
- `pandas` - For medicine database management
- `openai` - For LLM integration
- `fuzzywuzzy` - For fuzzy string matching

### 3. Configure OpenAI API Key

You have two options:

#### Option A: Configuration File (Recommended)

1. Copy the example config:
   ```bash
   cp config/config.example.json config/config.json
   ```

2. Edit `config/config.json` and replace `"your-openai-api-key-here"` with your actual API key:
   ```json
   {
     "openai": {
       "api_key": "sk-your-actual-key-here"
     }
   }
   ```

#### Option B: Environment Variable

Set the environment variable:

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-actual-key-here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-your-actual-key-here
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-your-actual-key-here"
```

### 4. Run the Application

#### Quick Start (Recommended)

**Linux/Mac:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

#### Manual Start

```bash
cd src
python medicine_scanner.py
```

## Configuration Options

Edit `config/config.json` to customize:

### OpenAI Settings
```json
"openai": {
  "api_key": "your-key",
  "model": "gpt-3.5-turbo",      // LLM model to use
  "temperature": 0.3,             // Response creativity (0-1)
  "max_tokens": 200               // Max response length
}
```

### Camera Settings
```json
"camera": {
  "device_index": 0,              // Camera ID (0 is default)
  "frame_width": 1280,            // Video width
  "frame_height": 720             // Video height
}
```

### OCR Settings
```json
"ocr": {
  "languages": ["en"],            // OCR languages
  "confidence_threshold": 0.5     // Min confidence (0-1)
}
```

### Scanner Settings
```json
"scanner": {
  "scan_interval_seconds": 2,              // Auto-scan interval
  "display_results_duration_seconds": 5    // Results display time
}
```

## Medicine Database

The system uses `data/medicines.csv` to validate medicine names. Add more medicines:

```csv
name
Aspirin
YourNewMedicine
AnotherMedicine
```

**Note:** The LLM will analyze medicines even if they're not in the database!

## Testing

Run the test suite to verify installation:

```bash
cd tests
python test_ocr.py
```

Expected output:
```
✓ Configuration loaded successfully
✓ Database loaded with X medicines
✓ OCR Reader initialized successfully
```

## Troubleshooting

### Issue: "Could not open camera"

**Solutions:**
1. Check if another app is using the camera
2. Try different camera indices in config (0, 1, 2...)
3. Check camera permissions:
   - **Mac:** System Preferences → Security & Privacy → Camera
   - **Windows:** Settings → Privacy → Camera

### Issue: "OpenAI API key not found"

**Solutions:**
1. Verify the key in `config/config.json`
2. Check for typos (keys start with `sk-`)
3. Ensure the JSON syntax is correct (no trailing commas)

### Issue: "No module named 'cv2'"

**Solution:**
```bash
pip install opencv-python
```

### Issue: OCR not working / No text detected

**Solutions:**
1. Improve lighting conditions
2. Hold medicine packaging steady
3. Move closer to camera
4. Lower `confidence_threshold` in config (try 0.3)

### Issue: Slow performance

**Solutions:**
1. Increase `scan_interval_seconds` in config
2. Reduce camera resolution
3. Close other applications
4. Ensure stable internet for LLM calls

### Issue: EasyOCR taking long to initialize

This is normal on first run. EasyOCR downloads language models (~100MB). Subsequent runs will be faster.

## Usage Tips

1. **Good Lighting**: Ensure the medicine text is well-lit
2. **Clear Text**: Hold packaging so text is clearly visible
3. **Steady Camera**: Keep the medicine still for a few seconds
4. **Close Distance**: Move medicine closer if text is small
5. **Manual Scan**: Press 'S' for better control over when to scan

## System Requirements

- **RAM**: 4GB minimum (8GB recommended for EasyOCR)
- **Internet**: Required for OpenAI API calls
- **Camera**: Any USB webcam or built-in camera
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+

## Cost Estimation

OpenAI GPT-3.5-turbo costs approximately:
- **$0.0005** per medicine scan (input)
- **$0.0015** per medicine scan (output)
- **~$0.002** per scan total

100 scans ≈ $0.20 USD

## Next Steps

After successful setup:
1. Test with a medicine label
2. Adjust camera position for best angle
3. Customize scan interval if needed
4. Add more medicines to database
5. Review logs for debugging

## Support

Having issues? Check:
1. This setup guide
2. Main [README.md](README.md)
3. Console output for error messages
4. Log files for detailed debugging

---

**Ready to scan!**


