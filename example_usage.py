#!/usr/bin/env python3
"""
Ejemplos de uso del sistema de tratamiento de audio
Demuestra cómo usar los procesadores de audio
"""

from audio_processor import AudioProcessor
from advanced_demucs_processor import DemucsAudioProcessor
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_1_basic_processing():
    """
    Ejemplo 1: Procesamiento básico de audio susurrado
    
    Este ejemplo demuestra el pipeline completo:
    - Carga de audio ruidoso/susurrado
    - Reducción de ruido espectral
    - Normalización y ganancia dinámica
    - Realce de presencia
    - Transcripción con Whisper
    """
    print("\n" + "="*70)
    print("EJEMPLO 1: PROCESAMIENTO BÁSICO DE AUDIO SUSURRADO")
    print("="*70 + "\n")
    
    # Crear procesador
    processor = AudioProcessor(sr=16000, language="es")
    
    # Procesar un archivo de audio
    # NOTA: Reemplazar con tu archivo real
    audio_file = "audio_susurrado.wav"
    
    if not Path(audio_file).exists():
        print(f"⚠️  Archivo no encontrado: {audio_file}")
        print("Por favor, coloca tu archivo de audio en el directorio raíz")
        return
    
    try:
        metadata = processor.process_pipeline(
            audio_file,
            apply_presence_boost=True,
            verbose=True
        )
        print("\n✓ Procesamiento completado")
        print(f"✓ Transcripción: {metadata['transcription']}")
    except Exception as e:
        logger.error(f"Error: {e}")


def example_2_batch_processing():
    """
    Ejemplo 2: Procesamiento en lote
    
    Procesar múltiples archivos de audio de un directorio
    """
    print("\n" + "="*70)
    print("EJEMPLO 2: PROCESAMIENTO EN LOTE")
    print("="*70 + "\n")
    
    processor = AudioProcessor(sr=16000, language="es")
    
    # Procesar todos los archivos en un directorio
    audio_dir = "./audios_input"
    
    if not Path(audio_dir).exists():
        print(f"⚠️  Directorio no encontrado: {audio_dir}")
        print("Por favor, crea el directorio y coloca archivos de audio")
        return
    
    try:
        results = processor.batch_process(audio_dir)
        print(f"\n✓ {len(results)} archivos procesados")
        
        for result in results:
            print(f"\n📄 {result['original_file']}")
            print(f"   Transcripción: {result['transcription'][:100]}...")
    except Exception as e:
        logger.error(f"Error: {e}")


def example_3_demucs_separation():
    """
    Ejemplo 3: Separación de fuentes con Demucs
    
    Separa voz de música y ruido ambiental
    Ideal para audios con mucho ruido de fondo complejo
    """
    print("\n" + "="*70)
    print("EJEMPLO 3: SEPARACIÓN DE FUENTES CON DEMUCS")
    print("="*70 + "\n")
    
    processor = DemucsAudioProcessor(sr=16000, model="htdemucs")
    
    # Procesar con Demucs
    audio_file = "audio_con_musica.mp3"
    
    if not Path(audio_file).exists():
        print(f"⚠️  Archivo no encontrado: {audio_file}")
        print("Por favor, proporciona un archivo de audio")
        return
    
    try:
        metadata = processor.process_with_demucs(audio_file)
        print("\n✓ Separación completada")
        print(f"✓ Componentes encontrados:")
        for component, path in metadata['separated_components'].items():
            print(f"   - {component}: {path}")
        print(f"✓ Vocal mejorado: {metadata['enhanced_vocal_path']}")
    except Exception as e:
        logger.error(f"Error: {e}")


def example_4_advanced_workflow():
    """
    Ejemplo 4: Flujo de trabajo avanzado
    
    Combina procesamiento básico + Demucs + análisis
    """
    print("\n" + "="*70)
    print("EJEMPLO 4: FLUJO DE TRABAJO AVANZADO")
    print("="*70 + "\n")
    
    audio_file = "audio_complejo.wav"
    
    if not Path(audio_file).exists():
        print(f"⚠️  Archivo no encontrado: {audio_file}")
        return
    
    try:
        print("Paso 1: Separar fuentes...")
        demucs_proc = DemucsAudioProcessor()
        demucs_result = demucs_proc.process_with_demucs(audio_file)
        
        print("\nPaso 2: Mejorar componente vocal...")
        vocal_path = demucs_result['enhanced_vocal_path']
        
        print("\nPaso 3: Transcribir componente vocal mejorado...")
        basic_proc = AudioProcessor()
        basic_proc.process_pipeline(vocal_path)
        
        print("\n✓ Flujo de trabajo completado exitosamente")
    except Exception as e:
        logger.error(f"Error: {e}")


def show_menu():
    """Mostrar menú de ejemplos"""
    print("\n" + "="*70)
    print("SISTEMA DE TRATAMIENTO DE AUDIO - EJEMPLOS")
    print("="*70)
    print("\n1. Procesamiento básico (audio susurrado)")
    print("2. Procesamiento en lote (múltiples archivos)")
    print("3. Separación de fuentes con Demucs")
    print("4. Flujo de trabajo avanzado (combinado)")
    print("5. Salir")
    print("\n" + "-"*70)


def main():
    """Función principal con menú interactivo"""
    while True:
        show_menu()
        choice = input("Selecciona una opción (1-5): ").strip()
        
        if choice == "1":
            example_1_basic_processing()
        elif choice == "2":
            example_2_batch_processing()
        elif choice == "3":
            example_3_demucs_separation()
        elif choice == "4":
            example_4_advanced_workflow()
        elif choice == "5":
            print("\nSaliendo...")
            break
        else:
            print("⚠️  Opción no válida")


if __name__ == "__main__":
    # Para uso no interactivo, descomenta el ejemplo que quieras ejecutar:
    # example_1_basic_processing()
    # example_2_batch_processing()
    # example_3_demucs_separation()
    # example_4_advanced_workflow()
    
    # O ejecuta el menú interactivo
    main()
