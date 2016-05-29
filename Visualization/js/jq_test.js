
$(document).ready(function(){

  var HEADER = ['ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans',
   'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
   'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
   'energy_sw_up_-3', 'energy_sw_up_-2',  'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
   'energy_sw_dn_-3', 'energy_sw_dn_-2','energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
   'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
   'energy_lw_dn_-3', 'energy_lw_dn_-2','energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2'];

   var date_list = new Array('1991-12-01', '1992-03-01', '1992-06-01', '1992-09-01', '1992-12-01', '1993-03-01', '1993-06-01', '1993-09-01', '1993-12-01', 
  '1994-03-01', '1994-06-01', '1994-09-01', '1994-12-01', '1995-03-01', '1995-06-01', '1995-09-01', '1995-12-01', '1996-03-01', '1996-06-01', '1996-09-01', '1996-12-01', 
  '1997-03-01', '1997-06-01', '1997-09-01', '1997-12-01', '1998-03-01', '1998-06-01', '1998-09-01', '1998-12-01', '1999-03-01', '1999-06-01', '1999-09-01', '1999-12-01', 
  '2000-03-01', '2000-06-01', '2000-09-01', '2000-12-01', '2001-03-01', '2001-06-01', '2001-09-01', '2001-12-01', '2002-03-01', '2002-06-01', '2002-09-01', '2002-12-01', 
  '2003-03-01', '2003-06-01', '2003-09-01', '2003-12-01', '2004-03-01', '2004-06-01', '2004-09-01', '2004-12-01', '2005-03-01', '2005-06-01', '2005-09-01', '2005-12-01', 
  '2006-03-01', '2006-06-01', '2006-09-01', '2006-12-01', '2007-03-01', '2007-06-01', '2007-09-01', "")

var n_cluster_list = new Array(
  7, 3, 9, 4, 7, 4, 13, 2, 7, 4, 13, 4, 7, 2, 28, 2, 6, 3, 15, 4, 7, 3,
   12, 3, 11, 4, 21, 3, 9, 2, 9, 3, 8, 3, 21, 5, 7, 4,  11, 3, 7, 3, 9, 
   2, 9, 3, 20, 3, 9, 4, 18, 4, 11, 4, 12, 5, 7, 3, 6, 4, 5, 2, 5, 4,""
  )


var colors = ['#4B0082', '#FFD700', '#FF69B4', '#B22222', '#CD5C5C', '#87AE73', '#FFFF00', 
'#FFE4E1', '#556B2F', '#808000', '#8FBC8F', '#FFC0CB', '#FF6347', '#F08080', 
'#FF4500', '#FFDEAD', '#00FF00', '#98FB98', '#2F4F4F', '#ADFF2F', '#DEB887', 
'#FFF5EE', '#00FA9A', '#FF00FF', '#FFEFD5', '#FFEBCD', '#7FFF00', '#696969'];

	// drawMap('1991-12-01');
	 showValue(64);
  // showAverageLinesChart(0);
  // showBarGraph('1991-12-01');
  // showMap('1991-12-01');

//  for(var i = 0; i < 28;i++){


// $('#clusterLabels').append('<button id="cluster_'+ i + 'class="btn cluster" style="width:80%;background-color:' + colors[i]+ '";></button>');


//  }


// $(function() {
    
//     $('#clusterMap').mousemove(function(e) {
        
//         if(!this.canvas) {
//             this.canvas = $('<canvas />')[0];
//             this.canvas.width = this.width;
//             this.canvas.height = this.height;
//             this.canvas.getContext('2d').drawImage(this, 0, 0, this.width, this.height);
//         }
        
//         var pixelData = this.canvas.getContext('2d').getImageData(event.offsetX, event.offsetY, 1, 1).data;
        
//         $('#rgb').html('R:' + pixelData[0] + '<br>G:' + pixelData[1] + '<br>B:' + pixelData[2] );
//         // + ' A:' + pixelData[3]);
 
//     });
        
// });



// changeClusters();

function changeClusters(){

var date = $('#date').text();
$('#map').html('');
  showMap(date);
 $('#barGraph').html('');
 showBarGraph(date); 
  $('#histograms').html('');
var n_cluster = parseInt($('#clusterNum').text());
  $('.cluster').addClass('hidden');
 for (var i = 0 ; i < n_cluster ; i++){
  var name = "#cluster_" + i ;
  $(name).removeClass('hidden');
 }
}

// //
   $('.changeDate').click(function(){

   changeClusters();

   });


   $('.btn-lineChart').click(function(){

      $('#time-slider').removeClass('hidden');
      $('#linechart').html('');
      var name = $(this).attr('name');
      $('#season-lineChart').text(name);
      var steps = [1, 4, 4, 4, 4];
      var firstDates = [0, 1 , 2, 3 , 0];
      var lastDates = [63, 61, 62, 63, 60]; 
      var value = parseInt(this.value); 
      showBarGraph(date_list[value]);   
      showAverageLinesChart(value);   
      $('#goNext').val(steps[value]); 
      $('#goPrev').val(steps[value]);
      $('#goFirst').val(firstDates[value]);
      firstDate(firstDates[value]);
      $('#goLast').val(lastDates[value]);
      changeClusters();    

   });


    $('.cluster').click(function(){
    
    $('#histograms').html('');
    var date = $('#date').text();
    var button_id = $(this).attr('id');
    var cluster = parseInt(button_id.split("_")[1]);
    // $('#date').text("./HISTOGRAM/" + date + "-" + cluster + "-0.csv");
  
    for (var i = 0; i < 34; i++){
      showHistograms(date, cluster, i);
    }
  
});


$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})
 

});