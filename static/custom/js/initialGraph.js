$(document).ready(function(){
    var style = [
        { selector: 'node[label = "Concept"]',
          css: {'background-color': '#6FB1FC', 'content': 'data(name)'}
        },
        { selector: 'node[label = "Style"]',
          css: {'background-color': '#fcf146', 'content': 'data(name)'}
        },
        { selector: 'node[label = "Example"]',
          css: {'background-color': '#F5A45D', 'content': 'data(name)'}
        },
        { selector: 'node[label = "Type"]',
          css: {'background-color': '#3844f5', 'content': 'data(name)'}
        },
        { selector: 'node[label = "Color"]',
          css: {'background-color': '#f52635', 'content': 'data(name)'}
        },
        { selector: 'node[label = "Fabrictype"]',
          css: {'background-color': '#6bf51e', 'content': 'data(name)'}
        },
        { selector: 'node[label = "People"]',
          css: {'background-color': '#f50e8f', 'content': 'data(name)'}
        },
        { selector: 'node[label = "Mould"]',
          css: {'background-color': '#3bf5ba', 'content': 'data(name)'}
        },
        { selector: 'node[label = "Designer"]',
          css: {'background-color': '#21f563', 'content': 'data(name)'}
        },
        { selector: 'edge',
          css: {'content': 'data(relationship)', 'target-arrow-shape': 'triangle'}
        }
    ];

    var elements = {
        nodes: [

        ],
        edges: []
    };

    var layout = { name: 'circle'};

    var cy = cytoscape({
    container: document.getElementById('cy'),
    style:style,
    elements: elements,
    layout: layout,
    });

});
