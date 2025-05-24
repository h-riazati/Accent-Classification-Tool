# Accent Filter Tool

This tool downloads a public video URL (direct MP4 or Loom), extracts its audio, and classifies the speaker's English accent using a chosen pre-trained model.

## Setup
```bash
pip install -r src/requirements.txt
```

## CLI Usage
```bash
python src/classify.py --url "<VIDEO_URL>" --out sample.wav --model dima806
```

## Web UI Usage
```bash
streamlit run src/app.py
```

## Testing
```bash
pytest
```