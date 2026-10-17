# 🌐 Interfaz Web - Tratamiento Audio Processor

## Descripción

Interfaz web moderna y profesional para procesar archivos de audio directamente desde tu navegador. 

**Características:**
- ✅ Interfaz intuitiva y responsiva
- ✅ Arrastrar y soltar archivos
- ✅ Visualización de progreso en tiempo real
- ✅ Reproductor de audio integrado
- ✅ Descarga de resultados
- ✅ Soporte multi-idioma para transcripción

---

## 🚀 Inicio Rápido

### 1. Instalar dependencias web
```bash
pip install flask werkzeug
```

### 2. Ejecutar servidor
```bash
cd /projects/sandbox/Tratamiento
source venv/bin/activate
python web_app.py
```

### 3. Abrir en navegador
```
http://localhost:5000
```

---

## 📋 Archivos de la Interfaz

```
Tratamiento/
├── web_app.py                 # Backend Flask (servidor)
├── templates/
│   └── index.html            # Página principal HTML
└── static/
    ├── style.css             # Estilos CSS modernos
    └── script.js             # Lógica JavaScript
```

---

## 🎨 Características de la Interfaz

### 📤 Subir Audio
- Arrastra y suelta archivos
- O haz clic para seleccionar
- Soporta: WAV, MP3, OGG, FLAC, M4A
- Máximo: 500MB

### 🔊 Procesar
- Selecciona idioma para transcripción
- Haz clic en "Procesar Audio"
- Ve el progreso en tiempo real con 5 pasos

### 🎵 Reproducir Resultados
- Reproductor de audio integrado
- Controles estándar (play, pause, volumen)
- Barra de progreso

### 📝 Transcripción
- Visualización completa del texto
- Copiar al portapapeles
- Descargar como archivo TXT

### ⬇️ Descargas
- Descargar audio procesado (WAV)
- Descargar transcripción (TXT)

---

## 🔌 Endpoints API

### POST `/api/upload`
Subir archivo de audio

**Request:**
```json
{
  "file": <binary audio file>
}
```

**Response:**
```json
{
  "success": true,
  "filename": "mi_audio.wav",
  "size": 5242880
}
```

### POST `/api/process`
Procesar audio

**Request:**
```json
{
  "filename": "mi_audio.wav",
  "language": "es"
}
```

**Response:**
```json
{
  "success": true,
  "transcription": "Texto transcrito...",
  "clean_audio": "mi_audio_clean.wav",
  "metadata": {...}
}
```

### GET `/api/status`
Obtener estado actual del procesamiento

**Response:**
```json
{
  "status": "processing",
  "progress": 75,
  "message": "Transcribiendo con Whisper...",
  "file": "mi_audio.wav"
}
```

### GET `/api/files`
Listar archivos disponibles

**Response:**
```json
{
  "uploaded": ["archivo1.wav", "archivo2.mp3"],
  "processed": ["archivo1_clean.wav"]
}
```

### GET `/api/download/<filename>`
Descargar archivo procesado

### POST `/api/delete/<filename>`
Eliminar archivo

---

## 🎯 Casos de Uso

### 1. Procesar Audio Susurrado
1. Arrastra tu audio susurrado
2. Selecciona "Español"
3. Haz clic en "Procesar Audio"
4. Espera a que complete
5. Descarga el audio limpio y la transcripción

### 2. Transcribir Reunión Grabada
1. Sube la grabación
2. Selecciona el idioma
3. Procesa
4. Copia la transcripción
5. Úsala en tu editor de texto

### 3. Limpiar Audio de Podcast
1. Carga el episodio
2. Procesa
3. Descarga el audio limpio
4. Usa para reeditación

---

## 🛠️ Personalización

### Cambiar Puerto
```python
# En web_app.py, última línea
app.run(debug=True, host='0.0.0.0', port=8000)  # Puerto 8000
```

### Cambiar Límite de Tamaño
```python
# En web_app.py
app.config['MAX_CONTENT_LENGTH'] = 1000 * 1024 * 1024  # 1GB
```

### Agregar Más Idiomas
```python
# En templates/index.html
<option value="it">Italiano</option>
<option value="pl">Polaco</option>
```

---

## 📊 Estructura de Directorios

```
uploads/                    # Archivos subidos por usuario
├── audio1.wav
├── audio2.mp3
└── ...

processed_audio/            # Archivos procesados
├── audio1_clean.wav
├── audio1_transcription.txt
├── audio1_metadata.json
└── ...
```

---

## 🔒 Seguridad

- ✅ Validación de tipo de archivo
- ✅ Nombre de archivo sanitizado
- ✅ Límite de tamaño
- ✅ Limpieza de directorio temporal
- ✅ Manejo de errores seguro

---

## 🐛 Solución de Problemas

### Puerto 5000 en uso
```bash
# Cambiar en web_app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Error "Module not found"
```bash
pip install flask werkzeug
```

### Memoria insuficiente
```bash
# Reducir tamaño máximo
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024
```

### Timeout en procesamiento
Algunos audios grandes pueden tomar más tiempo. Aumenta el timeout del servidor o procesa archivos más pequeños.

---

## 💡 Tips

1. **Primeras ejecuciones**: Whisper descargará el modelo (~140MB) en la primera ejecución
2. **GPU**: La interfaz detecta automáticamente GPU si está disponible
3. **Múltiples usuarios**: Cada usuario obtiene archivos separados
4. **Procesamiento paralelo**: Puedes procesar múltiples archivos abriendo pestañas

---

## 📱 Responsive Design

La interfaz funciona en:
- ✅ Desktop
- ✅ Tablet  
- ✅ Móvil

---

## 🎨 Temas

La interfaz usa:
- Tema oscuro por defecto (profesional)
- Colores degradados (púrpura a verde)
- Animaciones suaves
- Interfaz moderna

---

## 📞 Soporte

Si encuentras problemas:
1. Verifica los logs en la terminal
2. Consulta `README.md` para más información
3. Verifica que todas las dependencias estén instaladas

---

## ✨ Próximas Mejoras

- [ ] Separación de fuentes en UI
- [ ] Historial de procesamientos
- [ ] Estadísticas de uso
- [ ] Autenticación de usuarios
- [ ] Base de datos para almacenamiento

---

¡Disfruta procesando tus audios! 🎵
