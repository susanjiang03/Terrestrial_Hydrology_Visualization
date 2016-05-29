// function showBarGraph(date){

// var average_bar_dataFile_dir = "./average"
// var csvFile = average_bar_dataFile_dir + "/average_" + date + ".csv"

// var margin = {top: 20, right: 20, bottom: 30, left: 20},
//     width = 1200 - margin.left - margin.right,
//     height = 200 - margin.top - margin.bottom;

// var x = d3.scale.ordinal()
//     .rangeRoundBands([0, width], .1);

// var y = d3.scale.linear()
//     .range([height, 0]);

// var xAxis = d3.svg.axis()
//     .scale(x)
//     .orient("bottom");

// var yAxis = d3.svg.axis()
//     .scale(y)
//     .orient("left")
//     .ticks(10, "");

// var svg = d3.select("#barGraph").append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//   .append("g")
//     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// d3.csv(csvFile, type, function(error, data) {
//   if (error) throw error;

//   x.domain(data.map(function(d) { return d.indicator; }));
//   y.domain([0, d3.max(data, function(d) { return d.average; })]);

//   svg.append("g")
//       .attr("class", "x axis")
//       .attr("transform", "translate(0," + height + ")")
//       .call(xAxis);

//   svg.append("g")
//       .attr("class", "y axis")
//       .call(yAxis)
//     .append("text")
//       .attr("transform", "rotate(-90)")
//       .attr("y", 6)
//       .attr("dy", ".71em")
//       .style("text-anchor", "end")
//       .text("average days");

//   svg.selectAll(".bar")
//       .data(data)
//     .enter().append("rect")
//       .attr("class", "bar")
//       .attr("x", function(d) { return x(d.indicator); })
//       .attr("width", x.rangeBand())
//       .attr("y", function(d) { return y(d.average); })
//       .attr("height", function(d) { return height - y(d.average); });
// });

// function type(d) {
//   d.average = +d.average;
//   return d;
// }

// }

// // var HISTOGRAMDATA_DIR = './HISTOGRAMS/'

//     function showHistograms(date, cluster, var) {

//           var HEADER = ['ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans',
//    'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
//    'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
//    'energy_sw_up_-3', 'energy_sw_up_-2',  'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
//    'energy_sw_dn_-3', 'energy_sw_dn_-2','energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
//    'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
//    'energy_lw_dn_-3', 'energy_lw_dn_-2','energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2'];   

// // plot a histogram from mpg data in a .csv file
// function parser(d) {
//     d.pMPG = +d.MPG;
//     return d;
// }

// function mpghist(csvdata) {
//     var binsize = 5;
//     var minbin = 0;
//     var maxbin = 95;
//     var numbins = (maxbin - minbin) / binsize;

//     // whitespace on either side of the bars in units of MPG
//     var binmargin = 0.3; 
//     var margin = {top: 30, right: 20, bottom: 30, left: 40};
//     var width = 162 - margin.left - margin.right;
//     var height = 180 - margin.top - margin.bottom;

//     // Set the limits of the x axis
//     var xmin = minbin - 1
//     var xmax = maxbin + 1

//     histdata = new Array(numbins);
//     for (var i = 0; i < numbins; i++) {
//     histdata[i] = { numfill: 0, meta: "" };
//   }

//   // Fill histdata with y-axis values and meta data
//     csvdata.forEach(function(d) {
//     var bin = Math.floor((d.pMPG - minbin) / binsize);
//     if ((bin.toString() != "NaN") && (bin < histdata.length)) {
//       histdata[bin].numfill += 1;
//       histdata[bin].meta += "<tr><td>" + d.lat +
//         " " + d.lon + 
//         "</td><td>    " + 
//         d.pMPG.toFixed(0) + " days</td></tr>";
//     }
//     });

//     // This scale is for determining the widths of the histogram bars
//     // Must start at 0 or else x(binsize a.k.a dx) will be negative
//     var x = d3.scale.linear()
//     .domain([0, (xmax - xmin)])
//     .range([0, width]);

//     // Scale for the placement of the bars
//     var x2 = d3.scale.linear()
//     .domain([xmin, xmax])
//     .range([0, width]);
  
//     var y = d3.scale.linear()
//     .domain([0, d3.max(histdata, function(d) { 
//             return d.numfill; 
//             })])
//     .range([height, 0]);

