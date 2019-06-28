// COMET v1.0.0

// CSS
import './w3.css';
import './style.css';

// Images
import './icon.svg';

// Dependencies
import Dygraph from 'dygraphs';
import $ from 'jquery';

$(document).ready(() => {

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

  function updateParams() {
    $.getJSON('/api/params', (response) => {
      let params = response.app.params;
      $.each(params, (key, param) => {
        $(`#app-params input[name=${param.name}]`).val(param.value);
      });
    });
  }

  function updateActiveJob(activeJobs) {
    $('.app-active-job').html('None');
    $('.app-active-job-percent').html((0.00).toFixed(2));
    if (activeJobs.length) {
      $('.app-active-job').html(activeJobs[0][0]);
      $('.app-active-job-percent').html(activeJobs[0][1].toFixed(2));
    }
  }

  $('.app-title').text(app.title);
  $('.app-version').text(app.version);

  $('#app-control button').prop('disabled', true);
  $('#app-params input').prop('disabled', true);

  $('#start').click(() => {
    $('button').prop('disabled', true);
    $('#app-params input').prop('disabled', true);
    $.post('/api/start', getParamValues(), function(response) {
    });
  });

  $('#stop').click(() => {
    $('#app-control button').prop('disabled', true);
    $.post('/api/stop', {}, function(response) {
    });
  });

  $('#pause').click(() => {
    $('#app-control button').prop('disabled', true);
    $('#pause').prop('disabled', true);
    $.post('/api/pause', {}, function(response) {
    });
  });

  setInterval(() => {
    $.getJSON('/api/status', response => {
      $('body').show();
      let state = response.app.status.state;
      let state_color = 'grey';
      updateActiveJob(response.app.status.active_jobs);
      if (state != app.previous_state) {
        $('#app-control button').prop('disabled', true);
        $('#app-params input').prop('disabled', true);
        $('.app-status').html(state);
        updateParams();
        switch (state.toLowerCase()) {
          case 'halted':
            $('#start').prop('disabled', false);
            $('#app-params input').prop('disabled', false);
            state_color = 'green';
            break;
          case 'configure':
            $('#stop').prop('disabled', false);
            $('#pause').prop('disabled', false);
            state_color = 'orange';
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
    }).fail(response => {
      $('body').hide();
    });
  }, 250);

  // params

  $.getJSON('/api/params', response => {
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

  $.getJSON('/api/devices', response => {
    let devices = response.app.devices;
    let ul = $('#app-devices');
    $.each(devices, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // collections

  $.getJSON('/api/collections', response => {
    let collections = response.app.collections;
    let ul = $('#app-collections');
    $.each(collections, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // jobs

  $.getJSON('/api/jobs', response => {
    let jobs = response.app.jobs;
    let ul = $('#app-jobs');
    $.each(jobs, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // services

  $.getJSON('/api/services', response => {
    let services = response.app.services;
    let ul = $('#app-services');
    $.each(services, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // settings

  $.getJSON('/api/settings', response => {
    let settings = response.app.settings;
    let ul = $('#app-settings');
    $.each(settings, (key, value) => ul.append($("<li />").text(`${key}: ${value}`)));
  });

  // dygraphs

  $.getJSON('/api/collections', response => {
    let collections = response.app.collections;
    // create graph panels
    $.each(collections, (key, name) => {
      let graph = $(`<div id="dygraph_${name}" style="width:100%; height:300px;" />`);
      let content = $(`<div class="w3-container app-panel-content" />`);
      content.append(graph);
      let header = $(`<header class="w3-panel w3-light-grey w3-padding w3-margin-top">${name}</header>`);
      let panel = $(`<div class="w3-card" />`);
      panel.append(header);
      panel.append(content);
      $('#app-panels').append(panel);
    });
    // create graph objects
    var graphs = [];
    $.each(collections, (key, name) => {
      var offset = 0;
      var data = [];
      var g = new Dygraph(document.getElementById(`dygraph_${name}`), data, {
        drawPoints: true,
        labels: ['Time', 'Temp', 'Humid']
      });
      // creat update method
      graphs.push(() => {
        $.getJSON(`/api/collections/${name}/data/offset/${offset}`, response => {
          if (response.app.collection.size < offset) {
            offset = 0;
            data = [];
            return;
          }
          $.each(response.app.collection.records, (key, value) => {
            data.push([new Date(value[0]*1000), value[1], value[2]]); // TODO expose matrics!
          });
          g.updateOptions( { 'file': data } );
          offset += response.app.collection.records.length;
        });
      });
    });
    // syncronious graph update
    setInterval(() => {
      $.each(graphs, (key, graph) => {
        graph();
      });
    }, 1000);
  });

});
