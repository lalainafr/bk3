

// PAYMENT CHECK

// ajax check card information
$('#btn-check-card').click(function (e) {
    e.preventDefault();
    
    // user id de la personne qui appuie sur le bouton 'COMMANDER'
    let id = $(this).attr("data-id")

    let profile = ''

    $.ajax({
        type: "GET",
        url: "http://127.0.0.1:8000/list-profile",
        success: function (response) {
            // liste des profiles des user renvoyés en JSON avec le lien ci-dessus
            profile_data = response.profile_datas

            for (let index = 0; index < profile_data.length; index++) {
                // On cherhe l'index du profil qui corresepond à l'user id
                if (profile_data[index].user__id == id) {
                    profile = profile_data[index];
                }
            }

            console.log(profile)
      
            // Une fois trouvé, on récupére les informations du profil qui seront comparées avec les données entrées dans le formulaire par le user pour le paiement
            let accountNb = profile['accountNb']
            let bankName = profile['bankName']
            let user_birthdate = profile['birthday'].substr(0, 10) // on prend les 10 premiere lettre '2005-02-05'

            console.log(accountNb, bankName, user_birthdate)


            // On récupere les données tapées par l'user à partir du formulaire
            let check_birthdate =  $('#check-birthdate').val()
            let check_accountNb =  $('#check-accountNb').val()
            let check_bankName =  $('#check-bankName').val()

            console.log('check_birthdate:' +  check_birthdate)
            console.log('check_accountNb:' +  check_accountNb)
            console.log('check_bankName:' +  check_bankName)

            // LOGIQUE
            // On compare les données (profile) de l'user à partir de la base de données avec les données saisies dans le formulaire
            if (check_birthdate == user_birthdate) {
                $('#status-birthdate').html('<i class="fa-regular text-success fa-circle-check"></i>')
            } else {
                $('#status-birthdate').html('<i class="fa-regular text-danger fa-circle-xmark"></i>')
            }

            if (check_accountNb == accountNb) {
                $('#status-cardNumber').html('<i class="fa-regular text-success fa-circle-check"></i>')
            } else {
                $('#status-cardNumber').html('<i class="fa-regular text-danger fa-circle-xmark"></i>')
            }

            if (check_bankName == bankName) {
                  $('#status-bankName').html('<i class="fa-regular text-success fa-circle-check"></i>')
            } else {
                $('#status-bankName').html('<i class="fa-regular text-danger fa-circle-xmark"></i>')
            }

            // all checked (les 3 éléments correspondent: date de naissance, carte bancaire et nome de la banque)
            if (check_birthdate == user_birthdate && check_accountNb == accountNb &&  check_bankName == bankName) {
                $('#all-checked').html('<i class="fa-regular text-success fa-circle-check fa-3x"></i>')
                $('#valid-card').html('CARTE VALIDE')
                $('#validation-info-card').html('INFORMATIONS BANCAIRES CORRECTES ET VALIDES')
                // activer le bouton 'PAYER'
                $('#btn-payer').removeClass('disabled');
                // désactiver le bouton 'PAYER'
                $('#btn-check-card').addClass('disabled');
            }
        }
    });
});



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
                    console.log('data:', result);

                const quantity_order = $(`#value-${id}`).text();
                const prix_order = $(`#prix-${id}`).text();
                const subtotal_order = quantity_order * prix_order

                // Affichage sous total après la MAJ de la quantity du order coté front end
                $(`#subtotal-${id}`).html(subtotal_order.toFixed(2));

                // console.log ('quantity:', quantity_order,'prix:', prix_order, 'subtotal:',subtotal_order);

                let total = 0

                const subtotals = document.querySelectorAll(".subtotal");

                for (let i = 0; i < subtotals.length; i++) {
                    const subtotal = Number(subtotals[i].textContent);

                    total += subtotal;
}
                console.log('total final:' + total)

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

