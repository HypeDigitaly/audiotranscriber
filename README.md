# 🎤 **Audio Transcription Script Setup Guide**

This script transcribes audio files to text using **OpenAI's Whisper API**. All settings are now **configurable at the top of the script**.

## 📋 **Quick Setup**

### **Step 1: Install Dependencies**
```bash
pip install openai
```

### **Step 2: Configure Your Settings**
Open `trans.py` and edit the **CONFIGURATION SECTION** at the top:

```python
# ============================================================================
# 🔧 CONFIGURATION SECTION - EDIT THESE VALUES
# ============================================================================

# OpenAI API Configuration
OPENAI_API_KEY = "your-openai-api-key-here"  # ⚠️ REPLACE WITH YOUR ACTUAL KEY
DEFAULT_LANGUAGE = "en"  # Change to your preferred language

# Output Settings
AUTO_SAVE_TRANSCRIPTS = False  # Set to True for automatic saving
DEFAULT_OUTPUT_DIR = ""  # Set your preferred save location

# Display Settings
USE_EMOJIS = True  # Set to False if you don't want emojis
SHOW_PROGRESS = True  # Set to False for minimal output
```

### **Step 3: Get Your OpenAI API Key**
1. Go to [OpenAI's API Keys page](https://platform.openai.com/api-keys)
2. Sign up/login to your account
3. Click **"Create new secret key"**
4. Copy the key and paste it in the `OPENAI_API_KEY` setting

### **Step 4: Run the Script**
```bash
python trans.py
```

---

## ⚙️ **Configuration Options Explained**

### **🔑 API Settings**
| Setting | Description | Example |
|---------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (**required**) | `"sk-abc123..."` |
| `DEFAULT_LANGUAGE` | Language code for transcription | `"en"`, `"es"`, `"fr"` |

### **📁 File Settings**
| Setting | Description | Default |
|---------|-------------|---------|
| `MAX_FILE_SIZE_MB` | Maximum file size (OpenAI limit) | `25` |
| `SUPPORTED_FORMATS` | Allowed audio formats | `['.mp3', '.mp4', ...]` |

### **💾 Output Settings**
| Setting | Description | Example |
|---------|-------------|---------|
| `DEFAULT_OUTPUT_DIR` | Where to save transcripts | `"C:/Users/You/Desktop"` |
| `AUTO_SAVE_TRANSCRIPTS` | Save automatically without asking | `True` or `False` |
| `TRANSCRIPT_FILE_SUFFIX` | Added to filename | `"_transcript"` |

### **🎨 Display Settings**
| Setting | Description | Example |
|---------|-------------|---------|
| `SHOW_PROGRESS` | Show progress messages | `True` or `False` |
| `USE_EMOJIS` | Use emojis in output | `True` or `False` |

---

## 🚀 **Common Configuration Examples**

### **Example 1: Basic English Transcription**
```python
OPENAI_API_KEY = "sk-your-key-here"
DEFAULT_LANGUAGE = "en"
AUTO_SAVE_TRANSCRIPTS = True
DEFAULT_OUTPUT_DIR = "C:/Users/YourName/Desktop/Transcripts"
```

### **Example 2: Spanish with Custom Settings**
```python
OPENAI_API_KEY = "sk-your-key-here"
DEFAULT_LANGUAGE = "es"
AUTO_SAVE_TRANSCRIPTS = True
TRANSCRIPT_FILE_SUFFIX = "_transcripcion"
USE_EMOJIS = True
```

### **Example 3: Minimal Output (No Emojis)**
```python
OPENAI_API_KEY = "sk-your-key-here"
DEFAULT_LANGUAGE = "en"
SHOW_PROGRESS = False
USE_EMOJIS = False
AUTO_SAVE_TRANSCRIPTS = True
```

---

## 🎵 **Supported Audio Formats**

- **MP3** - Most common format
- **MP4** - Video files with audio
- **WAV** - Uncompressed audio
- **M4A** - Apple audio format
- **WEBM** - Web audio format
- **MPEG/MPGA** - MPEG audio formats

**File Size Limit:** 25 MB (OpenAI's limit)

---

## 🔧 **Language Codes**

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `en` | Spanish | `es` |
| French | `fr` | German | `de` |
| Italian | `it` | Portuguese | `pt` |
| Russian | `ru` | Japanese | `ja` |
| Chinese | `zh` | Korean | `ko` |

---

## 💡 **Usage Tips**

### **For Single Files:**
1. Run the script
2. Choose option `1`
3. Enter your audio file path
4. View the transcript
5. Choose to save if desired

### **For Multiple Files:**
1. Run the script
2. Choose option `2`
3. Enter multiple file paths (one per line)
4. Press Enter on empty line to finish
5. View all transcripts
6. Choose to save combined transcript

### **Auto-Save Feature:**
- Set `AUTO_SAVE_TRANSCRIPTS = True`
- All transcripts save automatically
- No need to manually choose save options

---

## ⚠️ **Important Notes**

1. **Keep your API key secret** - Don't share it publicly
2. **Check file sizes** - Must be under 25 MB
3. **Audio quality matters** - Clear audio = better transcripts
4. **Internet required** - Uses OpenAI's online service

---

## 🆘 **Troubleshooting**

### **"API key is required" Error**
- Make sure you set `OPENAI_API_KEY` in the configuration
- Don't leave it as `"your-openai-api-key-here"`

### **"File too large" Error**
- Compress your audio file
- Use a lower bitrate/quality
- Split long recordings

### **"Unsupported format" Error**
- Convert to MP3, WAV, or another supported format
- Use free tools like Audacity or online converters

---

## 📞 **Need Help?**

1. Check the configuration section in `trans.py`
2. Review the `config_example.py` file for examples
3. Make sure your OpenAI API key is valid and has credits
4. Verify your audio file is in a supported format and under 25 MB
