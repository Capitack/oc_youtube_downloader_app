import os
import subprocess
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont

# Ensure yt-dlp is installed
def ensure_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

ensure_package("yt_dlp")
from yt_dlp import YoutubeDL

def setup_ffmpeg():
    # Check for FFmpeg in the local folder
    ffmpeg_folders = [
        os.path.join(os.getcwd(), "ffmpeg-7.1.1-essentials_build", "bin"),
        os.path.join(os.getcwd(), "ffmpeg", "bin"),
    ]
    
    for ffmpeg_path in ffmpeg_folders:
        if os.path.exists(ffmpeg_path):
            ffmpeg_exe = os.path.join(ffmpeg_path, 'ffmpeg.exe')
            if os.path.exists(ffmpeg_exe):
                os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]
                print(f"Using FFmpeg from: {ffmpeg_path}")
                return True
    
    messagebox.showwarning(
        "FFmpeg Not Found",
        "FFmpeg is required for merging video and audio streams.\n\n"
        "Please download FFmpeg and place it in the application folder."
    )
    return False

# Initialize FFmpeg path
FFMPEG_AVAILABLE = setup_ffmpeg()

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OC's YouTube Video Downloader")
        self.root.geometry("700x550")
        self.root.minsize(600, 500)
        
        # Set application icon
        try:
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Could not load icon: {e}")
        
        # Thread control
        self.download_thread = None
        self.stop_download = False
        self.downloading = False

        self.url = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.selected_resolution = tk.StringVar()
        self.download_type = tk.StringVar(value="video")  # 'video' or 'audio'
        self.available_resolutions = {}

        self.create_widgets()

    def create_widgets(self):
        # URL input
        url_frame = tk.Frame(self.root)
        url_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(url_frame, text="YouTube URL:").pack(side=tk.LEFT)
        tk.Entry(url_frame, textvariable=self.url, width=60).pack(side=tk.LEFT, padx=5)
        
        # Download type selection
        type_frame = tk.Frame(self.root)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(type_frame, text="Download Type:").pack(side=tk.LEFT)
        tk.Radiobutton(type_frame, text="Video", variable=self.download_type, value="video", 
                      command=self.on_download_type_change).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(type_frame, text="Audio Only", variable=self.download_type, value="audio",
                      command=self.on_download_type_change).pack(side=tk.LEFT)
        
        # Resolution selection
        res_frame = tk.Frame(self.root)
        res_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(res_frame, text="Get Available Formats", command=self.fetch_formats).pack(side=tk.LEFT)
        self.res_dropdown = ttk.Combobox(res_frame, textvariable=self.selected_resolution, width=30, state='readonly')
        self.res_dropdown.pack(side=tk.LEFT, padx=10)
        
        # Output folder
        folder_frame = tk.Frame(self.root)
        folder_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Button(folder_frame, text="Select Download Folder", command=self.browse_folder).pack(side=tk.LEFT)
        tk.Label(folder_frame, textvariable=self.output_dir, wraplength=400, justify=tk.LEFT).pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Progress bar and download/cancel buttons
        self.progress_label = tk.Label(self.root, text="", wraplength=650, justify="left")
        self.progress_label.pack(pady=5)

        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=500, mode="determinate")
        self.progress_bar.pack(pady=5)
        
        # Button frame
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        self.download_btn = tk.Button(btn_frame, text="Download", 
                                    command=self.start_download_thread,
                                    width=15)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        self.cancel_btn = tk.Button(btn_frame, text="Cancel", 
                                  command=self.cancel_download,
                                  state=tk.DISABLED,
                                  width=15)
        self.cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Footer frame with improved styling
        footer_frame = tk.Frame(self.root, bd=1, relief=tk.SUNKEN)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10, padx=10)
        
        # Create a custom font for the footer
        bold_font = tkfont.Font(weight='bold')
        link_font = tkfont.Font(underline=True, size=10)
        
        # Donation section with improved visibility
        donation_frame = tk.Frame(footer_frame, bg='#f0f8ff', bd=1, relief=tk.RAISED, padx=10, pady=10)
        donation_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Donation text with improved styling
        tk.Label(donation_frame, 
                text="❤️ Donate if you find this tool useful ❤️", 
                font=bold_font, 
                bg='#f0f8ff').pack(pady=(0, 5))
        
        # PayPal link with improved styling
        paypal_frame = tk.Frame(donation_frame, bg='#f0f8ff')
        paypal_frame.pack()
        
        paypal_url = "https://paypal.me/opeadewuyi"
        paypal_link = tk.Label(paypal_frame, 
                             text=paypal_url, 
                             fg="blue", 
                             cursor="hand2",
                             font=link_font,
                             bg='#f0f8ff')
        paypal_link.pack(side=tk.LEFT)
        paypal_link.bind("<Button-1>", lambda e: self.open_url(paypal_url))
        
        # Copy button
        copy_btn = tk.Button(paypal_frame, 
                           text="📋", 
                           command=lambda: self.copy_to_clipboard(paypal_url),
                           bd=1,
                           relief=tk.RAISED)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Disclaimer text
        disclaimer_frame = tk.Frame(footer_frame)
        disclaimer_frame.pack(fill=tk.X, pady=(10, 0))
        
        disclaimer_text = """Please respect YouTube's Terms of Service. By using this tool, you agree that this is for educational or personal channel use only.

Made with ❤️ by OC"""
        
        tk.Label(disclaimer_frame, 
                text=disclaimer_text, 
                justify=tk.CENTER, 
                wraplength=650,
                fg='#666666',
                font=('Arial', 8)).pack()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_dir.set(folder)

    def on_download_type_change(self):
        """Handle download type change (video/audio)"""
        if hasattr(self, 'res_dropdown'):
            self.selected_resolution.set('')
            self.res_dropdown['values'] = []
            self.fetch_formats()

    def fetch_formats(self):
        try:
            url = self.url.get().strip()
            if not url:
                raise ValueError("Please enter a valid URL")

            ydl_opts = {"quiet": True, "skip_download": True}
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get("formats", [])

            if self.download_type.get() == "video":
                # For video: get video formats
                formats = [f for f in formats if f.get('vcodec') != 'none']
                # Sort by resolution (height) desc, then by bitrate desc
                formats.sort(key=lambda x: (x.get('height', 0), x.get('tbr', 0)), reverse=True)
                
                self.available_resolutions.clear()
                display_list = []
                seen_heights = set()

                for f in formats:
                    height = f.get('height')
                    if height and height not in seen_heights:
                        res_str = f"{height}p"
                        self.available_resolutions[res_str] = f['format_id']
                        display_list.append(res_str)
                        seen_heights.add(height)
            else:
                # For audio: get audio formats
                audio_formats = []
                for f in formats:
                    if f.get('acodec') != 'none':
                        # Get format info
                        ext = f.get('ext', 'mp3')
                        abr = f.get('abr', 0)
                        if abr:
                            audio_formats.append((f, f"{ext.upper()} ({int(abr)}kbps)"))
                
                # Sort by bitrate (highest first)
                audio_formats.sort(key=lambda x: x[0].get('abr', 0), reverse=True)
                
                self.available_resolutions.clear()
                display_list = []
                
                for f, display in audio_formats:
                    format_id = f['format_id']
                    self.available_resolutions[display] = format_id
                    display_list.append(display)

            if display_list:
                self.res_dropdown["values"] = display_list
                self.res_dropdown.current(0)
            else:
                messagebox.showinfo("No Formats", "No video formats found.")

        except Exception as e:
            error_msg = str(e)
            self.show_error("Error", error_msg)

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
        
    def copy_to_clipboard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.root.update()
        self.progress_label.config(text="URL copied to clipboard!")
        
    def show_error(self, title, message):
        # Create a top-level window for the error message
        error_win = tk.Toplevel(self.root)
        error_win.title(title)
        
        # Add error message with scrollbar
        frame = tk.Frame(error_win)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        error_text = tk.Text(frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, 
                           height=10, width=60)
        error_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        error_text.insert(tk.END, message)
        error_text.config(state=tk.DISABLED)
        
        scrollbar.config(command=error_text.yview)
        
        # Add copy button
        btn_frame = tk.Frame(error_win)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(btn_frame, text="Copy Error", 
                 command=lambda: self.copy_to_clipboard(message)).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Close", 
                 command=error_win.destroy).pack(side=tk.RIGHT)
    
    def toggle_ui_state(self, state):
        """Enable/disable UI elements during download"""
        widgets = [self.url, self.output_dir, self.res_dropdown, self.download_btn]
        for widget in widgets:
            if hasattr(widget, 'config'):
                widget.config(state=tk.NORMAL if state else tk.DISABLED)
        self.cancel_btn.config(state=tk.NORMAL if not state else tk.DISABLED)
        self.downloading = not state
        self.root.update()
    
    def start_download_thread(self):
        """Start the download in a separate thread"""
        if self.downloading:
            return
            
        self.stop_download = False
        self.download_thread = threading.Thread(target=self.download_video)
        self.download_thread.daemon = True
        self.toggle_ui_state(False)
        self.download_thread.start()
        self.check_thread()
    
    def check_thread(self):
        """Check if the download thread is still running"""
        if self.download_thread and self.download_thread.is_alive():
            self.root.after(100, self.check_thread)
        else:
            self.toggle_ui_state(True)
    
    def cancel_download(self):
        """Cancel the current download"""
        if not self.downloading:
            return
            
        self.stop_download = True
        self.progress_label.config(text="Cancelling download...")
        self.root.update()
    
    def format_eta(self, seconds):
        """Convert seconds to HH:MM:SS format"""
        if not isinstance(seconds, (int, float)) or seconds < 0:
            return "--:--:--"
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0.0%').strip()
            eta = d.get('eta', 0)
            speed = d.get('speed', 0)
            try:
                percent = float(percent_str.strip('%'))
            except ValueError:
                percent = 0.0
                
            # Format speed
            if speed:
                if speed > 1000000:  # MB/s
                    speed_str = f"{speed/1000000:.1f} MB/s"
                else:  # KB/s
                    speed_str = f"{speed/1000:.1f} KB/s"
            else:
                speed_str = "-- KB/s"
                
            self.progress_bar['value'] = percent
            self.progress_label.config(
                text=f"Progress: {percent_str} | "
                     f"Speed: {speed_str} | "
                     f"ETA: {self.format_eta(eta)}"
            )
            self.root.update_idletasks()
        elif d['status'] == 'finished':
            self.progress_label.config(text="Download finished. Processing...")

    def download_video(self):
        try:
            url = self.url.get().strip()
            folder = self.output_dir.get().strip()
            resolution = self.selected_resolution.get()

            if not url or not folder or not resolution:
                raise ValueError("Missing URL, folder, or resolution selection")

            format_id = self.available_resolutions[resolution]
            output_template = os.path.join(folder, f"{int(time.time())} - %(title)s.%(ext)s")
            is_audio = self.download_type.get() == "audio"

            if is_audio:
                # Audio download options
                ydl_opts = {
                    "format": format_id,
                    "outtmpl": output_template.replace('.%(ext)s', '.%(ext)s'),
                    "progress_hooks": [self.progress_hook],
                    "postprocessors": [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'ffmpeg_location': None,
                }
                self.progress_label.config(text="Starting audio download...")
            else:
                # Video download options
                if not FFMPEG_AVAILABLE:
                    messagebox.showerror("Error", "FFmpeg is required but not found. Cannot merge video and audio.")
                    return

                ydl_opts = {
                    "format": f"{format_id}+bestaudio",
                    "outtmpl": output_template,
                    "merge_output_format": "mp4",
                    "progress_hooks": [self.progress_hook],
                    "postprocessors": [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                    'ffmpeg_location': None,
                }
                self.progress_label.config(text="Starting video download with FFmpeg...")
            
            self.progress_label.config(text="Starting download with FFmpeg...")
            self.root.update_idletasks()

            with YoutubeDL(ydl_opts) as ydl:
                if self.stop_download:
                    self.progress_label.config(text="Download cancelled!")
                    return
                ydl.download([url])
                
                if self.stop_download:
                    self.progress_label.config(text="Download cancelled!")
                    return

            self.progress_label.config(text="✅ Download and merge completed!")
            if not self.stop_download:
                messagebox.showinfo("Success", "Download complete!")

        except Exception as e:
            if not self.stop_download:  # Only show error if not cancelled
                error_msg = str(e)
                self.show_error("Error", error_msg)
        finally:
            # Ensure UI is re-enabled even if an error occurs
            self.root.after(0, lambda: self.toggle_ui_state(True))

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
