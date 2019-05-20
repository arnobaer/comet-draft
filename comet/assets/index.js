var app = angular.module("comet", []);

app.service('statusService', function($http, $interval) {
  var data = { running: false };
  $interval(function() {
    $http.get("/api/status").then(function(response) {
      data = response.data;
    });
  }, 1000);
  this.data = function() {
    data.running = data.mode == 'running';
    return data;
  }
  this.toggle = function() {
    data.running = !data.running;
  }
});

app.controller("status", function($scope, $http, $interval, statusService) {
  $interval(function() {
    var data = statusService.data();
    $scope.mode = data.mode;
    $scope.running = data.mode == 'running';
    $scope.samples = data.samples;
  }, 500);
});

app.controller("control", function($scope, $http, $interval, statusService) {
  $scope.start = function() {
    $http.post("/api/toggle");
    statusService.toggle();
  };
  $scope.stop = function() {
    $http.post("/api/toggle");
    statusService.toggle();
  };
  $scope.resetA = function() {
    $http.post("/api/reset/a");
  };
  $scope.resetB = function() {
    $http.post("/api/reset/b");
  };
  $scope.gain = function() {
    $http.post("/api/gain");
  };
  $interval(function() {
    var data = statusService.data();
    $scope.running = data.running;
  }, 500);
});

app.controller("measure", function($scope, $http, $interval) {
  // Create plot 1
  $scope.plot1 = new Dygraph(
    document.getElementById("plot1"),
    [],
    {
      title: "50 samples",
      labels: ["x", "temp", "humid", "A", "B"]
    }
  );
  $interval(function() {
    $http.get("/api/latest/50").then(function(response) {
      $scope.plot1.updateOptions( { 'file': response.data.data } );
    });
  }, 1000);
  // Create plot 2
  $scope.plot2 = new Dygraph(
    document.getElementById("plot2"),
    [],
    {
      legend: "always",
      title: "100 samples",
      labels: ["x", "temp", "humid", "A", "B"],
      xlabel: "time",
    }
  );
  $interval(function() {
    $http.get("/api/latest/100").then(function(response) {
      $scope.plot2.updateOptions( { 'file': response.data.data } );
    });
  }, 2000);
  // Create plot 3
  $scope.plot3 = new Dygraph(
    document.getElementById("plot3"),
    [],
    {
      title: "200 samples",
      labels: ["x", "temp", "humid", "A", "B"]
    }
  );
  $interval(function() {
    $http.get("/api/latest/200").then(function(response) {
      $scope.plot3.updateOptions( { 'file': response.data.data } );
    });
  }, 4000);
  // Create plot 4
  $scope.plot4 = new Dygraph(
    document.getElementById("plot4"),
    [],
    {
      title: "400 samples",
      labels: ["x", "temp", "humid", "A", "B"]
    }
  );
  $interval(function() {
    $http.get("/api/latest/400").then(function(response) {
      $scope.plot4.updateOptions( { 'file': response.data.data } );
    });
  }, 8000);
});

app.controller("log", function($scope, $http, $interval) {
  var ms = 1000;
  $interval(function() {
    $http.get("/api/log").then(function(response) {
      var log = response.data.log;
      // Convert UNIX timestamp to date time object
      log.forEach(function(value) {
        value.ts = new Date(value.ts * 1000);
      });
      $scope.items = log;
    });
  }, ms);
});