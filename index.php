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
          <a  class="dropdown-toggle h4" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false" value> Change by : &nbsp;&nbsp; <span id="season-lineChart" value="">  </span>  </a>
          <ul class="dropdown-menu">
          <li onclick="showAverageLinesChart(this.value)" value=0 class="btn-lineChart changeDate" name="All seasons"><a> All seasons </a></li>
           <li onclick="showAverageLinesChart(this.value)" value=1 class="btn-lineChart changeDate" name="Spring"><a> Spring </a></li>
             <li onclick="showAverageLinesChart(this.value)" value=2 class="btn-lineChart changeDate" name="Summer"><a > Summer </a></li>
             <li onclick="showAverageLinesChart(this.value)" value=3 class="btn-lineChart changeDate" name="Fall"> <a >Fall </a></li>
            <li onclick="showAverageLinesChart(this.value)" value=4 class="btn-lineChart changeDate" name="Winter"> <a> Winter</a></li>
          </ul>
        </div>
  </div>


<div class = "row col-lg-12">
 <div class="row col-lg-11" id="map">



</div>
<div  class = "col-lg-1" style="height:300px;" id="clusterLabels">

            <button id="cluster_0" class="btn hidden cluster" style="background-color:#4B0082;"></button>
            <button id="cluster_1" class="btn hidden cluster" style="background-color:#0000FF;"> </button>
            <button id="cluster_2" class="btn hidden cluster" style="background-color:#FF69B4;"></button>
            <button id="cluster_3" class="btn hidden cluster" style="background-color:#B22222;"></button>
            <button id="cluster_4" class="btn hidden cluster" style="background-color:#CD5C5C;"></button>
            <button id="cluster_5" class="btn hidden cluster" style="background-color:#87AE73;"></button>
            <button id="cluster_6" class="btn hidden cluster" style="background-color:#FFFF00;"> </button>
            <button id="cluster_7" class="btn hidden cluster" style="background-color:#FFE4E1;"></button>
            <button id="cluster_8" class="btn hidden cluster" style="background-color:#556B2F;"></button>
            <button id="cluster_9" class="btn hidden cluster" style="background-color:#808000;"></button>
            <button id="cluster_10" class="btn hidden cluster" style="background-color:#8FBC8F;"></button>
            <button id="cluster_11" class="btn hidden cluster" style="background-color:#FFC0CB;"></button>
            <button id="cluster_12" class="btn hidden cluster" style="background-color:#FF6347;"></button>
            <button id="cluster_13" class="btn hidden cluster" style="background-color:#F08080;"></button>
            <button id="cluster_14" class="btn hidden cluster" style="background-color:#FF4500;"></button>
            <button id="cluster_15" class="btn hidden cluster" style="background-color:#FFDEAD;"></button>
            <button id="cluster_16" class="btn hidden cluster" style="background-color:#00FF00;"></button>
            <button id="cluster_17" class="btn hidden cluster" style="background-color:#98FB98;"></button>
            <button id="cluster_18" class="btn hidden cluster" style="background-color:#2F4F4F;"></button>
            <button id="cluster_19" class="btn hidden cluster" style="background-color:#ADFF2F;"></button>
            <button id="cluster_20" class="btn hidden cluster" style="background-color:#DEB887;"></button>
            <button id="cluster_21" class="btn hidden cluster" style="background-color:#FFF5EE;"></button>
            <button id="cluster_22" class="btn hidden cluster" style="background-color:#00FA9A;"></button>
            <button id="cluster_23" class="btn hidden cluster" style="background-color:#FF00FF;"></button>
            <button id="cluster_24" class="btn hidden cluster" style="background-color:#FFEFD5;"></button>
            <button id="cluster_25" class="btn hidden cluster" style="background-color:#FFEBCD;"></button>
            <button id="cluster_26" class="btn hidden cluster" style="background-color:#7FFF00;"></button>
            <button tid="cluster_27" class="btn hidden cluster" style="background-color:#696969';"></button>


        </div>
</div>


 <div class="row col-lg-10 hidden" style ="height:5vh;" id="time-slider">
      <div class="col-lg-9" style="top:1vh;">
       <input type="range" id="myRange" value="64" min="0" max="64" step ="1" onchange="showValue(this.value)" class="changeDate">
      </div>

    <div class = "col-lg-3 ">
      <button  id ="goFirst" type="button" class="btn btn-default col-lg-3" value="0" onclick="firstDate(this.value);">
        <span class="glyphicon glyphicon-step-backward" aria-hidden="true"></span>
      </button>
      <button id = "goPrev"  ype="button" class="btn btn-default col-lg-3 changeDate" value="1" onclick="prevDate(this.value);">
        <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
      </button>

      <button id="goNext" type="button" class="btn btn-default col-lg-3 changeDate"  value="1" onclick="nextDate(this.value);">
        <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
      </button>

      <button id="goLast" type="button" class="btn btn-default col-lg-3 changeDate" value="63" onclick="lastDate(this.value);">
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