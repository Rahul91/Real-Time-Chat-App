var mainApp = angular.module("mainApp");
mainApp.controller("loginController", function ($scope, $rootScope, loginService, $localStorage) {
    $scope.login = function (username, password) {
        var result = loginService.validate(username, password)
        result.then(function(response) {
                    $localStorage.token = response.data;
                    console.log($localStorage.token);
                },
                function(error) {}
            );   
    }
});