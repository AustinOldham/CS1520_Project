function like_js(other_username) {
	$.ajax({url: "/likeuser/" + other_username, success: function(result){
		if (result == 'success') {
			$("#like_unlike_button").text("Unlike");
			$("#like_unlike_button").attr("onclick", "unlike_js(\"" + other_username + "\")")
			$("#like_unlike_button").attr("class", "btn btn-warning")
		}
	}});
}

function unlike_js(other_username) {
	$.ajax({url: "/unlikeuser/" + other_username, success: function(result){
		if (result == 'success') {
			$("#like_unlike_button").text("Like");
			$("#like_unlike_button").attr("onclick", "like_js(\"" + other_username + "\")")
			$("#like_unlike_button").attr("class", "btn btn-primary")
		}
	}});
}