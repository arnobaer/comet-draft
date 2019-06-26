// COMET v1.0.0

import './w3.css';
import $ from "jquery";

(function() {

  let title = 'COMET APP';
  $('title').text(title);

  var previous_state = null;

  $('#ctrl button').addClass('w3-blue').prop('disabled', true);

  $('#start').click(function() {
    $('button').prop('disabled', true);
    $.post('/api/start', function(response) {
    });
  });

  $('#stop').click(function() {
    $('#ctrl button').prop('disabled', true);
    $.post('/api/stop', function(response) {
    });
  });

  $('#pause').click(function() {
    $('#ctrl button').prop('disabled', true);
    $('#pause').prop('disabled', true);
    $.post('/api/pause', function(response) {
    });
  });

  setInterval(function() {
    $.getJSON('/api/status', function(response) {
      let state = response.state;
      if (state != previous_state) {
        $('#ctrl button').prop('disabled', true);
        $('.comet-status').html(state);
        switch (state.toLowerCase()) {
          case 'halted':
            $('#start').prop('disabled', false);
            break;
          case 'running':
            $('#stop').prop('disabled', false);
            $('#pause').prop('disabled', false).html('Pause');
            break;
          case 'paused':
            $('#stop').prop('disabled', false);
            $('#pause').prop('disabled', false).html('Continue');
            break;
        }
      }
      previous_state = state;
    });
  }, 250);

})();
