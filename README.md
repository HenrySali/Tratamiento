# Tratamiento 🎵
## Sistema Avanzado de Procesamiento de Audio

Sistema profesional de tratamiento de audio basado en técnicas avanzadas de **Procesamiento Digital de Señales (DSP)** y **Aprendizaje Profundo**, diseñado para rescatar audios susurrados, con ruido o baja intensidad.

### ✨ Características Principales

#### 🔊 Pipeline de Procesamiento Neuronal
- **Reducción de Ruido Espectral**: Tecnología neuronal que preserva la voz natural
- **Normalización Dinámica**: Amplificación inteligente sin saturación
- **Filtros Paso-Alto (DSP)**: Eliminación de ruido de baja frecuencia
- **Ecualización de Presencia**: Realce de consonantes fricativas (2-4 kHz)
- **Transcripción con OpenAI Whisper**: Reconocimiento de voz en español

#### 🎼 Separación de Fuentes (Demucs)
- **Separación Neuronal**: Divide audio en vocales, batería, bajo, otros
- **Extracción de Voz**: Ideal para audio con música de fondo
- **Mejora de Componentes**: Realzado y ecualización de componentes separados

#### 📊 Análisis y Validación
- **Validación de Archivos**: Soporte para WAV, MP3, OGG, FLAC, M4A
- **Análisis Espectral**: Información detallada de energía por bandas
- **Metadata Completo**: Almacenamiento de información de procesamiento
- **Procesamiento en Lote**: Múltiples archivos simultáneamente

---

## 📦 Instalación

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes Python)

### Pasos de Instalación

1. **Clonar o descargar el repositorio**
   ```bash
   cd Tratamiento
   ```

2. **Crear entorno virtual** (recomendado)
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

### Librerías Utilizadas

| Librería | Propósito |
|----------|----------|
| **torch** | Framework de deep learning (PyTorch) |
| **torchaudio** | Procesamiento de audio con PyTorch |
| **librosa** | Análisis y manipulación de audio |
| **noisereduce** | Reducción de ruido espectral neuronal |
| **openai-whisper** | Reconocimiento de voz (transcripción) |
| **soundfile** | Lectura/escritura de archivos de audio |
| **scipy** | Procesamiento digital de señales |
| **demucs** | Separación neuronal de fuentes (Meta AI) |
| **numpy** | Computación numérica |

---

## 🚀 Uso Rápido

### Procesamiento Individual

```python
from audio_processor import AudioProcessor

# Crear procesador
processor = AudioProcessor(sr=16000, language="es")

# Procesar archivo de audio
metadata = processor.process_pipeline("mi_audio_susurrado.wav")

# Obtener transcripción
print(metadata['transcription'])
```

### Desde línea de comandos

```bash
# Procesar un archivo
python audio_processor.py audio_ruidoso.wav

# Procesar múltiples archivos
python audio_processor.py --batch ./audios_input/
```

### Separación de Fuentes con Demucs

```python
from advanced_demucs_processor import DemucsAudioProcessor

processor = DemucsAudioProcessor()
metadata = processor.process_with_demucs("audio_con_musica.mp3")

# Resultados:
# - metadata['separated_components']['vocals']
# - metadata['separated_components']['drums']
# - metadata['separated_components']['bass']
# - metadata['separated_components']['other']
```

---

## 📋 Documentación Detallada

### Clase AudioProcessor

#### Constructor
```python
processor = AudioProcessor(sr=16000, language="es")
```

**Parámetros:**
- `sr` (int): Sample rate objetivo (16000 Hz es óptimo para Whisper)
- `language` (str): Idioma para transcripción (es, en, fr, etc.)

#### Métodos Principales

##### `process_pipeline(audio_path, apply_presence_boost=True)`
Pipeline completo de procesamiento

**Parámetros:**
- `audio_path`: Ruta del archivo de audio
- `apply_presence_boost`: Aplicar realce de presencia (default: True)

