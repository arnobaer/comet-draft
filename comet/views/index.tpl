{% extends "base.tpl" %}
{% block content %}

  <div class="w3-container" ng-controller="status" style="margin-top: 72px !important;">
{% raw %}
    <div class="w3-content w3-light-gray w3-padding">
      <p>Mode: <strong>{{mode}}</strong></p>
      <p>Acquired samples: {{samples}}</p>
    </div>
    <div class="w3-content w3-margin-bottom">
      <div class="w3-theme w3-left" style="height: 1px;" ng-style="style"></div>
    </div>
{% endraw %}
  </div>

  <div class="w3-container">
    <div class="w3-content" ng-controller="control">
      <button class="w3-red w3-button" ng-click="start()" ng-hide="running">Start</button>
      <button class="w3-theme w3-button" ng-click="resetA()">Reset A</button>
      <button class="w3-theme w3-button" ng-click="resetB()">Reset B</button>
      <button class="w3-theme w3-button" ng-click="gain()">Gain</button>
      <button class="w3-red w3-button" ng-click="stop()" ng-show="running">Stop</button>
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
