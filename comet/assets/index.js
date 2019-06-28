// COMET v1.0.0

// CSS
import './w3.css';
import './style.css';

// Images
import './icon.svg';

// Dependencies
import $ from "jquery";

(function() {

  var app = {
    title: 'COMET',
    version: '1.0.0',
    previous_state: null
  };

  // Retruns current parameter values
  function getParamValues() {
    let params = {};
    $.each($('#app-params input'), (key, elem) => {
      params[elem.name] = elem.value;
    });
    return params;
  }

  $('.app-title').text(app.title);
  $('.app-version').text(app.version);

  $('#app-control button').prop('disabled', true);
  $('#app-params input').prop('disabled', true);

  $('#start').click(function() {
    $('button').prop('disabled', true);
    $('#app-params input').prop('disabled', true);
    $.post('/api/start', getParamValues(), function(response) {
    });
  });

  $('#stop').click(function() {
    $('#app-control button').prop('disabled', true);
    $.post('/api/stop', {}, function(response) {
    });
  });

  $('#pause').click(function() {
    $('#app-control button').prop('disabled', true);
    $('#pause').prop('disabled', true);
    $.post('/api/pause', {}, function(response) {
    });
  });

  setInterval(function() {
    $.getJSON('/api/status', function(response) {
      let state = response.app.status.state;
      let state_color = 'grey';
      if (state != app.previous_state) {
        $('#app-control button').prop('disabled', true);
        $('#app-params input').prop('disabled', true);
        $('.app-status').html(state);
        switch (state.toLowerCase()) {
          case 'halted':
            $('#start').prop('disabled', false);
            $('#app-params input').prop('disabled', false);
            state_color = 'green';
            break;
          case 'running':
            $('#stop').prop('disabled', false);
            $('#pause').prop('disabled', false).html('Pause');
            state_color = 'red';
            break;
          case 'paused':
            $('#stop').prop('disabled', false);
            $('#pause').prop('disabled', false).html('Continue');
            state_color = 'orange';
            break;
        }
        $('.app-status.w3-tag').css('background-color', state_color);
      }
      app.previous_state = state;
    });
  }, 250);

  // params

  $.getJSON('/api/params', function(response) {
    let params = response.app.params;
    let div = $('#app-params');
    $.each(params, (key, param) => {
      let box = $(`<div />`);
      div.append(box);
      let unit = param.unit ? ` [${param.unit}]` : '';
      box.append($(`<label for="param_${param.name}">${param.label}${unit}</label>`));
      let type = '';
      switch (param.type) {
        case 'int':
        case 'float':
          type = 'number';
          break;
        default:
          type = 'text';
          break;
      }
      box.append($(`<input id="param_${param.name}" class="w3-input" type="${type}" name="${param.name}" value="${param.value}"/>`));
    });
  });

  // devices

  $.getJSON('/api/devices', function(response) {
    let devices = response.app.devices;
    let ul = $('#app-devices');
    $.each(devices, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // collections

  $.getJSON('/api/collections', function(response) {
    let collections = response.app.collections;
    let ul = $('#app-collections');
    $.each(collections, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // procedures

  $.getJSON('/api/procedures', function(response) {
    let procedures = response.app.procedures;
    let ul = $('#app-procedures');
    $.each(procedures, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // processes

  $.getJSON('/api/processes', function(response) {
    let processes = response.app.processes;
    let ul = $('#app-processes');
    $.each(processes, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // settings

  $.getJSON('/api/settings', function(response) {
    let settings = response.app.settings;
    let ul = $('#app-settings');
    $.each(settings, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

})();
