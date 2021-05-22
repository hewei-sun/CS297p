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