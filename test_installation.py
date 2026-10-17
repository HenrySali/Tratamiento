#!/usr/bin/env python3
"""
Script de prueba de instalación
Verifica que todas las librerías y dependencias estén correctamente instaladas
"""

import sys
import importlib
from pathlib import Path

# Lista de módulos requeridos
REQUIRED_MODULES = [
    ('torch', 'PyTorch'),
    ('torchaudio', 'Torchaudio'),
    ('librosa', 'Librosa'),
    ('noisereduce', 'Noisereduce'),
    ('whisper', 'OpenAI Whisper'),
    ('soundfile', 'Soundfile'),
    ('scipy', 'SciPy'),
    ('numpy', 'NumPy'),
    ('demucs', 'Demucs'),
]

def test_import(module_name, display_name):
    """Probar importación de módulo"""
    try:
        importlib.import_module(module_name)
        print(f"  ✓ {display_name}")
        return True
    except ImportError as e:
        print(f"  ✗ {display_name}: {e}")
        return False

def test_audio_file_support():
    """Verificar soporte de formatos de audio"""
    try:
        import soundfile as sf
        import librosa
        
        # Crear archivo de prueba WAV
        import numpy as np
        test_sr = 16000
        duration = 1
        y = np.zeros(test_sr * duration)
        
        test_file = Path("test_audio.wav")
        sf.write(test_file, y, test_sr)
        
        # Intentar cargar
        y_loaded, sr_loaded = librosa.load(str(test_file), sr=test_sr)
        
        # Limpiar
        test_file.unlink()
        
        print("  ✓ Soporte de audio (WAV)")
        return True
    except Exception as e:
        print(f"  ✗ Soporte de audio: {e}")
        return False

def test_gpu_availability():
    """Verificar disponibilidad de GPU (opcional)"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"  ✓ GPU disponible: {torch.cuda.get_device_name(0)}")
            print(f"    Memoría: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
            return True
        else:
            print("  ℹ GPU no disponible (procesamiento en CPU)")
            return False
    except Exception as e:
        print(f"  ✗ Error verificando GPU: {e}")
        return False

def test_whisper_models():
    """Verificar disponibilidad de modelos Whisper"""
    try:
        import whisper
        print("  ℹ Modelos Whisper disponibles:")
        print("    - tiny (39M)")
        print("    - base (74M) ← RECOMENDADO")
        print("    - small (244M)")
        print("    - medium (769M)")
        print("    - large (1.5B)")
        
        # Intentar cargar modelo base
        print("  Descargando modelo base...")
        model = whisper.load_model("base", device="cpu")
        print("  ✓ Modelo Whisper 'base' disponible")
        return True
    except Exception as e:
        print(f"  ✗ Error con Whisper: {e}")
        return False

def test_demucs_models():
    """Verificar Demucs"""
    try:
        import subprocess
        result = subprocess.run(["demucs", "--help"], capture_output=True, text=True)
        if result.returncode == 0:
            print("  ✓ Demucs CLI disponible")
            print("    Modelos: htdemucs (default), mdx_extra")
            return True
        else:
            print("  ✗ Demucs CLI no disponible")
            return False
    except Exception as e:
        print(f"  ✗ Error con Demucs: {e}")
        return False

def test_scripts():
    """Verificar existencia de scripts principales"""
    scripts = [
        'audio_processor.py',
        'advanced_demucs_processor.py',
        'example_usage.py',
    ]
    
    all_exist = True
    for script in scripts:
        if Path(script).exists():
            print(f"  ✓ {script}")
        else:
            print(f"  ✗ {script} no encontrado")
            all_exist = False
    
    return all_exist

def main():
    """Función principal"""
    print("\n" + "="*70)
    print("PRUEBA DE INSTALACIÓN - SISTEMA DE TRATAMIENTO DE AUDIO")
    print("="*70 + "\n")
    
    results = {}
    
    # Test 1: Módulos Python
    print("1. Verificando módulos Python...")
    modules_ok = True
    for module_name, display_name in REQUIRED_MODULES:
        if not test_import(module_name, display_name):
            modules_ok = False
    results['modules'] = modules_ok
    
    # Test 2: Soporte de audio
    print("\n2. Verificando soporte de audio...")
    results['audio_support'] = test_audio_file_support()
    
    # Test 3: GPU (opcional)
    print("\n3. Verificando GPU (opcional)...")
    test_gpu_availability()
    
    # Test 4: Whisper
    print("\n4. Verificando Whisper...")
    results['whisper'] = test_whisper_models()
    
    # Test 5: Demucs
    print("\n5. Verificando Demucs...")
    results['demucs'] = test_demucs_models()
    
    # Test 6: Scripts
    print("\n6. Verificando scripts...")
    results['scripts'] = test_scripts()
    
    # Resumen
    print("\n" + "="*70)
    print("RESUMEN")
    print("="*70 + "\n")
    
    all_ok = all(results.values())
    
    for test_name, status in results.items():
        icon = "✓" if status else "✗"
        print(f"  {icon} {test_name.replace('_', ' ').capitalize()}")
    
    print("\n" + "="*70)
    
    if all_ok:
        print("✓ INSTALACIÓN CORRECTA")
        print("\nPuedes comenzar a usar el sistema:")
        print("  python audio_processor.py <archivo_audio.wav>")
        print("  python example_usage.py")
        print("="*70 + "\n")
        return 0
    else:
        print("✗ PROBLEMAS DETECTADOS")
        print("\nSoluciona los errores anteriores ejecutando:")
        print("  pip install -r requirements.txt")
        print("="*70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
