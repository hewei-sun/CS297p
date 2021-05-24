function upMenu(id){
    var ups=[];
    var ids=[];
    $.ajax({
        type : "post",
        async : false, 
        url : "/upMenu",
        data : {},
        dataType : "json", 
        success : function(result) {
            if (result) {
                //console.log(result);
                //console.log(result["uplist"]);
                for(var i=0;i<result["uplist"].length;i++){
                    ids.push(result["uplist"][i][0]);
                    ups.push(result["uplist"][i][1]);
                }
            }

        }
    })
    //console.log(ups);
    var menu = document.getElementById(id);
    for (let i = 0; i < ups.length; i++) {
        var str= ups[i]+" "+ids[i];
        //console.log(str);
        menu.add(new Option(str, ids[i]));
    }
}

function videoMenu(id){
    var ups=[];
    var ids=[];
    $.ajax({
        type : "post",
        async : false, 
        url : "/viMenu",
        data : {},
        dataType : "json", 
        success : function(result) {
            if (result) {
                //console.log(result);
                //console.log(result["uplist"]);
                for(var i=0;i<result["vlist"].length;i++){
                    for (var j=0;j<result["vlist"][i].length;j++){
                        ids.push(result["vlist"][i][j][0]);
                        ups.push(result["vlist"][i][j][1]);
                    }
                }
            }
        }
    })
    //console.log(ups);
    var menu = document.getElementById(id);
    for (let i = 0; i < ups.length; i++) {
        var str= ups[i];
        //console.log(str);
        menu.add(new Option(str, ids[i]));
    }
}

function rankMenu(field){
    var fields=[];
    $.ajax({
        type : "post",
        async : false, 
        url : "/rankM",
        data : {},
        dataType : "json", 
        success : function(result) {
            if (result) {
                //console.log(result);
                console.log(result["field"]);
                for(var i=0;i<result["field"].length;i++){
                    fields.push(result["field"][i]);
                }
            }
        }
    })
    //console.log(ups);
    var menu = document.getElementById(field);
    for (let i = 0; i < fields.length; i++) {
        //var str= ups[i];
        //console.log(str);
        menu.add(new Option(fields[i], "RANK"+fields[i]));
    }
}