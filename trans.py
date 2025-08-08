#!/usr/bin/env python3
"""
Audio Transcription Script using OpenAI Whisper API
Based on: https://github.com/naeljb/speech-to-text/blob/main/Transcribe%20audio%20in%20python%20with%20Whisper-1.ipynb

This script can transcribe single or multiple audio files to text using OpenAI's Whisper-1 model.
Supports formats: mp3, mp4, mpeg, mpga, m4a, wav, webm
"""

# ============================================================================
# 🔧 CONFIGURATION SECTION - EDIT THESE VALUES
# ============================================================================

# OpenAI API Configuration
OPENAI_API_KEY = "YOUR_API_KEY"  # Replace with your actual API key
DEFAULT_LANGUAGE = "en"  # Default language for transcription (en, es, fr, de, etc.)

# File Settings
MAX_FILE_SIZE_MB = 25  # Maximum file size in MB (OpenAI limit)
SUPPORTED_FORMATS = ['.mp3', '.mp4', '.mpeg', '.mpga', '.m4a', '.wav', '.webm']

# Output Settings
DEFAULT_OUTPUT_DIR = ""  # Leave empty to save in same directory as script
AUTO_SAVE_TRANSCRIPTS = False  # Set to True to automatically save all transcripts
TRANSCRIPT_FILE_SUFFIX = "_transcript"  # Suffix for saved transcript files

# Display Settings
SHOW_PROGRESS = True  # Show progress messages during transcription
USE_EMOJIS = True  # Use emojis in console output

# ============================================================================
# END CONFIGURATION SECTION
# ============================================================================

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional
from openai import OpenAI