//     var xAxis = d3.svg.axis()
//     .scale(x2)
//     .orient("bottom");
//     var yAxis = d3.svg.axis()
//     .scale(y)
//     .ticks(8)
//     .orient("left");

//     var tip = d3.tip()
//     .attr('class', 'd3-tip')
//     .direction('e')
//     .offset([0, 20])
//     .html(function(d) {

//       return '<table id="tiptable">' + d.meta + "</table>";
//   });

//     // put the graph in the "mpg" div
//     var svg = d3.select("#histograms").append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//     .append("g")
//     .attr("transform", "translate(" + margin.left + "," + 
//             margin.top + ")");

//     svg.call(tip);

//     // set up the bars
//     var bar = svg.selectAll(".bar")
//     .data(histdata)
//     .enter().append("g")
//     .attr("class", "bar")
//     .attr("transform", function(d, i) { return "translate(" + 
//          x2(i * binsize + minbin) + "," + y(d.numfill) + ")"; })
//     .on('mouseover', tip.show)
//     .on('mouseout', tip.hide);

//     // add rectangles of correct size at correct location
//     bar.append("rect")
//     .attr("x", x(binmargin))
//     .attr("width", x(binsize - 2 * binmargin))
//     .attr("height", function(d) { return height - y(d.numfill); });

//     // add the x axis and x-label
//     svg.append("g")
//     .attr("class", "x axis")
//     .attr("transform", "translate(0," + height + ")")
//     .call(xAxis);
//     svg.append("text")
//     .attr("class", "xlabel")
//     .attr("text-anchor", "middle")
//     .attr("x", width / 2)
//     .attr("y", height + margin.bottom)
//     .text(HEADER[variable]);

//     // add the y axis and y-label
//     svg.append("g")
//     .attr("class", "y axis")
//     .attr("transform", "translate(0,0)")
//     .call(yAxis);
//     svg.append("text")
//     .attr("class", "ylabel")
//     .attr("y", 0 - margin.left) // x and y switched due to rotation
//     .attr("x", 0 - (height / 2))
//     .attr("dy", "0.8em")
//     .attr("transform", "rotate(0)")
//     .style("text-anchor", "top")
//     .text("Counts");
// }

// // Read in .csv data and make graph
// d3.csv( csvFile, parser,
//        function(error, csvdata) {
//      mpghist(csvdata);

// });

// };





// function showAverageLinesChart(value){

// var average_lineChat_path = "./average_seasons"
// var tsvFiles = ["average.csv", "average_-03-01.csv", "average_-06-01.csv", "average_-09-01.csv", "average_-12-01.csv"]


// var margin = {top: 10, right: 50, bottom:20 , left: 30},
//     width = 500 - margin.left - margin.right,
//     height = 450 - margin.top - margin.bottom;

// var parseDate = d3.time.format("%Y-%m-%d").parse;

// var x = d3.time.scale()
//     .range([0, width]);

// var y = d3.scale.linear()
//     .range([height, 0]);

// var color = d3.scale.category10();

// var xAxis = d3.svg.axis()
//     .scale(x)
//     .orient("bottom");

// var yAxis = d3.svg.axis()
//     .scale(y)
//     .orient("left");

// var tip = d3.tip()
// .attr('class', 'd3-tip')
// .direction('e')
// .offset([0, 20])
// .html(function(d) {

// return  d.meta;
// });

// var line = d3.svg.line()
//     .interpolate("basis")
//     .x(function(d) { return x(d.date); })
//     .y(function(d) { return y(d.day); });

// var svg = d3.select("#linechart").append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//   .append("g")
//     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


// d3.csv(average_lineChat_path + "/" + tsvFiles[value], function(error, data) {
//   if (error) throw error;

//   color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));

//   data.forEach(function(d) {
//     d.date = parseDate(d.date);
//   });

//   var indicators = color.domain().map(function(name) {
//     return {
//       name: name,
//       values: data.map(function(d) {
//         return {date: d.date, day: +d[name]};
//       })
//     };
//   });

//   x.domain(d3.extent(data, function(d) { return d.date; }));

//   y.domain([
//     d3.min(indicators, function(c) { return d3.min(c.values, function(v) { return v.day; }); }),
//     d3.max(indicators, function(c) { return d3.max(c.values, function(v) { return v.day; }); })
//   ]);

