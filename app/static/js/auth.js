/* ==========================================
   VAULTX AUTHENTICATION JAVASCRIPT
========================================== */

document.addEventListener("DOMContentLoaded", () => {

    /* ==========================================
       PAGE FADE ANIMATION
    ========================================== */

    document.body.style.opacity = "0";

    setTimeout(() => {

        document.body.style.transition = "opacity .6s ease";

        document.body.style.opacity = "1";

    }, 100);


    /* ==========================================
       PASSWORD SHOW / HIDE
    ========================================== */

    const toggles = document.querySelectorAll(".toggle-password");

    toggles.forEach(toggle => {

        toggle.addEventListener("click", () => {

            const target = document.getElementById(
                toggle.dataset.target
            );

            if (!target) return;

            if (target.type === "password") {

                target.type = "text";

                toggle.classList.remove("fa-eye");

                toggle.classList.add("fa-eye-slash");

            } else {

                target.type = "password";

                toggle.classList.remove("fa-eye-slash");

                toggle.classList.add("fa-eye");

            }

        });

    });


    /* ==========================================
       PASSWORD STRENGTH
    ========================================== */

    const password = document.getElementById("password");

    const bar = document.getElementById("strengthFill");

    const text = document.getElementById("strengthText");


    if (password && bar && text) {

        password.addEventListener("input", () => {

            const value = password.value;

            let score = 0;

            if (value.length >= 8) score++;

            if (/[A-Z]/.test(value)) score++;

            if (/[a-z]/.test(value)) score++;

            if (/[0-9]/.test(value)) score++;

            if (/[^A-Za-z0-9]/.test(value)) score++;

            switch (score) {

                case 0:
                case 1:

                    bar.style.width = "20%";
                    bar.style.background = "#ef4444";
                    text.innerText = "Weak Password";

                    break;

                case 2:
                case 3:

                    bar.style.width = "60%";
                    bar.style.background = "#f59e0b";
                    text.innerText = "Medium Password";

                    break;

                case 4:
                case 5:

                    bar.style.width = "100%";
                    bar.style.background = "#22c55e";
                    text.innerText = "Strong Password";

                    break;

            }

        });

    }


    /* ==========================================
       PASSWORD MATCH CHECK
    ========================================== */

    const confirm = document.getElementById("confirmPassword");

    if (password && confirm) {

        confirm.addEventListener("input", () => {

            if (confirm.value === "") {

                confirm.style.border = "";

                return;

            }

            if (confirm.value === password.value) {

                confirm.style.border = "2px solid #22c55e";

            } else {

                confirm.style.border = "2px solid #ef4444";

            }

        });

    }


    /* ==========================================
       INPUT FOCUS EFFECT
    ========================================== */

    document.querySelectorAll(".input-box input").forEach(input => {

        input.addEventListener("focus", () => {

            input.parentElement.style.transform = "scale(1.02)";

        });

        input.addEventListener("blur", () => {

            input.parentElement.style.transform = "scale(1)";

        });

    });


    /* ==========================================
       RIPPLE EFFECT
    ========================================== */

    document.querySelectorAll(".register-btn").forEach(button => {

        button.addEventListener("click", function(e) {

            const ripple = document.createElement("span");

            const rect = this.getBoundingClientRect();

            const size = Math.max(rect.width, rect.height);

            ripple.style.width = size + "px";
            ripple.style.height = size + "px";

            ripple.style.left = (e.clientX - rect.left - size / 2) + "px";
            ripple.style.top = (e.clientY - rect.top - size / 2) + "px";

            ripple.classList.add("ripple");

            this.appendChild(ripple);

            setTimeout(() => {

                ripple.remove();

            }, 600);

        });

    });


    /* ==========================================
       FLOATING CARD ANIMATION
    ========================================== */

    const card = document.querySelector(".auth-card");

    if (card) {

        card.animate(

            [

                {
                    transform: "translateY(15px)",
                    opacity: 0
                },

                {
                    transform: "translateY(0px)",
                    opacity: 1
                }

            ],

            {

                duration: 900,

                easing: "ease-out",

                fill: "forwards"

            }

        );

    }

});