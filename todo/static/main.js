(function () {
  'use strict';

  angular.module('ToDo', [])

  .controller('ToDoController', ['$scope', '$log', '$http',
    function($scope, $log, $http) {
      var suc = function(results) {
            $scope.shit = results
          }

      var err = function(error) {
            $log.log(error);
          }

      $scope.listAll= function() {
        $http.get('/list').
          success(suc).
          error(err);
      };
      $scope.addTask= function() {
        var task = $scope.task;
        $http.post('/add', {"task": task}).
          success(suc).
          error(err);
      };
      $scope.action= function(addr,id) {
        $http.post(addr, {"id": id}).
          success(suc).
          error(err);
      };
    }
  ]);

}());