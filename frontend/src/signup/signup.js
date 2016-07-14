var mainApp = angular.module("mainApp");
mainApp.controller("signupController", function ($scope, signupService, $localStorage) {
    $scope.signup = function (username, password, firstname, lastname) {
        var result = signupService.signup(username, password, firstname, lastname)
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