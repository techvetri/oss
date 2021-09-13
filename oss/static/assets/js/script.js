const WS_URL = "wss://607f343e98c2.ngrok.io/ws/"
const endpoint = "https://607f343e98c2.ngrok.io/v1/"

let socket;

$(document).ready(function () {
    $("#get-qr").click(function () {
        if(window.localStorage.getItem("auth_token")!=null){
            window.location.href = "/dashboard";
        }
        if(socket===undefined){
            socket = new WebSocket(WS_URL+"login/");

        }else {
            socket.send("get-qr");
        }


        socket.onerror = function (event) {
        //console.log(event);
            socket=undefined;
        }

        socket.onclose = function (event) {
            //console.log(event);
            socket = undefined;

        }

        socket.onmessage = function (event) {
            let data = event.data;
            let json_data = JSON.parse(data)

            if(json_data["type"]==="qr-img"){
                 const b64_data = json_data["data"];
                $("#qr-loader").hide();

                document.getElementById("qr-image").src = 'data:image/png;base64,'+b64_data;
                $("#qr-image").show();

            }else if(json_data["type"] === "message"){
                const response_data = json_data["data"]
                window.localStorage.setItem("auth_token", response_data["auth_token"]);
                window.localStorage.setItem("fcm_token", response_data["fcm_token"]);
                window.localStorage.setItem("user_id", response_data["user_id"]);
                window.localStorage.setItem("user_image", response_data["user_image"]);
                window.localStorage.setItem("user_name", response_data["user_name"])
                window.localStorage.setItem("user_email", response_data["user_email"]);
                window.localStorage.setItem("user_phone", response_data["user_phone"]);

                window.location.href = "/dashboard"

            }

        }

        socket.onopen = function (event) {
            $("#qr-login").show();
            $("#qr-image").hide();
            socket.send("get-qr");
            $("#qr-loader").show();

        }
    })


})

let product_count = 12;
let prev_prod_count = 0;

function get_searched_product(search_data) {
    $("#search-result").html("")
    $.ajax({
        url: endpoint+"get-product",
        type: "POST",
        data: {
            "user_id": window.localStorage.getItem("user_id"),
            "product_count": product_count,
            "prev_prod_count": prev_prod_count,
            "product_search_name":search_data.getAttribute("data")
        },
        beforeSend:function (xhr) {
            xhr.setRequestHeader("Authorization", window.localStorage.getItem("auth_token"))
        },
        timeout:3000,
        success:function (data) {
            searchProductAdapter(data);
        },
        error:function (error) {
            if(error.status === 401){
                alert("Your session is ended please relogin to continue.");
                window.localStorage.clear();
                window.location.href="/";
            }
        }
    })
}

function get_products() {

     $.ajax({
        url: endpoint+"get-product",
        type: "POST",
        data: {
            "user_id": window.localStorage.getItem("user_id"),
             "product_count": product_count,
            "prev_prod_count": prev_prod_count,
            "product_search_name":""
        },
        beforeSend:function (xhr) {
            xhr.setRequestHeader("Authorization", window.localStorage.getItem("auth_token"))
        },
        timeout:3000,
        success:function (data) {
            productAdapter(data);
        },
        error:function (error) {
            if(error.status === 401){
                alert("Your session is ended please relogin to continue.");
                window.localStorage.clear();
                window.location.href="/";
            }
        }
    })

}

function load_more_product() {
    $("#btn-load-more").hide();
    $("#load-more-product").show();
    get_products();
}

