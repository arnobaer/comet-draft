// COMET v1.0.0

import './w3.css';
import $ from "jquery";

(function() {

  let title = 'COMET APP';
  $('title').text(title);

  var previous_state = null;

  $('#app-control button').addClass('w3-blue').prop('disabled', true);

  $('#start').click(function() {
    $('button').prop('disabled', true);
    $('#app-params input').prop('disabled', true);
    $.post('/api/start', function(response) {
    });
  });

  $('#stop').click(function() {
    $('#app-control button').prop('disabled', true);
    $.post('/api/stop', function(response) {
    });
  });

  $('#pause').click(function() {
    $('#app-control button').prop('disabled', true);
    $('#pause').prop('disabled', true);
    $.post('/api/pause', function(response) {
    });
  });

  setInterval(function() {
    $.getJSON('/api/status', function(response) {
      let state = response.app.status.state;
      if (state != previous_state) {
        $('#app-control button').prop('disabled', true);
        $('.comet-status').html(state);
        switch (state.toLowerCase()) {
          case 'halted':
            $('#start').prop('disabled', false);
            $('#app-params input').prop('disabled', false);
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

  // params

  $.getJSON('/api/params', function(response) {
    let params = response.app.params;
    let div = $('#app-params');
    $.each(params, (key, param) => {
      let div2 = div.append($('<div />'));
      let unit = param.unit ? ` [${param.unit}]` : '';
      div2.append($(`<label for="param_${param.name}">${param.label}${unit}</label>`));
      let type = 'text';
      switch (param.type) {
        case 'int':
        case 'float':
          type = 'number';
          break;
        default:
          break;
      }
      div2.append($(`<input id="param_${param.name}" class="w3-input" type="${type}" value="${param.value}"/>`));
    });
  });

  // devices

  $.getJSON('/api/devices', function(response) {
    let devices = response.app.devices;
    let ul = $('#app-devices ul');
    $.each(devices, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // collections

  $.getJSON('/api/collections', function(response) {
    let collections = response.app.collections;
    let ul = $('#app-collections ul');
    $.each(collections, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // procedures

  $.getJSON('/api/procedures', function(response) {
    let procedures = response.app.procedures;
    let ul = $('#app-procedures ul');
    $.each(procedures, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // processes

  $.getJSON('/api/processes', function(response) {
    let processes = response.app.processes;
    let ul = $('#app-processes ul');
    $.each(processes, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // settings

  $.getJSON('/api/settings', function(response) {
    let settings = response.app.settings;
    let ul = $('#app-settings ul');
    $.each(settings, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

})();
