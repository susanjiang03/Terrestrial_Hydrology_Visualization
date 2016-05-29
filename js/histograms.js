
// var HISTOGRAMDATA_DIR = './HISTOGRAMS/'

    function showHistograms(date,cluster,variable){

    // var csvFile = "./HISTOGRAMS/" + date + "-" + cluster + "-" + variable + ".csv";

          var HEADER = ['ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans',
   'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
   'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
   'energy_sw_up_-3', 'energy_sw_up_-2',  'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
   'energy_sw_dn_-3', 'energy_sw_dn_-2','energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
   'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
   'energy_lw_dn_-3', 'energy_lw_dn_-2','energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2'];   

function parser(d) {
    d.pDays = +d.Days;
    return d;
}

function Dayshist(csvdata) {
    var binsize = 5;
    var minbin = 0;
    var maxbin = 95;
    var numbins = (maxbin - minbin) / binsize;

    // whitespace on either side of the bars in units of Days
    var binmargin = 0.3; 
    var margin = {top: 20, right: 5, bottom: 30, left: 40};
    var width = 160 - margin.left - margin.right;
    var height = 120 - margin.top - margin.bottom;

    // Set the limits of the x axis
    var xmin = minbin - 1
    var xmax = maxbin + 1

    histdata = new Array(numbins);
    for (var i = 0; i < numbins; i++) {
    histdata[i] = { numfill: 0, meta: "" };
  }

  // Fill histdata with y-axis values and meta data
    csvdata.forEach(function(d) {
    var bin = Math.floor((d.pDays - minbin) / binsize);
    if ((bin.toString() != "NaN") && (bin < histdata.length)) {
      histdata[bin].numfill += 1;
      histdata[bin].meta += "<tr><td>" +  d.pDays.toFixed(0) + " days</td></tr>";
    }
    // d.num = histdata[bin].numfill;

    });

    // This scale is for determining the widths of the histogram bars
    // Must start at 0 or else x(binsize a.k.a dx) will be negative
    var x = d3.scale.linear()
    .domain([0, (xmax - xmin)])
    .range([0, width])
    // Scale for the placement of the bars
    var x2 = d3.scale.linear()
    .domain([xmin, xmax])
    .range([0, width]);
  
    var y = d3.scale.linear()
    .domain([0, d3.max(histdata, function(d) { 
            return d.numfill; 
            })])
    .range([height, 0]);

    var xAxis = d3.svg.axis()
    .scale(x2)
    .orient("bottom");
    var yAxis = d3.svg.axis()
    .scale(y)
    .ticks(8)
    .orient("left");

    var tip = d3.tip()
    .attr('class', 'd3-tip')
    .direction('e')
    .offset([0, 20])
    .html(function(d) {

      return '<table id="tiptable">' + d.meta + "</table>";
  });

    // put the graph in the "Days" div
    var svg = d3.select("#histograms").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + 
            margin.top + ")");

    svg.call(tip);

    // set up the bars
    var bar = svg.selectAll(".bar")
    .data(histdata)
    .enter().append("g")
    .attr("class", "bar")
    .attr("transform", function(d, i) { return "translate(" + 
         x2(i * binsize + minbin) + "," + y(d.numfill) + ")"; })
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

    // add rectangles of correct size at correct location
    bar.append("rect")
    .attr("x", x(binmargin))
    .attr("width", x(binsize - 2 * binmargin))
    .attr("height", function(d) { return height - y(d.numfill); });

    // add the x axis and x-label
    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);
    svg.append("text")
    .attr("class", "xlabel")
    .attr("text-anchor", "middle")
    .attr("x", width / 2)
    .attr("y", height + margin.bottom)
    .text(variable + " : " + HEADER[variable]);

    // add the y axis and y-label
    svg.append("g")
    .attr("class", "y axis")
    .attr("transform", "translate(0,0)")
    .call(yAxis);
    svg.append("text")
    .attr("class", "ylabel")
    .attr("y", 0 - margin.left) // x and y switched due to rotation
    .attr("x", 0 - (height / 2))
    .attr("dy", "1em")
    // .attr("transform", "rotate(-90)")
    // .style("text-anchor", "middle")
    // .text("");
}

// for(var i = 0; i < 34; i++){
// Read in .csv data and make graph
d3.csv("./HISTOGRAMS/" + date +"-" + cluster + "-"+ variable + ".csv", parser,
       function(error, csvdata) {
     Dayshist(csvdata);
});
// }



}
