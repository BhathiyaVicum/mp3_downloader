import os
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import yt_dlp

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader & MP3 Converter")
        self.root.geometry("800x600")
        
        # Variables
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads" / "YouTube Downloads"))
        self.current_status = tk.StringVar(value="Ready to download...")
        self.is_downloading = False
        
        # Create download directory
        Path(self.download_path.get()).mkdir(parents=True, exist_ok=True)
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 YouTube Downloader & MP3 Converter", 
                               font=('Arial', 20, 'bold'))
        title_label.grid(row=0, column=0, pady=10)
        
        # URL Input Frame
        url_frame = ttk.LabelFrame(main_frame, text="YouTube URLs", padding="10")
        url_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        url_frame.columnconfigure(0, weight=1)
        
        # URL Text Area
        self.url_text = scrolledtext.ScrolledText(url_frame, height=5, width=70)
        self.url_text.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # URL Buttons
        button_frame = ttk.Frame(url_frame)
        button_frame.grid(row=1, column=0, columnspan=3, pady=5)
        
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_urls).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Paste from Clipboard", 
                  command=self.paste_urls).pack(side=tk.LEFT, padx=5)
        
        # Options Frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        options_frame.columnconfigure(1, weight=1)
        
        # Format Selection
        ttk.Label(options_frame, text="Output Format:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.format_var = tk.StringVar(value="mp3")
        format_combo = ttk.Combobox(options_frame, textvariable=self.format_var, 
                                   values=["mp3", "m4a", "wav", "flac"], state="readonly")
        format_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Quality Selection
        ttk.Label(options_frame, text="Audio Quality:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.quality_var = tk.StringVar(value="192")
        quality_combo = ttk.Combobox(options_frame, textvariable=self.quality_var, 
                                    values=["128", "192", "256", "320"], state="readonly")
        quality_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Download Location
        ttk.Label(options_frame, text="Save to:").grid(row=2, column=0, sticky=tk.W, pady=5)
        
        location_frame = ttk.Frame(options_frame)
        location_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        location_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(location_frame, textvariable=self.download_path).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(location_frame, text="Browse", command=self.browse_folder).grid(row=0, column=1)
        
        # Download Button
        self.download_btn = ttk.Button(main_frame, text="🚀 Start Download", 
                                       command=self.start_download)
        self.download_btn.grid(row=3, column=0, pady=10)
        
        # Progress Frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        # Status Label
        ttk.Label(progress_frame, textvariable=self.current_status).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Progress Bar
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(main_frame, text="Download Log", padding="10")
        log_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log Text
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def clear_urls(self):
        self.url_text.delete('1.0', tk.END)
        
    def paste_urls(self):
        try:
            clipboard_text = self.root.clipboard_get()
            self.url_text.insert(tk.END, clipboard_text)
        except:
            messagebox.showwarning("Clipboard Error", "Could not paste from clipboard")
            
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
            
    def log_message(self, message):
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def update_progress(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d and d['total_bytes']:
                progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
                self.progress_bar['value'] = progress
                self.current_status.set(f"Downloading: {progress:.1f}%")
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate']:
                progress = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                self.progress_bar['value'] = progress
                self.current_status.set(f"Downloading: {progress:.1f}%")
        elif d['status'] == 'finished':
            self.current_status.set("Processing audio...")
            self.progress_bar['value'] = 100
            
    def download_video(self, url):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.format_var.get(),
                    'preferredquality': self.quality_var.get(),
                }],
                'outtmpl': os.path.join(self.download_path.get(), '%(title)s.%(ext)s'),
                'progress_hooks': [self.update_progress],
                'quiet': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                self.log_message(f"✓ Downloaded: {info.get('title', 'Unknown')}")
                return True
                
        except Exception as e:
            self.log_message(f"✗ Error downloading {url}: {str(e)}")
            return False
            
    def start_download(self):
        if self.is_downloading:
            messagebox.showwarning("In Progress", "Download already in progress")
            return
            
        urls = self.url_text.get('1.0', tk.END).strip().split('\n')
        urls = [url.strip() for url in urls if url.strip()]
        
        if not urls:
            messagebox.showwarning("No URLs", "Please enter at least one YouTube URL")
            return
            
        valid_urls = []
        for url in urls:
            if 'youtube.com' in url or 'youtu.be' in url:
                valid_urls.append(url)
            else:
                self.log_message(f"⚠ Invalid YouTube URL skipped: {url}")
                
        if not valid_urls:
            messagebox.showerror("Invalid URLs", "No valid YouTube URLs found")
            return
            
        self.download_btn.config(state='disabled')
        self.is_downloading = True
        self.log_text.delete('1.0', tk.END)
        self.progress_bar['value'] = 0
        
        thread = threading.Thread(target=self.process_downloads, args=(valid_urls,))
        thread.daemon = True
        thread.start()
        
    def process_downloads(self, urls):
        total = len(urls)
        successful = 0
        
        self.log_message(f"Starting download of {total} video(s)...")
        
        for i, url in enumerate(urls):
            self.current_status.set(f"Processing video {i+1} of {total}...")
            if self.download_video(url):
                successful += 1
                
        self.root.after(0, self.download_complete, successful, total)
        
    def download_complete(self, successful, total):
        self.is_downloading = False
        self.download_btn.config(state='normal')
        self.current_status.set("Download complete!")
        
        message = f"Download complete!\nSuccessfully downloaded: {successful}/{total} files"
        messagebox.showinfo("Complete", message)
        
        # Open download folder
        os.startfile(self.download_path.get())

def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()