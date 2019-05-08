<!DOCTYPE html>
<html>
<meta charset="utf-8">
<title>COMET</title>
<script src="https://www.w3schools.com/lib/w3.js"></script>
<script src="/static/dygraph.min.js"></script>
<link rel="stylesheet" href="/static/dygraph.min.css" />
<body>
  <div id="graphdiv1"></div>
  <div id="graphdiv2"></div>
  <div id="graphdiv3"></div>
  <div id="graphdiv4"></div>

  <script type="text/javascript">
  function createPlot(id, samples, interval) {
    w3.getHttpObject("/api/latest/" + samples, initPlot);
    function initPlot(data) {
      var g = new Dygraph(
        // containing div
        document.getElementById(id),
        data.data,
        {
          labels: [ "x", "foo", "bar" ],
        });
      this.interval = setInterval(function() {
        w3.getHttpObject("/api/latest/" + samples, updateData);
        function updateData(d) {
          g.updateOptions( { 'file': d.data } );
          }
        }, interval);
      }
    }
    createPlot("graphdiv1", 50, 1000);
    createPlot("graphdiv2", 100, 2000);
    createPlot("graphdiv3", 200, 3000);
    createPlot("graphdiv4", 400, 4000);
  </script>
</body>
</html>
