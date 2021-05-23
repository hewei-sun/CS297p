function videoRef(field){
    var video=[];
    $.ajax({
        type : "post",
        async : false, 
        url : "/reVideoRank/"+field,
        data : {},
        dataType : "json", 
        success : function(result) {
            if (result) {
                console.log(result);
                console.log(result["videos"]);
            }

        }
    })
}