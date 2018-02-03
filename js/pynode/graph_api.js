js_update_timer = null;
js_do_update = true;
js_positioning_counter = 0;
js_GLOBAL_ID = 0;

function enable_update(enable) {
    js_do_update = enable;
}

function next_global_id() {
    id_value = js_GLOBAL_ID;
    js_GLOBAL_ID += 1;
    return id_value;
}

function update_instant() {
    try { greuler_instance.update({skipLayout: true}); }
    catch(err) { js_update_timer = setTimeout(update_instant, 20); }
}

function update_instant_layout() {
    try { updateLayout(); }
    catch(err) { js_update_timer = set_timeout(update_instant_layout, 20); }
}

function js_update(layout) {
    if (typeof(layout) === 'undefined') layout = true;
    if (js_do_update) {
        try {
            if (layout) {
                js_update_timer = setTimeout(update_instant_layout, 50);
                updateLayout();
            }
            else {
                js_update_timer = setTimeout(update_instant, 50);
                greuler_instance.update({skipLayout: true});
            }
        }
        catch(err) {}
    }
}

function js_add_node(data) {
    if (!data.static) {
        var x = 0; var y = 0;
        var size = Math.floor(Math.sqrt(js_positioning_counter));
        if (Math.pow(size, 2) !== js_positioning_counter) size += 1;
        if (size % 2 === 0) size += 1;
        var half_size = Math.floor(size / 2.0);
        var difference = Math.pow(size, 2) - js_positioning_counter;
        if (difference <= size) { y = -half_size; x = -half_size + (size - difference); }
        else if (difference <= (size * 2) - 1) { y = -half_size + (difference - size); x = -half_size; }
        else if (difference <= (size * 3) - 2) { y = half_size; x = -half_size + (difference - (size * 2)) + 1; }
        else if (difference <= (size * 4) - 3) { y = -half_size + (size - (difference - (size * 3) + 3)); x = half_size; }
        data.x = (greuler_instance.options.data.size[0] / 2.0) + (x * 25); data.y = (greuler_instance.options.data.size[1] / 2.0) + (-y * 25);
        js_positioning_counter += 1;
    }
    greuler_instance.graph.addNode(data);
    js_update(true);
    setTimeout(refreshLayout, 65);
}

function js_remove_node(node_id) {
    greuler_instance.graph.removeNode({id: node_id});
    js_update(true);
}

function js_add_edge(data) {
    greuler_instance.graph.addEdge(data);
    if (greuler_instance.graph.edges.length >= greuler_instance.graph.nodes.length - 3 && (greuler_instance.graph.nodes.length - 2) % 9 === 0) js_positioning_counter = 0;
    js_update(true);
}

function js_remove_edge(edge_id) {
    greuler_instance.graph.removeEdge({id: edge_id});
    js_update(true);
}

function js_add_all(element_data) {
    enable_update(false);
    for (var i = 0; i < element_data.length; i++) {
        var x = element_data[i];
        if (x[0] === 0) js_add_node(x[1]);
        else if (x[0] === 1) js_add_edge(x[1]);
    }
    enable_update(true);
    js_update(true);
}

function js_remove_all(element_data) {
    enable_update(false);
    for (var i = 0; i < element_data.length; i++) {
        var x = element_data[i];
        if (x[0] === 0) js_remove_node(x[1].id);
        else if (x[0] === 1) js_remove_edge(x[1].id);
    }
    enable_update(true);
    js_update(true);
}

function js_set_spread(spread) {
    greuler_instance.graph.linkDistance = spread;
    greuler_instance.options.data.linkDistance = spread;
    js_update(true);
}

function js_clear() {
    greuler_instance.graph.removeEdges(greuler_instance.graph.edges);
    greuler_instance.graph.removeNodes(getGraphNodes());
    js_update_timer = null;
    js_do_update = true;
    js_positioning_counter = 0;
    js_update(true);
}

function js_node_set_value(node_id, value) {
    if (greuler_instance.graph.hasNode({id: node_id})) {
        greuler_instance.graph.getNode({id: node_id}).label = value;
        js_update(false);
    }
}

function js_node_set_position(node_id, x, y, relative) {
    if (greuler_instance.graph.hasNode({id: node_id})) {
        n = greuler_instance.graph.getNode({id: node_id});
        if (x === null || y === null) {
            n.fixed = false;
            n.static = true;
            return;
        }
        n.fixed = true;
        n.static = true;
        n.relativePosition = relative;
        if (relative) { n.rx = x; n.ry = y; }
        else { n.ax = x; n.ay = y; n.x = x; n.y = y; }
        setTimeout(update_instant_layout, 215);
    }
}

function js_node_get_position(node) {
    // Not currently implemented
}

function js_node_set_label(node_id, text, label_id) {
    if (greuler_instance.graph.hasNode({id: node_id})) {
        var n = greuler_instance.graph.getNode({id: node_id});
        if (label_id === 0) { n.topRightLabel = text; }
        else if (label_id === 1) { n.topLeftLabel = text; }
        js_update(false);
    }
}

