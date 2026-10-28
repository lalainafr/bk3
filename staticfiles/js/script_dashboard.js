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



// <!-- Sélection du menu -->
document
    .querySelectorAll("#sidebarMenu .nav-link")
    .forEach((link) => {
        link.addEventListener("click", function () {
            document
                .querySelectorAll("#sidebarMenu .nav-link")
                .forEach((item) => {
                    item.classList.remove("active");
                });

            this.classList.add("active");
        });
    });





