function abrirVistaPerfil() {
    document.getElementById('infoPerfil').classList.add('show');
}

function cerrarPerfil() {
    document.getElementById('infoPerfil').classList.remove('show');
}


function mostrarPago(metodo) {

    const zona = document.getElementById("zonaPago");

    zona.innerHTML = ''; // borra el anterior

    if (metodo === "transferencia") {
        zona.innerHTML = document.getElementById("pago-transferencia").innerHTML;
    } else if (metodo === "mp") {
        zona.innerHTML = document.getElementById("pago-mp").innerHTML;
    } else if (metodo === "tarjeta") {
        zona.innerHTML = document.getElementById("pago-tarjeta").innerHTML;
    }
}