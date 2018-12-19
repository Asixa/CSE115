peopledata = {}

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

function Draw(response) {
    peopledata = JSON.parse(response);
    DrawDonut();
    DrawChart();
    DrawWordCloud();
    DrawElenment();
}

function DrawElenment() {
    document.title = peopledata['author']['name'];
    document.getElementById("My_Name").innerHTML = peopledata['author']['name'];
    document.getElementById("My_Citation").innerHTML = peopledata['author']['citedby'];
    document.getElementById("My_Hidex").innerHTML = peopledata['author']['hindex'];
    document.getElementById("My_i10").innerHTML = peopledata['author']['i10index'];
    document.getElementById("My_PubCount").innerHTML = peopledata['author']['publictaion_count'];
    document.getElementById("My_affiliation").innerHTML = peopledata['author']['affiliation'];
    document.getElementById("My_Icon").src = "https://scholar.google.com/citations?view_op=view_photo&user=" + peopledata['author']['id'];
    document.getElementById("My_table").innerHTML += "<tbody>";
    for (var i of peopledata['publication'])
        document.getElementById("My_table").innerHTML += "<tr><td>" + i[0] + "</td><td>" + i[1] + "</td><td>" + i[2] + "</td></tr>";
    document.getElementById("My_table").innerHTML += "</tbody>";

}

function LoadPage() {
    ajaxPostRequest("/getinfo", window.location.href.split('?')[1], Draw);
    Plotly.setPlotConfig({
        mapboxAccessToken: 'pk.eyJ1IjoiZXRwaW5hcmQiLCJhIjoiY2luMHIzdHE0MGFxNXVubTRxczZ2YmUxaCJ9.hwWZful0U2CQxit4ItNsiQ'
    });

}


function DrawChart() {
    var x = [];
    var y = [];
    for (var i in peopledata['author']['cites_per_year']) {
        x.push(i);
        y.push(Number(peopledata['author']['cites_per_year'][i]))
    }
    var data = [{
        x: x,
        y: y,
        type: 'bar'
    }];
    Plotly.newPlot('chart', data);
}

function DrawDonut() {
    var len = 25
    var labels = [];
    var values = [];

    for (var i in peopledata['publisher']) {
        labels.push(i.length < len ? i : i.substring(0, len) + "...");
        values.push(Number(peopledata['publisher'][i]) + 1)
    }

    var data = [{
        values: values,
        labels: labels,
        domain: { column: 0 },
        name: 'GHG Emissions',
        hoverinfo: 'label+percent',
        hole: .4,
        type: 'pie'
    }];

    var layout = [{
        annotations: [{
            font: {
                size: 20
            },
            showarrow: false,
            text: '',
            x: 0.17,
            y: 0.5
        }],
        height: 400,
        width: '100%',
        showlegend: false,
        grid: { rows: 2, columns: 2 }
    }];

    Plotly.newPlot('donat', data, layout);
}


function DrawWordCloud() {
    WordCloud(document.getElementById('word_canvas'), {
        list: peopledata['words']
    });
}