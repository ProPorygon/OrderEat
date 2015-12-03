function addOrder(variable) {
    var totalspan = d3.select("#totalprice");
    totalprice = parseFloat(totalspan[0][0].innerText.split("$")[1]);
    var item = variable[0].innerText.trim();
    var price = parseFloat(item.split("$")[1]);
    totalprice += price;
    totalprice = totalprice.toFixed(2);
    item = item.split("$")[0];
    var replaced = item.split(' ').join('_');
    replaced = replaced.split("'").join('');
    replaced = replaced.split("*").join('');
    replaced = replaced.split("&").join('');
    replaced = replaced.split("(").join('');
    replaced = replaced.split(")").join('');
    replaced = replaced.split('"').join('');
    replaced = replaced.split("/").join('');
    replaced = replaced.split(".").join('');
    var list = d3.select("#selected");
    //console.log(list);
    var appended = list.append("li")
                        .attr("id", replaced)
                        .style("display", "none")
                        .classed("list-group-item", true)
                        .classed("selected", true)
                        .text(item)
                        .append("span")
                        .style("float", "right")
                        .text("$" + price);
    $("#" + replaced).fadeIn(100);
    totalspan.text("$" + totalprice);
}

function rmOrder(variable) {
    var totalspan = d3.select("#totalprice");
    var totalprice = parseFloat(totalspan[0][0].innerText.split("$")[1]);
    var item = variable[0].innerText.trim();
    var price = parseFloat(item.split("$")[1]);
    totalprice -= price;
    totalprice = totalprice.toFixed(2);
    if (totalprice < 0) {totalprice = 0;}
    item = item.split("$")[0];
    var replaced = item.split(' ').join('_');
    replaced = replaced.split("'").join('');
    replaced = replaced.split("*").join('');
    replaced = replaced.split("&").join('');
    replaced = replaced.split("(").join('');
    replaced = replaced.split(")").join('');
    replaced = replaced.split('"').join('');
    replaced = replaced.split("/").join('');
    replaced = replaced.split(".").join('');
    $("#" + replaced).fadeOut(250, function() {
        d3.select("#" + replaced).remove();
    });
    totalspan.text("$" + totalprice);
}