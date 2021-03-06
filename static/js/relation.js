

function showRelation(id,relation,ups){
    console.log(relation);
    console.log(ups);
    var datas = [];
    for(var i =0;i<ups.length;i++){
        datas.push({
            name: ups[i][1],
            symbol:'image://static/cupFaces/'+ups[i][0]+'.png'
        });
    }
    datas.forEach(function (node) {
        node.x=parseInt(Math.random()*3000);  //这里是最重要的如果数据中有返回节点x,y位置这里就不用设置，如果没有这里一定要设置node.x和node.y，不然无法定位节点 也实现不了拖拽了；
        node.y=parseInt(Math.random()*2500);
        node.symbolSize=[42,42];
        node.sizeFlag=[42,42];
        /*if(node.attributes.modularity_class != 4){
            node.symbolSize=[42,42];
            node.sizeFlag=[42,42];
        }else{
            node.symbolSize=[64,64];
            node.sizeFlag=[64,64];
        }*/
        //node.category = node.attributes.modularity_class;
        node.label={
            normal:{
                show:false
            }
        }
    });
    var link=[];
    for(var i= 0;i<relation.length;i++){
        link.push({
            source: relation[i][0],
            target: relation[i][1]
        });
    }
    var winWidth=document.body.clientWidth;
    var winHeight=document.body.clientHeight;
    var option = {
        //title: {
            //text: 'uploader relationship'
        //},
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
            {
                type: 'graph',
                layout:'none',
                circular:{rotateLabel:true},
                animation:false,
                //layout: 'force',
                symbolSize: 10,
                roam: true,
                draggable: false,
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
function initInvisibleGraphic() {
    // Add shadow circles (which is not visible) to enable drag.
     mychart.setOption({
        graphic: echarts.util.map(option.series[0].data, function (item, dataIndex) {
            //使用图形元素组件在节点上划出一个隐形的图形覆盖住节点
            var tmpPos=mychart.convertToPixel({'seriesIndex': 0},[item.x,item.y]);
            return {
                type: 'circle',
                id:dataIndex,
                position: tmpPos,
                shape: {
                    cx: 0,
                    cy: 0,
                    r: 20
                },
                // silent:true,
                invisible: true,
                draggable: true,
                ondrag: echarts.util.curry(onPointDragging, dataIndex),
                z: 100              //使图层在最高层
            };
        })
    });
    window.addEventListener('resize', updatePosition());
    mychart.on('dataZoom', updatePosition());
}

function onPointDragging(dataIndex) {      //节点上图层拖拽执行的函数
    var tmpPos=mychart.convertFromPixel({'seriesIndex': 0},this.position);
    option.series[0].data[dataIndex].x = tmpPos[0];
    option.series[0].data[dataIndex].y = tmpPos[1];
    mychart.setOption(option);
    updatePosition();
}

function updatePosition() {    //更新节点定位的函数
    mychart.setOption({
        graphic: echarts.util.map(option.series[0].data, function (item, dataIndex) {
            var tmpPos=mychart.convertToPixel({'seriesIndex': 0},[item.x,item.y]);
            return {
                position: tmpPos
            };
        })
    });
}
    var mychart = echarts.init(document.getElementById(id));
    mychart.clear();
    mychart.setOption(option);
    initInvisibleGraphic();
    mychart.on('graphRoam', updatePosition());
}