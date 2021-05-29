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

    for(var i =1;i<=total;i++){
        strf = "<button type=\"button\" class=\"btn btn-default\"  style=\"width:80px;height:50px\" onclick=\"javascript:self.location='/videoRank/"+fields+"/"+i+"'\">"+i+"</button>";
        $("#button").append(strf);
    }

    //for(var j = 0;j<vList.length;j++){
    for(var j = (page-1)*10;j<page*10;j++){
        var k = j+1;
        strf = "<tr><td><h2>"+vList[j][0]+"</h2></td><td>&nbsp&nbsp&nbsp&nbsp</td><td><a href=\"javascript:self.location='/videoA/"+vList[j][2]+"'\"><img src='/static/cvideoFaces/"+vList[j][2]+".png' width=\"180\" height=\"120\" alt=\"no such image\"/></a></td><td>&nbsp&nbsp&nbsp&nbsp</td><td><table><tr><td><a href=\"javascript:self.location='/videoA/"+vList[j][2]+"'\"  style='color:black;'><h3>"+vList[j][1]+"</h3></a></td></tr><tr><td><a href=\"javascript:self.location='/uploaderA/"+vList[j][6]+"'\"  style='color:black;'>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+vList[j][5]+"</a></td></tr><tr><td><table><tr><td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbspPlay:\t"+vList[j][3]+"\t</td><td>&nbsp</td><td>\tLive Comments:\t"+vList[j][4]+"</td></tr></table></td></tr></table></td></tr><tr><td>&nbsp</td></tr>";
        $("#col").append(strf);
    }
}

function upButton(uplist,page){
    var strf = "";
    var total = (uplist.length-1)/10+1;

    for(var i =1;i<=total;i++){
        strf = "<button type=\"button\" class=\"btn btn-default\"  style=\"width:80px;height:50px\" onclick=\"javascript:self.location='/uploaderRanking/"+i+"'\">"+i+"</button>";
        $("#button").append(strf);
    }

    for (var i = (page-1)*10;i<page*10; i++) {
        var strUp = "<tr><td><h2>"+uplist[i][0]+"</h2></td><td>&nbsp&nbsp</td><td><a href=\"javascript:self.location='/uploaderA/"+uplist[i][1]+"'\"><img src='/static/cupFaces/"+uplist[i][1]+".png' width=\"200\" height=\"200\" alt=\"no such image\"/></a></td><td>&nbsp&nbsp</td><td><table><tr><td><h3><a href=\"javascript:self.location='/uploaderA/"+uplist[i][1]+"'\"  style='color:black;'>" +uplist[i][2].toString() + "</a></h3></td></tr><tr><td><table><tr><td>"+uplist[i][3].toString()+ "</td><td>&nbsp</td><td>Level:\t"+uplist[i][10]+ "</td></tr><tr><td>Follower:\t"+uplist[i][7]+ "</td><td>&nbsp</td><td>Following:\t"+uplist[i][8]+ "</td></tr><tr><td>Like:\t"+uplist[i][12]+ "</td><td>&nbsp</td><td>View:\t"+uplist[i][13]+"</td></tr></table></td></tr><tr><td>Official:\t"+uplist[i][11]+ "</td></tr><tr><td>Bio:\t"+uplist[i][9]+ "</td></tr></table></td></tr><tr><td>&nbsp</td></tr>";
        //console.log(strUp)
        $("#tab").append(strUp);
    }
}