function getDateString(date){
    return (date.getMonth()+1)+'/'+date.getDate()+'/'+date.getFullYear();
}

function getTimeString(date){
    var time_str = '';
    time_str += date.getHours() + ':';
    if(date.getMinutes() > 10){
        time_str += date.getMinutes();
    }else{
        time_str += '0' + date.getMinutes();
    }
    return time_str;
}

//populate messages using JS
function populateMessageList(){
    console.log("populateMessageList executing");

    var ul = document.getElementById("list");

    var messages = {{ messages | tojson }};
    var curr_date = "";
    for(var i=0;i<messages.length;i++){
        var li = document.createElement("li");
        console.log("messages[i] = " + messages[i]);
        var obj = JSON.parse(messages[i]);

        //var message_date = UTCToLocalDate(new Date(parseInt(obj.time))); //convert date to local timezone for display
        var message_date = new Date(parseInt(obj.time));
        console.log(message_date.getTime());

        if(curr_date != getDateString(message_date)){
            curr_date = getDateString(message_date);
            var date_break = document.createElement("li");
            date_break.appendChild(document.createTextNode(curr_date));
            date_break.style.cssText = 'text-align:center;';
            ul.appendChild(date_break);
            ul.appendChild(document.createElement("br"));
        }

        var time_str = getTimeString(message_date);
        if(obj.from_user == '{{current_user}}'){
            li.innerHTML = "<span style=\"color:blue\">" + time_str + ' ' + obj.from_user + "</span> " + obj.message;
        }else{				
            li.innerHTML = "<span style=\"color:red\">" + time_str + ' ' + obj.from_user + "</span> " + obj.message;
        }

        //li.classList.add("pull-left");
        ul.appendChild(li);
        ul.appendChild(document.createElement("br"));
    }

    ul.scrollTop = ul.scrollHeight;
}
window.onload = populateMessageList;