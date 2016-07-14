var mainApp = angular.module("mainApp");
mainApp.controller("signupController", function ($scope, signupService, $localStorage) {
    $scope.signup = function (username, password, first_name, last_name) {
        var result = signupService.signup(username, password, first_name, last_name)
        result.then(function(response) {
                    console.log('success: ', response.data);
                    // $localStorage.token = response.data;
                    // console.log($localStorage.token);
                },
                function(error) {
                    console.log('failure: ', response.data);
                }
            );   
    }
});