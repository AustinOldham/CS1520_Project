function edit_profile(myusername) {
	$.ajax({url: "/likeuser/" + other_username, success: function(result){
		if (result == 'success') {
			$("#like_unlike_button").text("Unlike");
			$("#like_unlike_button").attr("onclick", "unlike_js(\"" + other_username + "\")")
			$("#like_unlike_button").attr("class", "btn btn-warning")
		}
	}});
}