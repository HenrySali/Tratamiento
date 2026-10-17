// ========================================
// TRATAMIENTO - Audio Processor Web UI
// JavaScript
// ========================================

// Estado global
let currentFile = null;
let currentFilename = null;
let processingStatus = null;

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const processBtn = document.getElementById('processBtn');
const languageSelect = document.getElementById('languageSelect');
const uploadProgress = document.getElementById('uploadProgress');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');

const statusSection = document.getElementById('statusSection');
const statusFill = document.getElementById('statusFill');
const statusMessage = document.getElementById('statusMessage');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');

const audioPlayer = document.getElementById('audioPlayer');
const audioSource = document.getElementById('audioSource');
const transcriptionBox = document.getElementById('transcriptionBox');
const copyBtn = document.getElementById('copyBtn');
const downloadAudioBtn = document.getElementById('downloadAudioBtn');
const downloadTranscriptBtn = document.getElementById('downloadTranscriptBtn');
const processAnotherBtn = document.getElementById('processAnotherBtn');
const retryBtn = document.getElementById('retryBtn');

// ========== EVENT LISTENERS ==========

// Upload Area
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});
uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});
uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Process Button
processBtn.addEventListener('click', processAudio);

// Results Buttons
copyBtn.addEventListener('click', copyTranscription);
downloadAudioBtn.addEventListener('click', downloadAudio);
downloadTranscriptBtn.addEventListener('click', downloadTranscript);
processAnotherBtn.addEventListener('click', resetUI);
retryBtn.addEventListener('click', resetUI);

// ========== FILE HANDLING ==========

function handleFileSelect(file) {
    // Validar tipo de archivo
    const allowedTypes = ['audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/flac', 'audio/mp4'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const allowedExtensions = ['wav', 'mp3', 'ogg', 'flac', 'm4a'];

    if (!allowedExtensions.includes(fileExtension)) {
        showError(`Formato de archivo no permitido. Usa: ${allowedExtensions.join(', ')}`);
        return;
    }

    currentFile = file;
    currentFilename = file.name;

    // Mostrar información del archivo
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.style.display = 'block';
    uploadProgress.style.display = 'none';

    // Limpiar secciones previas
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// ========== FILE UPLOAD ==========

async function uploadFile() {
    if (!currentFile) {
        showError('Por favor selecciona un archivo');
        return;
    }

    const formData = new FormData();
    formData.append('file', currentFile);

    uploadProgress.style.display = 'block';
    fileInfo.style.display = 'none';

    try {
        // Simular progreso (la mayoría de navegadores no permiten saber el progreso real)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += Math.random() * 30;
            if (progress > 90) progress = 90;
            updateUploadProgress(progress);
        }, 200);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al subir archivo');
        }

        const data = await response.json();
        updateUploadProgress(100);
        progressText.textContent = 'Carga completada!';

        // Mostrar información después de subir
        setTimeout(() => {
            uploadProgress.style.display = 'none';
            fileInfo.style.display = 'block';
        }, 1000);

        return true;
    } catch (error) {
        clearInterval(progressInterval);
        showError(`Error al subir: ${error.message}`);
        uploadProgress.style.display = 'none';
        fileInfo.style.display = 'block';
        return false;
    }
}

function updateUploadProgress(progress) {
    progress = Math.min(progress, 100);
    progressFill.style.width = progress + '%';
    progressText.textContent = `Subiendo... ${Math.round(progress)}%`;
}

// ========== AUDIO PROCESSING ==========

async function processAudio() {
    if (!currentFile) {
        showError('Por favor selecciona un archivo');
        return;
    }

    // Subir archivo primero
    const uploadSuccess = await uploadFile();
    if (!uploadSuccess) return;

    // Mostrar estado de procesamiento
    statusSection.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    fileInfo.style.display = 'none';

    const language = languageSelect.value;

    try {
        // Iniciar procesamiento
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                filename: currentFilename,
                language: language
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Error al procesar audio');
        }

        const data = await response.json();

        // Simular progreso mientras se procesa
        simulateProcessingProgress();

        // Esperar a que se complete
        await waitForCompletion();

        // Mostrar resultados
        showResults(data);

    } catch (error) {
        showError(`Error procesando audio: ${error.message}`);
        statusSection.style.display = 'none';
    }
}

