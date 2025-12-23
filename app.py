"""
Application principale Jarvis - Professeur de dioula avec interface web
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import shutil
from jarvis_agent import JarvisTeacher
from voice_interface import VoiceInterface
import uvicorn

# Initialiser l'application FastAPI
app = FastAPI(
    title="Jarvis - Professeur de Dioula",
    description="Agent IA pour enseigner le dioula avec support vocal",
    version="1.0.0"
)

# Créer les dossiers nécessaires
UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Initialiser Jarvis et l'interface vocale
jarvis = JarvisTeacher()
voice_interface = VoiceInterface()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Page d'accueil avec interface utilisateur"""
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Jarvis - Professeur de Dioula</title>
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

            .text-input-section {
                margin-top: 20px;
            }

            textarea {
                width: 100%;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 1em;
                resize: vertical;
                min-height: 100px;
                font-family: inherit;
            }

            textarea:focus {
                outline: none;
                border-color: #667eea;
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Jarvis</h1>
            <p class="subtitle">Votre Professeur de Dioula Personnel</p>

            <div class="intro">
                <h2>Bienvenue ! I ni ce! 👋</h2>
                <p>Jarvis est votre professeur de dioula qui vous aide à apprendre et pratiquer la langue dioula.</p>
                <ul>
                    <li>🎤 <strong>Parlez en dioula</strong> - Enregistrez votre voix</li>
                    <li>🤖 <strong>Jarvis répond</strong> - En dioula avec phonétique</li>
                    <li>🔊 <strong>Écoutez</strong> - Prononciation correcte avec la voix Alloy</li>
                    <li>📚 <strong>Apprenez</strong> - Accès au dictionnaire dioula complet</li>
                </ul>
            </div>

            <div class="section">
                <h3>Option 1A: Enregistrer votre voix directement 🎙️</h3>
                <div style="text-align: center; padding: 30px; background: #f8f9fa; border-radius: 15px;">
                    <div class="icon" id="recordIcon">🎤</div>
                    <p id="recordStatus" style="color: #666; margin-bottom: 20px;">Cliquez pour commencer l'enregistrement</p>
                    <div class="button-group">
                        <button class="btn" id="recordBtn">🎙️ Enregistrer</button>
                        <button class="btn" id="stopBtn" style="display: none; background: #dc3545;">⏹️ Arrêter</button>
                        <button class="btn" id="sendRecordingBtn" style="display: none;">📤 Envoyer à Jarvis</button>
                    </div>
                    <div id="recordingTime" style="display: none; margin-top: 15px; font-size: 1.5em; color: #667eea;">
                        <span id="timeDisplay">00:00</span>
                    </div>
                    <audio id="recordingPreview" controls style="display: none; margin-top: 20px; width: 100%;"></audio>
                </div>
            </div>

            <div class="section">
                <h3>Option 1B: Ou uploader un fichier audio</h3>
                <div class="upload-area" id="uploadArea">
                    <div class="icon">📁</div>
                    <p style="font-size: 1.2em; margin-bottom: 10px;">Cliquez pour sélectionner un fichier audio</p>
                    <p style="color: #666; font-size: 0.9em;">ou glissez-déposez votre fichier ici</p>
                    <p style="color: #999; font-size: 0.8em; margin-top: 10px;">Formats acceptés: MP3, WAV, M4A, WEBM</p>
                    <input type="file" id="audioFile" accept="audio/*">
                </div>
                <div class="file-info" id="fileInfo"></div>
                <div style="text-align: center; margin-top: 20px;">
                    <button class="btn" id="submitBtn" disabled>Envoyer à Jarvis</button>
                </div>
            </div>

            <div class="section text-input-section">
                <h3>Option 2: Écrire à Jarvis (Texte)</h3>
                <textarea id="textInput" placeholder="Écrivez votre question ou message en français ou en dioula..."></textarea>
                <div style="text-align: center; margin-top: 15px;">
                    <button class="btn" id="submitTextBtn">Envoyer le texte à Jarvis</button>
                </div>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 15px; color: #667eea;">Jarvis réfléchit...</p>
            </div>

            <div class="result" id="result">
                <div class="transcript">
                    <h4>📝 Vous avez dit:</h4>
                    <p id="transcriptText"></p>
                </div>
                <div class="response">
                    <h4>🎓 Jarvis répond:</h4>
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
            const submitTextBtn = document.getElementById('submitTextBtn');
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const textInput = document.getElementById('textInput');

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
                result.classList.remove('show');
                submitBtn.disabled = true;

                try {
                    const response = await fetch('/process-audio', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (response.ok) {
                        document.getElementById('transcriptText').textContent = data.transcript;
                        document.getElementById('responseText').textContent = data.response;
                        document.getElementById('audioPlayer').src = '/audio/' + data.audio_file;

                        result.classList.add('show');
                    } else {
                        alert('Erreur: ' + data.detail);
                    }
                } catch (error) {
                    alert('Erreur de connexion: ' + error.message);
                } finally {
                    loading.classList.remove('show');
                    submitBtn.disabled = false;
                }
            });

            // Voice Recording Functions
            recordBtn.addEventListener('click', async () => {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];
                    recordingSeconds = 0;

                    mediaRecorder.ondataavailable = (event) => {
                        audioChunks.push(event.data);
                    };

                    mediaRecorder.onstop = () => {
                        recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
                        const audioUrl = URL.createObjectURL(recordedBlob);
                        recordingPreview.src = audioUrl;
                        recordingPreview.style.display = 'block';

                        // Stop all tracks
                        stream.getTracks().forEach(track => track.stop());
                    };

                    mediaRecorder.start();

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
                    alert("Erreur: Impossible d'accéder au microphone. Vérifiez vos permissions.");
                    console.error("Error accessing microphone:", error);
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
                    recordStatus.textContent = 'Enregistrement terminé! Écoutez et envoyez à Jarvis.';

                    // Stop timer
                    clearInterval(recordingTimer);
                }
            });

            sendRecordingBtn.addEventListener('click', async () => {
                if (!recordedBlob) {
                    alert('Aucun enregistrement disponible');
                    return;
                }

                const formData = new FormData();
                formData.append('file', recordedBlob, 'recording.webm');

                loading.classList.add('show');
                result.classList.remove('show');
                sendRecordingBtn.disabled = true;

                try {
                    const response = await fetch('/process-audio', {
                        method: 'POST',
                        body: formData
                    });

                    const data = await response.json();

                    if (response.ok) {
                        document.getElementById('transcriptText').textContent = data.transcript;
                        document.getElementById('responseText').textContent = data.response;
                        document.getElementById('audioPlayer').src = '/audio/' + data.audio_file;

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
                        alert('Erreur: ' + data.detail);
                    }
                } catch (error) {
                    alert('Erreur de connexion: ' + error.message);
                } finally {
                    loading.classList.remove('show');
                    sendRecordingBtn.disabled = false;
                }
            });

            // Text input submission
            submitTextBtn.addEventListener('click', async () => {
                const text = textInput.value.trim();
                if (!text) {
                    alert('Veuillez entrer un message');
                    return;
                }

                loading.classList.add('show');
                result.classList.remove('show');
                submitTextBtn.disabled = true;

                try {
                    const response = await fetch('/process-text', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ text: text })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        document.getElementById('transcriptText').textContent = text;
                        document.getElementById('responseText').textContent = data.response;
                        document.getElementById('audioPlayer').src = '/audio/' + data.audio_file;

                        result.classList.add('show');
                    } else {
                        alert('Erreur: ' + data.detail);
                    }
                } catch (error) {
                    alert('Erreur de connexion: ' + error.message);
                } finally {
                    loading.classList.remove('show');
                    submitTextBtn.disabled = false;
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
    Endpoint pour traiter un fichier audio
    """
    try:
        # Sauvegarder le fichier uploadé
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Traiter avec Jarvis
        transcript, response, audio_path = voice_interface.process_voice_input(
            str(file_path),
            jarvis
        )

        if not audio_path:
            raise HTTPException(status_code=500, detail="Erreur lors du traitement audio")

        return {
            "transcript": transcript,
            "response": response,
            "audio_file": Path(audio_path).name
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/process-text")
async def process_text(data: dict):
    """
    Endpoint pour traiter du texte directement
    """
    try:
        text = data.get("text", "")
        if not text:
            raise HTTPException(status_code=400, detail="Texte vide")

        # Obtenir la réponse de Jarvis
        response = jarvis.get_response(text)

        # Générer l'audio
        import time
        output_filename = f"jarvis_text_{int(time.time())}.mp3"
        audio_path = voice_interface.text_to_speech(
            text=response,
            output_filename=output_filename,
            voice="alloy"
        )

        return {
            "response": response,
            "audio_file": output_filename
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """
    Endpoint pour servir les fichiers audio
    """
    audio_path = voice_interface.audio_output_dir / filename
    if not audio_path.exists():
        raise HTTPException(status_code=404, detail="Fichier audio introuvable")

    return FileResponse(audio_path, media_type="audio/mpeg")


@app.get("/health")
async def health_check():
    """Vérification de l'état du service"""
    return {"status": "ok", "message": "Jarvis est prêt à enseigner!"}


if __name__ == "__main__":
    print("🎓 Démarrage de Jarvis - Professeur de Dioula")
    print("📚 Initialisation du système RAG...")
    print("🎤 Préparation de l'interface vocale...")
    print("\n🌐 Application disponible sur: http://localhost:8000")
    print("\nAppuyez sur Ctrl+C pour arrêter le serveur\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
