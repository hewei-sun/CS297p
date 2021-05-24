function videoRef(field){
    var video=[];
    var title = document.getElementById("col");
    for (var i = title.childNodes.length-1;i>=0;i--){
        //console.log(title.childNodes[i]);
        title.remove(title.childNodes[i]);
    }
    alert("This would take a few minutes...")
    $.ajax({
        type : "post",
        async : false, 
        url : "/reVideoRank/"+field,
        data : {},
        dataType : "json", 
        timeout: 0,
        success : function(result) {
            if (result) {
                //console.log(result);
                //console.log(result["videos"]);
                //for(var i=0;i<result["videos"].length;i++){
                for(var i=0;i<5;i++){
                    video.push(result["videos"][i]);
                }
            }

        }
    })
    //console.log(video);
    addList(video);
    alert("finished!")
}

function addList(vList){
    var strf = "";
    for(var j = 0;j<vList.length;j++){
    //for(var j = 0;j<5;j++){
        var k = j+1;
        strf = "<tr><td>"+vList[j][0]+"</td><td><a href=\"javascript:self.location='videoA/"+vList[j][2]+"'\"  style='color:black;'>"+vList[j][1]+"</a></td><td>"+vList[j][3]+"</td><td>"+vList[j][4]+"</td><td><a href=\"javascript:self.location='uploaderA/"+vList[j][6]+"'\"  style='color:black;'>"+vList[j][5]+"</a></td><td><a href=\"javascript:self.location='videoA/"+vList[j][2]+"'\"><img src='/static/videoFaces/"+vList[j][2]+".png' width=\"150\" height=\"100\" alt=\"no such image\"/></a></td></tr>";
        $("#col").append(strf);
    }
}