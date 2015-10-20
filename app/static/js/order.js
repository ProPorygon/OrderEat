function addOrder(variable) {
    var item = variable[0].innerText.trim();
    var replaced = item.split(' ').join('_');
    replaced = replaced.split("'").join('');
    replaced = replaced.split("*").join('');
    var list = d3.select("#selected");
    console.log(list);
    var appended = list.append("li")
                        .attr("id", replaced)
                        .style("display", "none")
                        .classed("list-group-item", true)
                        .classed("selected", true)
                        .text(item);
    $("#" + replaced).fadeIn(100);
}

function rmOrder(variable) {
    var item = variable[0].innerText.trim();
    var replaced = item.split(' ').join('_');
    replaced = replaced.split("'").join('');
    replaced = replaced.split("*").join('');
    $("#" + replaced).fadeOut(250, function() {
        d3.select("#" + replaced).remove();
    });
    //d3.select("#" + replaced).remove();
    //toRemove.remove()
}