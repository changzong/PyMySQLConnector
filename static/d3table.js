var id_string = "d3table";
console.log("*****************************************");
var dataset = [];
var sub_dataset = [];
var sub_element;
var columns = table_content[0];
var cumheight = 0;
var row_num = table_content.length + 1;
var list_by_column = [];
var sub_column = [];
var padding = 10;
var input_top, input_left;
var ua = navigator.userAgent.toLowerCase();
if (ua.indexOf('firefox') > -1) {
    input_top = 620;
    input_left = 130;
}
else if (ua.indexOf('chrome') > -1) {
    input_top = 520;
    input_left = 70;
}

var margin = {top: 70, right: 20, bottom: 30, left: 60 },
    width = 180 * columns.length - margin.left - margin.right,
    height = 250 * table_content.length - margin.top - margin.bottom;
    //height = 600 - margin.top - margin.bottom;
//var zoom = d3.behavior.zoom()
    //.scaleExtent([1, 10])
    //.on("zoom", zoomed);

d3.select("svg").remove();
d3.select(".tooltip").remove();
//d3.select(".editor").remove();
d3.select(".submit").remove();
d3.select(".remove").remove();
var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .attr("fill", "#ff8000")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
    //.call(zoom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + (margin.top-10) + ")");

function zoomed() {
    svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}

function count_len(str) {
    var len = 0;
    for (var i=0; i<str.length; i++) {
        if (str.charCodeAt(i)>127 || str.charCodeAt(i)==94) {
            len += 2;
        }
        else {
            len ++;
        }
    }
    return len;
}

for (var i=0; i<columns.length; i++)
{
    for (var j=table_content.length - 1; j>0; j--)
    {
        sub_element = {
            content: table_content[j][i],
            space: cumheight += height/row_num};
        sub_dataset.push(sub_element);
        sub_column.push(count_len(String(table_content[j][i])));
    }
    element = {name: columns[i], value: sub_dataset};
    dataset.push(element);
    cumheight = 0;
    sub_dataset = [];
    list_by_column.push(sub_column);
    sub_column = [];
}
var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], 0.002);
x.domain(dataset.map(function(d) { return d.name; }));
/////////////////////////////////////////////
//The scale based on the width of each column
var x_cell_len = d3.scale.linear()
    .range([0, width]);
var table_length = 0;
var cell_length = [];
for (var i=0; i<columns.length; i++)
{
    cell_length.push(20 + Math.max.apply(null, list_by_column[i]));
    table_length = table_length + cell_length[i];
}
x_cell_len.domain([0, table_length]);
////////////////////////////////////////////
var y = d3.scale.linear()
    .range([height, 0]);
y.domain([0, height]);

function color(data)
{
    color_list = ["#FFFFFF", "#E5F2F4"];
    return color_list[data];
}
var index_list = [];
var index = 0;
var current_pos = 0;
var cumu_cell_length = [0];

var tooltip = d3.select("body")
    .append("div")
    .attr("class","tooltip")
    .style("position", "absolute")
    .style("z-index", "10")
    .style("visibility", "hidden");
// var editor = d3.select("body")
//     .append("input")
//     .attr("class","editor")
//     .attr("type", "text")
//     .style("visibility", "hidden")
//     .style("position", "absolute");
var submit = d3.select("body")
    .append("input")
    .attr("type", "submit")
    .attr("value", "Submit")
    .attr("class", "submit")
    .style("visibility", "hidden")
    .style("position", "absolute")
    .on("click", edit_handler);
var remove = d3.select("body")
    .append("input")
    .attr("type", "submit")
    .attr("value", "Remove")
    .attr("class", "remove")
    .style("visibility", "hidden")
    .style("position", "absolute")
    .on("click", remove_handler);

var bar = svg.selectAll(".bar")
    .data(dataset)
    .enter().append("g")
    .attr("id", function(d, i) {
        return i.toString();
    })
    //.attr("transform", function(d) { return "translate(" + x(d.name) + ",0)"; })
    .attr("transform", function(d, i) {
        var c = current_pos;
        current_pos += x_cell_len(cell_length[i]);
        cumu_cell_length.push(current_pos);
        return "translate(" + c + ",0)";
    })
    .style("fill", function(d, i) {
        return color(i%2);
    });