function productAdapter(products){

    const prod_count = products["payload"]["product_count"]
    const product = products["payload"]["product"]
    prev_prod_count +=prod_count;

    for (const productElement in product) {

        const product_data = product[productElement];
        let product_rating = "";
        let product_stock = "";
        const rating = parseInt(product_data["product_ratings"])
        const stock = parseInt(product_data["product_stock"])
        if(stock>0){
            product_stock+='<p style="color:green;">In Stock</p>'
        }else {
            product_stock+='<p style="color:red;">Sold out</p>'

        }
        for(let i=0;i<rating;i++){
            product_rating+= '<i style="color: orange" class="material-icons">star</i>';
        }


        let modal = '<div class="col-md-4 d-flex justify-content-center" style="margin-top: 10px; margin-bottom: 10px;" >';
        modal+='<div class="card" style="width: 20rem;">';
        modal+='<img src="'+product_data["product_image"]+'" class="cardimg-top" alt="..." height="170" width="150">';
        modal+='<div class="card-body">';
        modal+='<h6 class="card-title">'+product_data["product_name"]+'</h6>';
        modal+='<div style="display: flex; justify-content: space-between"><span>&#x20b9;'+product_data["product_price"]+'</span> <span>'+product_rating+'</span> </div>';

        modal+='<div>'+product_stock+'</div>';
        const str_data = {
            "product_id": product_data["product_id"],
            "product_name": product_data["product_name"],
            "product_image": product_data["product_image"],
            "product_rating": product_data["product_ratings"],
            "product_price": product_data["product_price"],
            "product_stock": product_data["product_stock"]
        };

        const b64_data = btoa(JSON.stringify(str_data))

        //console.log()
        modal+='<form action="/product_detail" method="GET">';
        modal+='<input type="hidden" name="product_detail" value="'+b64_data+'" >';
        modal+='<a onclick="this.parentNode.submit();" class="btn btn-primary">View Product</a>';
        modal+='</form>';
        modal+='</div>';
        modal+='</div>';
        modal+='</div>';

        $("#product-container").append(modal);
    }
    $("#btn-load-more").attr("onclick", "load_more_product()").show();
    $("#load-more-product").hide();

    $("#product-loader").hide();

}

function searchProductAdapter(products){
    $("#product-container").html("")
    $("#load-more-product").show();
    $("#btn-load-more").hide();

    const prod_count = products["payload"]["product_count"]
    const product = products["payload"]["product"]
    prev_prod_count +=prod_count;

    for (const productElement in product) {

        const product_data = product[productElement];
        let product_rating = "";
        let product_stock = "";
        const rating = parseInt(product_data["product_ratings"])
        const stock = parseInt(product_data["product_stock"])
        if(stock>0){
            product_stock+='<p style="color:green;">In Stock</p>'
        }else {
            product_stock+='<p style="color:red;">Sold out</p>'

        }
        for(let i=0;i<rating;i++){
            product_rating+= '<i style="color: orange" class="material-icons">star</i>';
        }


        let modal = '<div class="col-md-4 d-flex justify-content-center" style="margin-top: 10px; margin-bottom: 10px;" >';
        modal+='<div class="card" style="width: 20rem;">';
        modal+='<img src="'+product_data["product_image"]+'" class="cardimg-top" alt="..." height="170" width="150">';
        modal+='<div class="card-body">';
        modal+='<h6 class="card-title">'+product_data["product_name"]+'</h6>';
        modal+='<div style="display: flex; justify-content: space-between"><span>&#x20b9;'+product_data["product_price"]+'</span> <span>'+product_rating+'</span> </div>';

        modal+='<div>'+product_stock+'</div>';
        const str_data = {
            "product_id": product_data["product_id"],
            "product_name": product_data["product_name"],
            "product_image": product_data["product_image"],
            "product_rating": product_data["product_ratings"],
            "product_price": product_data["product_price"],
            "product_stock": product_data["product_stock"]
        };

        const b64_data = btoa(JSON.stringify(str_data))

        //console.log()
        modal+='<form action="/product_detail" method="GET">';
        modal+='<input type="hidden" name="product_detail" value="'+b64_data+'" >';
        modal+='<a onclick="this.parentNode.submit();" class="btn btn-primary">View Product</a>';
        modal+='</form>';
        modal+='</div>';
        modal+='</div>';
        modal+='</div>';

        $("#product-container").append(modal);
    }
    $("#load-more-product").hide();

    $("#product-loader").hide();

}

