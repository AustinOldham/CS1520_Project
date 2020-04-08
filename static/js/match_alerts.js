function saveAlerted() {
	//Stores a cookie that records which matches the user has been alerted about.
	//TODO: Overwrite the cookie with the current list of matches each time.
}

function alertUser() {
	//Alerts the user when a match is made.
	var newMatchedArray = getNewMatched();
	if (newMatchedArray.length === 0) {
		return false;
	}
	var alertText = "You have the following new matches:\n";
	alertText += newMatchedArray.join("\n");  //Adds each new match to the alert.
	alert(alertText);
	return true;
}

function getNewMatched() {
	//Returns a list of new matches.
	return getAllMatched();  //Placeholder
}

function getAllMatched() {
	//Returns a list of every match on the page.
	var elementArray = document.getElementsByClassName("matched");
	var matchedArray = new Array(elementArray.length);
	for (var i = 0; i < elementArray.length; i++) {
		matchedArray[i] = elementArray[0].innerText;
	}
	return matchedArray;
}

function getAllLiked() {
	//Returns a list of every liked user on the page that has not matched with the current user.
	var elementArray = document.getElementsByClassName("liked");
	var likedArray = new Array(elementArray.length);
	for (var i = 0; i < elementArray.length; i++) {
		likedArray[i] = elementArray[0].innerText;
	}
	return likedArray;
}

window.onload = function() {
	alertUser();
	saveAlerted();
}