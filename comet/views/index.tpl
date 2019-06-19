{% extends "base.tpl" %}
{% block content %}

  <div class="w3-container" ng-controller="status" style="margin-top: 72px !important;">
{% raw %}
    <div class="w3-content w3-light-gray w3-padding">
      <p>State: <strong>{{state}}</strong></p>
      <p>Acquired samples: {{samples}}</p>
    </div>
    <div class="w3-content w3-margin-bottom">
      <div class="w3-theme w3-left" style="height: 1px;" ng-style="style"></div>
    </div>
{% endraw %}
  </div>

  <div class="w3-container">
    <div class="w3-content" ng-controller="control">
      <button id="api_start" class="w3-red w3-button" ng-click="start()" ng-hide="running">Start</button>
      <button id="api_stop" class="w3-red w3-button" ng-click="stop()" ng-show="running">Stop</button>

      <h3>Parameters</h3>
      <div id="controls">
{% for param in app.params.values() %}
      <div>
{% if param.is_numeric %}
        <script>$(function() {
          $( "#param_{{ param.name }}" ).spinner({
{% if param.step is not none %}
            step: {{ param.step }},
{% endif %}
{% if param.min is not none %}
            min: {{ param.min }},
{% endif %}
{% if param.max is not none %}
            max: {{ param.max }},
{% endif %}
            numberFormat: "n{{ param.prec or '0'}}"
          });
        });</script>
{% endif %}
        <label for="param_{{ param.name }}">{{ param.label }}</label><br>
        <input id="param_{{ param.name }}" {% if not param.required %}required{% endif %} {% if not param.is_numeric %}style="padding: 6px;" class="ui-spinner ui-corner-all ui-widget ui-widget-content" {% endif %}name="{{ param.name }}" value="{{ param.value }}">{% if param.unit %} [{{ param.unit }}]{% endif %}
      </div>
{% endfor %}
    </div>
    </div>
  </div>

  <div class="w3-container" id="comet_collections">
    <div class="w3-content">
      <h3>Collections</h3>
{% for k, v in app.collections.items() %}
      <div>{{ k }}: {{ v }}</div>
{% endfor %}
    </div>
  </div>

  <div class="w3-container" id="comet_states">
    <div class="w3-content" ng-controller="states">
      <h3>States</h3>
{% for k, proc in app.states.items() %}
      <div class="w3-bar w3-padding w3-grey" ng-class="">{{ proc.label}} {{ proc }}</div>
{% endfor %}
    </div>
  </div>

  <div class="w3-container" id="comet_attrs">
    <div class="w3-content">
      <h3>Attributes</h3>
{% for k, v in app.attrs.items() %}
      <div>{{ k }}: {{ v }}</div>
{% endfor %}
    </div>
  </div>

  <div class="w3-container">
    <div class="w3-content" ng-controller="measure">
      <div id="plot1"></div>
      <div id="plot2"></div>
      <div id="plot3"></div>
      <div id="plot4"></div>
    </div>
  </div>

  <div class="w3-container">
    <div class="w3-content" ng-controller="log">
{% raw %}
      <h4>Log</h4>
      <ul class="w3-ul w3-border">
        <li ng-repeat="item in items">
          {{item.ts|date:'yyyy-MM-dd HH:mm:ss Z'}} | {{item.message}}
        </li>
      </ul>
{% endraw %}
    </div>
  </div>

{% endblock %}