class AudioTranscriber:
    """
    A class to handle audio transcription using OpenAI's Whisper API
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize the transcriber with OpenAI API key
        
        Args:
            api_key (str): Your OpenAI API key (optional, uses config if not provided)
        """
        # Use provided API key or fall back to configuration
        key_to_use = api_key if api_key else OPENAI_API_KEY
        
        if not key_to_use or key_to_use == "your-openai-api-key-here":
            raise ValueError("Please set your OpenAI API key in the configuration section or provide it as parameter")
        
        self.client = OpenAI(api_key=key_to_use)
        self.supported_formats = set(SUPPORTED_FORMATS)
        self.max_file_size = MAX_FILE_SIZE_MB * 1024 * 1024  # Convert MB to bytes
        self.show_progress = SHOW_PROGRESS
        self.use_emojis = USE_EMOJIS
    
    def validate_audio_file(self, file_path: str) -> bool:
        """
        Validate if the audio file is supported and within size limits
        
        Args:
            file_path (str): Path to the audio file
            
        Returns:
            bool: True if file is valid, False otherwise
        """
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            error_msg = f"Error: File does not exist: {file_path}"
            print(f"❌ {error_msg}" if self.use_emojis else error_msg)
            return False
        
        # Check file format
        if path.suffix.lower() not in self.supported_formats:
            error_msg = f"Error: Unsupported format '{path.suffix}'. Supported formats: {', '.join(self.supported_formats)}"
            print(f"❌ {error_msg}" if self.use_emojis else error_msg)
            return False
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > self.max_file_size:
            error_msg = f"Error: File size ({file_size / (1024*1024):.1f} MB) exceeds {MAX_FILE_SIZE_MB} MB limit"
            print(f"❌ {error_msg}" if self.use_emojis else error_msg)
            return False
        
        return True
    
    def transcribe_single_audio(self, file_path: str, language: str = None) -> Optional[str]:
        """
        Transcribe a single audio file
        
        Args:
            file_path (str): Path to the audio file
            language (str): Language code (uses DEFAULT_LANGUAGE if not provided)
            
        Returns:
            Optional[str]: Transcribed text or None if error occurred
        """
        if not self.validate_audio_file(file_path):
            return None
        
        # Use provided language or fall back to configuration
        lang = language if language else DEFAULT_LANGUAGE
        
        try:
            if self.show_progress:
                progress_msg = f"Transcribing: {file_path}"
                print(f"🎵 {progress_msg}" if self.use_emojis else progress_msg)
            
            with open(file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text",
                    language=lang
                )
            
            if self.show_progress:
                success_msg = f"Successfully transcribed: {Path(file_path).name}"
                print(f"✅ {success_msg}" if self.use_emojis else success_msg)
            
            # Auto-save if configured
            if AUTO_SAVE_TRANSCRIPTS:
                self._auto_save_transcript(transcript, file_path)
            
            return transcript
            
        except Exception as e:
            error_msg = f"Error transcribing {file_path}: {e}"
            print(f"❌ {error_msg}" if self.use_emojis else error_msg)
            return None
    
    def _auto_save_transcript(self, transcript: str, original_file_path: str) -> None:
        """
        Automatically save transcript based on configuration settings
        
        Args:
            transcript (str): The transcribed text
            original_file_path (str): Path to the original audio file
        """
        try:
            base_name = Path(original_file_path).stem
            output_dir = DEFAULT_OUTPUT_DIR if DEFAULT_OUTPUT_DIR else Path(original_file_path).parent
            output_path = Path(output_dir) / f"{base_name}{TRANSCRIPT_FILE_SUFFIX}.txt"
            
            self.save_transcript_to_file(transcript, str(output_path))
        except Exception as e:
            error_msg = f"Error auto-saving transcript: {e}"
            print(f"⚠️ {error_msg}" if self.use_emojis else error_msg)
    
    def transcribe_multiple_audios(self, file_paths: List[str], language: str = None) -> Dict[str, str]:
        """
        Transcribe multiple audio files
        
        Args:
            file_paths (List[str]): List of paths to audio files
            language (str): Language code (uses DEFAULT_LANGUAGE if not provided)
            
        Returns:
            Dict[str, str]: Dictionary with filenames as keys and transcripts as values
        """
        transcriptions = {}
        lang = language if language else DEFAULT_LANGUAGE
        
        for i, file_path in enumerate(file_paths):
            file_name = Path(file_path).stem  # Get filename without extension
            key = f"{file_name}_transcript_{i}"
            
            transcript = self.transcribe_single_audio(file_path, lang)
            if transcript:
                transcriptions[key] = transcript
                if self.show_progress:
                    stored_msg = f"Transcript stored as: '{key}'"
                    print(f"📝 {stored_msg}" if self.use_emojis else stored_msg)
            else:
                if self.show_progress:
                    skip_msg = f"Skipping {file_path} due to error"
                    print(f"⚠️ {skip_msg}" if self.use_emojis else skip_msg)
        
        return transcriptions
    
    def save_transcript_to_file(self, transcript: str, output_path: str) -> bool:
        """
        Save transcript to a text file
        
        Args:
            transcript (str): The transcribed text
            output_path (str): Path where to save the text file
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transcript)
            if self.show_progress:
                save_msg = f"Transcript saved to: {output_path}"
                print(f"💾 {save_msg}" if self.use_emojis else save_msg)
            return True
        except Exception as e:
            error_msg = f"Error saving transcript: {e}"
            print(f"❌ {error_msg}" if self.use_emojis else error_msg)
            return False
    
    def combine_transcripts(self, transcriptions: Dict[str, str], separator: str = "\n\n--- Next Audio ---\n\n") -> str:
        """
        Combine multiple transcripts into one string
        
        Args:
            transcriptions (Dict[str, str]): Dictionary of transcripts
            separator (str): Separator between transcripts
            
        Returns:
            str: Combined transcript text
        """
        return separator.join(transcriptions.values())


def get_api_key() -> str:
    """
    Get OpenAI API key from configuration, environment variable, or user input
    
    Returns:
        str: The API key
    """
    # First, try configuration
    if OPENAI_API_KEY and OPENAI_API_KEY != "your-openai-api-key-here":
        return OPENAI_API_KEY
    
    # Then try environment variable
    env_key = os.getenv('OPENAI_API_KEY')
    if env_key:
        return env_key
    
    # Finally, ask user for input
    emoji_prefix = "🔑 " if USE_EMOJIS else ""
    print(f"{emoji_prefix}OpenAI API key not found in configuration or environment variables.")
    print("Please enter your OpenAI API key:")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        error_msg = "Error: API key is required!"
        print(f"❌ {error_msg}" if USE_EMOJIS else error_msg)
        sys.exit(1)
    
    return api_key


def main():
    """
    Main function to run the audio transcription script
    """
    title = "Audio Transcription Script using OpenAI Whisper"
    if USE_EMOJIS:
        print(f"🎤 {title}")
    else:
        print(title)
    print("=" * 50)
    
    # Get API key
    api_key = get_api_key()
    
    # Initialize transcriber (will use configuration settings)
    try:
        transcriber = AudioTranscriber()
    except ValueError as e:
        error_msg = str(e)
        print(f"❌ {error_msg}" if USE_EMOJIS else error_msg)
        return
    
    # Menu options
    while True:
        print("\nChoose an option:")
        print("1. Transcribe a single audio file")
        print("2. Transcribe multiple audio files")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            # Single file transcription
            file_path = input("Enter the path to your audio file: ").strip().strip('"')
            
            if not file_path:
                print("❌ Please provide a valid file path")
                continue
            
            transcript = transcriber.transcribe_single_audio(file_path)
            
            if transcript:
                print("\n" + "="*50)
                print("📄 TRANSCRIPT:")
                print("="*50)
                print(transcript)
                print("="*50)
                
                # Ask if user wants to save to file (unless auto-save is enabled)
                if not AUTO_SAVE_TRANSCRIPTS:
                    save_choice = input("\nSave transcript to file? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        output_path = input("Enter output file path (or press Enter for default): ").strip()
                        if not output_path:
                            base_name = Path(file_path).stem
                            output_dir = DEFAULT_OUTPUT_DIR if DEFAULT_OUTPUT_DIR else Path(file_path).parent
                            output_path = Path(output_dir) / f"{base_name}{TRANSCRIPT_FILE_SUFFIX}.txt"
                        
                        transcriber.save_transcript_to_file(transcript, str(output_path))
                else:
                    auto_msg = "Transcript automatically saved (AUTO_SAVE_TRANSCRIPTS is enabled)"
                    print(f"💾 {auto_msg}" if USE_EMOJIS else auto_msg)
        
        elif choice == "2":
            # Multiple files transcription
            print("Enter audio file paths (one per line, empty line to finish):")
            file_paths = []
            
            while True:
                path = input("File path: ").strip().strip('"')
                if not path:
                    break
                file_paths.append(path)
            
            if not file_paths:
                print("❌ No file paths provided")
                continue
            
            transcriptions = transcriber.transcribe_multiple_audios(file_paths)
            
            if transcriptions:
                print(f"\n✅ Successfully transcribed {len(transcriptions)} files")
                
                # Display all transcripts
                for key, transcript in transcriptions.items():
                    print(f"\n{'='*20} {key} {'='*20}")
                    print(transcript)
                
                # Ask if user wants to save combined transcript (unless auto-save handled individual files)
                if not AUTO_SAVE_TRANSCRIPTS:
                    save_choice = input("\nSave combined transcript to file? (y/n): ").strip().lower()
                    if save_choice == 'y':
                        combined_transcript = transcriber.combine_transcripts(transcriptions)
                        output_path = input("Enter output file path (or press Enter for 'combined_transcript.txt'): ").strip()
                        if not output_path:
                            output_dir = DEFAULT_OUTPUT_DIR if DEFAULT_OUTPUT_DIR else "."
                            output_path = Path(output_dir) / "combined_transcript.txt"
                        
                        transcriber.save_transcript_to_file(combined_transcript, str(output_path))
                else:
                    combined_msg = "Individual transcripts automatically saved (AUTO_SAVE_TRANSCRIPTS is enabled)"
                    print(f"💾 {combined_msg}" if USE_EMOJIS else combined_msg)
        
        elif choice == "3":
            goodbye_msg = "Goodbye!"
            print(f"👋 {goodbye_msg}" if USE_EMOJIS else goodbye_msg)
            break
        
        else:
            invalid_msg = "Invalid choice. Please select 1, 2, or 3."
            print(f"❌ {invalid_msg}" if USE_EMOJIS else invalid_msg)


if __name__ == "__main__":
    main()
