<!-- Este código hace que la fecha del check out siempre sea mayor o igual a la del check in -->

document.addEventListener('DOMContentLoaded', () => {
    const checkin = document.getElementById('checkin');
    const checkout = document.getElementById('checkout');
    if (!checkin || !checkout) return;

    const hoy = new Date().toISOString().split('T')[0];

    checkin.min = hoy;
    checkout.min = hoy;

    checkin.addEventListener('change', () => {
        if (checkin.value) {
            checkout.min = checkin.value;

            if (!checkout.value || checkout.value < checkin.value) {
                checkout.value = checkin.value;
            }
        } else {

            checkout.min = hoy;
        }
    });

    checkout.addEventListener('change', () => {
        if (checkout.value && checkout.value < checkout.min) {
            checkout.value = checkout.min;
        }
    });
});