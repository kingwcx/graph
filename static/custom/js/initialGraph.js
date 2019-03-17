 var jq = $.noConflict();
jq(document).ready(function(){
    var style = [
        { selector: 'node[label = "Process"]',
          css: {'background-color': '#6FB1FC', 'content': 'data(name)'}
        },
        { selector: 'node[label = "Style"]',
          css: {'background-color': '#fcf146', 'content': 'data(name)'}
        },
        { selector: 'node[label = "People"]',
          css: {'background-color': '#fcf146', 'content': 'data(name)'}
        },
        { selector: 'edge',
          css: {'content': 'data(relationship)', 'target-arrow-shape': 'triangle'}
        }
    ];

    var elements = {
        nodes: [],
        edges: []
    };

    var layout = { name: 'circle'};

    jq.ajax({
        url:"{% url 'admin:load_graph' %}",
        type:"GET",


        success:function (data) {
            alert(data.nodes);
            alert("请求成功");
            var cy = cytoscape({
            container: document.getElementById('cy'),
                style:style,
                elements: {
                    nodes:data.nodes,
                    edges:data.edges,
                },
                layout: layout,
            });
        },

        error:function () {
            alert("服务器请求超时,请重试!");
        }

    });
});