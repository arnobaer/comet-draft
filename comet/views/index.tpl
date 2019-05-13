{% extends "base.tpl" %}
{% block content %}

  <div class="w3-container" style="margin-top: 72px !important;">
{% raw %}
    <div class="w3-content w3-light-gray w3-padding w3-margin-bottom" ng-controller="status">
      <p>Mode: <strong>{{mode}}</strong></p>
      <p>Acquired samples: {{samples}}</p>
      <p>Samples in-memory size: {{memory}}</p>
    </div>
{% endraw %}
  </div>

  <div class="w3-container">
    <div class="w3-content" ng-controller="control">
      <button class="w3-theme w3-button" ng-click="toggle()">Start/Stop</button>
      <button class="w3-theme w3-button" ng-click="resetA()">Reset A</button>
      <button class="w3-theme w3-button" ng-click="resetB()">Reset B</button>
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
