/* helper functions */


function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

    document.body.appendChild(form);
    form.submit();
}

function postByIds(path, ids) {
    var params = {};
    for (var i=0; i<ids.length; ++i) {
        id = ids[i];
        params[id] = document.getElementById(id).value;
    }
    post(path, params, "post");
}

function postCheckByIds(path, ids) {
    var params = {};
    for (var i=0; i<ids.length; ++i) {
        id = ids[i];
        console.log(id);
        params[id] = document.getElementById(id).checked;
    }
    post(path, params, "post");
}

function postUserProfile() {
    var email = document.getElementById('emailaddr').value;
    var name = document.getElementById('employeename').value;
    var phone = document.getElementById('phonenum').value;
    var userProfile = {};

    if (!email){
        alert("请填写公司邮箱！(Email address is required!)");
        return;
    } else if (email.trim().toLowerCase().split('@')[1] != 'lfmail.net') {
        alert("请使用公司邮箱注册！(LF business email only!)");
        return;
    }

    if (!name) {
        alert("请填写姓名！(Your name is required!)");
        return;
    }

    if (!phone) {
        alert("请填写手机号码！(Mobile phone is required!)");
        return;
    }

    userProfile['email'] = email;
    userProfile['name'] = name;
    userProfile['phone'] = phone;

    post('/user-register', userProfile);
}

function untoggleSidebarItems() {
    $('.active').removeClass('active');
}

function getCountries() {
    var e = document.getElementById("townname");
    var tn = e.options[e.selectedIndex].value;
    $("#countryname").empty();
    $.get( "/q/countries", { towninfo: tn } )
     .done(function( data ) {
         $("#countryname").append($('<option>', {value: '', text: '请选择'}));
        for (var i = 0; i < data.data.length; i++) {
            var d = data.data[i];
            $("#countryname").append($('<option>',
                {value: d.cn + ';' + d.cc + ';' + d.ti + ';' + d.cid,
                 text: d.cn}));
        }
     });
}

function getTerminals() {
    var e = document.getElementById("countryname");
    var cn = e.options[e.selectedIndex].value;
    $("#devno").empty();
    $("#devno").append($('<option>',
        {value: '',
         text: '请选择'}));
    $.get( "/q/terminals", { countryinfo: cn } )
     .done(function( data ) {
        for (var i = 0; i < data.data.length; i++) {
            var d = data.data[i];
            $("#devno").append($('<option>',
                {value: d.tn + ';' + d.tc + ';' + d.ci + ';' + d.cid,
                 text: d.tn+d.tc}));
        }
     });
}

function getGeoTree(cb) {
    $.get("/q/geotree")
    .done( function( data ) {
        cb(data);
    });
}
