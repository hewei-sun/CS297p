function initChart(id,dates,infodata,videos){
    
    //console.log(infodata[0]);
    //console.log(infodata);
    var serie=[];
    for(var i=0;i<videos.length;i++){
        serie.push({
            name:videos[i][0],
            type:'line',
            markLine: {
                silent: false,
                lineStyle:{
                    type:"solid",
                    color:"	#000080"
                },
                data: [{
                    xAxis: videos[i][1]
                }],
                label: {
                    normal: {
                        formatter: videos[i][0]
                    }
                }
            }
        });
    }
    /*
    if(id=="Rank"||id=="Following"){
        serie.push({
            name:id,
            type:'line',
            data:infodata.slice(1,)
        })
    }else{
        var datas=[];
        for(var i=0;i<infodata.length-1;i++){
            datas.push(infodata[i+1]-infodata[i]);
        }
        serie.push({
            name:id,
            type:'line',
            data:datas
        })
    }
    */
    serie.push({
        name:id,
        type:'line',
        data:infodata
    });
    if(id=="Rank"){
        var count=0;
        for(var i=0;i<infodata.length;i++){
            if(infodata[i]==0){
                infodata[i]=101;
                i++;
            }
        }
        if (count ==infodata.length){
            var str="<h5>no rank data for this up due to he/she/they never reached Top 100</h5>";
            $("#Rank").append(str);
            return;
        }
        var str="<h5>all data ranks greater than 100 will be shown as 101</h5>";
        $("#Rank").append(str);
    }
    
    
    var option = {
        tooltip: {
            show:true,
            trigger: 'axis'
        },
        legend: {
            data:id
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            feature: {
                mark : {show: true},
                dataView : {show: true, readOnly: false},
                magicType : {show: true, type: ['line', 'bar']},
                restore : {show: true},
                saveAsImage : {show: true}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: dates
        },
        yAxis: {
            min: 'dataMin',
            type: 'value',
            axisLabel : {
                formatter: '{value}'
            }
        },
        series : serie
    };
    var mychart = echarts.init(document.getElementById(id));
    mychart.clear();
    mychart.setOption(option);
}