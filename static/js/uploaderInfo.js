function initChart(id,dates,infodata,videos){
    var mychart = echarts.init(document.getElementById(id));
    mychart.clear();
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
            data: dates.slice(1,)
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
    mychart.setOption(option);
}