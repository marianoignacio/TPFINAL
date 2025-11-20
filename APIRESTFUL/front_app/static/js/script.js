// ---- PERFIL ----
// function abrirVistaPerfil() {
//     const perfilModal = document.getElementById('infoPerfil');
//     perfilModal.classList.add('show');
// }

// function closeModal() {
//     const perfilModal = document.getElementById('infoPerfil');
//     perfilModal.classList.remove('show');
// }
function abrirVistaPerfil() {
  document.getElementById('infoPerfil').classList.add('show');
}

function closeModal() {
  document.getElementById('infoPerfil').classList.remove('show');
}

function handleSubmit(event) {
    event.preventDefault(); 
    const nombre = document.getElementById('name').value;
    const apellido = document.getElementById('surname').value;
    const username = document.getElementById('username').value;

    // Mostrar el nombre en el perfil
    const perfilTexto = document.getElementById('perfilNombre');
    if (perfilTexto) {
        perfilTexto.textContent = `${nombre} ${apellido} (${username})`;
    }

    closeModal();
}
// Guardar nombre al enviar
localStorage.setItem('perfilNombre', `${nombre} ${apellido} (${username})`);

// Mostrar al cargar la página
window.onload = () => {
    const guardado = localStorage.getItem('perfilNombre');
    if (guardado) {
        document.getElementById('perfilNombre').textContent = guardado;
    }
};