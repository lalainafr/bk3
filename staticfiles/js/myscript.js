

// Faire disparaitre le message après 5s 
document.addEventListener("DOMContentLoaded", function () {
    const alerts = document.querySelectorAll(".auto-hide");

    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = "opacity 0.5s ease";
            alert.style.opacity = "0";

            setTimeout(function() {
                alert.remove();
            }, 500); // Attend la fin de l'animation
        }, 5000); // 5 secondes
    });
});


// Selection soit 1 film soit 1 evenement, pas les 2 à la fois  (création de seance)
const film = document.getElementById('id_film');
const evenement = document.getElementById('id_evenement');

film.addEventListener("change", (event) => {
    const select = event.target;
    if (select.value !== ""){
        evenement.setAttribute("disabled", "disabled");
        evenement.value = "";
}
});

evenement.addEventListener("change", (event) => {
    const select = event.target;
    if (select.value !== ""){
        film.setAttribute("disabled", "disabled");
        film.value = "";
}
});
