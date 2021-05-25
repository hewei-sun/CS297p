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

function addList(vList,page,fields){
    //page start at 0
    var strf = "";
    //log(vList.length);
    var total = (vList.length-1)/10+1;
    //console.log(total);
    strf="<center>";
    $("#table").append(strf);
    for(var i =1;i<=total;i++){
        strf = "<button type=\"button\" class=\"btn btn-default\"  style=\"width:80px;height:50px\" onclick=\"javascript:self.location='/videoRank/"+fields+"/"+i+"'\">"+i+"</button>";
        $("#table").append(strf);
    }
    strf="</center>";
    $("#table").append(strf);
    //for(var j = 0;j<vList.length;j++){
    for(var j = (page-1)*10;j<page*10;j++){
        var k = j+1;
        strf = "<tr><td>"+vList[j][0]+"</td><td><a href=\"javascript:self.location='/videoA/"+vList[j][2]+"'\"  style='color:black;'>"+vList[j][1]+"</a></td><td>"+vList[j][3]+"</td><td>"+vList[j][4]+"</td><td><a href=\"javascript:self.location='/uploaderA/"+vList[j][6]+"'\"  style='color:black;'>"+vList[j][5]+"</a></td><td><a href=\"javascript:self.location='/videoA/"+vList[j][2]+"'\"><img src='/static/videoFaces/"+vList[j][2]+".png' width=\"150\" height=\"100\" alt=\"no such image\"/></a></td></tr>";
        $("#col").append(strf);
    }
}

function upButton(uplist,page){
    var strf = "";
    var total = (uplist.length-1)/10+1;
    strf="<center>";
    $("#button").append(strf);
    for(var i =1;i<=total;i++){
        strf = "<button type=\"button\" class=\"btn btn-default\"  style=\"width:80px;height:50px\" onclick=\"javascript:self.location='/uploaderRanking/"+i+"'\">"+i+"</button>";
        $("#button").append(strf);
    }
    strf="</center>";
    $("#button").append(strf);
    for (var i = (page-1)*10;i<page*10; i++) {
        var strUp = "<tr><td>"+uplist[i][0]+"</td><td><a href=\"javascript:self.location='/uploaderA/"+uplist[i][1]+"'\"  style='color:black;'>" +uplist[i][2].toString() + "</a></td><td>"+uplist[i][3].toString()+ "</td><td><a href=\"javascript:self.location='/uploaderA/"+uplist[i][1]+"'\"><img src='/static/upFaces/"+uplist[i][1]+".png' width=\"100\" height=\"100\" alt=\"no such image\"/></a></td><td>"+uplist[i][5]+ "</td><td>"+uplist[i][6]+ "</td><td>"+uplist[i][7]+ "</td><td>"+uplist[i][8]+ "</td><td>"+uplist[i][9]+ "</td><td>"+uplist[i][10]+ "</td><td>"+uplist[i][11]+ "</td><td>"+uplist[i][12]+ "</td><td>"+uplist[i][13]+"</td></tr>";
                //console.log(strUp)
        $("#tab").append(strUp);
    }
}