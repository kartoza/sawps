let modal = document.getElementById("resendEmailModal");

let btn = document.getElementById("resendEmailLink");

let span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.getElementById("resendEmailForm").onsubmit = function(event) {
    event.preventDefault();
    let email = document.getElementById("email").value;

    let xhr = new XMLHttpRequest();
    // eslint-disable-next-line no-undef
    xhr.open("POST", account_resend_verification_url, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    // eslint-disable-next-line no-undef
    xhr.setRequestHeader("X-CSRFToken", csrf_token);

    xhr.onload = function() {
        if (xhr.status == 200) {
            alert("Verification email resent. Please check your inbox.");
            modal.style.display = "none";
        } else {
            alert("Error resending verification email. Please try again.");
        }
    };

    xhr.send("email=" + encodeURIComponent(email));
}