**Retorna:** Dict con metadata del procesamiento

**Ejemplo:**
```python
metadata = processor.process_pipeline("audio.wav")
print(metadata['transcription'])
print(metadata['clean_audio_path'])
```

##### `load_audio(audio_path)`
Cargar archivo de audio

**Retorna:** (y, sr) - Array de audio y sample rate

##### `reduce_noise(y, sr, prop_decrease=0.85)`
Reducción de ruido espectral

**Parámetros:**
- `y`: Array de audio
- `sr`: Sample rate
- `prop_decrease`: Intensidad de reducción (0-1)

##### `normalize_audio(y, target_db=-20.0)`
Normalización dinámica con ganancia adaptativa

**Parámetros:**
- `y`: Array de audio
- `target_db`: Nivel objetivo en dB

##### `apply_highpass_filter(y, sr, cutoff_freq=100)`
Filtro paso-alto para eliminar ruido de baja frecuencia

**Parámetros:**
- `cutoff_freq`: Frecuencia de corte en Hz (100-150 Hz recomendado)

##### `enhance_presence(y, sr)`
Realza banda de presencia (2-4 kHz) para mejorar claridad

##### `batch_process(audio_dir)`
Procesar múltiples archivos de un directorio

---

### Clase DemucsAudioProcessor

#### Constructor
```python
processor = DemucsAudioProcessor(sr=16000, model="htdemucs")
```

**Parámetros:**
- `sr`: Sample rate (16000 Hz)
- `model`: Modelo Demucs ("htdemucs" o "mdx_extra")

#### Métodos Principales

##### `separate_sources_demucs(audio_path)`
Separa fuentes de audio en componentes

**Retorna:** Dict con rutas de componentes {drums, bass, vocals, other}

##### `analyze_vocal_component(vocal_path)`
Analiza características espectrales del componente vocal

**Retorna:** (y, sr) - Array de audio y sample rate

##### `enhance_vocal(vocal_path, output_path=None)`
Mejora componente vocal separado con compresión dinámica y ecualización

##### `process_with_demucs(audio_path)`
Pipeline completo: separación → mejora → transcripción

---

## 📁 Estructura de Archivos

```
Tratamiento/
├── audio_processor.py              # Procesador básico
├── advanced_demucs_processor.py     # Separación de fuentes
├── example_usage.py                 # Ejemplos de uso
├── requirements.txt                 # Dependencias
├── README.md                        # Esta documentación
├── processed_audio/                 # Salida del procesamiento
│   ├── *_clean.wav                  # Audio limpio
│   ├── *_transcription.txt          # Transcripción en texto
│   └── *_metadata.json              # Metadata
└── demucs_output/                   # Salida de Demucs
    └── htdemucs/
        └── [nombre_audio]/
            ├── drums.wav
            ├── bass.wav
            ├── vocals.wav
            └── other.wav
```

---

## 🔍 Ejemplos Prácticos

### Ejemplo 1: Audio Susurrado de Baja Intensidad

```python
from audio_processor import AudioProcessor

processor = AudioProcessor(language="es")

# Procesar audio susurrado
metadata = processor.process_pipeline("grabacion_susurrada.wav")

# Resultado:
# - Audio limpio: processed_audio/grabacion_susurrada_clean.wav
# - Transcripción: processed_audio/grabacion_susurrada_transcription.txt
# - Metadata: processed_audio/grabacion_susurrada_metadata.json
```

### Ejemplo 2: Audio con Ruido de Fondo

```python
from audio_processor import AudioProcessor

processor = AudioProcessor(language="es")

metadata = processor.process_pipeline(
    "audio_ruidoso.wav",
    apply_presence_boost=True
)

# Recupera la voz incluso con ruido significativo
print(metadata['transcription'])
```

### Ejemplo 3: Audio con Música de Fondo