bar.selectAll("rect")
    .data(function(d){
        return d.value;
    })
    .enter().append("rect")
    .attr("y", function(d) {
        return y( d.space ) - height/row_num - height/row_num/4;
    })
    .attr("height", height/row_num)
    .attr("width", function(d, i){
        if (i == table_content.length-2){
            index++;
            return x_cell_len(cell_length[index-1]);
        }
        return x_cell_len(cell_length[index]);
    })
    .style("stroke", "#409DAD")
    .style("stroke-width", 0.1)
    .on("mouseover", function(d){
        d3.select(this).style("cursor", "pointer")
            .style("stroke-width", 1);
        tooltip.style("visibility", "visible").html(d.content);
    })
    .on("mousemove", function(){
        tooltip.style("top", (d3.event.pageY-10)+"px")
            .style("left",(d3.event.pageX+10)+"px")
    })
    .on("mouseout", function(){
        tooltip.style("visibility", "hidden");
        d3.select(this).style("stroke-width", 0.1);
    })
    .on("click", function(d, i){
        var row = (row_num - i - 2).toString();
        var column = d3.select(this).node().parentNode.id;
        if (column != 0) {
            remove.style("visibility", "hidden");
            var editor = d3.select("body")
                .append("input")
                .attr("class","editor")
                .attr("type", "text")
                .style("visibility", "hidden")
                .style("position", "absolute");
            d3.selectAll(".editor").style("visibility", "hidden");
            editor.attr("id", "editor" + row + column).style("visibility", "visible")
                .style("position","absolute")
                .style("top", (input_top + y( d.space ) - height/row_num - height/row_num/4 + height/row_num/2) + "px")
                .style("left", (cumu_cell_length[column] + input_left) + "px")
                .style("width", (x_cell_len(cell_length[column])-10)+"px");
            submit.attr("id", "submit" + row + column).style("visibility", "visible")
                .style("top", (input_top + y( d.space ) - height/row_num - height/row_num/4 + height/row_num/2) + "px");
            if (column == 7 || column == 9) {
                editor.attr("type", "text").attr("onFocus", "WdatePicker({lang:'zh-cn', dateFmt:'yyyy-MM-dd HH:mm:ss'})");
            }
            else {
                editor.attr("type", "text").attr("onFocus", null);
            }
        }
        else {
            editor.style("visibility", "hidden");
            submit.style("visibility", "hidden");
            remove.attr("id", "remove" + row).style("visibility", "visible")
                .style("top", (input_top + y( d.space ) - height/row_num - height/row_num/4 + height/row_num/2) + "px")
                .style("left", "2px");
        }
    });

current_pos = 0;
index = 0;

bar.selectAll("content")
    .data(function(d){
        return d.value;
    })
    .enter().append("text")
    .attr("x", padding)
    .attr("y", function(d){
        return y( d.space ) - height/row_num - height/row_num/4 + height/row_num/2;
    })
    .style("text-anchor", "left")
    .style("fill", "Black")
    .style("font", "15px Arial")
    .style("font-weight", "normal")
    .text(function(d, i){
        if (typeof d.content == "string") {
                return d.content;
        }
        else {
            return String(d.content).replace(/,/g, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
    });

//Half hard code the style of the table head
var table_head = svg.append("g");

table_head.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", x_cell_len(table_length))
    .attr("height", height/row_num/4)
    .style("fill", "#409DAD")
    .style("stroke", "#409DAD")
    .style("stroke-width", 0.1);
table_head.append("text")
    .attr("x", 0)
    .attr("y", 20)
    .style("text-anchor", "left")
    .style("fill", "White")
    .style("font", "20px Arial")
    .style("font-weight", "bold")
    .text("TableManager");
//////////////////////////////////////////////////
//Split long strings in half with complete words.
function string_spliter(s)
{
    var middle = Math.floor(s.length / 2);
    var before = s.lastIndexOf(' ', middle);
    var after = s.indexOf(' ', middle + 1);
    if (middle - before < after - middle) {
        middle = before;
    } else {
        middle = after;
    }
    var s1 = s.substr(0, middle);
    var s2 = s.substr(middle + 1);
    return [s1, s2];
}
//////////////////////////////////////////////////
current_pos = padding;

table_head.append("rect")
    .attr("x", 0)
    .attr("y", height/row_num/4)
    .attr("width", x_cell_len(table_length))
    .attr("height", height/row_num/2)
    .style("fill", "#409DAD")
    .style("stroke", "#409DAD")
    .style("stroke-width", 0.1);

var head_for_cell = table_head.selectAll("headcontent")
    .data(dataset)
    .enter().append("g")
    .attr("transform", function(d, i) {
        var c = current_pos+x_cell_len(cell_length[i])*0.5-10;
        current_pos += x_cell_len(cell_length[i]);
        return "translate(" + c + ",0)";
    });
head_for_cell.selectAll("headcontent")
    .data(function(d, i){
        return string_spliter(columns[i]);
    })
    .enter().append("text")
    .attr("y", function(d, i){
        return height/row_num/2;
    })
    .style("text-anchor", "middle")
    .style("fill", "White")
    .style("font", "15px Arial")
    .style("font-weight", "bold")
    .text(function(d, i){
        console.log(d);
        return d;
    });