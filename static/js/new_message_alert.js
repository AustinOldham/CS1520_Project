function check_for_new_messages() {
    console.log("running new messages check");
	$.ajax({url: "/countMessages", success: function(result){
        console.log(result);
        var num_messages = parseInt(result);
        var new_messages = num_messages - load_current_message_count();
        console.log(new_messages);
        if(new_messages > 0){
            alert("You have " + new_messages + " new message(s)");
            color_matches_link();
        }
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

function color_matches_link(){
    var matches_link = document.getElementById("my-matches-link");
    matches_link.style.color = "yellow";
}

window.onload = function() {
    check_for_new_messages();
}