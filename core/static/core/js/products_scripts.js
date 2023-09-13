function send_product_data(product_id, name, description, quantity, price) {
    var stripe = Stripe('pk_test_51M80oLI26erAkqnm5Pqok2mL6hb3adLZxWjsG2xdo7wYJaZwxghHuAWlaMp5iiGMHXfu1cDxMmawlP4eMxIUCWBq00CZSRDAqO');

    if (quantity == 0) {
        return alert("Product is finished");
    }

    var data = {
        "product_id": product_id,
        "name": name,
        "description": description,
        "price": price
    }

    $.ajax({
        url: 'http://djangoproject:8000/api/v1/stripe/session/',
        headers: {
            'X-CSRFToken': $.cookie("csrftoken")
        },
        method: 'get',
        dataType: 'json',
        data: data,
        success: function(data){
            var session_id = data['session']['id'];

            stripe.redirectToCheckout({
                sessionId: session_id
            })
            .then(function(result){
            });
        }
    });
}