class product {

    products;
    constructor(products) {
        this.products = products;
        this.fetchProductDetails();
        this.fetchUserDetails();
    }

    setProduct(){
        let product_rating = "";
        let product_stock = "";
        const rating = parseInt(this.products["product_rating"])
        const stock = parseInt(this.products["product_stock"])
        if (stock > 0) {
            product_stock += '<p style="color:green;">In Stock</p>'
        } else {
            product_stock += '<p style="color:red;">Sold out</p>'

        }
        for (let i = 0; i < rating; i++) {
            product_rating += '<i style="color: orange" class="material-icons">star</i>';
        }

        $("#product-img").attr("src",this.products["product_image"]);
        $("#product_name").html(this.products["product_name"]);
        $("#product_price").html("&#x20b9;"+this.products["product_price"]);
        $("#product_price").attr("value", this.products["product_price"]);
        $("#product_stock").html(product_stock)
        $("#product_rating").html(product_rating);
        if(parseInt(this.products["product_stock"])>0){
            $("#btn-buy-now").attr("onclick","Checkout.prototype.buyProduct("+this.products["product_id"]+");");
        }else {
            $("#btn-buy-now").addClass("bg-secondary");

        }
        $("#btn-add-to-cart").attr("onclick","addToCart("+this.products["product_id"]+");");

    }

    fetchProductDetails(){

        $.ajax({
        url: endpoint+"get-product-details",
        type: "POST",
        data: {"user_id": window.localStorage.getItem("user_id"),
            "product_id": this.products["product_id"]
        },
        beforeSend:function (xhr) {
            xhr.setRequestHeader("Authorization", window.localStorage.getItem("auth_token"))
        },
        timeout:3000,
        success:function (data) {
            product.prototype.productDetailsAdapter(data);
        },
        error:function (error) {
            if(error.status === 401){
                alert("Your session is ended please relogin to continue.");
                window.localStorage.clear();
                window.location.href="/";
            }
        }
    })
    }

    productDetailsAdapter(data){

        const payload = data["payload"];
        const payloadProductDetails = payload["product_details"];

        $("#product_manufacturer").html("&nbsp;"+payload["manufacturer"]);
        $("#product_brand").html("&nbsp;"+payload["product_brand"]);
        $("#product_description").html("&nbsp;"+payload["product_description"])
        let productDetails = "";

        for(const productDetail in payloadProductDetails){
            productDetails+='<span style="font-weight: bold">'+productDetail+':&nbsp;</span><span>'+payloadProductDetails[productDetail]+'</span> <br>';

        }

        $("#product-details").append(productDetails);
        $("#product-loader").hide();
        $("#container-main").show();
    }

    fetchUserDetails(){
        $.ajax({
        url: endpoint+"get-user-detail",
        type: "POST",
        data: {"user_id": window.localStorage.getItem("user_id")
        },
        beforeSend:function (xhr) {
            xhr.setRequestHeader("Authorization", window.localStorage.getItem("auth_token"))
        },
        timeout:3000,
        success:function (data) {
            product.prototype.userAddressAdapter(data);
            },
        error:function (error) {
            if(error.status === 401){
                alert("Your session is ended please relogin to continue.");
                window.localStorage.clear();
                window.location.href="/";
            }
        }
    })
    }

