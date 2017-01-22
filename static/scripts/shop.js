function ajax() {

    var i = document.getElementById("input").value;
    var input = { 'text' : i };
    
    var h = document.getElementById("h1");
    h.innerHTML = i;

    $.ajax({
	url: '/upcase',
	type: 'GET',
	data: input,
	success: function( d ) {
	    var h2 = document.getElementById("h2");
	    d = JSON.parse(d);
	    h2.innerHTML = d['result'];
	}

     });
    /*
    $.get("/upcase", input, function(d) {
	    var h2 = document.getElementById("h2");
	    d = JSON.parse(d);
	    h2.innerHTML = d['result'];	
    });
     */
};

document.getElementById("b").addEventListener( 'click', post );
