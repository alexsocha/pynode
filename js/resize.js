function resize() {
    document.getElementById("appContainer").style.marginLeft = (document.getElementById("appWrapper").offsetWidth / 2 - (document.getElementById("appContainer").offsetWidth / 2)) + "px";
    document.getElementById("appContainer").style.visibility = "visible";
    document.getElementById("editor").style.width = (document.getElementById("appContainer").offsetWidth - 560) + "px";
}

function editor_resize() {
}

var resizeLayoutTimer = undefined;
var fixLayoutTimer = undefined;

var boundaryID = 837456;
var tlBoundary = {
    id: boundaryID,
    x: 0,
    y: 0,
    fixed: true,
    static: true,
    label: "",
    topRightLabel: "",
    topLeftLabel: "",
    labelStyle: "0,transparent,transparent,True",
    topRightLabelStyle: "0,transparent,transparent,True",
    topLeftLabelStyle: "0,transparent,transparent,True",
    r: 0
};
var brBoundary = {
    id: boundaryID + 1,
    x: 0,
    y: 0,
    fixed: true,
    static: true,
    label: "",
    topRightLabel: "",
    topLeftLabel: "",
    labelStyle: "0,transparent,transparent,True",
    topRightLabelStyle: "0,transparent,transparent,True",
    topLeftLabelStyle: "0,transparent,transparent,True",
    r: 0
};
var doConstraints = true;

function updateLayout() {
    resizeLayoutTimer = undefined;
    if (greuler_instance !== undefined) {
        setNodePositions();

        var w = document.getElementById("outputBox").clientWidth;
        var h = document.getElementById("outputBox").clientHeight;
        var tlBoundaryIndex = -1;
        var brBoundaryIndex = -1;

        for (var i = 0; i < greuler_instance.graph.nodes.length; i++) {
            if (greuler_instance.graph.nodes[i].id == boundaryID) {
                tlBoundaryIndex = i;
                brBoundaryIndex = i + 1;
                break;
            }
        }
        if (tlBoundaryIndex === -1 || brBoundaryIndex === -1) {
            greuler_instance.graph.addNode(tlBoundary);
            greuler_instance.graph.addNode(brBoundary);
            updateLayout();
            return;
        }

        greuler_instance.graph.nodes[tlBoundaryIndex].x = 1;
        greuler_instance.graph.nodes[tlBoundaryIndex].y = 1;
        greuler_instance.graph.nodes[brBoundaryIndex].x = w - 1;
        greuler_instance.graph.nodes[brBoundaryIndex].y = h - 1;

        var constraints = [];
        for (var i = 0; i < greuler_instance.graph.nodes.length; i++) {
            var node = greuler_instance.graph.nodes[i];
            if (node.id === tlBoundary.id || node.id === brBoundary.id || node.static) {
                continue;
            }
            if (doConstraints) {
                if (node.x < 0) {
                    node.x = w / 4;
                }
                if (node.x > w) {
                    node.x = (3 * w) / 4;
                }
                if (node.y < 0) {
                    node.y = h / 4;
                }
                if (node.y > h) {
                    node.y = (3 * h) / 4;
                }
            }
            constraints.push({axis: "x", type: "separation", left: tlBoundaryIndex, right: i, gap: node.r + 4});
            constraints.push({axis: "y", type: "separation", left: tlBoundaryIndex, right: i, gap: node.r + 4});
            constraints.push({axis: "x", type: "separation", left: i, right: brBoundaryIndex, gap: node.r + 4});
            constraints.push({axis: "y", type: "separation", left: i, right: brBoundaryIndex, gap: node.r + 4});
        }

        greuler_instance.layout.handleDisconnected(false);
        if (doConstraints) {
            greuler_instance.options.data.constraints = constraints;
        }
        else {
            greuler_instance.options.data.constraints = [];
        }
        greuler_instance.update();
        if (fixLayoutTimer === undefined) {
            fixLayoutTimer = setInterval(fixLayout, 4000);
        }
    }
}

var draggingNode = false;
function fixLayout() {
    if (!doConstraints) {
        return;
    }
    if (greuler_instance !== undefined && greuler_instance.graph !== undefined) {
        if (draggingNode) {
            return;
        }
        var w = document.getElementById("outputBox").clientWidth;
        var h = document.getElementById("outputBox").clientHeight;
        var didFix = false;
        for (var i = 0; i < greuler_instance.graph.nodes.length; i++) {
            var node = greuler_instance.graph.nodes[i];
            if (node.id === tlBoundary.id || node.id === brBoundary.id || node.static) {
                continue;
            }
            if (node.x < 0) {
                node.x = w / 4;
                didFix = true;
            }
            if (node.x > w) {
                node.x = (3 * w) / 4;
                didFix = true;
            }
            if (node.y < 0) {
                node.y = h / 4;
                didFix = true;
            }
            if (node.y > h) {
                node.y = (3 * h) / 4;
                didFix = true;
            }
        }
        if (didFix) {
            greuler_instance.update();
        }
    }
    else if (fixLayoutTimer !== undefined) {
        clearInterval(fixLayoutTimer);
        fixLayoutTimer = undefined;
    }
}

function setNodePositions() {
    var didUpdate = false;
    if (greuler_instance !== undefined && greuler_instance.graph !== undefined) {
        var w = document.getElementById("outputBox").clientWidth;
        var h = document.getElementById("outputBox").clientHeight;
        for (var i = 0; i < greuler_instance.graph.nodes.length; i++) {
            var node = greuler_instance.graph.nodes[i];
            if (node.id === tlBoundary.id || node.id === brBoundary.id || !node.static) {
                continue;
            }
            if (node.relativePosition) {
                if (node.x !== w * node.rx || node.y !== h * node.ry) didUpdate = true;
                node.x = w * node.rx;
                node.y = h * node.ry;
            }
            else {
                if (node.x !== node.ax || node.y !== node.ay) didUpdate = true;
                node.x = node.ax;
                node.y = node.ay;
            }
        }
    }
    return didUpdate;
}

function refreshLayout() {
    var doUpdate = setNodePositions();
    if (doUpdate) {
        updateLayout();
    }
}

function dragNode(dragging, nodeId) {
    if (!dragging && draggingNode) {
        clickNode(nodeId);
    }
    draggingNode = dragging;
}

function output_resize() {
    if (greuler_instance !== undefined) {
        var w = document.getElementById("outputBox").clientWidth;
        var h = document.getElementById("outputBox").clientHeight;
        greuler_instance.layout.size([w, h]);
        greuler_instance.options.data.size = [w, h];
        greuler_instance.options.width = w;
        greuler_instance.options.height = h;
        greuler_instance.root.attr("width", w).attr("height", h);
        greuler_instance.defaultOptions(greuler_instance.options);
        if (resizeLayoutTimer === undefined) {
            resizeLayoutTimer = setTimeout(updateLayout, 100);
        }
    }
}

function updateContraints(enable) {
    if (enable) {
        doConstraints = true;
        updateLayout();
    }
    else {
        if (fixLayoutTimer !== undefined) {
            clearInterval(fixLayoutTimer);
            fixLayoutTimer = undefined;
        }
        doConstraints = false;
        updateLayout();
    }
}

function getGraphNodes() {
    var nodes = [];
    for (var i = 0; i < greuler_instance.graph.nodes.length; i++) {
        if (greuler_instance.graph.nodes[i].id === tlBoundary.id || greuler_instance.graph.nodes[i].id === brBoundary.id) {
            continue;
        }
        nodes.push(greuler_instance.graph.nodes[i])
    }
    return nodes;
}