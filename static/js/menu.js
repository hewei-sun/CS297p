function upMenu(id){
    var ups=[],ids=[];
    console.log("dshfk");
    $.ajax({
        type : "post",
        async : false, 
        url : "/upMenu",
        data : {},
        dataType : "json", 
        success : function(result) {
            if (result) {
                console.log(result);
                for(var i=0;i<result.length;i++){
                    ups.push(result[i][0]);
                    ids.push(result[i][1]);
                }
            }

        }
    })
    console.log("dshfk");
    var menu = document.getElementById(id);
    for (let i = 0; i < ups.length; i++) {
        var str= ups[i]+" "+ids[i];
        console.log(str);
        menu.add(new Option(str, ids[i]));
    }
}