//   svg.append("g")
//       .attr("class", "x axis")
//       .attr("transform", "translate(0," + height + ")")
//       .call(xAxis);

//   svg.append("g")
//       .attr("class", "y axis")
//       .call(yAxis)
//     .append("text")
//       .attr("transform", "rotate(0)")
//       .attr("y", 6)
//       .attr("dy", ".100em")
//       .style("text-anchor", "end")
//       .text("day (d)");

//   var indicator = svg.selectAll(".indicator")
//       .data(indicators)
//       .enter().append("g")
//       .attr("class", "indicator");

//   indicator.append("path")
//       .attr("class", "line")
//       .attr("d", function(d) { return line(d.values); })
//       .style("stroke", function(d) { return color(d.name); });

//   indicator.append("text")
//       .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
//       .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.day) + ")"; })
//       .attr("x", 3)
//       .attr("dy", ".100em")
//       .text(function(d) { return d.name; });

// // var mouseG = svg.append("g")
// //       .attr("class", "mouse-over-effects");

// //     mouseG.append("path") // this is the black vertical line to follow mouse
// //       .attr("class", "mouse-line")
// //       .style("stroke", "black")
// //       .style("stroke-width", "1px")
// //       .style("opacity", "0");
      
// //     var lines = document.getElementsByClassName('line');

// //     var mousePerLine = mouseG.selectAll('.mouse-per-line')
// //       .data(cities)
// //       .enter()
// //       .append("g")
// //       .attr("class", "mouse-per-line");

// //     mousePerLine.append("circle")
// //       .attr("r", 7)
// //       .style("stroke", function(d) {
// //         return color(d.name);
// //       })
// //       .style("fill", "none")
// //       .style("stroke-width", "1px")
// //       .style("opacity", "0");

// //     mousePerLine.append("text")
// //       .attr("transform", "translate(10,3)");

// //     mouseG.append('svg:rect') // append a rect to catch mouse movements on canvas
// //       .attr('width', width) // can't catch mouse events on a g element
// //       .attr('height', height)
// //       .attr('fill', 'none')
// //       .attr('pointer-events', 'all')
// //       .on('mouseout', function() { // on mouse out hide line, circles and text
// //         d3.select(".mouse-line")
// //           .style("opacity", "0");
// //         d3.selectAll(".mouse-per-line circle")
// //           .style("opacity", "0");
// //         d3.selectAll(".mouse-per-line text")
// //           .style("opacity", "0");
// //       })
// //       .on('mouseover', function() { // on mouse in show line, circles and text
// //         d3.select(".mouse-line")
// //           .style("opacity", "1");
// //         d3.selectAll(".mouse-per-line circle")
// //           .style("opacity", "1");
// //         d3.selectAll(".mouse-per-line text")
// //           .style("opacity", "1");
// //       })
// //       .on('mousemove', function() { // mouse moving over canvas
// //         var mouse = d3.mouse(this);
// //         d3.select(".mouse-line")
// //           .attr("d", function() {
// //             var d = "M" + mouse[0] + "," + height;
// //             d += " " + mouse[0] + "," + 0;
// //             return d;
// //           });

// //         d3.selectAll(".mouse-per-line")
// //           .attr("transform", function(d, i) {
// //             console.log(width/mouse[0])
// //             var xDate = x.invert(mouse[0]),
// //                 bisect = d3.bisector(function(d) { return d.date; }).right;
// //                 idx = bisect(d.values, xDate);
            
// //             var beginning = 0,
// //                 end = lines[i].getTotalLength(),
// //                 target = null;

// //             while (true){
// //               target = Math.floor((beginning + end) / 2);
// //               pos = lines[i].getPointAtLength(target);
// //               if ((target === end || target === beginning) && pos.x !== mouse[0]) {
// //                   break;
// //               }
// //               if (pos.x > mouse[0])      end = target;
// //               else if (pos.x < mouse[0]) beginning = target;
// //               else break; //position found
// //             }
            
// //             d3.select(this).select('text')
// //               .text(y.invert(pos.y).toFixed(2));
              
// //             return "translate(" + mouse[0] + "," + pos.y +")";
// //           });



// });

// // }