<!--
User Profile Sidebar by @keenthemes
A component of Metronic Theme - #1 Selling Bootstrap 3 Admin Theme in Themeforest: http://j.mp/metronictheme
Licensed under MIT
-->
<!doctype html>
<html lang="en">
   <head>
      <meta charset="utf-8">
      <title> Terrestrial  Hydrology Visualization </title>

        <script src="//code.jquery.com/jquery-1.10.2.js"></script>
        <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
        <script src="./bootstrap-3.3.6-dist/js/bootstrap.min.js"></script>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">

        <link rel="stylesheet" href="./bootstrap-3.3.6-dist/css/bootstrap.min.css">
        <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css" rel="stylesheet">
         <link href="./css/test.css" rel="stylesheet">

        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.0/jquery.min.js"></script>
        <link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
        <script src="//code.jquery.com/jquery-1.10.2.js"></script>
        <script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>

        <script src="//d3js.org/d3.v3.min.js"></script>
        <script src="https://d3js.org/d3.geo.projection.v0.min.js"></script>
        <script src="http://labratrevenge.com/d3-tip/javascripts/d3.tip.v0.6.3.js"></script>
        <script src ="https://d3js.org/topojson.v1.min.js"></script>
         <script src="./js/index.js"></script>

        <script type='text/javascript' src='./js/jq_test.js'></script>
        <script type='text/javascript' src='./js/test.js'></script>
        <!-- <script type='text/javascript' src='./js/d3Graphs.js'></script> -->

        <script src="./js/lineChart.js"> </script>
        <script src="./js/histograms.js"></script>
        <script src="./js/bar.js"></script>

        <script src="./js/map.js"></script>

     
   
</head>

<body>

<nav class="navbar navbar-inverse">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
        <span class="sr-only">Toggle navigation</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#"> Home </a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse " id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="dropdown ">
          <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false"> Mean Shift Clustering  <span class="caret"></span></a>
          <ul class="dropdown-menu">
            <li><a href="#"> Histogram </a></li>
<!--             <li><a href="#">Another action</a></li>
            <li><a href="#">Something else here</a></li>
            <li role="separator" class="divider"></li>
            <li><a href="#">Separated link</a></li>
            <li role="separator" class="divider"></li>
            <li><a href="#">One more separated link</a></li> -->
          </ul>
        </li>
      </ul>
      <form class="navbar-form navbar-left" role="search">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Search">
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>
      
  </div><!-- /.container-fluid -->
</nav>



<div class ="container col-lg-10 col-lg-offset-1" >
  <div class="col-lg-12"> 
    <div class="col-lg-3 h4 middle"> Date : &nbsp;&nbsp;<span id="date">  </span></div>
    <div class="col-lg-4 h4 middle"> Estimated number of clusters :  <span id="clusterNum" class = ""> </span></div>

    <div class="dropdown col-lg-3" style="top:1vh">
          <a  class="dropdown-toggle h4 btn btn-primary btn-block" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false" value> Change by : &nbsp;&nbsp; <span id="season-lineChart" value="">  </span>  </a>
          <ul class="dropdown-menu">
          <li  value=0 class="season" name="All seasons"><a> All seasons </a></li>
           <li  value=1 class="season" name="Spring"><a> Spring </a></li>
             <li  value=2 class="season" name="Summer"><a > Summer </a></li>
             <li value=3 class="season" name="Fall"> <a >Fall </a></li>
            <li   value=4 class="season" name="Winter"> <a> Winter</a></li>
          </ul>
        </div>
  </div>


<div class = "row col-lg-12">
 <div class="row col-lg-11" id="map">



</div>
<div  class = "col-lg-1" style="height:300px;" id="clusterLabels">

<?php

$colors = ['#4B0082', '#FFD700', '#FF69B4', '#B22222', '#CD5C5C', '#87AE73', '#FFFF00', 
'#FFE4E1', '#556B2F', '#808000', '#8FBC8F', '#FFC0CB', '#FF6347', '#F08080', 
'#FF4500', '#FFDEAD', '#00FF00', '#98FB98', '#2F4F4F', '#ADFF2F', '#DEB887', 
'#FFF5EE', '#00FA9A', '#FF00FF', '#FFEFD5', '#FFEBCD', '#7FFF00', '#696969'];

for($i = 0; $i < sizeof($colors); $i++){

  echo '<button id="cluster_'.$i.'" class="btn hidden cluster" style="background-color:'.$colors[$i].'" data-toggle="tooltip" data-placement="right" title="cluster 0"></button>';
}

?>

        </div>
</div>


 <div class="row col-lg-10 hidden" style ="height:5vh;" id="time-slider">
      <div class="col-lg-9" style="top:1vh;">
       <input type="range" id="myRange" value="64" min="0" max="64" step ="1" onchange="showValue(this.value)" class="changeDate">
      </div>

    <div class = "col-lg-3 ">
      <button type="button" class="changeDate btn btn-default col-lg-3" value="0">
        <span class="glyphicon glyphicon-step-backward" aria-hidden="true"></span>
      </button>
      <button type="button" class="changeDate btn btn-default col-lg-3 changeDate" value="--">
        <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
      </button>

      <button  type="button" class="changeDate  btn btn-default col-lg-3 changeDate"  value="++">
        <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
      </button>

      <button type="button" class="changeDate btn btn-default col-lg-3 changeDate" value="-1">
        <span class="glyphicon glyphicon-step-forward" aria-hidden="true"></span>
      </button>
    </div>
  </div>




 <div class="col-lg-12" id="barGraph">

</div>



  <div class= "" id="linechart">

    </div>


<div class ="col-lg-12" id="histograms">

</div> 

 </div> <!-- end of container -->

</body>

</html>