function wishlist(x) {
console.log("asgnhjktdsgrr");
    var i = document.getElementsByClassName(x);
    var input = {'name' : i[0].innerHTML,
                 //'price' : i[1].innerHTML,
                 'link' : i[2].href,
                };
    if(document.getElementById("wish").innerHTML == "Remove From Wishlist"){
        input['task'] = 'remove';
    }else{
        input['task'] = 'add';
    }
    console.log(input);

    $.ajax({
	url: '/addtowish',
	type: 'GET',
	data: input,
	success: function( d ) {
        if(document.getElementById("wish").innerHTML == "Remove From Wishlist"){
            document.getElementById("wish").innerHTML = "Add to Wishlist";
        }else{
            document.getElementById("wish").innerHTML = "Remove From Wishlist";
        }
    }
    });
    /*
    $.get("/upcase", input, function(d) {
	    var h2 = document.getElementById("h2");
	    d = JSON.parse(d);
	    h2.innerHTML = d['result'];	
    });
     */
}

function shoppinglist(x) {

    var i = document.getElementsByClassName(x);
    var input = {'name' : i[0].innerHTML,
                 //'price' : i[1].innerHTML,
                 'link' : i[2].href,
                };
    if(document.getElementById("shop").innerHTML == "Remove From Shopping list"){
        input['task'] = 'remove';
    }else{
        input['task'] = 'add';
    }
    //console.log(input);

    $.ajax({
	url: '/addtoshopping',
	type: 'GET',
	data: input,
	success: function( d ) {
                if(document.getElementById("shop").innerHTML == "Remove From Shopping list"){
            document.getElementById("shop").innerHTML = "Add to Shopping list";
        }else{
            document.getElementById("shop").innerHTML = "Remove From Shopping list";
        }
    }
    });
    /*
    $.get("/upcase", input, function(d) {
	    var h2 = document.getElementById("h2");
	    d = JSON.parse(d);
	    h2.innerHTML = d['result'];	
    });
     */
}


