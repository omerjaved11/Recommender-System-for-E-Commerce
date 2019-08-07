function category_filter(obj,category_name) {

    $.ajax({
        url: '/products/shop/'+category_name ,
        method: 'GET',
        success: function(data){
            $('#products').html(data);
        }
    });


}

