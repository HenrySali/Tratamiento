# 🌐 INTERFAZ WEB - GUÍA COMPLETA

¡Ya tienes la **interfaz web** para subir tus audios directamente desde el navegador! 🎉

---

## 🚀 CÓMO EJECUTAR

### En Linux/Mac:
```bash
cd /projects/sandbox/Tratamiento
./run_web.sh
```

### En Windows:
```cmd
cd \projects\sandbox\Tratamiento
run_web.bat
```

### Manualmente:
```bash
source venv/bin/activate
python web_app.py
```

---

## 🌐 ABRIR EN NAVEGADOR

Una vez que veas:
```
 * Running on http://127.0.0.1:5000
```

**Abre en tu navegador:**
```
http://localhost:5000
```

---

## 📤 CÓMO SUBIR UN AUDIO

### Opción 1: Arrastra y Suelta (más fácil)
1. Simplemente **arrastra tu archivo** de audio a la zona gris
2. Déjalo caer
3. ¡Listo! Se carga automáticamente

### Opción 2: Botón de Selección
1. Haz clic en "**Selecciona archivo**"
2. Elige tu audio
3. Se cargará automáticamente

---

## ⚙️ PROCESAR TU AUDIO

1. **Selecciona el idioma** (Español, Inglés, Francés, etc.)
2. Haz clic en "**⚡ Procesar Audio**"
3. **Espera** a que complete (verás los 5 pasos)
4. ¡Listo! Se abrirá la sección de resultados

---

## 📊 VER RESULTADOS

Después del procesamiento verás:

### 🔊 Audio Procesado
- Reproductor de audio integrado
- Botones: Play, Pause, Volumen
- Barra de progreso

### 📝 Transcripción
- Todo el texto que se dijo
- Botón "Copiar Transcripción"
- Puedes copiar y pegar donde quieras

### ⬇️ Descargar
Dos botones:
1. **🎵 Descargar Audio** - Audio limpio (WAV)
2. **📄 Descargar Transcripción** - Texto (TXT)

---

## 💾 DÓNDE SE GUARDAN LOS ARCHIVOS

Después de procesar, encuentras todo aquí:

```
/projects/sandbox/Tratamiento/processed_audio/
├── tu_archivo_clean.wav           (Audio limpio)
├── tu_archivo_transcription.txt   (Transcripción)
└── tu_archivo_metadata.json       (Información del proceso)
```

---

## 🎯 EJEMPLOS DE USO

### Ejemplo 1: Audio Susurrado
1. Arrastra `audio_susurrado.wav`
2. Selecciona "Español"
3. Procesa
4. **Resultado:** Audio claramente escuchable + texto

### Ejemplo 2: Reunión Grabada con Ruido
1. Carga `reunion_ruidosa.mp3`
2. Escoge idioma
3. Procesa
4. **Resultado:** Se entiende todo perfectamente

### Ejemplo 3: Múltiples Audios
1. Procesa uno
2. Descarga resultados
3. Haz clic en "Procesar Otro Audio"
4. Sube el siguiente
5. ¡Repite!

---

## 🎨 INTERFAZ

### Características:
✅ **Moderna y profesional**
✅ **Oscura** (fácil para la vista)
✅ **Responsiva** (funciona en móvil, tablet, PC)
✅ **Animaciones suaves**
✅ **Rápida**
✅ **Intuitiva**

### Colores:
- 🟣 Púrpura: Acciones principales
- 🟢 Verde: Éxito/completado
- 🔴 Rojo: Errores
- ⚫ Oscuro: Fondo moderno

---

## ⏱️ TIEMPOS DE PROCESAMIENTO

| Duración | Tiempo Aproximado |
|----------|------------------|
| 1 minuto | 30-60 segundos |
| 5 minutos | 2-3 minutos |
| 10 minutos | 4-6 minutos |
| 30 minutos | 10-15 minutos |

*Tiempos en CPU. Más rápido con GPU*

---

## 🔌 FORMATOS SOPORTADOS

Puedes subir estos formatos:
- ✅ `.wav` - WAV (recomendado)
- ✅ `.mp3` - MP3
- ✅ `.ogg` - OGG Vorbis
- ✅ `.flac` - FLAC
- ✅ `.m4a` - MP4 Audio

**Límite:** 500MB por archivo

---

