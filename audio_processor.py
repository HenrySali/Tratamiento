#!/usr/bin/env python3
"""
Audio Treatment Pipeline - Procesador avanzado de audio
Gestiona, limpia, amplifica, valida y transcribe audios

Pipeline DSP + Deep Learning:
1. Carga de audio en 16kHz (ideal para Whisper)
2. Reducción de ruido neuronal (noisereduce)
3. Normalización y ganancia dinámica
4. Ecualización espectral (filtros paso-alto)
5. Transcripción con OpenAI Whisper
6. (Opcional) Separación de fuentes con Demucs
"""

import os
import librosa
import noisereduce as nr
import numpy as np
import soundfile as sf
import whisper
from pathlib import Path
import json
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AudioProcessor:
    """Procesador avanzado de audio con técnicas DSP y deep learning"""
    
    def __init__(self, sr=16000, language="es"):
        """
        Inicializar el procesador
        
        Args:
            sr: Sample rate objetivo (16000 Hz por defecto - óptimo para Whisper)
            language: Idioma para transcripción (es, en, fr, etc.)
        """
        self.sr = sr
        self.language = language
        self.output_dir = Path("processed_audio")
        self.output_dir.mkdir(exist_ok=True)
        self.metadata = {}
        
        # Cargar modelo Whisper (puede ser 'tiny', 'base', 'small', 'medium', 'large')
        logger.info("Cargando modelo Whisper...")
        self.model = whisper.load_model("base", device="cpu")
    
    def validate_audio(self, audio_path):
        """Validar que el archivo de audio existe y es accesible"""
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {audio_path}")
        
        if not path.suffix.lower() in ['.wav', '.mp3', '.ogg', '.flac', '.m4a']:
            raise ValueError(f"Formato no soportado: {path.suffix}")
        
        logger.info(f"✓ Audio validado: {path.name}")
        return path
    
    def load_audio(self, audio_path):
        """
        Cargar audio del archivo
        
        Args:
            audio_path: Ruta del archivo de audio
            
        Returns:
            y: Array de audio cargado
            sr: Sample rate
        """
        logger.info(f"Cargando audio: {audio_path}")
        y, sr = librosa.load(audio_path, sr=self.sr)
        logger.info(f"  - Sample rate: {sr} Hz")
        logger.info(f"  - Duración: {len(y)/sr:.2f} segundos")
        logger.info(f"  - Amplitud máxima: {np.max(np.abs(y)):.4f}")
        return y, sr
    
    def reduce_noise(self, y, sr, prop_decrease=0.85):
        """
        Reducción de ruido espectral neuronal
        
        Args:
            y: Array de audio
            sr: Sample rate
            prop_decrease: Porcentaje de reducción (0-1, recomendado 0.85)
            
        Returns:
            Audio con ruido reducido
        """
        logger.info(f"Aplicando reducción de ruido (prop_decrease={prop_decrease})...")
        try:
            reduced_noise = nr.reduce_noise(y=y, sr=sr, prop_decrease=prop_decrease)
            logger.info(f"  ✓ Ruido reducido exitosamente")
            return reduced_noise
        except Exception as e:
            logger.warning(f"  ! Error en reducción de ruido: {e}")
            return y
    
    def normalize_audio(self, y, target_db=-20.0):
        """
        Normalización y ecualización dinámica
        
        Args:
            y: Array de audio
            target_db: Nivel objetivo en dB (por defecto -20 dB)
            
        Returns:
            Audio normalizado
        """
        logger.info(f"Normalizando audio (target: {target_db} dB)...")
        
        # Calcular RMS (Root Mean Square) actual
        rms_current = np.sqrt(np.mean(y**2))
        
        if rms_current > 0:
            # Convertir a dB
            current_db = 20 * np.log10(rms_current)
            
            # Calcular ganancia necesaria
            gain_db = target_db - current_db
            gain_linear = 10 ** (gain_db / 20)
            
            # Aplicar ganancia
            normalized = y * gain_linear
            
            # Limitar para evitar saturación
            max_val = np.max(np.abs(normalized))
            if max_val > 0.95:
                normalized = normalized / max_val * 0.95
            
            logger.info(f"  - DB actual: {current_db:.2f} dB")
            logger.info(f"  - Ganancia aplicada: {gain_db:.2f} dB")
            logger.info(f"  ✓ Audio normalizado")
            return normalized
        else:
            logger.warning("  ! Audio silencioso, no se puede normalizar")
            return y
    
    def apply_highpass_filter(self, y, sr, cutoff_freq=100):
        """
        Aplicar filtro paso-alto para eliminar ruido de baja frecuencia
        
        Args:
            y: Array de audio
            sr: Sample rate
            cutoff_freq: Frecuencia de corte en Hz (100-150 Hz recomendado)
            
        Returns:
            Audio filtrado
        """
        logger.info(f"Aplicando filtro paso-alto (cutoff: {cutoff_freq} Hz)...")
        
        from scipy.signal import butter, sosfilt
        
        # Diseñar filtro Butterworth paso-alto
        sos = butter(6, cutoff_freq, btype='high', fs=sr, output='sos')
        filtered = sosfilt(sos, y)
        
        logger.info(f"  ✓ Filtro paso-alto aplicado")
        return filtered
    
    def enhance_presence(self, y, sr):
        """
        Realzar banda de presencia (2-4 kHz) para mejorar claridad de consonantes fricativas
        
        Args:
            y: Array de audio
            sr: Sample rate
            
        Returns:
            Audio con presencia mejorada
        """
        logger.info("Realzando banda de presencia (2-4 kHz)...")
        
        # Usar STFT para procesamiento en el dominio de la frecuencia
        D = librosa.stft(y)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=D.shape[0]*2-2)
        
        # Crear máscara de ganancia para la banda de presencia
        mask = np.ones(D.shape[0])
        presence_band = (freqs >= 2000) & (freqs <= 4000)
        mask[presence_band] = 1.3  # Aumentar 30% en esta banda
        
        # Aplicar ganancia
        D_enhanced = D * mask[:, np.newaxis]
        
        # Convertir de vuelta
        enhanced = librosa.istft(D_enhanced)
        
        logger.info(f"  ✓ Presencia mejorada")
        return enhanced
    
    def process_pipeline(self, audio_path, apply_presence_boost=True, 
                        apply_separation=False, verbose=True):
        """
        Pipeline completo de procesamiento de audio
        
        Args:
            audio_path: Ruta del archivo de audio
            apply_presence_boost: Aplicar realce de presencia
            apply_separation: Usar Demucs para separación de fuentes
            verbose: Mostrar información detallada
            
        Returns:
            Dict con metadata del procesamiento
        """
        logger.info("="*60)
        logger.info("INICIANDO PIPELINE DE PROCESAMIENTO DE AUDIO")
        logger.info("="*60)
        
        try:
            # Validar entrada
            audio_path = self.validate_audio(audio_path)
            
            # Cargar audio
            y, sr = self.load_audio(audio_path)
            filename = audio_path.stem
            
            # Reducción de ruido
            y = self.reduce_noise(y, sr, prop_decrease=0.85)
            
            # Filtro paso-alto
            y = self.apply_highpass_filter(y, sr, cutoff_freq=100)
            
            # Normalización
            y = self.normalize_audio(y, target_db=-20.0)
            
            # Realce de presencia (opcional)
            if apply_presence_boost:
                y = self.enhance_presence(y, sr)
            
            # Guardar audio limpio
            clean_path = self.output_dir / f"{filename}_clean.wav"
            sf.write(clean_path, y, sr)
            logger.info(f"✓ Audio limpio guardado: {clean_path}")
            
            # Transcripción con Whisper
            logger.info("Transcribiendo con OpenAI Whisper...")
            result = self.model.transcribe(
                str(clean_path),
                language=self.language,
                fp16=False,
                verbose=False
            )
            
            transcription = result["text"]
            logger.info("="*60)
            logger.info("TRANSCRIPCIÓN OBTENIDA:")
            logger.info("="*60)
            logger.info(transcription)
            logger.info("="*60)
            
            # Guardar transcripción
            transcript_path = self.output_dir / f"{filename}_transcription.txt"
            with open(transcript_path, 'w', encoding='utf-8') as f:
                f.write(transcription)
            logger.info(f"✓ Transcripción guardada: {transcript_path}")
            
            # Guardar metadata
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "original_file": str(audio_path),
                "sample_rate": sr,
                "duration_seconds": len(y) / sr,
                "clean_audio_path": str(clean_path),
                "transcription": transcription,
                "transcription_file": str(transcript_path),
                "processing_steps": [
                    "noise_reduction",
                    "highpass_filter",
                    "normalization",
                    "presence_boost" if apply_presence_boost else None,
                    "whisper_transcription"
                ]
            }
            
            metadata_path = self.output_dir / f"{filename}_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            logger.info(f"✓ Metadata guardado: {metadata_path}")
            
            return metadata
            
        except Exception as e:
            logger.error(f"✗ Error en procesamiento: {e}")
            raise
    
    def batch_process(self, audio_dir):
        """
        Procesar múltiples archivos de audio en un directorio
        
        Args:
            audio_dir: Directorio con archivos de audio
            
        Returns:
            Lista de resultados
        """
        audio_dir = Path(audio_dir)
        audio_extensions = ['.wav', '.mp3', '.ogg', '.flac', '.m4a']
        audio_files = [f for f in audio_dir.glob('*') 
                      if f.suffix.lower() in audio_extensions]
        
        if not audio_files:
            logger.warning(f"No se encontraron archivos de audio en {audio_dir}")
            return []
        
        logger.info(f"Encontrados {len(audio_files)} archivos de audio")
        results = []
        
        for i, audio_file in enumerate(audio_files, 1):
            logger.info(f"\n[{i}/{len(audio_files)}] Procesando: {audio_file.name}")
            try:
                metadata = self.process_pipeline(str(audio_file))
                results.append(metadata)
            except Exception as e:
                logger.error(f"Error procesando {audio_file.name}: {e}")
        
        return results


def main():
    """Función principal para uso desde línea de comandos"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python audio_processor.py <archivo_audio>")
        print("  python audio_processor.py --batch <directorio>")
        print("\nEjemplo:")
        print("  python audio_processor.py audio_susurrado.wav")
        print("  python audio_processor.py --batch ./audios/")
        sys.exit(1)
    
    processor = AudioProcessor(sr=16000, language="es")
    
    if sys.argv[1] == "--batch" and len(sys.argv) >= 3:
        # Procesamiento en lote
        results = processor.batch_process(sys.argv[2])
        logger.info(f"\n✓ Procesamiento en lote completado: {len(results)} archivos")
    else:
        # Procesamiento individual
        audio_file = sys.argv[1]
        processor.process_pipeline(audio_file)


if __name__ == "__main__":
    main()
