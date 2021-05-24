function initChart(id,infodata){
    var mychart = echarts.init(document.getElementById(id));
    console.log(infodata[0]);
    console.log(infodata);
    var option = {
        tooltip: {
            show:true,
            trigger: 'axis'
        },
        legend: {
            data:['Following','Follower','Like','View','Rank']
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
            data: infodata[0]
        },
        yAxis: {
            type: 'value',
            axisLabel : {
                formatter: '{value}'
            }
        },
        series : [
            {
                name:'Following',
                type:'line',
                data:infodata[1]
            },
            {
                name:'Follower',
                type:'line',
                data:infodata[2]
            },
            {
                name:'Like',
                type:'line',
                data:infodata[3]
            },
            {
                name:'View',
                type:'line',
                data:infodata[4]
            },
            {
                name:'Rank',
                type:'line',
                data:infodata[5]
            }
        ]
    };
    mychart.setOption(option);
}