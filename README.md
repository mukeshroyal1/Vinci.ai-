# Interactive Audio Processor - Python Version

A comprehensive Python-based audio processing tool using the Cleanvoice API. This is a complete Python port of the JavaScript interactive audio processor with all the same functionality.

## Features

### 🔊 Audio Cleaning
- **Remove Background Noise** - Clean up unwanted background sounds
- **Remove Long Silences** - Eliminate dead air and pauses
- **Remove Stutters** - Clean up speech stutters and repetitions
- **Remove Filler Words** - Remove "um", "uh", and other filler sounds
- **Remove Mouth Sounds** - Eliminate lip smacks and mouth noises
- **Remove Hesitations** - Clean up hesitation sounds
- **Reduce Breath Sounds** - Lower the volume of breathing sounds

### 🎛️ Audio Enhancement
- **Normalize Audio Levels** - Adjust audio to consistent loudness
- **AI Sound Enhancement** - AI-powered quality improvement
- **Preserve Music Segments** - Keep music during audio cleaning

### 📝 Analysis
- **Transcribe Audio** - Convert speech to text
- **Comprehensive Enhancement** - Apply all enhancements at once

## Installation

1. **Install Python 3.7+** (if not already installed)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**
   ```bash
   export CLEANVOICE_API_KEY="your_api_key_here"
   ```
   
   Or modify the `api_key` variable in `interactive_audio_processor.py`

## Usage

### Interactive Mode
Run the interactive processor:
```bash
python interactive_audio_processor.py
```

### Available Commands
- `rm bg` - Remove background noise
- `rm silence` - Remove long silences
- `rm stutter` - Remove stutters
- `rm filler` - Remove filler words
- `rm mouth` - Remove mouth sounds
- `rm hesitation` - Remove hesitations
- `rm breath` - Reduce breath sounds
- `normalize` - Normalize audio levels
- `ai enhance` - AI sound enhancement
- `preserve music` - Preserve music segments
- `transcribe` - Convert speech to text
- `comprehensive` - Apply all enhancements
- `help` - Show help menu
- `quit` - Exit the program

### Programmatic Usage
You can also use the AudioProcessor class directly in your Python code:

```python
from audio_processor import AudioProcessor

# Initialize with your API key
processor = AudioProcessor('your_api_key_here')

# Upload a file
signed_url = processor.upload_file('path/to/audio.mp3', 'audio.mp3')

# Process the audio
result = processor.remove_silences(signed_url, {'export_format': 'mp3'})

# Wait for completion
final_result = processor.wait_for_completion(result['id'])

# Download the result
download_url = final_result['result']['download_url']
```

## Supported File Formats

- **Audio**: MP3, WAV, M4A, FLAC, AAC

## File Structure

- `audio_processor.py` - Core AudioProcessor class with all API methods
- `interactive_audio_processor.py` - Interactive command-line interface
- `requirements.txt` - Python dependencies
- `README_PYTHON.md` - This documentation

## API Methods

The `AudioProcessor` class includes all the same methods as the JavaScript version:

### Core Processing
- `process_audio(files, config)` - Generic audio processing
- `remove_silences(files, config)` - Remove long silences
- `remove_stutters(files, config)` - Remove stutters
- `remove_fillers(files, config)` - Remove filler words
- `remove_mouth_sounds(files, config)` - Remove mouth sounds
- `remove_hesitations(files, config)` - Remove hesitations
- `denoise_audio(files, keep_music, config)` - Remove background noise
- `reduce_breath_sounds(files, mute_lufs, config)` - Reduce breath sounds
- `normalize_audio(files, target_lufs, config)` - Normalize audio levels
- `enhance_with_ai(files, config)` - AI sound enhancement
- `preserve_music(files, config)` - Preserve music segments

### Analysis & Transcription
- `transcribe_audio(files, config)` - Convert speech to text
- `summarize_audio(files, config)` - Generate audio summary
- `create_social_content(files, config)` - Create social media content

### Advanced Features
- `merge_tracks(files, normalize, config)` - Merge multiple audio tracks
- `enhance_audio_comprehensive(files, options)` - Apply all enhancements
- `export_audio(files, format, config)` - Export in specific format

### Utility Methods
- `upload_file(file_path, filename)` - Upload file to Cleanvoice
- `get_edit_status(edit_id)` - Check processing status
- `wait_for_completion(edit_id, poll_interval, max_wait_time)` - Wait for completion
- `delete_edit(edit_id)` - Delete edit job

## Configuration Options

All processing methods accept an optional `additional_config` parameter for customization:

```python
config = {
    'export_format': 'mp3',  # 'auto', 'mp3', 'wav', 'flac', 'm4a'
    'transcription': True,    # Include transcription
    'summarize': True,       # Include summary
    'target_lufs': -16,      # Target loudness level
    'mute_lufs': -80,        # Mute threshold
    'keep_music': True,      # Preserve music segments
    'export_timestamps': True # Include timestamps
}
```

## Error Handling

The Python version includes comprehensive error handling:
- API errors are caught and displayed with helpful messages
- File upload/download errors are handled gracefully
- Network timeouts are managed with retry logic
- Invalid commands are caught and suggestions are provided

## Examples

### Basic Audio Cleaning
```python
from audio_processor import AudioProcessor

processor = AudioProcessor('your_api_key')
signed_url = processor.upload_file('input.mp3', 'input.mp3')
result = processor.remove_silences(signed_url)
final = processor.wait_for_completion(result['id'])
```

### Comprehensive Enhancement
```python
# Apply all enhancements at once
result = processor.enhance_audio_comprehensive(
    signed_url, 
    {
        'export_format': 'mp3',
        'transcription': True,
        'target_lufs': -16
    }
)
```

### Batch Processing
```python
# Process multiple files
files = ['file1.mp3', 'file2.wav', 'file3.m4a']
signed_urls = [processor.upload_file(f, f) for f in files]
result = processor.merge_tracks(signed_urls, normalize=True)
```

## Troubleshooting

1. **API Key Issues**: Make sure your Cleanvoice API key is valid and has sufficient credits
2. **File Format Issues**: Ensure your audio files are in supported formats
3. **Network Issues**: Check your internet connection and firewall settings
4. **Memory Issues**: For large files, ensure you have sufficient disk space

## License

This project uses the Cleanvoice API. Please refer to their terms of service for usage guidelines.
