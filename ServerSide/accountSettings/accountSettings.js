function logOut(){
    fetch("/log_out", {
            method: "GET"

    }).then(response => location.reload() )
}

function deleteAcc(){
    fetch("/delete_account", {
            method: "GET"

    }).then(response => location.reload() )
}

function changeProfile(){
    upload_form = document.getElementById("upload_file");
    if (upload_form.style.display =="flex"){
        upload_form.style.display = "none"
    }
    else{
       upload_form.style.display = "flex"
    }
}

function changePassword(){
    changePass_form = document.getElementById("change_pass-form");
    if (changePass_form.style.display =="flex"){
        changePass_form.style.display = "none"
    }
    else{
       changePass_form.style.display = "flex"
    }
}


document.getElementById('change_pass-form').addEventListener("submit", function(event) {
    event.preventDefault();  // Prevent default form submission

    // Get form data
    let formData = new FormData(document.getElementById('change_pass-form')); //the formData object  with the form's current keys/values, and encode file input content
    let password = formData.get('password');
    let confirm_password = formData.get('confirm-password');

    // Send form data to the server using Fetch API
    fetch('/change_password', {
        method: 'POST',
        body: formData
    })

    .then(response => {
        if (response.status === 200) {
            $("div.success").fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
         } else if (response.status === 409) { // username or email already taken
             $("alert-box failure").fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
        } else {
            $("alert-box failure").fadeIn( 300 ).delay( 1500 ).fadeOut( 400 );
        }
    });
});