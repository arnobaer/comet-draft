<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{title|upper}}</title>
  <link rel=icon href=/assets/icon.svg sizes="any" type="image/svg+xml">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <link rel="stylesheet" href="/assets/dygraph.css">
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.9/angular.min.js"></script>
  <script src="/assets/dygraph.min.js"></script>
</head>
<body ng-app="comet">

  <div class="w3-container">
    <img src="/assets/icon.svg" class="w3-left w3-margin-top w3-margin-right" style="width:48px;">
    <h3>{{title|upper}}</h3>
{% raw %}
    <div ng-controller="status">
      <p>Mode: {{mode}}</p>
    </div>
{% endraw %}
  </div>

  <div class="w3-container">
    <div ng-controller="control">
      <button class="w3-blue w3-button" ng-click="toggle()">Start/Stop</button>
      <button class="w3-blue w3-button" ng-click="resetA()">Reset A</button>
      <button class="w3-blue w3-button" ng-click="resetB()">Reset B</button>
    </div>
  </div>

  <div class="w3-container">
    <div ng-controller="measure">
      <div id="plot1"></div>
      <div id="plot2"></div>
      <div id="plot3"></div>
      <div id="plot4"></div>
    </div>
  </div>

  <div class="w3-container">
    <h4>Log</h4>
{% raw %}
    <div ng-controller="log">
      <ul class="w3-ul w3-border">
        <li ng-repeat="item in items">
          {{item.ts|date:'yyyy-MM-dd HH:mm:ss Z'}} | {{item.message}}
        </li>
      </ul>
    </div>
{% endraw %}
  </div>

  <script src="/assets/index.js"></script>
</body>
</html>
