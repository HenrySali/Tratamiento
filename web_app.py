#!/usr/bin/env python3
"""
Aplicación Web para Tratamiento de Audio
Interface moderna para procesar audios desde el navegador
"""

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import json
import logging
from audio_processor import AudioProcessor
from datetime import datetime
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración Flask
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB máximo
app.config['UPLOAD_FOLDER'] = Path('uploads')
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3', 'ogg', 'flac', 'm4a'}

# Crear directorios necesarios
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)
Path('processed_audio').mkdir(exist_ok=True)

# Variable global para seguimiento de procesos
current_process = {
    'status': 'idle',
    'progress': 0,
    'message': '',
    'file': ''
}


def allowed_file(filename):
    """Verificar si el archivo tiene extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Endpoint para subir archivos"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': f'File type not allowed. Allowed: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'}), 400
        
        # Guardar archivo
        filename = secure_filename(file.filename)
        filepath = app.config['UPLOAD_FOLDER'] / filename
        file.save(filepath)
        
        logger.info(f"Archivo subido: {filename}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'size': os.path.getsize(filepath)
        }), 200
        
    except Exception as e:
        logger.error(f"Error en upload: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/process', methods=['POST'])
def process_audio():
    """Endpoint para procesar audio"""
    try:
        data = request.json
        filename = data.get('filename')
        language = data.get('language', 'es')
        
        if not filename:
            return jsonify({'error': 'No filename provided'}), 400
        
        filepath = app.config['UPLOAD_FOLDER'] / secure_filename(filename)
        
        if not filepath.exists():
            return jsonify({'error': 'File not found'}), 404
        
        # Actualizar estado
        current_process['status'] = 'processing'
        current_process['file'] = filename
        current_process['progress'] = 0
        current_process['message'] = 'Iniciando procesamiento...'
        
        logger.info(f"Iniciando procesamiento de: {filename}")
        
        try:
            # Procesar audio
            processor = AudioProcessor(sr=16000, language=language)
            
            current_process['message'] = 'Cargando audio...'
            current_process['progress'] = 10
            
            current_process['message'] = 'Reduciendo ruido...'
            current_process['progress'] = 30
            
            current_process['message'] = 'Normalizando...'
            current_process['progress'] = 50
            
            current_process['message'] = 'Mejorando presencia...'
            current_process['progress'] = 70
            
            current_process['message'] = 'Transcribiendo con Whisper...'
            current_process['progress'] = 80
            
            metadata = processor.process_pipeline(str(filepath), apply_presence_boost=True)
            
            current_process['message'] = 'Procesamiento completado!'
            current_process['progress'] = 100
            current_process['status'] = 'completed'
            
            logger.info(f"Procesamiento completado: {filename}")
            
            return jsonify({
                'success': True,
                'metadata': metadata,
                'transcription': metadata['transcription'],
                'clean_audio': Path(metadata['clean_audio_path']).name
            }), 200
            
        except Exception as e:
            logger.error(f"Error procesando audio: {e}\n{traceback.format_exc()}")
            current_process['status'] = 'error'
            current_process['message'] = str(e)
            return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        logger.error(f"Error en endpoint process: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status')
def get_status():
    """Obtener estado actual del procesamiento"""
    return jsonify(current_process), 200


@app.route('/api/files')
def list_files():
    """Listar archivos disponibles"""
    try:
        uploaded_files = list(app.config['UPLOAD_FOLDER'].glob('*'))
        processed_files = list(Path('processed_audio').glob('*_clean.wav'))
        
        return jsonify({
            'uploaded': [f.name for f in uploaded_files],
            'processed': [f.name for f in processed_files]
        }), 200
    except Exception as e:
        logger.error(f"Error listando archivos: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/download/<filename>')
def download_file(filename):
    """Descargar archivo procesado"""
    try:
        filename = secure_filename(filename)
        filepath = Path('processed_audio') / filename
        
        if not filepath.exists():
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='audio/wav'
        )
    except Exception as e:
        logger.error(f"Error descargando: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/transcription/<filename>')
def get_transcription(filename):
    """Obtener transcripción de un archivo"""
    try:
        filename = secure_filename(filename)
        # Buscar el archivo de transcripción
        base_name = filename.replace('_clean.wav', '')
        transcript_path = Path('processed_audio') / f'{base_name}_transcription.txt'
        
        if not transcript_path.exists():
            return jsonify({'error': 'Transcription not found'}), 404
        
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcription = f.read()
        
        return jsonify({'transcription': transcription}), 200
    except Exception as e:
        logger.error(f"Error obteniendo transcripción: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Eliminar archivo"""
    try:
        filename = secure_filename(filename)
        filepath = app.config['UPLOAD_FOLDER'] / filename
        
        if filepath.exists():
            filepath.unlink()
            logger.info(f"Archivo eliminado: {filename}")
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error eliminando archivo: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Servir archivos subidos"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/processed_audio/<filename>')
def serve_processed(filename):
    """Servir archivos procesados"""
    return send_from_directory('processed_audio', filename)


if __name__ == '__main__':
    logger.info("Iniciando servidor de Tratamiento de Audio...")
    logger.info("Abre el navegador en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
