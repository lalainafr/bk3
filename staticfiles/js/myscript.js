
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