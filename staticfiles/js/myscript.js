
// EDIT order quantity from cart

$(".quantity-update-btn").on("click",function (event) {
    // split en compenent target id
    const [operation, id] = event.target.id.split('-');
    // console.log('request',operation, id);
    // appel AJAX
  $.ajax({
            url: "update",

            // data qui seront envoyé dana la vue de l'url "update" pour traiter l'incremenetation on la décrementation
            data: {
              operation, id
            },

            //CSRF protection with ajax- for http request that modify data
            headers: {
              'X-CSRFToken': Cookies.get('csrftoken'),
            },
            method: 'POST',
            success: function( result ) {
                // Mis à jour de la quantité coté front end
                $(`#value-${id}`).html(result);
                console.log(result)

                const quantity_order = $(`#value-${id}`).text();
                const prix_order = $(`#prix-${id}`).text();
                const subtotal_order = quantity_order * prix_order

                // Affichage sous total après la MAJ de la quantity du order coté front end
                $(`#subtotal-${id}`).html(subtotal_order.toFixed(2));

                // console.log ('quantity:', quantity_order,'prix:', prix_order, 'subtotal:',subtotal_order);

                let total = 0;

                $(".subtotal").each(function() {
                    const subtotal = Number($(this).text());
                    total =+ subtotal;
                });

                // Affichage  total après la MAJ de la quantity et subtotal du order coté front end
                $(`#total`).html(total.toFixed(2));
                
            },
            error: function (err) {
              console.error('failed ', err);
            }
          });
    }
    );

// DELETE order from cart
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
            console.log(data.subtotal);
            data.subtotal = 0

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


