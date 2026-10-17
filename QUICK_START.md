# 🚀 Guía Rápida de Inicio

## Instalación (primera vez)

```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar entorno
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Verificar instalación
python test_installation.py
```

## Uso Básico

### Opción 1: Línea de comandos (más simple)

```bash
# Procesar un archivo
python audio_processor.py archivo_audio.wav

# Procesar múltiples archivos
python audio_processor.py --batch ./audios/
```

Los resultados se guardan en `processed_audio/`

### Opción 2: Python (más control)

```python
from audio_processor import AudioProcessor

# Crear procesador
processor = AudioProcessor(sr=16000, language="es")

# Procesar audio
metadata = processor.process_pipeline("audio_susurrado.wav")

# Ver transcripción
print(metadata['transcription'])

# Ver ruta del audio limpio
print(metadata['clean_audio_path'])
```

### Opción 3: Separación de fuentes (para audio con música)

```python
from advanced_demucs_processor import DemucsAudioProcessor

processor = DemucsAudioProcessor()
result = processor.process_with_demucs("audio_con_musica.mp3")

print(result['separated_components'])  # Acceder a vocales, batería, etc.
```

---

## 📋 Tareas Comunes

### Procesar audios susurrados
```bash
python audio_processor.py audio_susurrado.wav
```

### Procesar carpeta completa
```bash
python audio_processor.py --batch ./audios_input/
```

### Extraer voz de una canción
```python
from advanced_demucs_processor import DemucsAudioProcessor
proc = DemucsAudioProcessor()
result = proc.process_with_demucs("cancion.mp3")
print(result['separated_components']['vocals'])
```

### Cambiar idioma de transcripción
```python
processor = AudioProcessor(language="en")  # Inglés
processor = AudioProcessor(language="fr")  # Francés
```

---

## 📁 Archivos Generados

Después de procesar, en `processed_audio/` encontrarás:

- `nombre_clean.wav` - Audio limpio y normalizado
- `nombre_transcription.txt` - Transcripción en texto
- `nombre_metadata.json` - Información del procesamiento

---

## ⚙️ Parámetros Ajustables

### Intensidad de reducción de ruido

```python
# Más agresivo (0.95 = máximo)
processor.reduce_noise(y, sr, prop_decrease=0.95)

# Más suave (0.70 = conservador)
processor.reduce_noise(y, sr, prop_decrease=0.70)
```

### Modelo Whisper (velocidad vs precisión)

```python
import whisper

processor.model = whisper.load_model("tiny")    # Muy rápido, menos preciso
processor.model = whisper.load_model("base")    # RECOMENDADO
processor.model = whisper.load_model("small")   # Más preciso, más lento
processor.model = whisper.load_model("medium")  # Muy preciso, muy lento
```

### Modelo Demucs

```python
# Más rápido, buena calidad
processor = DemucsAudioProcessor(model="htdemucs")

# Más lento, mejor calidad
processor = DemucsAudioProcessor(model="mdx_extra")
```

---

## 🔧 Solucionar Problemas

### Error: "ModuleNotFoundError"
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Error: "Modelo no encontrado"
Los modelos Whisper se descargan automáticamente la primera vez.
Requiere conexión a internet.

### Slow processing
- GPU no disponible (procesamiento en CPU es normal)
- Usar modelo Whisper más pequeño (tiny, base)
- Reducir duración de audio

---

## 💡 Ejemplos Rápidos

### Audio de reunión grabado con phone
```bash
python audio_processor.py grabacion_reunion.wav
```

### Entrevista con ruido de fondo
```bash
python audio_processor.py entrevista.mp3
```

### Podcast con música introductoria
```python
from advanced_demucs_processor import DemucsAudioProcessor
proc = DemucsAudioProcessor()
result = proc.process_with_demucs("podcast.mp3")
# Ahora tienes solo la voz en result['separated_components']['vocals']
```

---

## 📞 Necesitas Ayuda?

1. Revisa `README.md` para documentación completa
2. Ejecuta `python example_usage.py` para ver ejemplos interactivos
3. Verifica logs en `processed_audio/` para metadata de procesamiento

---

## ✨ Funcionalidad Clave

✓ Reducción de ruido neuronal  
✓ Normalización automática  
✓ Realce de voz clara  
✓ Transcripción automática (Whisper)  
✓ Separación de instrumentos (Demucs)  
✓ Procesamiento en lote  
✓ Análisis espectral  

---

¡Listo! Ya puedes comenzar a procesar audios 🎵
