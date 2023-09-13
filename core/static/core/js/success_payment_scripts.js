function decrement_product_quantity() {
    $.ajax({
        url: 'http://djangoproject:8000/api/v1/payment/decrement_product_quantity/',
        headers: {
            'X-CSRFToken': $.cookie("csrftoken")
        },
        method: 'put',
        success: function(data){
            console.log('Decremented product quantity');
        }
    });
}

decrement_product_quantity();
