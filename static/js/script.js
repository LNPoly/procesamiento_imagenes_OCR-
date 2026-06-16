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

//script para los efecto manuales. Modularizar en otro script
document.addEventListener('DOMContentLoaded', () => {
    const btnFiltrosManuales = document.getElementById('btnFiltrosManuales');
    const panelEfectos = document.getElementById('panelEfectos');
    const selectorEfectos = document.getElementById('selectorEfectos');
    const btnAgregarEfecto = document.getElementById('btnAgregarEfecto');
    const listaEfectosElegidos = document.getElementById('listaEfectosElegidos');
    const efectosOcultos = document.getElementById('efectosOcultos');
    const btnFinalizarEfectos = document.getElementById('btnFinalizarEfectos');
    const btnSubmitFinal = document.querySelector('#uploadForm button[type="submit"]');

    const colaEfectos = [];

    imageInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            panelEfectos.style.display = 'block';
            btnSubmitFinal.style.display = 'none'; 
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    localPreview.src = e.target.result;
                    previewWrapper.style.display = 'block';
                }
                reader.readAsDataURL(file);
            }
        }
    });

    btnAgregarEfecto.addEventListener('click', () => {
        const efecto = selectorEfectos.value;
        const nombreEfecto = selectorEfectos.options[selectorEfectos.selectedIndex].text;

        if (efecto && !colaEfectos.includes(efecto)) {
            colaEfectos.push(efecto);
            
            const li = document.createElement('li');
            li.textContent = nombreEfecto;
            listaEfectosElegidos.appendChild(li);

            efectosOcultos.value = colaEfectos.join(',');
            actualizarLivePreview();
        }
        selectorEfectos.value = ''; 
    });

    btnFinalizarEfectos.addEventListener('click', () => {
        panelEfectos.style.display = 'none';
        btnSubmitFinal.style.display = 'block'; 
    });

    function actualizarLivePreview() {
        const fileInput = document.getElementById('image');
        if (!fileInput.files[0]) return;

        const formData = new FormData();
        formData.append('image', fileInput.files[0]);
        formData.append('efectos', colaEfectos.join(','));

        fetch('/preview', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // Reemplazamos el src de la vista previa local con el string Base64 puro
                localPreview.src = data.preview_base64;
            }else {
                console.error("Error en la previsualización del servidor:", data.error);
            }
        });
    }
});

    