function SEND() {
    var NameElement = document.getElementById("addname");
    var name = NameElement.value;
    NameElement.value = "";
    var toSend = JSON.stringify({ "name": name });
    ajaxPostRequest("/send", toSend, callb);
}

function ajaxPostRequest(path, data, callback) {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
            callback(this.response);
        }
    };
    request.open("POST", path);
    if (data == "")
        request.send();
    else request.send(data)
}

function drawPeoples(response) {
    var people = JSON.parse(response);
    var code = "";
    for (var p of people) {
        var container =
            "<a href=\"People?" + p[1].toLowerCase() + "\" class=\"row \"><div class=\"MyContainer\"><div class=\"row\">" +
            "<div class=\"col-three\">" + " <img width=\"100\" height=\"100\" src=\"https://scholar.google.com/citations?view_op=view_photo&user=" + p[0] + "\" alt=\"\">" +
            "</div><div class=\"col-eight\"><h3>" + p[1] + "</h3><h4>" +
            p[2] + "</h4></div></div></div></a>";
        code += container;
    }
    document.getElementById("people_list").innerHTML = code;
}



function callb() {

}

function LoadPage() {

    ajaxPostRequest("/peoples", "", drawPeoples);
}