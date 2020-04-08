function saveAlerted() {
	//Stores a cookie that records which matches the user has been alerted about.
	var matchedArray = getAllMatched();
	var cookieString = "previouslyAlerted=";
	cookieString += JSON.stringify(matchedArray);

	cookieString += "; expires=";
	var date = new Date();
	date.setDate(date.getDate() + 30);  //Sets an expiration date 30 days from creation.
	var dateString = date.toUTCString();
	cookieString += dateString;

	document.cookie = cookieString;
}

function loadAlerted() {
	//Loads the cookie that stores the previously alerted users and returns it as an array.
	var cookiesList = document.cookie.split(";");
	var alertedArray = [];
	for (i = 0; i < cookiesList.length; i++) {
		if (cookiesList[i].indexOf("previouslyAlerted") === 0) {
			var alertedString = cookiesList[i].split("=")[1];
			alertedArray = JSON.parse(alertedString);
			break;
		}
	}
	return alertedArray;
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
	var matchedArray = getAllMatched();
	var alertedArray = loadAlerted();
	var newMatchedArray = matchedArray.filter(n => !alertedArray.includes(n));  //Removes all of the users in alertedArray from matchedArray.
	return newMatchedArray;
}

function getAllMatched() {
	//Returns a list of every match on the page.
	var elementArray = document.getElementsByClassName("matched");
	var matchedArray = new Array(elementArray.length);
	for (var i = 0; i < elementArray.length; i++) {
		matchedArray[i] = elementArray[i].innerText;
	}
	return matchedArray;
}

function getAllLiked() {
	//Returns a list of every liked user on the page that has not matched with the current user.
	var elementArray = document.getElementsByClassName("liked");
	var likedArray = new Array(elementArray.length);
	for (var i = 0; i < elementArray.length; i++) {
		likedArray[i] = elementArray[i].innerText;
	}
	return likedArray;
}

window.onload = function() {
	alertUser();
	saveAlerted();
}