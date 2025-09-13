#!/usr/bin/env python3
"""
Interactive Audio Processor - Python Version
A comprehensive audio processing tool using Cleanvoice API
"""

import os
import sys
import glob
import requests
from pathlib import Path
from audio_processor import AudioProcessor


class InteractiveAudioProcessor:
    """Interactive command-line audio processor with all functionality from the JavaScript version"""
    
    def __init__(self, api_key: str):
        self.processor = AudioProcessor(api_key)
        self.function_map = {
            'rm bg': {
                'func': 'denoise_audio',
                'name': 'Remove Background Noise',
                'params': [False, {'normalize': True}]
            },
            'rm silence': {
                'func': 'remove_silences',
                'name': 'Remove Long Silences',
                'params': [{'export_format': 'auto'}]
            },
            'rm stutter': {
                'func': 'remove_stutters',
                'name': 'Remove Stutters',
                'params': [{'export_format': 'auto'}]
            },
            'rm filler': {
                'func': 'remove_fillers',
                'name': 'Remove Filler Words',
                'params': [{'export_format': 'auto'}]
            },
            'rm mouth': {
                'func': 'remove_mouth_sounds',
                'name': 'Remove Mouth Sounds',
                'params': [{'export_format': 'auto'}]
            },
            'rm hesitation': {
                'func': 'remove_hesitations',
                'name': 'Remove Hesitations',
                'params': [{'export_format': 'auto'}]
            },
            'rm breath': {
                'func': 'reduce_breath_sounds',
                'name': 'Reduce Breath Sounds',
                'params': [-80, {'export_format': 'auto'}]
            },
            'normalize': {
                'func': 'normalize_audio',
                'name': 'Normalize Audio Levels',
                'params': [-16, {'export_format': 'auto'}]
            },
            'ai enhance': {
                'func': 'enhance_with_ai',
                'name': 'AI Sound Enhancement',
                'params': [{'export_format': 'auto'}]
            },
            'preserve music': {
                'func': 'preserve_music',
                'name': 'Preserve Music Segments',
                'params': [{'export_format': 'auto'}]
            },
            'transcribe': {
                'func': 'transcribe_audio',
                'name': 'Transcribe Audio to Text',
                'params': [{'export_format': 'auto'}]
            },
            'comprehensive': {
                'func': 'enhance_audio_comprehensive',
                'name': 'Comprehensive Enhancement',
                'params': [{'export_format': 'auto', 'transcription': True}]
            }
        }
    
    def show_help(self):
        """Display the help menu with all available commands"""
        print('\n🎵 Interactive Audio Processor (Python)')
        print('=====================================')
        print('Supports: Audio files (MP3, WAV, M4A, FLAC, AAC)')
        print('')
        print('Available commands:')
        print('')
        print('🔊 Audio Cleaning:')
        print('  rm bg          - Remove background noise')
        print('  rm silence     - Remove long silences')
        print('  rm stutter     - Remove stutters')
        print('  rm filler      - Remove filler words (um, uh)')
        print('  rm mouth       - Remove mouth sounds')
        print('  rm hesitation  - Remove hesitations')
        print('  rm breath      - Reduce breath sounds')
        print('')
        print('🎛️ Audio Enhancement:')
        print('  normalize      - Normalize audio levels')
        print('  ai enhance     - AI-powered sound enhancement')
        print('  preserve music - Keep music segments during edits')
        print('')
        print('📝 Analysis:')
        print('  transcribe     - Convert speech to text')
        print('')
        print('🚀 All-in-One:')
        print('  comprehensive  - Apply all enhancements')
        print('')
        print('❓ Other commands:')
        print('  help           - Show this help')
        print('  quit           - Exit the program')
        print('')
        print('📁 Supported file formats:')
        print('  Audio: MP3, WAV, M4A, FLAC, AAC')
        print('')
    
    def find_audio_file(self) -> tuple[str, str]:
        """Find the first audio file in the current directory"""
        supported_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.aac']
        
        for ext in supported_extensions:
            pattern = f"*{ext}"
            files = glob.glob(pattern, recursive=False)
            if files:
                file_path = files[0]
                filename = os.path.basename(file_path)
                return file_path, filename
        
        return None, None
    
    def download_file(self, url: str, output_path: str) -> bool:
        """Download a file from URL to local path"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(output_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            
            return True
        except Exception as e:
            print(f'❌ Error downloading file: {e}')
            return False
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    
    async def process_audio_file(self, command: str):
        """Process audio file with the given command"""
        try:
            config = self.function_map.get(command)
            if not config:
                print('❌ Unknown command. Type "help" to see available commands.')
                return
            
            print(f'\n🎵 {config["name"]}')
            print('================\n')
            
            # Look for audio files in the current directory
            file_path, filename = self.find_audio_file()
            
            if not file_path:
                print('❌ No supported audio file found in the current directory')
                print('💡 Supported formats: MP3, WAV, M4A, FLAC, AAC')
                return
            
            print(f'📁 Found audio file: {filename}')
            print('📤 Uploading file to Cleanvoice servers...')
            
            # Upload the file
            signed_url = self.processor.upload_file(file_path, filename)
            print('✅ File uploaded successfully!')
            
            # Process the audio
            params = config['params'].copy()
            print(f'\n🔧 Processing audio with {config["name"]}...')
            
            # Call the appropriate method
            method = getattr(self.processor, config['func'])
            processing_job = method(signed_url, *params)
            
            print('✅ Processing job created!')
            print(f'🆔 Job ID: {processing_job["id"]}')
            
            # Wait for completion
            print('\n⏳ Waiting for processing to complete...')
            print('This may take a few minutes depending on the file size...\n')
            
            result = self.processor.wait_for_completion(processing_job['id'], 5000, 300000)
            
            # Download the processed file
            print('📥 Downloading processed audio file...')
            download_url = result['result']['download_url']
            
            # Determine output file extension based on input file
            input_ext = Path(filename).suffix.lower()
            output_ext = input_ext  # Keep the same audio format
            
            output_path = f"{Path(filename).stem}-{command.replace(' ', '-')}{output_ext}"
            
            if self.download_file(download_url, output_path):
                print('\n✅ Processing completed successfully!')
                print(f'📁 File saved as: {output_path}')
                
                # Check file size
                file_size = os.path.getsize(output_path)
                print(f'📊 File size: {self.format_file_size(file_size)}')
                
                if file_size > 0:
                    print('🎉 The audio file is ready to play!')
                else:
                    print('⚠️ Warning: Downloaded file is empty')
                
                # Show statistics
                if 'statistics' in result['result']:
                    stats = result['result']['statistics']
                    print('\n📊 Processing Statistics:')
                    print(f'   Dead air removed: {stats.get("DEADAIR", 0)}')
                    print(f'   Breaths removed: {stats.get("BREATH", 0)}')
                    print(f'   Stutters removed: {stats.get("STUTTERING", 0)}')
                    print(f'   Mouth sounds removed: {stats.get("MOUTH_SOUND", 0)}')
                    print(f'   Filler sounds removed: {stats.get("FILLER_SOUND", 0)}')
                
                # Show transcription if available
                if 'transcription' in result['result'] and 'paragraphs' in result['result']['transcription']:
                    paragraphs = result['result']['transcription']['paragraphs']
                    print('\n📝 Transcription:')
                    for i, paragraph in enumerate(paragraphs[:3]):
                        print(f'   {i + 1}. [{paragraph["start"]}s - {paragraph["end"]}s] {paragraph["text"]}')
                    if len(paragraphs) > 3:
                        print(f'   ... and {len(paragraphs) - 3} more paragraphs')
                
                print('\n🎵 Ready for next command! Type "help" for options or "quit" to exit.')
            
        except Exception as e:
            print(f'❌ Error processing audio: {e}')
            print('\n💡 Make sure your API key is correct and you have internet connection')
    
    def run(self):
        """Start the interactive session"""
        print('🎵 Welcome to the Interactive Audio Processor (Python)!')
        print('=====================================================')
        self.show_help()
        
        while True:
            try:
                command = input('\n🎵 Enter command (or "help"): ').strip().lower()
                
                if command in ['quit', 'exit']:
                    print('\n👋 Goodbye! Thanks for using the Audio Processor!')
                    break
                
                if command == 'help':
                    self.show_help()
                    continue
                
                if command == '':
                    print('❌ Please enter a command. Type "help" for options.')
                    continue
                
                # Run the async function in sync context
                import asyncio
                asyncio.run(self.process_audio_file(command))
                
            except KeyboardInterrupt:
                print('\n\n👋 Goodbye! Thanks for using the Audio Processor!')
                break
            except Exception as e:
                print(f'❌ Unexpected error: {e}')


def main():
    """Main entry point"""
    # You can set your API key here or use environment variable
    api_key = os.getenv('CLEANVOICE_API_KEY', 'FJB8s8nbmY9UQcfeXFeB6tqJmjwDUkKN')
    
    if not api_key:
        print('❌ Please set your Cleanvoice API key in the CLEANVOICE_API_KEY environment variable')
        print('   or modify the api_key variable in the script')
        sys.exit(1)
    
    processor = InteractiveAudioProcessor(api_key)
    processor.run()


if __name__ == '__main__':
    main()
