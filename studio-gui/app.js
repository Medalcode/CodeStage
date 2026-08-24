document.addEventListener('DOMContentLoaded', () => {
  const promptInput = document.getElementById('prompt-input');
  const formatSelect = document.getElementById('format-select');
  const lengthSelect = document.getElementById('length-select');
  const voiceSelect = document.getElementById('voice-select');
  const btnGenerateScript = document.getElementById('btn-generate-script');
  const btnRenderVideo = document.getElementById('btn-render-video');
  const btnSwaggerDocs = document.getElementById('btn-swagger-docs');
  const scriptPreviewContainer = document.getElementById('script-preview-container');

  const monacoWrapper = document.getElementById('monaco-wrapper');
  const monacoFilename = document.getElementById('monaco-filename');

  const renderProgressCard = document.getElementById('render-progress-card');
  const statusMessage = document.getElementById('status-message');
  const progressPercent = document.getElementById('progress-percent');
  const progressBarFill = document.getElementById('progress-bar-fill');

  let currentScript = null;
  let socket = null;
  let monacoEditorInstance = null;

  // Initialize Monaco Editor Loader
  if (typeof require !== 'undefined') {
    require.config({ paths: { vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.45.0/min/vs' } });
    require(['vs/editor/editor.main'], function () {
      monacoEditorInstance = monaco.editor.create(document.getElementById('monaco-container'), {
        value: '// Código de escena...',
        language: 'javascript',
        theme: 'vs-dark',
        automaticLayout: true,
        minimap: { enabled: false },
        fontSize: 13,
      });

      monacoEditorInstance.onDidChangeModelContent(() => {
        if (currentScript && currentScript.scenes) {
          const editorScene = currentScript.scenes.find(s => s.type === 'editor');
          if (editorScene) {
            editorScene.codeLines = monacoEditorInstance.getValue().split('\n');
            fetch('/api/save-script', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ script: currentScript })
            });
          }
        }
      });
    });
  }

  // Initialize WebSockets Telemetry with Exponential Backoff
  let wsReconnectDelay = 2000;
  function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws/render`;
    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      wsReconnectDelay = 2000;
    };

    socket.onmessage = (event) => {
      const statusData = JSON.parse(event.data);
      updateRenderProgressUI(statusData);
    };

    socket.onclose = () => {
      setTimeout(() => {
        wsReconnectDelay = Math.min(wsReconnectDelay * 1.5, 30000);
        initWebSocket();
      }, wsReconnectDelay);
    };
  }

  function updateRenderProgressUI(statusData) {
    if (statusData.status === "rendering") {
      renderProgressCard.classList.remove('hidden');
      btnRenderVideo.disabled = true;
    }
    statusMessage.textContent = statusData.message;
    progressPercent.textContent = statusData.progress + "%";
    progressBarFill.style.width = statusData.progress + "%";

    if (statusData.status === "success") {
      btnRenderVideo.disabled = false;
      alert("🎉 ¡Video renderizado exitosamente!\n\nSe ha guardado en la carpeta 'output_videos/'.");
    } else if (statusData.status === "error") {
      btnRenderVideo.disabled = false;
      alert("❌ Error durante el renderizado: " + statusData.message);
    }
  }

  // Load initial script
  fetch('/api/current-script')
    .then(res => res.json())
    .then(script => {
      if (script && script.scenes) {
        currentScript = script;
        renderScriptPreview(script);
      }
    })
    .catch(err => console.error("Error cargando script:", err));

  // Generate Script via AI
  btnGenerateScript.addEventListener('click', async () => {
    const idea = promptInput.value.trim();
    if (!idea) {
      alert("Por favor ingresa una idea o prompt para el video.");
      return;
    }

    const target_length = lengthSelect.value;
    const voice = voiceSelect.value;

    btnGenerateScript.disabled = true;
    btnGenerateScript.innerHTML = "<span>⏳ Generando Guion y Audios por IA...</span>";

    try {
      const response = await fetch('/api/generate-script', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idea, target_length, voice })
      });
      const data = await response.json();

      if (data.success && data.script) {
        currentScript = data.script;
        renderScriptPreview(data.script);
      } else {
        alert("Error generando el guion.");
      }
    } catch (err) {
      alert("Error de conexión con el servidor: " + err.message);
    } finally {
      btnGenerateScript.disabled = false;
      btnGenerateScript.innerHTML = "<span>✨ Generar Guion e Historias por IA</span>";
    }
  });

  // Render Video MP4 with Selected Format
  btnRenderVideo.addEventListener('click', async () => {
    const compositionId = formatSelect.value;
    btnRenderVideo.disabled = true;
    renderProgressCard.classList.remove('hidden');

    try {
      await fetch('/api/render-video', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ compositionId })
      });
    } catch (err) {
      alert("Error al iniciar el renderizado: " + err.message);
      btnRenderVideo.disabled = false;
    }
  });

  // Open Swagger Docs
  btnSwaggerDocs.addEventListener('click', () => {
    window.open('/docs', '_blank');
  });

  function renderScriptPreview(script) {
    if (!script.scenes || script.scenes.length === 0) {
      scriptPreviewContainer.innerHTML = `
        <div class="empty-state">
          <p>No hay escenas generadas.</p>
        </div>
      `;
      monacoWrapper.classList.add('hidden');
      return;
    }

    let html = `
      <div style="margin-bottom: 16px;">
        <h3 style="font-size: 18px; color: #38bdf8;">${script.title || 'Guion'}</h3>
        <p style="font-size: 14px; color: #94a3b8;">${script.subtitle || ''}</p>
      </div>
    `;

    let editorScene = null;

    script.scenes.forEach((scene, index) => {
      if (scene.type === 'editor') {
        editorScene = scene;
      }
      const durSec = Math.round((scene.durationInFrames || 240) / 30);
      html += `
        <div class="scene-card">
          <span class="scene-type-badge">${scene.type} (${durSec}s)</span>
          <div class="scene-title">Escena ${index + 1}: ${scene.title || scene.filename || 'Detalle'}</div>
          <div class="scene-speech">"${scene.speechText || ''}"</div>
        </div>
      `;
    });

    scriptPreviewContainer.innerHTML = html;

    // Load code into Monaco Editor if editor scene exists
    if (editorScene && monacoEditorInstance) {
      monacoWrapper.classList.remove('hidden');
      monacoFilename.textContent = `📝 ${editorScene.filename || 'script.py'}`;
      const codeText = (editorScene.codeLines || []).join('\n');
      monacoEditorInstance.setValue(codeText);
    } else if (editorScene) {
      monacoWrapper.classList.remove('hidden');
      monacoFilename.textContent = `📝 ${editorScene.filename || 'script.py'}`;
    } else {
      monacoWrapper.classList.add('hidden');
    }
  }

  // Connect WebSockets on load
  initWebSocket();
});
