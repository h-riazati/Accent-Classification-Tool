import os
import tempfile
import subprocess
# import imageio_ffmpeg as ffmpeg
# Ensure MoviePy and ImageIO use the bundled ffmpeg binary
# os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg.get_ffmpeg_exe()
# os.environ["FFMPEG_BINARY"] = ffmpeg.get_ffmpeg_exe()
# Ensure PATH includes vendored ffmpeg
ffmpeg_dir = os.path.join(os.getcwd(), "ffmpeg")
os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
ffmpeg_path = os.path.join(ffmpeg_dir, "ffmpeg")

# DEBUG: confirm it’s where we expect
print(">> Using ffmpeg at:", ffmpeg_path, "exists?", os.path.exists(ffmpeg_path))
# from moviepy.config import change_settings
# change_settings({"FFMPEG_BINARY": ffmpeg_path})

from yt_dlp import YoutubeDL
# from moviepy.editor import VideoFileClip
from moviepy import VideoFileClip
import time
import requests
from urllib.parse import urlparse


def download_video(url: str, dest_folder: str) -> str:
    """
    Download a video from a given URL. Supports direct-file links (e.g. Loom, S3) and hosted platforms (YouTube, Aparat, Vimeo) via yt-dlp.

    Args:
        url (str): Public video URL.
        dest_folder (str): Local directory to save the downloaded video.

    Returns:
        str: Path to the saved video file.
    """
    os.makedirs(dest_folder, exist_ok=True)
    parsed = urlparse(url)
    hostname = parsed.netloc.lower()

    # Define platforms requiring yt-dlp
    extractor_domains = ('youtube.com', 'vimeo.com', 'aparat.com')

    if any(domain in hostname for domain in extractor_domains):
        # Use yt-dlp for hosted platforms
        return download_video_via_ytdlp(url, dest_folder)

    # Otherwise assume direct-file link: infer filename
    filename = os.path.basename(parsed.path) or 'video'
    if not any(filename.lower().endswith(ext) for ext in ('.mp4', '.mov', '.webm', '.mkv')):
        filename += '.mp4'
    dest_path = os.path.join(dest_folder, filename)

    # Try streaming download
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    content_type = resp.headers.get('Content-Type', '')
    # Fallback to yt-dlp if not a video
    if not content_type.startswith('video/'):
        return download_video_via_ytdlp(url, dest_folder)

    with open(dest_path, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return dest_path


def download_video_via_ytdlp(url: str, dest_folder: str) -> str:
    """
    Internal helper: download using yt-dlp for any URL fallback.
    """

    ydl_opts = {
        'outtmpl': os.path.join(dest_folder, '%(id)s.%(ext)s'),
        'format': 'mp4/best',
        'quiet': True,
        'no_warnings': True,
        'cookiefile': r'C:\Users\admin\Downloads\youtube_cookies.txt',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def extract_audio(video_path: str, wav_path: str, sample_rate: int = 16000):
    try:
        # clip = VideoFileClip(video_path)
        # clip.audio.write_audiofile(wav_path, fps=sample_rate)#, verbose=False, logger=None)
        # clip.close()
        cmd = [ffmpeg_path,
               '-y',  # overwrite
               '-i', video_path,
               '-vn',  # no video
               '-acodec', 'pcm_s16le',  # WAV format
               '-ar', str(sample_rate),
               '-ac', '1',  # mono
               wav_path]
        subprocess.run(cmd, check=True)
    except Exception as e:
        print(f'\n\nFailed to extract audio: {e}\n\n')