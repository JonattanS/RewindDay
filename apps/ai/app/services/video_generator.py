import json
import asyncio
import requests
import subprocess
from pathlib import Path
import base64
from typing import List, Dict, Optional
from PIL import Image
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

class VideoGenerator:
    def __init__(self, videos_dir: str = "videos"):
        self.videos_dir = Path(videos_dir)
        self.videos_dir.mkdir(exist_ok=True)
        
        # URLs de servicios locales
        self.ollama_url = "http://localhost:11434/api/generate"
        self.sd_url = "http://localhost:7860/api/txt2img"
    
    # ========================
    # PASO 1: GENERAR GUION
    # ========================
    
    def generate_script_with_ollama(self, context: str) -> Dict:
        """
        Genera guion usando LLaMA 2 localmente
        Retorna JSON con 5 escenas
        """
        try:
            logger.info("🎯 Generando guion con LLaMA 2...")
            
            prompt = f"""
Eres un experto en cinematografía. Genera un guion para un video de un evento importante.

EVENTO: {context}

Retorna SOLO JSON sin markdown, con exactamente 5 escenas:
{{
    "title": "Título descriptivo del video",
    "scenes": [
        {{
            "number": 1,
            "title": "Escena 1",
            "description": "Una descripción visual corta (20-30 palabras) para generar imagen",
            "narration": "La narración en español para esta escena (50-80 palabras)",
            "duration": 8,
            "mood": "happy"
        }},
        {{
            "number": 2,
            "title": "Escena 2",
            "description": "...",
            "narration": "...",
            "duration": 8,
            "mood": "happy"
        }},
        {{
            "number": 3,
            "title": "Escena 3",
            "description": "...",
            "narration": "...",
            "duration": 8,
            "mood": "happy"
        }},
        {{
            "number": 4,
            "title": "Escena 4",
            "description": "...",
            "narration": "...",
            "duration": 8,
            "mood": "happy"
        }},
        {{
            "number": 5,
            "title": "Escena 5",
            "description": "...",
            "narration": "...",
            "duration": 8,
            "mood": "happy"
        }}
    ]
}}
"""
            
            response = requests.post(
                self.ollama_url,
                json={
                    'model': 'mistral',
                    'prompt': prompt,
                    'stream': False,
                    'temperature': 0.7
                },
                timeout=300
            )
            
            result = response.json()
            text = result['response']
            
            # Extraer JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                script = json.loads(json_match.group())
                logger.info(f"✅ Guion generado: {len(script.get('scenes', []))} escenas")
                return script
            else:
                logger.error("No se encontró JSON en la respuesta")
                raise ValueError("No valid JSON in response")
                
        except Exception as e:
            logger.error(f"Error generando guion: {e}")
            raise
    
    # ========================
    # PASO 2: GENERAR IMÁGENES
    # ========================
    
    def generate_images_stable_diffusion(self, description: str, scene_num: int = 1) -> str:
        """
        Genera una imagen usando Stable Diffusion
        Retorna ruta de la imagen guardada
        """
        try:
            logger.info(f"🎨 Generando imagen para escena {scene_num}...")
            
            payload = {
                "prompt": f"{description}, professional, cinematic, 4K, high quality, sharp focus",
                "negative_prompt": "blurry, low quality, distorted, ugly, bad, deformed",
                "steps": 20,
                "sampler_name": "DPM++ 2M",
                "width": 1920,
                "height": 1080,
                "cfg_scale": 7.5,
                "seed": -1,
                "batch_size": 1,
                "n_iter": 1
            }
            
            response = requests.post(self.sd_url, json=payload, timeout=600)
            result = response.json()
            
            if 'images' not in result or not result['images']:
                raise ValueError("No images in response")
            
            # Guardar imagen
            img_base64 = result['images'][0]
            img_data = base64.b64decode(img_base64)
            img = Image.open(BytesIO(img_data))
            
            image_path = self.videos_dir / f"scene_{scene_num}.png"
            img.save(image_path)
            
            logger.info(f"✅ Imagen guardada: {image_path}")
            return str(image_path)
            
        except Exception as e:
            logger.error(f"Error generando imagen: {e}")
            raise
    
    # ========================
    # PASO 3: GENERAR NARRACIÓN
    # ========================
    
    def generate_narration_piper(self, text: str, scene_num: int = 1) -> str:
        """
        Genera narración usando Piper TTS
        Retorna ruta del archivo de audio
        """
        try:
            logger.info(f"🎤 Generando narración escena {scene_num}...")
            
            output_file = self.videos_dir / f"narration_{scene_num}.wav"
            
            # Comando piper
            cmd = [
                "piper",
                "--model", "es_MX-female-medium",
                "--output-file", str(output_file),
                "--length-scale", "1.0"
            ]
            
            process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=text)
            
            if process.returncode != 0:
                raise RuntimeError(f"Piper error: {stderr}")
            
            logger.info(f"✅ Narración guardada: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error generando narración: {e}")
            raise
    
    # ========================
    # PASO 4: GENERAR MÚSICA
    # ========================
    
    def generate_music_musicgen(self, mood: str, duration: int = 60) -> str:
        """
        Genera música usando MusicGen
        Retorna ruta del archivo de audio
        """
        try:
            logger.info(f"🎵 Generando música ({mood}, {duration}s)...")
            
            from audiocraft.models import MusicGen
            import torchaudio
            
            # Mapear mood a descripción
            mood_map = {
                "happy": "uplifting, joyful, energetic orchestral music",
                "sad": "melancholic, emotional, soft piano music",
                "epic": "epic, heroic, cinematic orchestral film score",
                "calm": "peaceful, relaxing, ambient calm music",
                "romantic": "romantic, tender, emotional violin music",
                "excited": "excited, energetic, dynamic orchestral music"
            }
            
            description = mood_map.get(mood, "cinematic orchestral music")
            
            # Generar
            model = MusicGen.get_model('medium')
            model.set_generation_params(
                duration=duration,
                use_sampling=True,
                top_k=250,
                temperature=1.0
            )
            
            wav = model.generate([description], progress=False)
            
            # Guardar
            output_file = self.videos_dir / "background_music.wav"
            torchaudio.save(str(output_file), wav[0].cpu(), sample_rate=16000)
            
            logger.info(f"✅ Música guardada: {output_file}")
            return str(output_file)
            
        except Exception as e:
            logger.error(f"Error generando música: {e}")
            raise
    
    # ========================
    # PASO 5: COMPILAR VIDEO
    # ========================
    
    def compile_video_ffmpeg(self, image_paths: List[str], narration_paths: List[str],
                            music_file: str, scenes: List[Dict], 
                            output_file: str) -> str:
        """
        Compila todo en video final usando FFmpeg
        """
        try:
            logger.info("🎬 Compilando video con FFmpeg...")
            
            import os
            
            # Crear archivo concat para FFmpeg
            concat_file = self.videos_dir / "concat_list.txt"
            with open(concat_file, 'w') as f:
                for image, scene in zip(image_paths, scenes):
                    duration = scene['duration']
                    f.write(f"file '{os.path.abspath(image)}'\n")
                    f.write(f"duration {duration}\n")
            
            # Concatenar narración
            narration_concat = self.videos_dir / "narration_concat.wav"
            self._concat_audio_files(narration_paths, str(narration_concat))
            
            # Comando FFmpeg
            cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-i", str(narration_concat),
                "-i", str(music_file),
                "-filter_complex",
                "[1]volume=1.0[a1];[2]volume=0.25[a2];[a1][a2]amix=inputs=2[a]",
                "-map", "[a]",
                "-c:v", "libx264",
                "-crf", "23",
                "-preset", "medium",
                "-c:a", "aac",
                "-b:a", "128k",
                str(output_file),
                "-y"
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            logger.info(f"✅ Video compilado: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error compilando video: {e}")
            raise
    
    def _concat_audio_files(self, audio_files: List[str], output_file: str):
        """
        Concatena múltiples archivos de audio
        """
        from pydub import AudioSegment
        
        combined = AudioSegment.empty()
        
        for audio_file in audio_files:
            sound = AudioSegment.from_wav(audio_file)
            combined += sound
        
        combined.export(output_file, format="wav")
    
    # ========================
    # PIPELINE COMPLETO
    # ========================
    
    async def generate_full_video(self, video_id: str, context: str, 
                                  title: str = "Video") -> Dict:
        """
        Genera video completo en 5 pasos
        Retorna diccionario con rutas y metadata
        """
        try:
            logger.info(f"🎬 Iniciando generación de video {video_id}...")
            
            output_file = self.videos_dir / f"{video_id}.mp4"
            
            # PASO 1: Guion
            script = self.generate_script_with_ollama(context)
            
            # PASO 2: Imágenes
            image_paths = []
            for i, scene in enumerate(script['scenes'], 1):
                image = self.generate_images_stable_diffusion(
                    scene['description'],
                    scene_num=i
                )
                image_paths.append(image)
            
            # PASO 3: Narración
            narration_paths = []
            for i, scene in enumerate(script['scenes'], 1):
                narration = self.generate_narration_piper(
                    scene['narration'],
                    scene_num=i
                )
                narration_paths.append(narration)
            
            # PASO 4: Música
            total_duration = sum(s['duration'] for s in script['scenes'])
            moods = [s.get('mood', 'epic') for s in script['scenes']]
            main_mood = max(set(moods), key=moods.count)  # Mood más común
            
            music = self.generate_music_musicgen(main_mood, total_duration)
            
            # PASO 5: Compilar
            video = self.compile_video_ffmpeg(
                image_paths=image_paths,
                narration_paths=narration_paths,
                music_file=music,
                scenes=script['scenes'],
                output_file=str(output_file)
            )
            
            logger.info(f"✅ Video generado exitosamente: {video}")
            
            return {
                "id": video_id,
                "title": title,
                "video_url": str(video),
                "status": "completed",
                "script": script,
                "image_count": len(image_paths),
                "duration_seconds": total_duration
            }
            
        except Exception as e:
            logger.error(f"❌ Error en generación: {e}")
            return {
                "id": video_id,
                "status": "failed",
                "error": str(e)
            }
