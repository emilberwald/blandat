var keyNames = ["E", "F", "F♯/G♭", "G", "G♯/A♭", "A", "A♯/B♭", "B", "C", "C♯/D♭", "D", "D♯/E♭"];
var intervalNames = ["1", "♭2", "2", "♭3", "3", "4", "♯4", "5", "♯5", "6", "♭7", "7"];
var tunings = {
    EADGBE_hightolow: [24, 19, 15, 10, 5, 0]
};
window.onload = function () {
    for (var i = 0; i < 12; i++) {
        document.getElementById("optiontitles").innerHTML += '<th>' + i.toString() + '<br/>' + intervalNames[i] + '</th>';
        document.getElementById("visible").innerHTML += '<td><input type="checkbox" id="visible' + i.toString() + '" interval="' + i.toString() + '" checked="checked" onchange="drawintervals()"/></td>';
    }
    var tuning = document.getElementById("tuning");
    for (var i = 0; i < 6; i++) {
        tuning.innerHTML += '<td><select id="key' + i.toString() + '" onchange="drawintervals()">';

        var key = document.getElementById("key" + i.toString());
        for (var j = 0; j < 12; j++) {
            var innerhtml = '<option value="' + j.toString() + '" ';
            if (j == (tunings.EADGBE_hightolow[i] % 12)) {
                innerhtml += 'selected="selected"';
            }
            innerhtml += '>' + keyNames[j].toString() + '</option>';
            key.innerHTML += innerhtml;
        }
        tuning.innerHTML += '</select></td>';
    }
    tuning.innerHTML += '<td><button onclick="offsettune(1); return false;"><</button><button onclick="offsettune(-1); return false;">></button></td>';

    var rootoption = document.getElementById("rootoption");
    rootoption.innerHTML += '<td><select id="root" onchange="drawintervals()">';
    for (var j = 0; j < 12; j++) {
        document.getElementById("root").innerHTML += '<option value="' + j.toString() + '">' + keyNames[j].toString() + '</option>';
    }
    rootoption.innerHTML += '</select></td>';
    rootoption.innerHTML += '<td><button onclick="offsetroot(-1); return false;"><</button><button onclick="offsetroot(1); return false;">></button></td>';

    drawintervals();
};
function offsetroot(delta) {
    var elem = document.getElementById("root");
    var val = (elem.selectedIndex + delta) % 12;
    while (val < 0)
        val += 12;
    elem.selectedIndex = val;
    drawintervals();
}
function offsettune(delta) {
    for (var i = 0; i < 6; i++) {
        var elem = document.getElementById("key" + i.toString());
        var val = (elem.selectedIndex + delta) % 12;
        while (val < 0)
            val += 12;
        elem.selectedIndex = val;
    }
    drawintervals();
}
function drawintervals() {
    var container = document.getElementById("container");
    var nOctaves = 3;
    var html = '<div class="topRow" style="height:30px">';
    for (var j = 0; j < nOctaves * 12; j++) {
        var dot = "";
        if (j % 12 == 3 || j % 12 == 5 || j % 12 == 7 || j % 12 == 9)
            dot = "•";
        if (j >= 12 && j % 12 == 0)
            dot = "••";
        html += '<div class="index"><span>' + j.toString() + '<br/>' + dot + '</span></div>';
    }
    html += '</div>';
    container.innerHTML = html;
    for (var i = 0; i < 6; i++) {
        var key = document.getElementById("key" + i.toString()).selectedIndex;
        var rootKeyOffset = document.getElementById("root").selectedIndex;
        var ID = "row" + i.toString();
        container.innerHTML += intervalRowHTML("intervalRow", key, rootKeyOffset, ID);
        var elem = document.getElementById(ID);
        if (elem) {
            IntervalView(elem);
        }
    }
    var html = '<div class="bottomRow" style="height:30px">';
    for (var j = 0; j < nOctaves * 12; j++) {
        var dot = "";
        if (j % 12 == 3 || j % 12 == 5 || j % 12 == 7 || j % 12 == 9)
            dot = "•";
        if (j >= 12 && j % 12 == 0)
            dot = "••";
        html += '<div class="index"><span>' + dot + '<br/>' + j.toString() + '</span></div>';
    }
    html += '</div>';
    container.innerHTML += html;
    function IntervalView(element) {
        var key = Number(element.getAttribute("key"));
        var rootKeyOffset = Number(element.getAttribute("root"));

        var innerHTML = InnerHTML(rootKeyOffset);
        element.innerHTML = "";
        for (var i = 0; i < nOctaves; i++) {
            for (var j = 0; j < 12; j++) {
                element.innerHTML += innerHTML[(j + Math.ceil(key)) % 12];
            }
        }
    }
    function intervalRowHTML(cssClass, key, rootKeyOffset, id) {
        return '<div class="' + cssClass + '" key="' + key + '" root="' + rootKeyOffset + '" id="' + id + '"></div>';
    }
    function InnerHTML(rootKeyOffset) {
        var innerHTML = [];
        for (var i = 0; i < 12; i++) {
            var interval = (i - rootKeyOffset) % 12;
            while (interval < 0)
                interval += 12;
            var visible = document.getElementById("visible" + interval.toString()).checked ? "visible" : "hidden";
            innerHTML[i] = '<div class="key ' + visible + '">' + (intervalNames[interval]) + '<br/><span>' + keyNames[i] + '</span></div>';
        }
        return innerHTML;
    }
}