async function waitForCompletion() {
    return new Promise((resolve) => {
        const checkStatus = async () => {
            try {
                const response = await fetch('/api/status');
                const status = await response.json();

                updateProcessingUI(status);

                if (status.status === 'completed' || status.status === 'error') {
                    resolve(status);
                } else {
                    setTimeout(checkStatus, 500);
                }
            } catch (error) {
                console.error('Error checking status:', error);
                setTimeout(checkStatus, 500);
            }
        };

        checkStatus();
    });
}

function simulateProcessingProgress() {
    const steps = [
        { step: 1, progress: 20, message: 'Cargando audio...' },
        { step: 2, progress: 35, message: 'Reduciendo ruido...' },
        { step: 3, progress: 50, message: 'Normalizando...' },
        { step: 4, progress: 70, message: 'Mejorando presencia...' },
        { step: 5, progress: 90, message: 'Transcribiendo...' }
    ];

    let currentStep = 0;

    const updateStep = () => {
        if (currentStep < steps.length) {
            const step = steps[currentStep];
            updateProcessingUI({
                progress: step.progress,
                message: step.message,
                status: 'processing'
            });
            updateStepUI(step.step);
            currentStep++;
            setTimeout(updateStep, 2000);
        }
    };

    updateStep();
}

function updateProcessingUI(status) {
    statusFill.style.width = status.progress + '%';
    statusMessage.textContent = status.message;
}

function updateStepUI(stepNumber) {
    for (let i = 1; i <= 5; i++) {
        const step = document.getElementById(`step${i}`);
        if (i < stepNumber) {
            step.classList.remove('active');
            step.classList.add('completed');
        } else if (i === stepNumber) {
            step.classList.add('active');
            step.classList.remove('completed');
        } else {
            step.classList.remove('active', 'completed');
        }
    }
}

function showResults(data) {
    statusSection.style.display = 'none';
    resultsSection.style.display = 'block';
    errorSection.style.display = 'none';

    // Mostrar audio
    const cleanAudioName = data.clean_audio;
    audioSource.src = `/processed_audio/${cleanAudioName}`;
    audioPlayer.load();

    // Mostrar transcripción
    transcriptionBox.textContent = data.transcription || 'No transcription available';

    // Guardar información para descargas
    window.currentData = data;
}

function showError(message) {
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
    statusSection.style.display = 'none';
    errorMessage.textContent = message;
}

// ========== DOWNLOAD FUNCTIONS ==========

function copyTranscription() {
    const text = transcriptionBox.textContent;
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Transcripción copiada al portapapeles!');
    }).catch(err => {
        showError('Error al copiar: ' + err);
    });
}

function downloadAudio() {
    if (!window.currentData) return;
    const filename = window.currentData.clean_audio;
    window.location.href = `/api/download/${filename}`;
}

function downloadTranscript() {
    if (!window.currentData) return;
    const filename = window.currentData.clean_audio.replace('_clean.wav', '_transcription.txt');
    const text = transcriptionBox.textContent;

    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
    element.setAttribute('download', 'transcription.txt');
    element.style.display = 'none';

    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// ========== UI HELPERS ==========

function resetUI() {
    currentFile = null;
    currentFilename = null;
    fileInput.value = '';
    fileInfo.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    statusSection.style.display = 'none';
    uploadProgress.style.display = 'none';
    uploadArea.classList.remove('dragover');

    // Reset progress
    progressFill.style.width = '0%';
    progressText.textContent = 'Subiendo... 0%';
    statusFill.style.width = '0%';

    // Reset steps
    for (let i = 1; i <= 5; i++) {
        document.getElementById(`step${i}`).classList.remove('active', 'completed');
    }
}

function showNotification(message) {
    // Crear notificación temporal
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => document.body.removeChild(notification), 300);
    }, 3000);
}

// ========== INITIALIZATION ==========

document.addEventListener('DOMContentLoaded', () => {
    console.log('✓ Tratamiento Audio Processor - UI Initialized');
});

// Prevent default drag behavior on the whole page
document.addEventListener('dragover', (e) => {
    e.preventDefault();
});

document.addEventListener('drop', (e) => {
    e.preventDefault();
});
