
function showAverageLinesChart(value){

var average_lineChat_path = "./average_seasons"
var tsvFiles = ["average.csv", "average_-03-01.csv", "average_-06-01.csv", "average_-09-01.csv", "average_-12-01.csv"]


var margin = {top: 10, right: 50, bottom:20 , left: 30},
    width = 900 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y-%m-%d").parse;

var x = d3.time.scale()
    .range([0, width]);

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var tip = d3.tip()
.attr('class', 'd3-tip')
.direction('e')
.offset([0, 20])
.html(function(d) {

return  d.meta;
});

var line = d3.svg.line()
    .interpolate("basis")
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.day); });

var svg = d3.select("#linechart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


d3.csv(average_lineChat_path + "/" + tsvFiles[value], function(error, data) {
  if (error) throw error;

  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

  data.forEach(function(d) {
    d.date = parseDate(d.date);
  });

  var indicators = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(d) {
        return {date: d.date, day: +d[name]};
      })
    };
  });

  x.domain(d3.extent(data, function(d) { return d.date; }));

  y.domain([
    d3.min(indicators, function(c) { return d3.min(c.values, function(v) { return v.day; }); }),
    d3.max(indicators, function(c) { return d3.max(c.values, function(v) { return v.day; }); })
  ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(0)")
      .attr("y", 6)
      .attr("dy", ".100em")
      .style("text-anchor", "end")
      .text("day (d)");

  var indicator = svg.selectAll(".indicator")
      .data(indicators)
      .enter().append("g")
      .attr("class", "indicator");

  indicator.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return color(d.name); });

  indicator.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.day) + ")"; })
      .attr("x", 3)
      .attr("dy", ".100em")
      .text(function(d) { return d.name; });

// var mouseG = svg.append("g")
//       .attr("class", "mouse-over-effects");

//     mouseG.append("path") // this is the black vertical line to follow mouse
//       .attr("class", "mouse-line")
//       .style("stroke", "black")
//       .style("stroke-width", "1px")
//       .style("opacity", "0");
      
//     var lines = document.getElementsByClassName('line');

//     var mousePerLine = mouseG.selectAll('.mouse-per-line')
//       .data(cities)
//       .enter()
//       .append("g")
//       .attr("class", "mouse-per-line");

//     mousePerLine.append("circle")
//       .attr("r", 7)
//       .style("stroke", function(d) {
//         return color(d.name);
//       })
//       .style("fill", "none")
//       .style("stroke-width", "1px")
//       .style("opacity", "0");

//     mousePerLine.append("text")
//       .attr("transform", "translate(10,3)");

//     mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
//       .attr('width', width) // can't catch mouse events on a g element
//       .attr('height', height)
//       .attr('fill', 'none')
//       .attr('pointer-events', 'all')
//       .on('mouseout', function() { // on mouse out hide line, circles and text
//         d3.select(".mouse-line")
//           .style("opacity", "0");
//         d3.selectAll(".mouse-per-line circle")
//           .style("opacity", "0");
//         d3.selectAll(".mouse-per-line text")
//           .style("opacity", "0");
//       })
//       .on('mouseover', function() { // on mouse in show line, circles and text
//         d3.select(".mouse-line")
//           .style("opacity", "1");
//         d3.selectAll(".mouse-per-line circle")
//           .style("opacity", "1");
//         d3.selectAll(".mouse-per-line text")
//           .style("opacity", "1");
//       })
//       .on('mousemove', function() { // mouse moving over canvas
//         var mouse = d3.mouse(this);
//         d3.select(".mouse-line")
//           .attr("d", function() {
//             var d = "M" + mouse[0] + "," + height;
//             d += " " + mouse[0] + "," + 0;
//             return d;
//           });

//         d3.selectAll(".mouse-per-line")
//           .attr("transform", function(d, i) {
//             console.log(width/mouse[0])
//             var xDate = x.invert(mouse[0]),
//                 bisect = d3.bisector(function(d) { return d.date; }).right;
//                 idx = bisect(d.values, xDate);
            
//             var beginning = 0,
//                 end = lines[i].getTotalLength(),
//                 target = null;

//             while (true){
//               target = Math.floor((beginning + end) / 2);
//               pos = lines[i].getPointAtLength(target);
//               if ((target === end || target === beginning) && pos.x !== mouse[0]) {
//                   break;
//               }
//               if (pos.x > mouse[0])      end = target;
//               else if (pos.x < mouse[0]) beginning = target;
//               else break; //position found
//             }
            
//             d3.select(this).select('text')
//               .text(y.invert(pos.y).toFixed(2));
              
//             return "translate(" + mouse[0] + "," + pos.y +")";
//           });



});

}