    userAddressAdapter(data){
        data = data["payload"];
        $("#first_name").html(data["first_name"]);
        $("#last_name").html(data["last_name"]);
        $("#address").html(data["user_address"]);
        $("#district").html(data["district"]);
        $("#state").html(data["state"]);
        $("#zip_code").html(data["zip_code"]);
        $("#landmark").html(data["landmark"]);
        $("#country").html(data["country"]);
        $("#phone_num").html(window.localStorage.getItem("user_phone"));
        $("#address_loader").hide();
    }

}
class Checkout{
    buyProduct(product_id){
        let validated = false;
        var orderQuantity = $("#product_quantity").val();

        var quantity;
        try{
            quantity = parseInt(orderQuantity);
            if(isNaN(quantity)){
                alert("invalid quantity!!");

            }else {
                validated = true;
            }

        }catch (e) {
            alert("invalid quantity!!")
        }

        if(validated){
            $("#btn-buy-now").attr("disabled","disabled");
            $("#btn-checkout-text").hide();
            $("#btn-checkout-spinner").show();

            $.ajax({
             url: endpoint+"place-order",
             type: "POST",
             data: {
                 "user_id":window.localStorage.getItem("user_id"),
                 "product_id": product_id,
                 "product_price": $("#product_price").attr("value"),
                 "quantity": quantity
             },
                beforeSend:function (xhr) {
            xhr.setRequestHeader("Authorization", window.localStorage.getItem("auth_token"))
        },
        timeout:3000,
        success:function (data) {
                 if(data["error"]!==""){
                     alert(data["error"])
                 }else {
                     Checkout.prototype.initPayment(data);
                 }

            $("#btn-checkout-text").show();
            $("#btn-checkout-spinner").hide();
            $("#btn-buy-now").removeAttr("disabled")
            },
        error:function (error) {

            if(error.status === 401){
                alert("Your session is ended please relogin to continue.");
                window.localStorage.clear();
                window.location.href="/";
            }else {
                alert("please retry!...")
                $("#btn-checkout-text").show();
                $("#btn-checkout-spinner").hide();
                $("#btn-buy-now").removeAttr("disabled");

            }
        }

         })
        }
    }

    initPayment(data){
        const payload = data["payload"]
        var options = {
            "key": "rzp_test_oXZ9pehi2xGpF5", // Enter the Key ID generated from the Dashboard
            "amount": payload["total_amount"], // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
            "currency": "INR",
            "name": "Mano Technology",
            "description": $("#product_name").html(),
            "image": window.location.origin+"/static/assets/images/logo.png",
            "order_id": payload["txn_id"], //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
            "handler": function (response) {
                alert("Successfully Order Places you can manage your Order on your Application");
            },
            "prefill": {
                "name": window.localStorage.getItem("user_name"),
                "email": window.localStorage.getItem("user_email"),
                "contact": window.localStorage.getItem("user_phone")
        },
        "notes": {
            "address": ""
        },
        "theme": {
            "color": "#3399cc"
            }
        };
        var rzp = new Razorpay(options);

        rzp.open()

        rzp.on("payment.failed",function (response) {
            alert(response.error.reason);
        })
    }
}

function logout() {
    window.localStorage.clear();
    window.location.href = "/";
}

//search product
function searchProduct() {
    var search_data = $("#search-box").val()
    let model = "";
    if(search_data===""){
        $("#search-result").html("")
    }else {
        $.ajax({
        url: endpoint+"search-product",
        type: "POST",
        data: {"user_id": window.localStorage.getItem("user_id"),
            "search_query": search_data
        },
        beforeSend:function (xhr) {
            xhr.setRequestHeader("Authorization", window.localStorage.getItem("auth_token"))
        },
        timeout:3000,
        success:function (data) {
            let responsePayload = data["payload"]["product_name"]
            $("#search-result").html("");
            for (const responsePayloadKey in responsePayload) {
                model+='<div class="search-result-data" onclick="get_searched_product(this)" data="'+responsePayload[responsePayloadKey]+'"><i class="material-icons" style="color: aliceblue;">search</i><span style="color: aliceblue">'+responsePayload[responsePayloadKey]+'</span></div>';
            }
            $("#search-result").append(model)
            },
        error:function (error) {
            if(error.status === 401){
                alert("Your session is ended please relogin to continue.");
                window.localStorage.clear();
                window.location.href="/";
            }
        }
    })
    }
}


