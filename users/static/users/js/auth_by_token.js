function auth_by_token() {
    var data = {
        "email": document.getElementById("email").value,
        "password": document.getElementById("password").value,
    }

    $.ajax({
        url: 'http://djangoproject:8000/djoser/auth/token/login',
        headers: {
            'X-CSRFToken': $.cookie("csrftoken")
        },    
        method: 'post',
        dataType: 'json',
        data: data,
        success: function(data){
            localStorage.setItem("auth_token", data["auth_token"]);
            document.location.href = "http://djangoproject:8000/";
        },
        error: function (jqXHR, exception) {
            console.error(exception);
            var errors_element = document.getElementById("errors");
            errors_element.innerHTML = jqXHR.responseText;
        }
    });
};
