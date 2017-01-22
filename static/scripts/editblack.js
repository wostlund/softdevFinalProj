function ajax() {
//taken from Mr. DW's tutorial
    var i = document.getElementById("textbox")
    var input = { 'edited-blacklist' : i };


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

