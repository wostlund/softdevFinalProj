function wishlist(x) {

    var i = document.getElementsByClassName(x);
    var input = {'name' : i[0].innerHTML,
                 'price' : i[1].innerHTML,
                 'link' : i[2].href,
                 'submit' : 'wishlist'
                };
    console.log(input['price']);

    $.ajax({
	url: '/dashboard',
	type: 'POST',
	data: input,
	success: function( d ) {
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
                 'price' : i[1].innerHTML,
                 'link' : i[2].href,
                 'submit' : 'shoppinglist'
                };
    

    $.ajax({
	url: '/dashboard',
	type: 'POST',
	data: input,
	success: function( d ) {
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


