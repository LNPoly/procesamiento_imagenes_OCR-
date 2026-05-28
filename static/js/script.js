const imageInput = document.getElementById('image');
const previewWrapper = document.getElementById('previewWrapper');
const localPreview = document.getElementById('localPreview');
const uploadForm = document.getElementById('uploadForm');
const resultWrapper = document.getElementById('resultWrapper');
const statusMsg = document.getElementById('statusMsg');
const finalImage = document.getElementById('finalImage');
const textAnalysisOutput = document.getElementById('textAnalysisOutput');

imageInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            localPreview.src = e.target.result;
            previewWrapper.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault(); 

    const formData = new FormData(this);

    try {
        statusMsg.textContent = "Procesando imagen y analizando texto... por favor espere.";
        statusMsg.style.color = "#ffffff";
        resultWrapper.style.display = 'block';

        const response = await fetch('/procesar', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            statusMsg.textContent = data.msg;
            statusMsg.style.color = "green";
            finalImage.src = data.url_procesada;
            textAnalysisOutput.textContent = data.texto_analisis;
        } else {
            statusMsg.textContent = data.error || "Ocurrió un error inesperado.";
            statusMsg.style.color = "red";
        }

    } catch (error) {
        console.error("Error en la petición:", error);
        statusMsg.textContent = "Error de conexión con el servidor.";
        statusMsg.style.color = "red";
    }
});