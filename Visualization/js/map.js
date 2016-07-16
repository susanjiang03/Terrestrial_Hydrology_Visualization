function ShowMap(date){

var COLORS = ['#4B0082', '#FFD700', '#0000FF', '#B22222', '#CD5C5C', '#87AE73', '#FFFF00', '#FFE4E1','#556B2F', 
'#808000', '#8FBC8F', '#FFC0CB', '#FF6347', '#F08080', '#FF4500', '#FFDEAD', '#00FF00', '#98FB98', '#2F4F4F', 
'#ADFF2F', '#DEB887', '#FFF5EE', '#00FA9A', '#FF00FF', '#FFEFD5', '#FFEBCD', '#7FFF00', '#696969']

var  HEADER = ['ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans',
   'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
   'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
   'energy_sw_up_-3', 'energy_sw_up_-2',  'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
   'energy_sw_dn_-3', 'energy_sw_dn_-2','energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
   'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
   'energy_lw_dn_-3', 'energy_lw_dn_-2','energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2'];

var dataset;

var test = d3.csv( "./CSV/" + date+ ".csv", function(d) {
    return {

        "id": d.index,
        "start_date": d.start_date,
        "type": "Point",
        "clusterLabel": +d.clusterLabel,
        "coordinates": [+d.lon, +d.lat],
       "ft_frozen": +d.ft_frozen,  'ft_thawed': +d.ft_thawed, 'ft_trans':+d.ft_trans, 'ft_itrans': +d.ft_itrans,
    'fw_fw_06_swe_minus3': +d.fw_fw_06_swe_minus3, 'fw_fw_06_swe_minus2': +d.fw_fw_06_swe_minus2, 'fw_fw_06_swe_minus1': +d.fw_fw_06_swe_minus1, 
    'fw_fw_06_swe_plus1': +d.fw_fw_06_swe_plus1, 'fw_fw_06_swe_plus2': +d.fw_fw_06_swe_plus2, 'swe_swe_average_minus3': +d.swe_swe_average_minus3,
    'swe_swe_average_minus2': +d.swe_swe_average_minus2, 'swe_swe_average_minus1': +d.swe_swe_average_minus1, 'swe_swe_average_plus1': +d.swe_swe_average_plus1, 
    'swe_swe_average_plus2': +d.swe_swe_average_plus2, 'energy_sw_up_minus3': +d.energy_sw_up_minus3, 'energy_sw_up_minus2': +d.energy_sw_up_minus2, 
    'energy_sw_up_minus1': +d.energy_sw_up_minus1, 'energy_sw_up_plus1': +d.energy_sw_up_plus1, 'energy_sw_up_plus2': +d.energy_sw_up_plus2, 
   'energy_sw_dn_minus3': +d.energy_sw_dn_minus3, 'energy_sw_dn_minus2': +d.energy_sw_dn_minus2,'energy_sw_dn_minus1': +d.energy_sw_dn_minus1, 
   'energy_sw_dn_plus1': +d.energy_sw_dn_plus1, 'energy_sw_dn_plus2': +d.energy_sw_dn_plus2, 'energy_lw_up_minus3': +d.energy_lw_up_minus3,
    'energy_lw_up_minus2': +d.energy_lw_up_minus2, 'energy_lw_up_minus1': +d.energy_lw_up_minus1, 'energy_lw_up_plus1': +d.energy_lw_up_plus1, 
    'energy_lw_up_plus2': +d.energy_lw_up_plus2, 'energy_lw_dn_minus3': +d.energy_lw_dn_minus3, 'energy_lw_dn_minus2': +d.energy_lw_dn_minus2,
    'energy_lw_dn_minus1': +d.energy_lw_dn_minus1, 
    // 'energy_lw_dn_plus1': +d.energy_lw_dn_plus1, 
    'energy_lw_dn_plus2': +d.energy_lw_dn_plus2,

        
      

    };
    }, function(data) {
        dataset = data;
    }); 


var width = 1000,
    height = 700;

var projection = d3.geo.miller()
    .scale(153)
    .translate([width / 2, height / 2])
    .precision(.1);

var path = d3.geo.path()
    .projection(projection);


var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function(d) {
        return " <span style='color:#edf'><table>" +
    "<tr><th>lat: " + d.coordinates[0] + "</th><th> &nbsp;&nbsp;lon: " + d.coordinates[1] + "</th></tr>" +
    '<tr><td>t_frozen :</td><td>'  + d.ft_frozen + '</td></tr>' +  '<tr><td>ft_thawed :</td><td> ' + d.ft_thawed +   '</td></tr>' + 
    '<tr><td>ft_trans :</td><td>'+ d.ft_trans  + '</td></tr>' + '<tr><td>ft_itrans :</td><td>' + d.ft_itrans + '</td></tr>' +
    '<tr><td>t_frozen :</td><td>'  + d.ft_frozen + '</td></tr>' +  '<tr><td>ft_thawed :</td><td> ' + d.ft_thawed +   '</td></tr>' + 
    '<tr><td>fw_fw_06_swe_-3 :</td><td>' + d.fw_fw_06_swe_minus3 + '</td></tr>' + '<tr><td>fw_fw_06_swe_-2 : </td><td>' + d.fw_fw_06_swe_minus2 + '</td></tr>' + 
    '<tr><td>fw_fw_06_swe_-1 :</td><td>' + d.fw_fw_06_swe_minus1 + '</td></tr>' +  '<tr><td>fw_fw_06_swe_+1 :</td><td>' + d.fw_fw_06_swe_plus1 + '</td></tr>' + 
    '<tr><td>fw_fw_06_swe_+2 :</td><td>' + d.fw_fw_06_swe_plus2 + '</td></tr>' + '<tr><td>swe_swe_average_-3 :</td><td>' + d.swe_swe_average_minus3 + '</td></tr>' + 
    '<tr><td>swe_swe_average_-2 :</td><td>' + d.swe_swe_average_minus2 + '</td></tr>' +'<tr><td>swe_swe_average_-1 :</td><td>' + d.swe_swe_average_minus1 +  '</td></tr>' + 
    '<tr><td>swe_swe_average_+1 :</td><td>' + d.swe_swe_average_plus1 + '</td></tr>' + '<tr><td>swe_swe_average_+2 :</td><td>' + d.swe_swe_average_plus2 + '</td></tr>'+ 
    '<tr><td>energy_sw_up_-3 :</td><td>' + d.energy_sw_up_minus3 + '</td></tr>' + '<tr><td>energy_sw_up_-2 : </td><td>' + d.energy_sw_up_minus2 + '</td></tr>' + 
    '<tr><td>energy_sw_up_-1 :</td><td>' + d.energy_sw_up_minus1 + '</td></tr>' + '<tr><td>energy_sw_up_+1 :</td><td>' + d.energy_sw_up_plus1 + '</td></tr>' + 
    '<tr><td>energy_sw_up_+2 :</td><td>' + d.energy_sw_up_plus2 +  '</td></tr>' +  '<tr><td>energy_sw_dn_-3 :</td><td>' + d.energy_sw_dn_minus3 +  '</td></tr>' +  
    '<tr><td>energy_sw_dn_-2 :</td><td>' + d.energy_sw_dn_minus2 + '</td></tr>' + '<tr><td>energy_sw_dn_-1 :</td><td>' + d.energy_sw_dn_minus1 + '</td></tr>' + 
    '<tr><td>energy_sw_dn_+1 :</td><td>' + d.energy_sw_dn_plus1 + '</td></tr>' +  '<tr><td>energy_sw_dn_+2 :</td><td>' + d.energy_sw_dn_plus2 + '</td></tr>' + 
    '<tr><td>energy_lw_up_-3 :</td><td>' + d.energy_lw_up_minus3 + '</td></tr>' + '<tr><td>energy_lw_up_-2 :</td><td>' + d.energy_lw_up_minus2 + '</td></tr>' + 
    '<tr><td>energy_lw_up_-1 :</td><td>' + d.energy_lw_up_minus1 + '</td></tr>' +  '<tr><td>energy_lw_up_+1 :</td><td>' + d.energy_lw_up_plus1 + '</td></tr>' +   
    '<tr><td>energy_lw_up_+2 :</td><td>' + d.energy_lw_up_plus2 + '</td></tr>' +  '<tr><td>energy_lw_dn_-3 :</td><td>' + d.energy_lw_dn_minus3 + '</td></tr>' + 
     '<tr><td>energy_lw_dn_-2 :</td><td>' + d.energy_lw_dn_minus2 + '</td></tr>' +  '<tr><td>energy_lw_dn_-1 :</td><td>' + d.energy_lw_dn_minus1 + '</td></tr>' +
      // '<tr><td>energy_lw_dn_+1 :</td><td>' + d.energy_lw_dn_plus1,+ '</td></tr>' + 
       '<tr><td>energy_lw_dn_+2 :</td><td>' + d.energy_lw_dn_plus2 + '</td></tr>' +
       '<tr><td>cluster :</td><td>' + d.clusterLabel + '</td></tr>' +

    "</table></span>";



    })
var svg = d3.select("#map").append("svg")
    .attr("width", width)
    .attr("height", height)
    .call(tip);


d3.json("./js/world-50m.json", function(error, world) {
    if (error) throw error;

    svg.insert("path")
        .datum(topojson.feature(world, world.objects.land))
        .attr("class", "land")
        .attr("d", path);

    svg.insert("path")
        .datum(topojson.mesh(world, world.objects.countries, function(a, b) {
            return a !== b;
        }))
        .attr("class", "boundary")
        .attr("d", path);


    var points = svg.append("g");

    points.selectAll("path")
        .data(dataset)
        .enter()
        .append("path")
        .attr("fill", function(d,i){
            for(var k=0;k<34;k++){
                if(k === dataset[i]["clusterLabel"]){
                    return COLORS[k];
                }
            }
        })
        .style("fill-opacity", 0.2)
        .attr("stroke", "#999")
        .attr("stroke-width", 0.5)
        .style("stroke-opacity", 0.5)
        .attr("d", path)
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);



});

d3.select(self.frameElement).style("height", height + "px");

}