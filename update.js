var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById('uptime').innerHTML = this.responseText
    }
};
xhttp.open('GET', '/uptime', true);
xhttp.send();
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById('memory_usage').innerHTML = this.responseText
    }
};
xhttp.open('GET', '/memory_usage', true);
xhttp.send();
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById('visitors').innerHTML = this.responseText
    }
};
xhttp.open('GET', '/visitors', true);
xhttp.send();
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById('temperature').innerHTML = this.responseText
    }
};
xhttp.open('GET', '/temperature', true);
xhttp.send();
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById('temperature_celsius').innerHTML = this.responseText
    }
};
xhttp.open('GET', '/temperature_celsius', true);
xhttp.send();
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById('humidity').innerHTML = this.responseText
    }
};
xhttp.open('GET', '/humidity', true);
xhttp.send();
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById('pressure').innerHTML = this.responseText
    }
};
xhttp.open('GET', '/pressure', true);
xhttp.send();
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
        document.getElementById('altitude').innerHTML = this.responseText
    }
};
xhttp.open('GET', '/altitude', true);
xhttp.send();
setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('uptime').innerHTML = this.responseText
        }
    };
    xhttp.open('GET', '/uptime', true);
    xhttp.send()
}, 60000);
setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('memory_usage').innerHTML = this.responseText
        }
    };
    xhttp.open('GET', '/memory_usage', true);
    xhttp.send()
}, 60000);
setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('temperature').innerHTML = this.responseText
        }
    };
    xhttp.open('GET', '/temperature', true);
    xhttp.send()
}, 60000);
setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('humidity').innerHTML = this.responseText
        }
    };
    xhttp.open('GET', '/humidity', true);
    xhttp.send()
}, 60000);
setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('temperature_celsius').innerHTML = this.responseText
        }
    };
    xhttp.open('GET', '/temperature_celsius', true);
    xhttp.send()
}, 60000);
setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('pressure').innerHTML = this.responseText
        }
    };
    xhttp.open('GET', '/pressure', true);
    xhttp.send()
}, 60000);
setInterval(function() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById('altitude').innerHTML = this.responseText
        }
    };
    xhttp.open('GET', '/altitude', true);
    xhttp.send()
}, 60000);
