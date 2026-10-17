#!/usr/bin/env python3
"""
Procesador Avanzado con Demucs - Separación neuronal de fuentes de audio
Separa voz de música, ruido ambiental y otros componentes usando Demucs (Meta AI)
"""

import os
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
import json
import subprocess
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DemucsAudioProcessor:
    """Procesador de audio con separación neuronal de fuentes usando Demucs"""
    
    def __init__(self, sr=16000, model="htdemucs"):
        """
        Inicializar procesador
        
        Args:
            sr: Sample rate (16000 Hz recomendado)
            model: Modelo Demucs a usar
                - 'htdemucs': High-Quality Demucs (recomendado)
                - 'mdx_extra': Meta Demucs Extra (más preciso)
        """
        self.sr = sr
        self.model = model
        self.output_dir = Path("demucs_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def separate_sources_demucs(self, audio_path):
        """
        Usar Demucs CLI para separar fuentes de audio
        
        Args:
            audio_path: Ruta del archivo de audio
            
        Returns:
            Dict con rutas de componentes separados
        """
        logger.info("="*60)
        logger.info("SEPARANDO FUENTES CON DEMUCS")
        logger.info("="*60)
        
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {audio_path}")
        
        logger.info(f"Archivo de entrada: {audio_path}")
        logger.info(f"Modelo: {self.model}")
        
        try:
            # Ejecutar Demucs
            # Demucs separa en: drums, bass, vocals, other
            cmd = [
                "demucs",
                "--model", self.model,
                "--out", str(self.output_dir),
                "--no-split",  # No dividir en chunks
                str(audio_path)
            ]
            
            logger.info(f"Ejecutando: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                logger.error(f"Error en Demucs: {result.stderr}")
                raise RuntimeError(f"Demucs failed: {result.stderr}")
            
            logger.info(f"Demucs output:\n{result.stdout}")
            
            # Las salidas están en self.output_dir/{modelo}/{canción}/
            separated_dir = self.output_dir / self.model / audio_path.stem
            
            if not separated_dir.exists():
                raise FileNotFoundError(f"Directorio de salida no encontrado: {separated_dir}")
            
            # Buscar los archivos de componentes
            components = {}
            for component in ['drums.wav', 'bass.wav', 'vocals.wav', 'other.wav']:
                component_path = separated_dir / component
                if component_path.exists():
                    component_name = component.replace('.wav', '')
                    components[component_name] = str(component_path)
                    logger.info(f"  ✓ Componente extraído: {component_name}")
            
            if not components:
                logger.warning("No se encontraron componentes separados")
                return {}
            
            logger.info(f"✓ Separación completada: {len(components)} componentes")
            return components
            
        except Exception as e:
            logger.error(f"Error en separación con Demucs: {e}")
            raise
    
    def analyze_vocal_component(self, vocal_path):
        """
        Analizar y mejorar el componente vocal separado
        
        Args:
            vocal_path: Ruta del archivo vocal separado
            
        Returns:
            Array de audio mejorado
        """
        logger.info(f"Analizando componente vocal: {vocal_path}")
        
        # Cargar componente vocal
        y, sr = librosa.load(vocal_path, sr=self.sr)
        
        # Análisis de características
        rms = np.sqrt(np.mean(y**2))
        rms_db = 20 * np.log10(rms) if rms > 0 else -np.inf
        
        logger.info(f"  - RMS: {rms:.4f} ({rms_db:.2f} dB)")
        logger.info(f"  - Duración: {len(y)/sr:.2f}s")
        
        # STFT para análisis espectral
        S = librosa.stft(y)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=S.shape[0]*2-2)
        
        # Energía por banda de frecuencia
        low_energy = np.sum(np.abs(S[freqs < 250, :]))
        mid_energy = np.sum(np.abs(S[(freqs >= 250) & (freqs < 2000), :]))
        high_energy = np.sum(np.abs(S[freqs >= 2000, :]))
        
        total_energy = low_energy + mid_energy + high_energy
        
        logger.info(f"  - Distribución energética:")
        logger.info(f"    - Bajos (<250Hz): {low_energy/total_energy*100:.1f}%")
        logger.info(f"    - Medios (250-2kHz): {mid_energy/total_energy*100:.1f}%")
        logger.info(f"    - Altos (>2kHz): {high_energy/total_energy*100:.1f}%")
        
        return y, sr
    
    def enhance_vocal(self, vocal_path, output_path=None):
        """
        Mejorar componente vocal separado
        
        Args:
            vocal_path: Ruta del archivo vocal
            output_path: Ruta para guardar el vocal mejorado
            
        Returns:
            Ruta del archivo mejorado
        """
        logger.info("Mejorando componente vocal...")
        
        y, sr = self.analyze_vocal_component(vocal_path)
        
        # Aplicar mejoras
        # 1. Normalizar
        max_val = np.max(np.abs(y))
        if max_val > 0:
            y = y / max_val * 0.95
        
        # 2. Comprensión dinámica suave
        # Detectar picos y reducirlos suavemente
        threshold = 0.5
        mask = np.abs(y) > threshold
        if np.any(mask):
            compression_ratio = 4  # 4:1
            above_threshold = np.abs(y[mask]) - threshold
            y[mask] = np.sign(y[mask]) * (threshold + above_threshold / compression_ratio)
        
        # 3. Realce de presencia en 2-4 kHz
        S = librosa.stft(y)
        freqs = librosa.fft_frequencies(sr=sr, n_fft=S.shape[0]*2-2)
        
        # Crear ganancia variable
        gain = np.ones(S.shape[0])
        presence_band = (freqs >= 2000) & (freqs <= 4000)
        gain[presence_band] = 1.5  # +50% en banda de presencia
        
        S_enhanced = S * gain[:, np.newaxis]
        y_enhanced = librosa.istft(S_enhanced)
        
        # Guardar
        if output_path is None:
            output_path = Path(vocal_path).parent / f"enhanced_{Path(vocal_path).name}"
        
        sf.write(output_path, y_enhanced, sr)
        logger.info(f"✓ Componente vocal mejorado guardado: {output_path}")
        
        return output_path
    
    def process_with_demucs(self, audio_path):
        """
        Pipeline completo: separar fuentes -> mejorar vocal -> transcribir
        
        Args:
            audio_path: Ruta del archivo de audio
            
        Returns:
            Dict con resultados completos
        """
        try:
            # Separar fuentes
            components = self.separate_sources_demucs(audio_path)
            
            if 'vocals' not in components:
                logger.warning("Componente vocal no encontrado en la separación")
                return {"error": "No vocal component found"}
            
            # Mejorar componente vocal
            vocal_enhanced_path = self.enhance_vocal(components['vocals'])
            
            # Guardar metadata
            metadata = {
                "timestamp": datetime.now().isoformat(),
                "original_file": str(audio_path),
                "separated_components": components,
                "enhanced_vocal_path": str(vocal_enhanced_path),
                "model_used": self.model
            }
            
            metadata_path = self.output_dir / f"{Path(audio_path).stem}_demucs_metadata.json"
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✓ Metadata guardado: {metadata_path}")
            
            return metadata
            
        except Exception as e:
            logger.error(f"Error en procesamiento con Demucs: {e}")
            raise


def main():
    """Función principal"""
    import sys
    
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python advanced_demucs_processor.py <archivo_audio>")
        print("\nEjemplo:")
        print("  python advanced_demucs_processor.py audio_con_musica.mp3")
        sys.exit(1)
    
    processor = DemucsAudioProcessor(sr=16000, model="htdemucs")
    
    audio_file = sys.argv[1]
    metadata = processor.process_with_demucs(audio_file)
    
    print("\n" + "="*60)
    print("PROCESAMIENTO COMPLETADO")
    print("="*60)
    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
