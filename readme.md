# 🎵 YouTube Downloader & MP3 Converter

A powerful and user-friendly desktop application to download YouTube videos and convert them to high-quality audio formats. Built with Python and tkinter.

## ✨ Features

- **Download YouTube Videos** - Enter single or multiple YouTube URLs
- **Audio Conversion** - Convert videos to MP3, M4A, WAV, or FLAC formats
- **Quality Selection** - Choose audio quality (128kbps to 320kbps)
- **Batch Processing** - Download multiple videos at once
- **Progress Tracking** - Real-time progress bar and status updates
- **Download Log** - Detailed logging of all operations
- **Custom Download Location** - Choose where to save your files
- **Clipboard Support** - Paste URLs directly from clipboard

## 📋 Prerequisites

Before installing, make sure you have:

- **Python 3.7 or higher** installed on your system
- **FFmpeg** installed (required for audio conversion)
- **Internet connection** for downloading videos

### Installing FFmpeg

#### Windows:
1. Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (download `ffmpeg-release-essentials.zip`)
2. Extract the zip file to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your system PATH:
   - Press `Win + R`, type `sysdm.cpl`
   - Go to Advanced → Environment Variables
   - Under System Variables, find `Path`, click Edit
   - Click New and add `C:\ffmpeg\bin`
   - Click OK on all windows
4. Verify installation by opening a new Command Prompt and typing:
   ffmpeg -version

## 🛠️ Installation

1. **Clone or download** this repository:

git clone <https://github.com/BhathiyaVicum/mp3_downloader>
cd <repository_folder>

2. **Clone or download** this repository:

pip install yt-dlp

## 🛠️ Run the Python script

Run the Python script: python youtube_downloader.py



