function enable_box_layout() {
	if (greuler_instance.root !== undefined) {
		greuler_instance.root.call(window.d3.behavior.zoom().on("zoom", null));
		updateContraints(true);
	}
}

function enable_drag_layout() {
	if (greuler_instance.root !== undefined) {
		greuler_instance.root.on("mousedown", mouse_down).call(window.d3.behavior.zoom().scaleExtent([0.4, 4.0]).on("zoom", pan_zoom));
        updateContraints(false);
	}
}
function mouse_down() {
	var stop = window.d3.event.button || window.d3.event.ctrlKey;
	if (stop) window.d3.event.stopImmediatePropagation();
}

function pan_zoom() {
    if (window.d3.event !== undefined && window.d3.event.sourceEvent !== undefined && window.d3.event.sourceEvent !== null) {
        window.d3.event.sourceEvent.preventDefault();
        greuler_instance.nodeGroup.attr("transform", "translate(" + window.d3.event.translate + ")" + " scale(" + window.d3.event.scale + ")");
        greuler_instance.edgeGroup.attr("transform", "translate(" + window.d3.event.translate + ")" + " scale(" + window.d3.event.scale + ")");
    }
}

function set_layout_type() {
	if (greuler_instance.nodeGroup !== undefined) {
		greuler_instance.nodeGroup.transition(500).attr("transform", "translate(0,0) scale(1.0)");
		greuler_instance.edgeGroup.transition(500).attr("transform", "translate(0,0) scale(1.0)");
		if (document.getElementById("layout1On").style.display === "none") { enable_box_layout() }
		else { enable_drag_layout() }
	}
}

var clickListener;
var clickListenerFunc;
function registerClickListener(func) {
	clickListener = func;
}

function clickNode(nodeId) {
	if (clickListener !== undefined) {
		clickListener(nodeId);
	}
	console.log("pynode:click:" + nodeId)
}
