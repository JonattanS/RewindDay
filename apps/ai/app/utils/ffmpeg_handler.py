import subprocess
import logging
from pathlib import Path
from typing import List

logger = logging.getLogger(__name__)

class FFmpegHandler:
    """Maneja todas las operaciones de FFmpeg"""
    
    @staticmethod
    def check_ffmpeg_installed() -> bool:
        """Verifica si FFmpeg está instalado"""
        try:
            subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def get_video_duration(video_file: str) -> float:
        """Obtiene duración de video en segundos"""
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1:nokey=1",
                video_file
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return float(result.stdout.strip())
        except Exception as e:
            logger.error(f"Error getting duration: {e}")
            return 0
    
    @staticmethod
    def concat_videos(video_list: List[str], output_file: str):
        """Concatena múltiples videos"""
        concat_file = Path("concat_list.txt")
        
        with open(concat_file, 'w') as f:
            for video in video_list:
                f.write(f"file '{Path(video).absolute()}'\n")
        
        cmd = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            output_file,
            "-y"
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        concat_file.unlink()
    
    @staticmethod
    def add_audio_to_video(video_file: str, audio_file: str, output_file: str):
        """Añade audio a video"""
        cmd = [
            "ffmpeg",
            "-i", video_file,
            "-i", audio_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            output_file,
            "-y"
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
    
    @staticmethod
    def compress_video(input_file: str, output_file: str, crf: int = 23):
        """Comprime video para reducir tamaño"""
        cmd = [
            "ffmpeg",
            "-i", input_file,
            "-c:v", "libx264",
            "-crf", str(crf),
            "-preset", "medium",
            "-c:a", "aac",
            "-b:a", "128k",
            output_file,
            "-y"
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)