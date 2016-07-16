
$(document).ready(function(){

  console.log("July 15 2016");
  var d = 0;
  var season = 0;
  var seasons =[0, 1, 2, 3, 4];
  var step = 1;
  var date = "";
  var steps = [1, 4, 4, 4, 4];
  var firstDates = [0, 1 , 2, 3 , 0];
  var lastDates = [63, 61, 62, 63, 60]; 


  var HEADER = ['ft_frozen', 'ft_thawed', 'ft_trans', 'ft_itrans',
   'fw_fw_06_swe_-3', 'fw_fw_06_swe_-2', 'fw_fw_06_swe_-1', 'fw_fw_06_swe_+1', 'fw_fw_06_swe_+2', 
   'swe_swe_average_-3', 'swe_swe_average_-2', 'swe_swe_average_-1', 'swe_swe_average_+1', 'swe_swe_average_+2', 
   'energy_sw_up_-3', 'energy_sw_up_-2',  'energy_sw_up_-1', 'energy_sw_up_+1', 'energy_sw_up_+2', 
   'energy_sw_dn_-3', 'energy_sw_dn_-2','energy_sw_dn_-1', 'energy_sw_dn_+1', 'energy_sw_dn_+2', 
   'energy_lw_up_-3', 'energy_lw_up_-2', 'energy_lw_up_-1', 'energy_lw_up_+1', 'energy_lw_up_+2', 
   'energy_lw_dn_-3', 'energy_lw_dn_-2','energy_lw_dn_-1', 'energy_lw_dn_+1', 'energy_lw_dn_+2'];

  var date_list = ['1991-12-01', '1992-03-01', '1992-06-01', '1992-09-01', '1992-12-01', '1993-03-01', '1993-06-01', '1993-09-01', '1993-12-01', 
  '1994-03-01', '1994-06-01', '1994-09-01', '1994-12-01', '1995-03-01', '1995-06-01', '1995-09-01', '1995-12-01', '1996-03-01', '1996-06-01', '1996-09-01', '1996-12-01', 
  '1997-03-01', '1997-06-01', '1997-09-01', '1997-12-01', '1998-03-01', '1998-06-01', '1998-09-01', '1998-12-01', '1999-03-01', '1999-06-01', '1999-09-01', '1999-12-01', 
  '2000-03-01', '2000-06-01', '2000-09-01', '2000-12-01', '2001-03-01', '2001-06-01', '2001-09-01', '2001-12-01', '2002-03-01', '2002-06-01', '2002-09-01', '2002-12-01', 
  '2003-03-01', '2003-06-01', '2003-09-01', '2003-12-01', '2004-03-01', '2004-06-01', '2004-09-01', '2004-12-01', '2005-03-01', '2005-06-01', '2005-09-01', '2005-12-01', 
  '2006-03-01', '2006-06-01', '2006-09-01', '2006-12-01', '2007-03-01', '2007-06-01', '2007-09-01', ""];

var n_cluster_list = [
  7, 3, 9, 4, 7, 4, 13, 2, 7, 4, 13, 4, 7, 2, 28, 2, 6, 3, 15, 4, 7, 3,
   12, 3, 11, 4, 21, 3, 9, 2, 9, 3, 8, 3, 21, 5, 7, 4,  11, 3, 7, 3, 9, 
   2, 9, 3, 20, 3, 9, 4, 18, 4, 11, 4, 12, 5, 7, 3, 6, 4, 5, 2, 5, 4,""];


var colors = ['#4B0082', '#FFD700', '#FF69B4', '#B22222', '#CD5C5C', '#87AE73', '#FFFF00', 
'#FFE4E1', '#556B2F', '#808000', '#8FBC8F', '#FFC0CB', '#FF6347', '#F08080', 
'#FF4500', '#FFDEAD', '#00FF00', '#98FB98', '#2F4F4F', '#ADFF2F', '#DEB887', 
'#FFF5EE', '#00FA9A', '#FF00FF', '#FFEFD5', '#FFEBCD', '#7FFF00', '#696969'];

 $('#date').text(date_list[0]);
 $('#clusterNum').text(n_cluster_list[0]);
 ShowMap(date_list[0]);


   $('.btn-lineChart').click(function(){

      $('#time-slider').removeClass('hidden');
      $('#map').html("");
      $('#linechart').html("");
      $('#barGraph').html("");
      var name = $(this).attr('name');
      $('#season-lineChart').text(name);
      season = parseInt($(this).val());
      d = firstDates[season]; 
      step = steps[season];
      date = date_list[d];
      $('#date').text(date);
      changeClusters(); 
      showAverageLinesChart(season);  

   });

$('.changeDate').click(function(){

  var f = $(this).val();
  switch(f) {
    case '0':
        d = firstDates[season];
        break;
    case '--':
        if(d > firstDates[season]){
           d = d - step; 
        }
        
        break;
    case '++':
        if( d < firstDates[season] ){
          d = d + step;
        }
        break;
    case '-1':
        d = lastDates[season];
        break;
}
  date = date_list[d];
  $('#date').text(date);
   changeClusters();  
});



function changeClusters(){

 $('#map').html('');
  ShowMap(date);
 $('#barGraph').html('');
 showBarGraph(date); 
  $('#histograms').html('');
  n_cluster = n_cluster_list[d];
  $('#clusterNum').text(n_cluster); 
  $('.cluster').addClass('hidden');
 for (var i = 0 ; i < n_cluster ; i++){
  var name = "#cluster_" + i ;
  $(name).removeClass('hidden');
 }
};



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