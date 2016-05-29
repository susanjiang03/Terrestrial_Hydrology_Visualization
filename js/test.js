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

function drawMap(date){

     var canvas = document.getElementById('clusterMap');
      var context = canvas.getContext('2d');
      var imageObj = new Image();

      imageObj.onload = function() {
        context.drawImage(imageObj, 0,0);
      };
      imageObj.src = './Maps/' + date + '.jpg';

}


drawMap('1991-12-01');


function showValue(newValue)
{ 
   var newDate = date_list[newValue];
  document.getElementById("date").innerHTML  = newDate;
   var n_cluster_ = n_cluster_list[newValue];
document.getElementById("clusterNum").innerHTML  = n_cluster_;
// drawMap(newDate);
 document.getElementById("map").innerHTML = "";
showMap(newDate);

}

function prevDate(step) {

    document.getElementById("myRange").stepDown(step);
     var newValue =  parseInt(document.getElementById("myRange").value);
     showValue(newValue);
}

function nextDate(step) {

    document.getElementById("myRange").stepUp(step); 
     var newValue =  parseInt(document.getElementById("myRange").value);
      showValue(newValue);
}


function firstDate(date){
document.getElementById("myRange").value = date;
showValue(date);
}

function lastDate(date){
document.getElementById("myRange").value = date;
 showValue(date);
}



