//ajax call for insert sample
function add_cart(product_id,quantity) {

    if(quantity == 1){
    var data = {"product_id": product_id,"quantity":quantity};
    var count = parseInt(document.getElementById('cart_count').innerText);
    count++;
    console.log(count);
    $.ajax({
        url: '/cart/update/',
        method: 'POST',
        data: data,
        success: document.getElementById('cart_count').innerText = count

    });

    }else{
        var quant = parseInt(document.getElementById('quantity').value);
        var count = parseInt(document.getElementById('cart_count').innerText);

        count=count+quant;
        console.log(count);

        var data = {"product_id": product_id,"quantity":quant};
        $.ajax({
        url: '/cart/update/',
        method: 'POST',
        data: data,
        success: document.getElementById('cart_count').innerText = count

    });

    }


}

function show_cart() {

    var ul = document.getElementById('header_cart_list');
    ul.innerText = '';
    $.ajax({
        url: '/cart/get_cart/',
        method: 'GET',
        dataType: 'json',
        success: function (data) {
            fill_ul(data);
        }

    });

    function fill_ul(data) {
        for (let entry of data) {
            var li = document.createElement('li');
            li.className = "header-cart-item";
            var img_div = document.createElement('div');
            img_div.className = "header-cart-item-img";

            var img = document.createElement('img');
            img.alt = "IMG";
            img.src = entry.image_url;

            img_div.appendChild(img);

            var text_div = document.createElement('div');
            text_div.className = "header-cart-item-txt";

            var product_title = document.createElement('a');
            product_title.className = "header-cart-item-name";
            product_title.innerText = entry.productName;

            var product_info = document.createElement('span');
            product_info.className = "header-cart-item-info";
            product_info.innerText = entry.quantity + " x " + entry.price;

            var cart_total = document.createElement('div');
            cart_total.className = "header-cart-total";
            cart_total.innerText =

                text_div.appendChild(product_title);
            text_div.appendChild(product_info);

            li.appendChild(img_div);
            li.appendChild(text_div);

            ul.appendChild(li);
        }
    };





}


function decrementQuantity(obj, product_id) {
    var $this = $(obj);
    var $input = $this.closest('div').find('input');
    var value = $input.val();
    var count = parseInt(document.getElementById('cart_count').innerText);

    if (value != 1) {
        value--;
        count--;
    }

    if (value == 1) {

        var button = $this.closest('div').find('button');
        button[0].disabled = true;
    }
    var data = {"product_id": product_id, "quantity": value};
    $.ajax({
        url: '/cart/update/',
        method: 'POST',
        data: data,
        success: document.getElementById('cart_count').innerText = count


    });
    console.log(value);
}

function incrementQuantity(obj, product_id) {
    var $this = $(obj);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());
    var count = parseInt(document.getElementById('cart_count').innerText);

    value++;
    var data = {"product_id": product_id, "quantity": value};
    $.ajax({
        url: '/cart/update/',
        method: 'POST',
        data: data,
        success: document.getElementById('cart_count').innerText = count + 1

    });
    if (value == 2) {
        var button = $this.closest('div').find('button');
        button[0].disabled = false;
    }

}

function remove_item(obj, product_id, quantity) {
    var $this = $(obj);
    var $input = $this.closest('tr');
    var data = {"product_id": product_id};
    var $quantity = {"product_quantity": quantity}
    var count = parseInt(document.getElementById('cart_count').innerText);
    $.ajax({
        url: '/cart/remove/',
        method: 'POST',
        data: data,
        success: $input.remove(),
        success: document.getElementById('cart_count').innerText = count - quantity

    });

}