## 🌍 IDIOMAS DISPONIBLES

Puedes transcribir en estos idiomas:
- 🇪🇸 Español
- 🇬🇧 Inglés
- 🇫🇷 Francés
- 🇩🇪 Alemán
- 🇮🇹 Italiano
- 🇵🇹 Portugués

*+ 70+ idiomas más disponibles*

---

## 🐛 SI ALGO NO FUNCIONA

### Error: "Conexión rechazada"
```
Solución: Asegúrate que el servidor esté corriendo
          Verifica que veas: "Running on http://localhost:5000"
```

### Error: "Puerto en uso"
```
Solución: Cambia el puerto en web_app.py
          Busca: app.run(..., port=5000)
          Cambia a: port=5001 (o 8000, 3000, etc.)
```

### El audio no se procesa
```
Solución: Recarga la página (F5 o CTRL+R)
          Intenta con un archivo más pequeño
          Verifica la consola (F12) para más detalles
```

### Transcripción en blanco
```
Solución: El audio puede ser inaudible
          Intenta procesar primero (limpiará el audio)
          Usa un archivo con voz clara
```

---

## 💡 CONSEJOS

1. **Primera ejecución lenta**: Whisper descarga el modelo (~140MB)
2. **GPU**: Si tienes GPU NVIDIA, el procesamiento es más rápido
3. **Múltiples pestañas**: Abre más pestañas para procesar varios audios
4. **Copiar automáticamente**: Copia la transcripción sin salir
5. **Descargar todo**: Botones para descargar audio + texto

---

## 🔄 FLUJO COMPLETO

```
1. SUBIR AUDIO
   ├─ Arrastra archivo
   └─ Se carga en servidor
   
2. SELECCIONAR OPCIONES
   ├─ Idioma para transcripción
   └─ Haz clic en "Procesar"
   
3. PROCESAMIENTO (pasos mostrados)
   ├─ Reducir ruido
   ├─ Normalizar
   ├─ Mejorar presencia
   └─ Transcribir
   
4. VER RESULTADOS
   ├─ Reproducir audio
   ├─ Leer transcripción
   └─ Descargar archivos
   
5. PROCESAR OTRO
   └─ Click en "Procesar Otro Audio"
```

---

## 🎓 SOBRE EL PROCESAMIENTO

La interfaz usa:

### 🔊 Reducción de Ruido Neuronal
Elimina ruido de fondo usando machine learning

### 📈 Normalización Dinámica
Amplifica automáticamente sin distorsión

### 🎯 Filtros DSP
Elimina ruidos de baja frecuencia

### 💬 Transcripción Whisper
IA de OpenAI que entiende el audio

---

## 📱 EN MÓVIL

¡La interfaz también funciona en tu teléfono!

```
1. Inicia el servidor en tu PC
2. Encuentra tu IP (ej: 192.168.1.100)
3. En móvil abre: http://192.168.1.100:5000
4. ¡Sube y procesa desde tu teléfono!
```

---

## 🔒 PRIVACIDAD

- ✅ Todos los archivos se procesan **localmente**
- ✅ **No** se suben a internet
- ✅ Puedes eliminar archivos manualmente
- ✅ Control total sobre tus datos

---

## 🆘 MÁS AYUDA

- Revisa `WEB_INTERFACE.md` para detalles técnicos
- Revisa `README.md` para documentación completa
- Verifica los logs en la terminal del servidor

---

## ✨ LO PRÓXIMO

Pronto tendremos:
- 📊 Separación de fuentes en la interfaz
- 📈 Estadísticas de procesamiento
- 🎨 Más temas de colores
- 💾 Historial de archivos
- 🔐 Autenticación de usuarios

---

## ✅ RESUMEN

```
┌─────────────────────────────────────────┐
│  ✓ Interfaz web lista                   │
│  ✓ Sube audios fácilmente              │
│  ✓ Procesa con 1 clic                  │
│  ✓ Descarga resultados                 │
│  ✓ Funciona en cualquier dispositivo    │
└─────────────────────────────────────────┘

Tu audio sucio → Tratamiento → Audio limpio + Texto
```

---

## 🚀 COMIENZA AHORA

```bash
./run_web.sh
# Abre: http://localhost:5000
# ¡Sube tu primer audio!
```

---

¡Disfruta procesando tus audios! 🎵✨
