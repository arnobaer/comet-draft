<!DOCTYPE html>
<html>
<meta charset="utf-8">
<title>COMET</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
<script src="https://www.w3schools.com/lib/w3.js"></script>
<script src="/static/dygraph.min.js"></script>
<link rel="stylesheet" href="/static/dygraph.min.css" />
<body>
  <h3>COMET</h3>
  <p>Mode: <span id="mode"></span></p>
  <p><button id="start_stop">Start/Stop</button></p>
  <p><button id="reset_bar">Reset bar</button></p>
  <p><button id="reset_baz">Reset baz</button></p>

  <div id="graphdiv1"></div>
  <div id="graphdiv2"></div>
  <div id="graphdiv3"></div>
  <div id="graphdiv4"></div>

  <h4>Log</h4>
  <div id="log"><div>

  <script type="text/javascript">
  var mode;

  function createPlot(id, samples, interval) {
    w3.getHttpObject("/api/latest/" + samples, initPlot);
    function initPlot(data) {
      var g = new Dygraph(
        // containing div
        document.getElementById(id),
        data.data,
        {
          labels: [ "x", "A", "B", "bar", "baz" ],
        });
      this.interval = setInterval(function() {
        if (mode == 'running') {
          w3.getHttpObject("/api/latest/" + samples, updateData);
          function updateData(d) {
            g.updateOptions( { 'file': d.data } );
            }
          }
        }, interval);
      }
    }
    createPlot("graphdiv1", 50, 1000);
    createPlot("graphdiv2", 100, 2000);
    createPlot("graphdiv3", 200, 3000);
    createPlot("graphdiv4", 400, 4000);
    window.interval = setInterval(function() {
      w3.getHttpObject("/api/status", updateData);
      function updateData(d) {
        mode = d.mode;
        document.getElementById('mode').innerHTML = mode;
        }
      }, 1000);

    // buttons
    $('#start_stop').click(function() {
      $.post('/api/start_stop', function() {
          $('#log').append("<div>start/stop triggered</div>");
        }
      );
    });
    $('#reset_bar').click(function() {
      $.post('/api/reset/bar', function() {
          $('#log').append("<div>resetted bar</div>");
        }
      );
    });
    $('#reset_baz').click(function() {
      $.post('/api/reset/baz', function() {
          $('#log').append("<div>resetted baz</div>");
        }
      );
    });
  </script>
</body>
</html>
