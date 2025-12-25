"""
Application Jarvis - Reconnaissance vocale Bambara avec Djelia AI et ElevenLabs
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path
import shutil
from bambara_voice_interface import BambaraVoiceInterface
import uvicorn

# Initialiser l'application FastAPI
app = FastAPI(
    title="Jarvis - Assistant Vocal Bambara",
    description="Reconnaissance vocale bambara avec Djelia AI et agent conversationnel ElevenLabs",
    version="1.0.0"
)

# Créer les dossiers nécessaires
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialiser l'interface vocale bambara
bambara_interface = BambaraVoiceInterface()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Page d'accueil avec interface utilisateur"""
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jarvis - Assistant Vocal Bambara</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }

            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }

            h1 {
                color: #667eea;
                text-align: center;
                margin-bottom: 10px;
                font-size: 2.5em;
            }

            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }

            .intro {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 20px;
                margin-bottom: 30px;
                border-radius: 8px;
            }

            .intro h2 {
                color: #667eea;
                margin-bottom: 10px;
            }

            .intro ul {
                margin-left: 20px;
                color: #555;
            }

            .intro li {
                margin: 8px 0;
            }

            .section {
                margin: 30px 0;
            }

            .section h3 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.3em;
            }

            .upload-area {
                border: 3px dashed #667eea;
                border-radius: 15px;
                padding: 40px;
                text-align: center;
                background: #f8f9fa;
                transition: all 0.3s;
                cursor: pointer;
            }

            .upload-area:hover {
                background: #e9ecef;
                border-color: #764ba2;
            }

            .upload-area.dragging {
                background: #e9ecef;
                border-color: #764ba2;
                transform: scale(1.02);
            }

            input[type="file"] {
                display: none;
            }

            .btn {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 30px;
                font-size: 1.1em;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
            }

            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
            }

            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }

            .result {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 15px;
                display: none;
            }

            .result.show {
                display: block;
                animation: slideIn 0.5s;
            }

            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }

            .transcript, .response {
                margin: 15px 0;
                padding: 15px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }

            .transcript h4, .response h4 {
                color: #667eea;
                margin-bottom: 10px;
            }

            .loading {
                display: none;
                text-align: center;
                margin: 20px 0;
            }

            .loading.show {
                display: block;
            }

            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            audio {
                width: 100%;
                margin-top: 15px;
            }

            .file-info {
                margin-top: 15px;
                padding: 10px;
                background: white;
                border-radius: 8px;
                display: none;
            }

            .file-info.show {
                display: block;
            }

            .icon {
                font-size: 3em;
                margin-bottom: 15px;
            }

            .button-group {
                display: flex;
                gap: 15px;
                justify-content: center;
                margin-top: 20px;
            }

            .recording {
                animation: pulse 1.5s infinite;
            }

            @keyframes pulse {
                0%, 100% {
                    transform: scale(1);
                    opacity: 1;
                }
                50% {
                    transform: scale(1.1);
                    opacity: 0.7;
                }
            }

            .record-dot {
                display: inline-block;
                width: 12px;
                height: 12px;
                background-color: #dc3545;
                border-radius: 50%;
                margin-right: 8px;
                animation: blink 1s infinite;
            }

            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.3; }
            }

            .tech-badge {
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                font-size: 0.9em;
                margin: 5px;
            }

            .logs {
                margin-top: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 10px;
                display: none;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
            }

            .logs.show {
                display: block;
            }

            .logs h4 {
                color: #667eea;
                margin-bottom: 10px;
            }

            .logs pre {
                background: white;
                padding: 15px;
                border-radius: 8px;
                overflow-x: auto;
                white-space: pre-wrap;
                word-wrap: break-word;
                margin: 0;
                color: #333;
                max-height: 300px;
                overflow-y: auto;
            }

            .error-box {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 15px 0;
                border-radius: 8px;
                display: none;
            }

            .error-box.show {
                display: block;
            }

            .error-box h4 {
                color: #856404;
                margin-bottom: 10px;
            }

            .error-box p {
                color: #856404;
                margin: 5px 0;
            }

            .success-indicator {
                color: #28a745;
                font-weight: bold;
            }

            .error-indicator {
                color: #dc3545;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🇲🇱 Jarvis</h1>
            <p class="subtitle">Assistant Vocal en Bambara</p>

            <div class="intro">
                <h2>Bienvenue ! I ni ce! 👋</h2>
                <p>Jarvis utilise l'intelligence artificielle pour comprendre et répondre en bambara.</p>
                <ul>
                    <li>🎤 <strong>Parlez en bambara</strong> - Reconnaissance vocale native avec Djelia AI</li>
                    <li>🤖 <strong>Agent intelligent</strong> - Conversations naturelles avec ElevenLabs</li>
                    <li>🔊 <strong>Réponses vocales</strong> - Audio de haute qualité</li>
                </ul>
                <div style="margin-top: 15px; text-align: center;">
                    <span class="tech-badge">Djelia AI</span>
                    <span class="tech-badge">ElevenLabs</span>
                </div>
            </div>

            <div class="section">
                <h3>Option 1: Enregistrer votre voix directement 🎙️</h3>
                <div style="text-align: center; padding: 30px; background: #f8f9fa; border-radius: 15px;">
                    <div class="icon" id="recordIcon">🎤</div>
                    <p id="recordStatus" style="color: #666; margin-bottom: 20px;">Cliquez pour commencer l'enregistrement</p>
                    <div class="button-group">
                        <button class="btn" id="recordBtn">🎙️ Enregistrer</button>
                        <button class="btn" id="stopBtn" style="display: none; background: #dc3545;">⏹️ Arrêter</button>
                        <button class="btn" id="sendRecordingBtn" style="display: none;">📤 Envoyer</button>
                    </div>
                    <div id="recordingTime" style="display: none; margin-top: 15px; font-size: 1.5em; color: #667eea;">
                        <span id="timeDisplay">00:00</span>
                    </div>
                    <audio id="recordingPreview" controls style="display: none; margin-top: 20px; width: 100%;"></audio>
                </div>
            </div>

            <div class="section">
                <h3>Option 2: Uploader un fichier audio 📁</h3>
                <div class="upload-area" id="uploadArea">
                    <div class="icon">📁</div>
                    <p style="font-size: 1.2em; margin-bottom: 10px;">Cliquez pour sélectionner un fichier audio</p>
                    <p style="color: #666; font-size: 0.9em;">ou glissez-déposez votre fichier ici</p>
                    <p style="color: #999; font-size: 0.8em; margin-top: 10px;">Formats acceptés: MP3, WAV, M4A, WEBM</p>
                    <input type="file" id="audioFile" accept="audio/*">
                </div>
                <div class="file-info" id="fileInfo"></div>
                <div style="text-align: center; margin-top: 20px;">
                    <button class="btn" id="submitBtn" disabled>Envoyer</button>
                </div>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 15px; color: #667eea;">Traitement en cours...</p>
            </div>

            <div class="error-box" id="errorBox">
                <h4>❌ Erreur détectée</h4>
                <p id="errorMessage"></p>
            </div>

            <div class="logs" id="logs">
                <h4>📋 Logs de traitement</h4>
                <pre id="logContent"></pre>
            </div>

            <div class="result" id="result">
                <div class="transcript">
                    <h4>📝 Vous avez dit:</h4>
                    <p id="transcriptText"></p>
                </div>
                <div class="response">
                    <h4>🤖 Réponse:</h4>
                    <p id="responseText"></p>
                    <audio id="audioPlayer" controls></audio>
                </div>
            </div>
        </div>

        <script>
            const uploadArea = document.getElementById('uploadArea');
            const fileInput = document.getElementById('audioFile');
            const fileInfo = document.getElementById('fileInfo');
            const submitBtn = document.getElementById('submitBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const errorBox = document.getElementById('errorBox');
            const errorMessage = document.getElementById('errorMessage');
            const logs = document.getElementById('logs');
            const logContent = document.getElementById('logContent');

            // Voice recording elements
            const recordBtn = document.getElementById('recordBtn');
            const stopBtn = document.getElementById('stopBtn');
            const sendRecordingBtn = document.getElementById('sendRecordingBtn');
            const recordIcon = document.getElementById('recordIcon');
            const recordStatus = document.getElementById('recordStatus');
            const recordingTime = document.getElementById('recordingTime');
            const timeDisplay = document.getElementById('timeDisplay');
            const recordingPreview = document.getElementById('recordingPreview');

            let selectedFile = null;
            let mediaRecorder = null;
            let audioChunks = [];
            let recordedBlob = null;
            let recordingTimer = null;
            let recordingSeconds = 0;

            // Function to display logs
            function displayLogs(logText, isError = false) {
                logContent.textContent = logText;
                logs.classList.add('show');

                if (isError) {
                    logContent.style.color = '#dc3545';
                } else {
                    logContent.style.color = '#333';
                }
            }

            // Function to display error
            function displayError(error, details = null) {
                errorMessage.textContent = error;
                if (details) {
                    errorMessage.innerHTML += '<br><br><strong>Détails:</strong><br>' + details.replace(/\n/g, '<br>');
                }
                errorBox.classList.add('show');
            }

            // Function to clear all displays
            function clearDisplays() {
                result.classList.remove('show');
                errorBox.classList.remove('show');
                logs.classList.remove('show');
            }

            // Function to detect best supported audio format for recording
            function getSupportedMimeType() {
                const types = [
                    'audio/webm;codecs=opus',
                    'audio/webm',
                    'audio/ogg;codecs=opus',
                    'audio/mp4',
                    'audio/aac',
                    'audio/mpeg'
                ];

                for (const type of types) {
                    if (MediaRecorder.isTypeSupported(type)) {
                        console.log('Using audio format:', type);
                        return type;
                    }
                }

                // Fallback - let browser choose
                console.warn('No preferred audio format supported, using default');
                return '';
            }

            // Function to get file extension from MIME type
            function getFileExtension(mimeType) {
                const extensions = {
                    'audio/webm': 'webm',
                    'audio/webm;codecs=opus': 'webm',
                    'audio/ogg;codecs=opus': 'ogg',
                    'audio/ogg': 'ogg',
                    'audio/mp4': 'mp4',
                    'audio/aac': 'aac',
                    'audio/mpeg': 'mp3'
                };
                return extensions[mimeType] || 'webm';
            }

            // Detect browser for better error messages
            const userAgent = navigator.userAgent.toLowerCase();
            const isSafari = userAgent.indexOf('safari') !== -1 && userAgent.indexOf('chrome') === -1;
            const isFirefox = userAgent.indexOf('firefox') > -1;
            const isChrome = userAgent.indexOf('chrome') > -1 && userAgent.indexOf('edge') === -1;

            console.log('Browser detected:', { isSafari, isFirefox, isChrome });
            console.log('MediaRecorder available:', typeof MediaRecorder !== 'undefined');

            // Upload area events
            uploadArea.addEventListener('click', () => fileInput.click());

            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragging');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragging');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragging');
                const file = e.dataTransfer.files[0];
                if (file && file.type.startsWith('audio/')) {
                    handleFileSelect(file);
                }
            });

            fileInput.addEventListener('change', (e) => {
                const file = e.target.files[0];
                if (file) {
                    handleFileSelect(file);
                }
            });

            function handleFileSelect(file) {
                selectedFile = file;
                fileInfo.innerHTML = `
                    <strong>📁 Fichier sélectionné:</strong> ${file.name}<br>
                    <strong>📊 Taille:</strong> ${(file.size / 1024).toFixed(2)} KB
                `;
                fileInfo.classList.add('show');
                submitBtn.disabled = false;
            }

            submitBtn.addEventListener('click', async () => {
                if (!selectedFile) return;

                const formData = new FormData();
                formData.append('file', selectedFile);

                loading.classList.add('show');
                clearDisplays();
                submitBtn.disabled = true;

                try {
                    const response = await fetch('/process-audio', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    // Afficher les logs si disponibles
                    if (data.error_log) {
                        displayLogs(data.error_log, data.success === false);
                    }

                    if (data.success !== false) {
                        // Succès
                        document.getElementById('transcriptText').textContent = data.transcript || 'Aucune transcription';
                        document.getElementById('responseText').textContent = data.response || 'Aucune réponse';

                        if (data.audio_file) {
                            document.getElementById('audioPlayer').src = '/audio/' + data.audio_file;
                        }

                        result.classList.add('show');
                    } else {
                        // Erreur
                        displayError(data.error || 'Une erreur est survenue', data.error_details);
                    }
                } catch (error) {
                    displayError('Erreur de connexion au serveur', error.message);
                    displayLogs('Erreur de connexion: ' + error.message, true);
                } finally {
                    loading.classList.remove('show');
                    submitBtn.disabled = false;
                }
            });

            // Voice Recording Functions
            let recordingMimeType = '';

            recordBtn.addEventListener('click', async () => {
                try {
                    // Check if MediaRecorder is supported
                    if (typeof MediaRecorder === 'undefined') {
                        const errorMsg = 'Votre navigateur ne supporte pas l\'enregistrement audio.\n' +
                                       'Veuillez utiliser Chrome, Firefox, Safari (version récente) ou Edge.';
                        displayError('Enregistrement non supporté', errorMsg);
                        return;
                    }

                    // Get the best supported MIME type for this browser
                    recordingMimeType = getSupportedMimeType();

                    // Request microphone access with better constraints
                    const constraints = {
                        audio: {
                            echoCancellation: true,
                            noiseSuppression: true,
                            autoGainControl: true
                        }
                    };

                    console.log('Requesting microphone access...');
                    const stream = await navigator.mediaDevices.getUserMedia(constraints);
                    console.log('Microphone access granted');

                    // Create MediaRecorder with the supported MIME type
                    const options = recordingMimeType ? { mimeType: recordingMimeType } : {};
                    mediaRecorder = new MediaRecorder(stream, options);

                    console.log('MediaRecorder created with:', {
                        mimeType: mediaRecorder.mimeType,
                        state: mediaRecorder.state
                    });

                    audioChunks = [];
                    recordingSeconds = 0;

                    mediaRecorder.ondataavailable = (event) => {
                        if (event.data.size > 0) {
                            audioChunks.push(event.data);
                            console.log('Audio chunk received:', event.data.size, 'bytes');
                        }
                    };

                    mediaRecorder.onstop = () => {
                        console.log('Recording stopped, processing...');

                        // Use the actual MIME type from the recorder
                        const actualMimeType = mediaRecorder.mimeType;
                        recordedBlob = new Blob(audioChunks, { type: actualMimeType });

                        console.log('Recorded blob created:', {
                            size: recordedBlob.size,
                            type: recordedBlob.type
                        });

                        const audioUrl = URL.createObjectURL(recordedBlob);
                        recordingPreview.src = audioUrl;
                        recordingPreview.style.display = 'block';

                        // Stop all tracks
                        stream.getTracks().forEach(track => track.stop());
                        console.log('Microphone released');
                    };

                    mediaRecorder.onerror = (event) => {
                        console.error('MediaRecorder error:', event.error);
                        displayError('Erreur d\'enregistrement', event.error.message);
                    };

                    // Start recording
                    mediaRecorder.start();
                    console.log('Recording started');

                    // Update UI
                    recordBtn.style.display = 'none';
                    stopBtn.style.display = 'inline-block';
                    recordIcon.classList.add('recording');
                    recordStatus.innerHTML = '<span class="record-dot"></span>Enregistrement en cours...';
                    recordingTime.style.display = 'block';

                    // Start timer
                    recordingTimer = setInterval(() => {
                        recordingSeconds++;
                        const mins = Math.floor(recordingSeconds / 60).toString().padStart(2, '0');
                        const secs = (recordingSeconds % 60).toString().padStart(2, '0');
                        timeDisplay.textContent = `${mins}:${secs}`;
                    }, 1000);

                } catch (error) {
                    console.error("Error accessing microphone:", error);

                    let errorMsg = "Impossible d'accéder au microphone.\n\n";

                    if (error.name === 'NotAllowedError') {
                        errorMsg += "Vous avez refusé l'accès au microphone.\n\n";
                        if (isSafari) {
                            errorMsg += "Sur Safari (Mac):\n" +
                                      "1. Allez dans Safari > Préférences > Sites web > Microphone\n" +
                                      "2. Autorisez localhost à accéder au microphone";
                        } else {
                            errorMsg += "Veuillez autoriser l'accès au microphone dans les paramètres de votre navigateur.";
                        }
                    } else if (error.name === 'NotFoundError') {
                        errorMsg += "Aucun microphone détecté.\n" +
                                  "Vérifiez qu'un microphone est connecté et sélectionné dans les préférences système.";
                    } else if (error.name === 'NotReadableError') {
                        errorMsg += "Le microphone est déjà utilisé par une autre application.\n" +
                                  "Fermez les autres applications utilisant le microphone.";
                    } else {
                        errorMsg += `Erreur: ${error.message}\n\n` +
                                  "Assurez-vous que:\n" +
                                  "- Vous utilisez localhost ou HTTPS\n" +
                                  "- Votre navigateur est à jour\n" +
                                  "- Le microphone est correctement configuré";
                    }

                    displayError("Erreur d'accès au microphone", errorMsg);
                }
            });

            stopBtn.addEventListener('click', () => {
                if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();

                    // Update UI
                    stopBtn.style.display = 'none';
                    recordBtn.style.display = 'inline-block';
                    sendRecordingBtn.style.display = 'inline-block';
                    recordIcon.classList.remove('recording');
                    recordStatus.textContent = 'Enregistrement terminé! Écoutez et envoyez.';

                    // Stop timer
                    clearInterval(recordingTimer);
                }
            });

            sendRecordingBtn.addEventListener('click', async () => {
                if (!recordedBlob) {
                    displayError('Aucun enregistrement disponible');
                    return;
                }

                // Determine the correct file extension from the blob type
                const fileExtension = getFileExtension(recordedBlob.type);
                const fileName = `recording.${fileExtension}`;

                console.log('Sending recording:', {
                    fileName: fileName,
                    blobType: recordedBlob.type,
                    blobSize: recordedBlob.size
                });

                const formData = new FormData();
                formData.append('file', recordedBlob, fileName);

                loading.classList.add('show');
                clearDisplays();
                sendRecordingBtn.disabled = true;

                try {
                    const response = await fetch('/process-audio', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    // Afficher les logs si disponibles
                    if (data.error_log) {
                        displayLogs(data.error_log, data.success === false);
                    }

                    if (data.success !== false) {
                        // Succès
                        document.getElementById('transcriptText').textContent = data.transcript || 'Aucune transcription';
                        document.getElementById('responseText').textContent = data.response || 'Aucune réponse';

                        if (data.audio_file) {
                            document.getElementById('audioPlayer').src = '/audio/' + data.audio_file;
                        }

                        result.classList.add('show');

                        // Reset recording UI
                        recordingPreview.style.display = 'none';
                        sendRecordingBtn.style.display = 'none';
                        recordedBlob = null;
                        recordingSeconds = 0;
                        timeDisplay.textContent = '00:00';
                        recordingTime.style.display = 'none';
                        recordStatus.textContent = "Cliquez pour commencer l'enregistrement";
                    } else {
                        // Erreur
                        displayError(data.error || 'Une erreur est survenue', data.error_details);
                    }
                } catch (error) {
                    displayError('Erreur de connexion au serveur', error.message);
                    displayLogs('Erreur de connexion: ' + error.message, true);
                } finally {
                    loading.classList.remove('show');
                    sendRecordingBtn.disabled = false;
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    """
    Endpoint pour traiter un fichier audio en bambara avec Djelia AI et ElevenLabs

    Workflow:
    1. Transcription audio avec Djelia AI (reconnaissance vocale bambara)
    2. Envoi du transcript à l'agent ElevenLabs
    3. Retour de la réponse de l'agent (texte et audio)
    """
    error_log = []

    try:
        # Sauvegarder le fichier uploadé
        error_log.append(f"📁 Réception du fichier: {file.filename}")
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        error_log.append(f"✅ Fichier sauvegardé: {file_path}")

        # Traiter avec l'interface bambara (Djelia AI + ElevenLabs)
        error_log.append("🔄 Début du traitement avec Djelia AI et ElevenLabs...")

        transcript, response, audio_path = bambara_interface.process_bambara_voice(
            str(file_path)
        )

        if not transcript and not response:
            error_log.append("❌ Aucune transcription ni réponse obtenue")
            return {
                "success": False,
                "transcript": "",
                "response": "Erreur lors du traitement audio",
                "audio_file": None,
                "error_log": "\n".join(error_log),
                "error": "Aucune transcription ni réponse n'a pu être générée"
            }

        error_log.append(f"✅ Transcription: {transcript}")
        error_log.append(f"✅ Réponse générée: {response[:100]}...")

        # Préparer la réponse
        result = {
            "success": True,
            "transcript": transcript,
            "response": response,
            "error_log": "\n".join(error_log)
        }

        # Ajouter le fichier audio si disponible
        if audio_path:
            result["audio_file"] = Path(audio_path).name
            error_log.append(f"✅ Fichier audio: {result['audio_file']}")
        else:
            result["audio_file"] = None
            error_log.append("⚠️ Aucun fichier audio généré")

        result["error_log"] = "\n".join(error_log)
        return result

    except HTTPException as he:
        error_log.append(f"❌ Erreur HTTP: {he.detail}")
        return {
            "success": False,
            "transcript": "",
            "response": "",
            "audio_file": None,
            "error_log": "\n".join(error_log),
            "error": he.detail
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        error_log.append(f"❌ Erreur inattendue: {str(e)}")
        error_log.append(f"📋 Détails complets:\n{error_details}")
        return {
            "success": False,
            "transcript": "",
            "response": "",
            "audio_file": None,
            "error_log": "\n".join(error_log),
            "error": str(e),
            "error_details": error_details
        }


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """
    Endpoint pour servir les fichiers audio
    """
    audio_path = bambara_interface.audio_output_dir / filename

    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Fichier audio introuvable")

    return FileResponse(audio_path, media_type="audio/mpeg")


@app.get("/health")
async def health_check():
    """Vérification de l'état du service"""
    return {
        "status": "ok",
        "message": "Jarvis Bambara est prêt!",
        "services": {
            "djelia_ai": "actif",
            "elevenlabs": "actif"
        }
    }


if __name__ == "__main__":
    print("🇲🇱 Démarrage de Jarvis - Assistant Vocal Bambara")
    print("🎤 Djelia AI - Reconnaissance vocale bambara")
    print("🤖 ElevenLabs - Agent conversationnel")
    print("\n🌐 Application disponible sur: http://localhost:8000")
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