function addToCart(product_id) {
    $("#btn-add-to-cart").attr("disabled","disabled");
    $("#btn-cart-text").hide();
    $("#btn-cart-spinner").show();
    $.ajax({
        url:endpoint+"add-to-cart",
        type:"POST",
        data:{
            "user_id": window.localStorage.getItem("user_id"),
            "product_id": product_id
        },
        beforeSend : function (xhr) {
            xhr.setRequestHeader("Authorization", window.localStorage.getItem("auth_token"))
        },
        timeout:  3000,
        success: function (data) {
            if(data["payload"] === "success"){
                alert("product is add to cart successfully")
            }else {
                alert(data["error"])
            }
            $("#btn-cart-text").show();
            $("#btn-cart-spinner").hide();
            $("#btn-add-to-cart").removeAttr("disabled");

        },
        error : function (error) {
             if(error.status === 401){
                alert("Your session is ended please relogin to continue.");
                window.localStorage.clear();
                window.location.href="/";
            }else {
                 alert("please try again!")
                 $("#btn-cart-text").show();
                $("#btn-cart-spinner").hide();
                $("#btn-add-to-cart").removeAttr("disabled");
             }
        }
    })
}



function get_cart() {

     $.ajax({
        url: endpoint+"get-cart",
        type: "POST",
        data: {
            "user_id": window.localStorage.getItem("user_id"),
             "product_count": product_count,
            "prev_prod_count": prev_prod_count,
            "product_search_name":""
        },
        beforeSend:function (xhr) {
            xhr.setRequestHeader("Authorization", window.localStorage.getItem("auth_token"))
        },
        timeout:3000,
        success:function (data) {
            cartAdapter(data);
        },
        error:function (error) {
            if(error.status === 401){
                alert("Your session is ended please relogin to continue.");
                window.localStorage.clear();
                window.location.href="/";
            }
        }
    })

}

function cartAdapter(products){

    const prod_count = products["payload"]["product_count"]
    const product = products["payload"]["product"]

    for (const productElement in product) {

        const product_data = product[productElement];
        let product_rating = "";
        let product_stock = "";
        const rating = parseInt(product_data["product_ratings"])
        const stock = parseInt(product_data["product_stock"])
        if(stock>0){
            product_stock+='<p style="color:green;">In Stock</p>'
        }else {
            product_stock+='<p style="color:red;">Sold out</p>'

        }
        for(let i=0;i<rating;i++){
            product_rating+= '<i style="color: orange" class="material-icons">star</i>';
        }


        let modal = '<div class="col-md-4 d-flex justify-content-center" style="margin-top: 10px; margin-bottom: 10px;" >';
        modal+='<div class="card" style="width: 20rem;">';
        modal+='<img src="'+product_data["product_image"]+'" class="cardimg-top" alt="..." height="170" width="150">';
        modal+='<div class="card-body">';
        modal+='<h6 class="card-title">'+product_data["product_name"]+'</h6>';
        modal+='<div style="display: flex; justify-content: space-between"><span>&#x20b9;'+product_data["product_price"]+'</span> <span>'+product_rating+'</span> </div>';

        modal+='<div>'+product_stock+'</div>';
        const str_data = {
            "product_id": product_data["product_id"],
            "product_name": product_data["product_name"],
            "product_image": product_data["product_image"],
            "product_rating": product_data["product_ratings"],
            "product_price": product_data["product_price"],
            "product_stock": product_data["product_stock"]
        };

        const b64_data = btoa(JSON.stringify(str_data))

        //console.log()
        modal+='<form action="/product_detail" method="GET">';
        modal+='<input type="hidden" name="product_detail" value="'+b64_data+'" >';
        modal+='<a onclick="this.parentNode.submit();" class="btn btn-primary">View Product</a>';
        modal+='</form>';
        modal+='</div>';
        modal+='</div>';
        modal+='</div>';

        $("#product-container").append(modal);
    }


    $("#product-loader").hide();

}