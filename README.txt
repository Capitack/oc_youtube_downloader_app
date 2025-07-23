

# 🚀 OC's YouTube Video Downloader

## 🎯 FEATURES THAT STAND OUT

### 🚫 NO ADS / ADWARE / BLOATWARE
*(donations are appreciated!)*

### 🎥 MAXIMUM RESOLUTION
Get the highest quality video available even 4k - no questions asked!

### 🎧 AUDIO & VIDEO
Download full videos or extract just the audio in high quality

### 🔈 AUDIO COMPATIBILITY NOTE
- Some players (like Windows Media Player) may not play audio due to Opus codec
- For best compatibility, use media players like:
  - VLC Media Player (recommended)
  - Windows 10/11 Movies & TV (with codec pack)
  - Mobile media players (most support Opus)
  - Modern web browsers

---

A simple and user-friendly YouTube video and audio downloader with a graphical interface. Download upto 4k videos and extract audio in high quality!



## ✨ Features
- **Download Options**:
  - Download YouTube videos in various resolutions
  - Extract audio only in high-quality MP3 format
- **User-Friendly Interface**:
  - Clean and intuitive GUI
  - Progress tracking with ETA
  - Download speed monitoring
  
- **Smart Features**:
  - Automatic format detection
  - FFmpeg integration for best quality downloads

-

## 🚀 Quick Start if you just want to download videos out of box 

### 📥 Download and Run
1. **Download** the latest release package (ZIP file) from the [Releases](https://github.com/Capitack/oc_youtube_downloader_apps) page
2. **Extract** the ZIP file to a folder of your choice
3. **Important**: Keep these files together in the same folder:
   - `OC_YouTube_Downloader.exe`
   - The `ffmpeg` folder (contains required FFmpeg files)
4. **Run** `OC_YouTube_Downloader.exe`
   - Windows might show a security warning since the app is unsigned
   - Click "More info" and then "Run anyway"
   - You only need to do this once

   ## 💖 Support
If you find this tool useful, please consider supporting future development through the donation link in the application. https://paypal.me/opeadewuyi

## 👩‍💻 For Developers / Advanced Users

### Prerequisites
- Python 3.7+
- FFmpeg (required for video/audio processing):
  1. Download from either:
     - [Official](https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip) or 
     - [Google Drive Mirror](https://drive.google.com/file/d/15L5lJJV8VfDjRyK6r9SKUgMbjV6CmDI9/view?usp=sharing)
  2. Extract the ZIP file
  3. Copy the 'ffmpeg-7.1.1-essentials_build' folder to this application's directory (or in the dist folder if building a .exe file)

  The final directory structure should look like:
   ```
   oc_youtube_downloader_app/
   ├── ffmpeg-7.1.1-essentials_build/
   │   ├── bin/
   │   ├── doc/
   │   └── ...
   └── oc_youtube_gui_downloader.py

   a screenshot is provided in the repository for ffmpeg folder placement

### Installation from Source
1. Clone this repository:
   ```
   git clone [repository-url]
   cd oc_downloader_app
   ```
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. add FFmpeg files to the `ffmpeg` folder

## 🎮 How to Use
1. **Download Video**:
   - Paste YouTube URL
   - Select "Video" download type
   - Click "Get Available Formats"
   - Choose your preferred resolution
   - Select download folder
   - Click "Download"

2. **Download Audio**:
   - Paste YouTube URL
   - Select "Audio Only" download type
   - Click "Get Available Formats"
   - Choose your preferred audio quality
   - Select download folder
   - Click "Download"

## 📊 Understanding the Interface
- **Progress Bar**: Shows download progress
- **Status Area**: Displays:
  - Download percentage
  - Current speed
  - Estimated time remaining (in HH:MM:SS format)
- **Donation Section**: Support future development
- **Disclaimer**: Important information about fair use

## 🛠 Requirements
- Python 3.6+
- Required packages (install via `pip install -r requirements.txt`):
  - yt-dlp
  - tkinter (usually comes with Python)
- FFmpeg (included in the repository)

## 🛠 Building the Executable (For Developers)
1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Run the build command:
   ```
   pyinstaller --onefile --add-data "ffmpeg;ffmpeg" --add-data "icon.ico;." --icon=icon.ico --noconsole oc_youtube_gui_downloader.py
   ```
3. The executable will be created in the `dist` folder

### Build Options
- `--onefile`: Creates a single executable file
- `--noconsole`: Hides the console window (recommended)
- `--icon=icon.ico`: Sets the application icon for the .exe file
- `--add-data "icon.ico;."`: Includes the icon file in the bundle
- `--add-data "ffmpeg;ffmpeg"`: Includes the FFmpeg binaries

## Troubleshooting

### Common Issues
- **FFmpeg not found**
  - Ensure the `ffmpeg` folder is in the same directory as the executable

- **Download failures**
  - Check your internet connection
  - Verify the video URL is correct and accessible
  - Some videos may have download restrictions

- **Permission errors**
  - Make sure you have write permissions in the download directory
  - Try running the application as administrator

- **Audio download issues**
  - FFmpeg is required for audio extraction
  - Ensure the FFmpeg binaries are properly included

## ⚖️ Legal Notice
This software is intended for personal and educational use only. Users are responsible for complying with YouTube's Terms of Service and all applicable laws regarding copyright and fair use.

### Important Notes:
- Do not download copyrighted content without permission
- Respect content creators' rights
- This tool is provided "as is" without warranty
- The developers are not responsible for misuse of this software

## 💖 Support
If you find this tool useful, please consider supporting future development through the donation link in the application. https://paypal.me/opeadewuyi

Thank you for using this tool!

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


