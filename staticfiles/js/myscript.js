
// DELETE CARD ORDER

$("#tbody").on("click", ".btn-del", function () {

    // récuperer le id du student à partir du 'data-sid'
    let id = $(this).attr("data-sid");

    mydata = {
        order_id: id,
    };

    mythis = $(this);
    // <input type="button" value="Delete" class="btn btn-outline-danger btn-del btn-sm" data-sid="52"></input>

    // appel AJAX
    $.ajax({
        method: "POST",
        url: "delete/",
        data: mydata,
        success: function (data) {
            console.log(data.status);

            if (data.status == 1) {
                console.log("Data deleted");
                // prendre et fadeOut le this (input...) le plus proche du tr
                $(mythis).closest("tr").fadeOut();
                // mettre à jour le total et le nombre de order dans la panier sur le navbar
                $("#order_count").text(data.order_count);
                $("#total").text(parseFloat(data.total).toFixed(2) + "€");
            }

            if (data.status == 0) {
                console.log("Unable to delete data");
            }
        },
    });
});


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


