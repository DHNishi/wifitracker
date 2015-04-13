/**
 * Created by dhnishi on 4/13/15.
 */

window.onload = function() {
    var button = document.getElementById('filterButton');
    button.onclick = function() {
        var ssid = document.getElementById('ssidSelect').value;
        var mac = document.getElementById('macSelect').value;
        console.log(ssid, mac);

        var url= "/densityGraph?";
        if (ssid !== "") {
            url += "ssid=" + ssid + "&";
        }
        if (mac !== "") {
            url += "mac=" + mac;
        }
        location.href = url;
    }
};
