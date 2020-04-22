function check_for_new_messages() {
    console.log("running new messages check");
	$.ajax({url: "/countMessages", success: function(result){
        console.log(result);
        var num_messages = parseInt(result);
        var new_messages = num_messages - load_current_message_count();
        console.log(new_messages);
        alert("You have " + new_messages + " new messages");
        store_new_message_count(result);
	}});
}

function load_current_message_count(){
    console.log(document.cookie);
    return parseInt(document.cookie);
}

function store_new_message_count(num){
    var cookieString = num.toString();
    document.cookie = cookieString;
}

window.onload = function() {
    check_for_new_messages();
}