function js_node_set_size(node_id, size) {
    if (greuler_instance.graph.hasNode({id: node_id})) {
        greuler_instance.graph.getNode({id: node_id}).r = size;
        greuler_instance.selector.getNode({id: node_id}).transition("highlight_node_size").duration(0);
        greuler_instance.selector.getNode({id: node_id}).transition("node_size").duration(500).attr("r", size);
        js_update(true);
    }
}

function js_node_set_color(node_id, color, text_style) {
    if (greuler_instance.graph.hasNode({id: node_id})) {
        greuler_instance.graph.getNode({id: node_id}).color = color;
        greuler_instance.graph.getNode({id: node_id}).labelStyle = text_style;
        greuler_instance.selector.getNode({id: node_id}).transition("highlight_node_color").duration(0);
        greuler_instance.selector.getNodeOuter({id: node_id}).selectAll("text.label").transition("highlight_node_outline").duration(0);
        greuler_instance.selector.getNode({id: node_id}).transition("node_color").duration(500).attr("fill", color);
        if (text_style.toString().split(",")[3] === "False") greuler_instance.selector.getNodeOuter({id: node_id}).selectAll("text.label").transition("node_stroke_color").duration(500).attr("stroke", text_style.toString().split(",")[2]);
        js_update(false);
    }
}

function js_node_set_value_style(node_id, style) {
    if (greuler_instance.graph.hasNode({id: node_id})) {
        greuler_instance.graph.getNode({id: node_id}).labelStyle = style;
        greuler_instance.selector.getNodeOuter({id: node_id}).selectAll("text.label").transition("highlight_node_outline").duration(0);
        greuler_instance.selector.getNodeOuter({id: node_id}).selectAll("text.label").transition("node_stroke_color").duration(0);
        if (style.toString().split(",")[3] === "False") greuler_instance.selector.getNodeOuter({id: node_id}).selectAll("text.label").attr("stroke", style.toString().split(",")[2]);
        js_update(false);
    }
}

function js_node_set_label_style(node_id, style, label_id) {
    if (greuler_instance.graph.hasNode({id: node_id})) {
        if (label_id === 0) greuler_instance.graph.getNode({id: node_id}).topRightLabelStyle = style;
        else if (label_id === 1) greuler_instance.graph.getNode({id: node_id}).topLeftLabelStyle = style;
        js_update(false);
    }
}

function js_node_highlight(node_id, size, color) {
    if (typeof(size) === 'undefined') size = null;
    if (typeof(color) === 'undefined') color = null;
    if (greuler_instance.graph.hasNode({id: node_id})) {
        data = {};
        if (size !== null) data.size = size;
        if (color !== null) data.color = color;
        greuler_instance.selector.highlightNode({id: node_id}, data);
    }
}

function js_edge_set_weight(edge_id, weight) {
    if (greuler_instance.graph.hasEdge({id: edge_id})) {
        greuler_instance.graph.getEdge({id: edge_id}).weight = weight;
        js_update(false);
    }
}

function js_edge_set_directed(edge_id, directed) {
    if (greuler_instance.graph.hasEdge({id: edge_id})) {
        greuler_instance.graph.getEdge({id: edge_id}).directed = directed;
        js_update(false);
    }
}

function js_edge_set_width(edge_id, width) {
    if (greuler_instance.graph.hasEdge({id: edge_id})) {
        greuler_instance.graph.getEdge({id: edge_id}).lineWidth = width;
        greuler_instance.selector.getEdge({id: edge_id}).transition("highlight_edge_width").duration(0);
        greuler_instance.selector.getEdge({id: edge_id}).transition("edge_width").duration(500).attr("stroke-width", width);
        js_update(false);
    }
}

function js_edge_set_color(edge_id, color) {
    if (greuler_instance.graph.hasEdge({id: edge_id})) {
        greuler_instance.graph.getEdge({id: edge_id}).stroke = color;
        animate_edge = greuler_instance.selector.getEdge({id: edge_id});
        greuler_instance.selector.getEdge({id: edge_id}).transition("highlight_edge_color").duration(0);
        animate_edge.transition("edge_color").duration(500).attr("stroke", color);
    }
}

function js_edge_set_weight_style(edge_id, style) {
    if (greuler_instance.graph.hasEdge({id: edge_id})) {
        greuler_instance.graph.getEdge({id: edge_id}).weightStyle = style;
        js_update(false);
    }
}

function js_edge_highlight(edge_id, width, color) {
    if (typeof(width) === 'undefined') width = null;
    if (typeof(color) === 'undefined') color = null;
    if (greuler_instance.graph.hasEdge({id: edge_id})) {
        data = {};
        if (width !== null) data.width = width;
        if (color !== null) data.color = color;
        greuler_instance.selector.highlightEdge({id: edge_id}, data);
    }
}

function js_edge_traverse(edge_id, initial_node_id, color, keep_path) {
    if (greuler_instance.graph.hasEdge({id: edge_id})) {
        greuler_instance.selector.traverseEdge({id: edge_id}, {stroke: color, keepStroke: keep_path}, initial_node_id);
    }
}

function js_run_function(name, args) {
    var data = JSON.parse(args);
    window[name].apply(null, data);
}
