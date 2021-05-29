function basicShow(info){
    var tags="";
    for(var i=0;i<info["tags"].length;i++){
        tags=tags+info["tags"][i]+",\t";
    }
    var rank = info["rank"];
    if(rank!=""){
        rank=rank.slice(8,9);
    }
    var strf="<table><tr><td><table><tr><td><img src='/static/cvideoFaces/"+info["bvid"]+".png' width=\"300\" height=\"200\" alt=\"no such image\"/></td><td>&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</td><td><table><tr><td><h3>"+info["title"]+"</h3></td></tr><tr><td><a href=\"javascript:self.location='/uploaderA/"+info["up_id"]+"'\"  style='color:black;'>"+info["up_name"]+"</a></td></tr><tr><td>&nbsp</td><tr><tr><td>Highest rank at the whole site:"+rank+"</td></tr><tr><td>Released at "+info["publish_time"]+"</td></tr><tr><td><table><tr><td>Play:\t"+info["play"]+"</td><td>&nbsp</td><td>Live Comments:"+info["view"]+"</td></tr><tr><td>Coin:"+info["coin"]+"</td><td>&nbsp</td><td>Like:"+info["like"]+"</td></tr><tr><td>Collect:"+info["collect"]+"</td><td>&nbsp</td><td>Share:"+info["share"]+"</td></tr></table></td></tr></table></td></tr></table></td></tr><tr><td>&nbsp</td><tr><tr><td><p>"+info["description"]+"</p></td></tr><tr><td><h5>"+tags+"</h5></td></tr></table>";
    $("#video").append(strf);
}

function wordCloud(){}

function wordClouda(){}