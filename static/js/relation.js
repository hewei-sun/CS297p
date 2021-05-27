function showRelation(id,relation,ups){
    console.log(relation);
    console.log(ups);
    var datas = [];
    for(var i =0;i<ups.length;i++){
        datas.push({
            name: ups[i][1],
            symbol:'image://static/upFaces/'+ups[i][0]+'.png'
        });
    }
    /*datas.forEach(function (node) {
             node.x=parseInt(Math.random()*1000);  //这里是最重要的如果数据中有返回节点x,y位置这里就不用设置，如果没有这里一定要设置node.x和node.y，不然无法定位节点 也实现不了拖拽了；
             node.y=parseInt(Math.random()*1000);
            if(node.attributes.modularity_class != 4){
                node.symbolSize=[42,42];
                node.sizeFlag=[42,42];
            }else{
                node.symbolSize=[64,64];
                node.sizeFlag=[64,64];
            }
            node.category = node.attributes.modularity_class;
            node.label={
                normal:{
                    show:true
                }
            }
        });*/
    var link=[];
    for(var i= 0;i<relation.length;i++){
        link.push({
            source: relation[i][0],
            target: relation[i][1]
        });
    }
    var option = {
        title: {
            text: 'uploader relationship'
        },
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
            {
                type: 'graph',
                //layout:'none',
                layout: 'force',
                symbolSize: 10,
                roam: true,
                draggable: true,
                label: {
                    show: true
                },
                edgeSymbol: ['circle', 'arrow'],
                edgeSymbolSize: [7, 10],
                edgeLabel: {
                    fontSize: 5
                },
                data: datas,
                links: link,
                lineStyle: {
                    opacity: 0.9,
                    width: 2,
                    curveness: 0
                }
            }
        ]
    };
    var mychart = echarts.init(document.getElementById(id));
    mychart.clear();
    mychart.setOption(option);
}