```python
from advanced_demucs_processor import DemucsAudioProcessor
from audio_processor import AudioProcessor

# Separar componentes
demucs = DemucsAudioProcessor()
result = demucs.process_with_demucs("cancion_con_voz.mp3")

# Procesar solo la voz mejorada
processor = AudioProcessor()
vocal_path = result['enhanced_vocal_path']
metadata = processor.process_pipeline(vocal_path)

print("Transcripción limpia:", metadata['transcription'])
```

### Ejemplo 4: Procesamiento en Lote

```python
from audio_processor import AudioProcessor

processor = AudioProcessor()

# Procesar 100 archivos de un directorio
results = processor.batch_process("./audios_input/")

# Iterar resultados
for result in results:
    print(f"{result['original_file']}: {result['transcription']}")
```

---

## ⚙️ Configuración Avanzada

### Ajustar Intensidad de Reducción de Ruido

```python
# Reducción más agresiva (hasta 1.0)
y_clean = processor.reduce_noise(y, sr, prop_decrease=0.95)

# Reducción más suave (conservadora)
y_clean = processor.reduce_noise(y, sr, prop_decrease=0.70)
```

### Cambiar Modelo de Whisper

```python
import whisper

# Modelos disponibles: tiny, base, small, medium, large
# Más grande = más preciso pero más lento
processor.model = whisper.load_model("small")  # Más preciso
# o
processor.model = whisper.load_model("tiny")   # Más rápido
```

### Cambiar Modelo Demucs

```python
# 'htdemucs': Más rápido, buena calidad (default)
# 'mdx_extra': Más preciso, más lento
processor = DemucsAudioProcessor(model="mdx_extra")
```

---

## 🎯 Casos de Uso

### ✓ Ideal para:
- Audios de reuniones grabados con mala calidad
- Conversaciones telefónicas degradadas
- Grabaciones de susurros o voces bajas
- Audio con ruido de fondo constante
- Música de fondo interferente
- Podcasts grabados en ambientes ruidosos
- Transcripción de entrevistas

### ✗ Limitaciones:
- No recupera audio completamente inaudible
- Ruido muy alto puede distorsionar resultado
- Requiere mínimo de sample rate 8 kHz
- Modelos grandes requieren tiempo de procesamiento

---

## 📊 Técnicas DSP Utilizadas

### 1. **Reducción de Ruido Espectral**
Usa análisis de Fourier para identificar y reducir componentes de ruido constante mientras preserva la voz.

### 2. **Normalización RMS**
Calcula la energía media (RMS) y amplifica proporcionalmente al nivel objetivo en dB.

```
Ganancia (dB) = Target (dB) - Current (dB)
```

### 3. **Filtro Paso-Alto (Butterworth)**
Elimina contenido por debajo de 100-150 Hz (ruido de viento, golpes, etc.)

```
Orden del filtro: 6
Frecuencia de corte: 100 Hz
```

### 4. **Realce de Presencia STFT**
Analiza audio en el dominio de la frecuencia y aumenta energía en 2-4 kHz donde están las consonantes fricativas.

### 5. **Separación Neuronal (Demucs)**
Red convolucional entrenada en millones de canciones para separar vocales, batería, bajo y otros elementos.

---

## 🔗 Referencias

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Librosa Documentation](https://librosa.org/)
- [Meta Demucs](https://github.com/facebookresearch/demucs)
- [noisereduce](https://github.com/timsainb/noisereduce)
- [SciPy Signal Processing](https://docs.scipy.org/doc/scipy/reference/signal.html)

---

## 📝 Licencia

Este proyecto utiliza librerías con licencias abiertas (MIT, Apache 2.0, etc.)

---

## 🤝 Contribuciones

Para reportar bugs o sugerencias, crea un issue en el repositorio.

---

## 📞 Soporte

Para ayuda con el uso del sistema, revisa los ejemplos en `example_usage.py` o consulta la documentación de las librerías utilizadas.