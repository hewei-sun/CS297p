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
                layout: 'force',
                symbolSize: 10,
                roam: true,
                label: {
                    show: true
                },
                edgeSymbol: ['circle', 'arrow'],
                edgeSymbolSize: [7, 10],
                edgeLabel: {
                    fontSize: 5
                },
                data: [{
                    name: '节点1',
                    symbol:'image://static/upFaces/10119428.png'
                }, {
                    name: '节点2',
                    symbol:'image://static/upFaces/10330740.png'
                }, {
                    name: '节点3',
                    symbol:'image://static/upFaces/10558098.png'
                }, {
                    name: '节点4',
                    symbol:'image://static/upFaces/113362335.png'
                }],
                links: [
                    {
                        source: 0,
                        target: 1,
                        symbolSize: [5, 20],
                        label: {
                            show: true
                        },
                        lineStyle: {
                            width: 5,
                            curveness: 0.2
                        }
                    }, 
                    {
                        source: '节点2',
                        target: '节点1',
                        label: {
                            show: true
                        },
                        lineStyle: {
                            curveness: 0.2
                        }
                    }, {
                        source: '节点1',
                        target: '节点3'
                    }, {
                        source: '节点2',
                        target: '节点3'
                    }, {
                        source: '节点2',
                        target: '节点4'
                    }, {
                        source: '节点1',
                        target: '节点4'
                    }
                ],
                lineStyle: {
                    opacity: 0.9,
                    width: 2,
                    curveness: 0
                }
            }
        ]
    };