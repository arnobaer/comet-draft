<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{ title|upper }}</title>
  <link rel=icon href=/assets/icon.svg sizes="any" type="image/svg+xml">
  <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
  <link rel="stylesheet" href="/assets/dygraph.css">
  <link rel="stylesheet" href="/assets/style.css">
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.6.9/angular.min.js"></script>
  <script src="/assets/dygraph.min.js"></script>
</head>
<body ng-app="comet">

  <!-- sticky header -->
  <div class="w3-container w3-top">
    <div class="w3-bar w3-theme">
      <div class="w3-content">
        <img id="logo" src="/assets/icon.svg" class="w3-left">
        <span class="w3-right w3-small w3-margin-top">Technical demonstrator application</span>
        <h3>{{ title|upper }}</h3>
      </div>
    </div>
  </div>

{% block content %}{% endblock %}

  <!-- footer -->
  <div class="w3-container w3-light-grey w3-margin-top">
    <div class="w3-content w3-text-grey">
      <p>Control &amp; Measurement Toolkit</p>
      <p>{{ title|upper }}, version {{ version }}</p>
    </div>
  </div>

  <script src="/assets/index.js"></script>
</body>
</html>
