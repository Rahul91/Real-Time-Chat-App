var mainApp = angular.module("mainApp");
mainApp.controller("signupController", function ($scope, $timeout, $interval, signupService, loginService, $localStorage, $location, toaster) {
    $scope.index = false;
    $scope.signup = function (username, password, first_name, last_name) {
        var result = signupService.signup(username, password, first_name, last_name)
        result.then(function(success) {
                    console.log('success: ', success.data);
                    if (success.status == 200){
                        toaster.pop('success', 'User Created');
                            var loginResult = loginService.validate(username, password)
                            loginResult.then(function(response) {
                                if (response.status == 200){
                                    localStorage.token = response.data["access_token"];
                                    console.log(localStorage.token);
                                    toaster.pop('success', 'LOGGED-IN');
                                    window.location.href='#/home'
                                }else{
                                    toaster.pop('error', response['statusText']);
                                }
                            },function(error) {});
                    }else{
                        toaster.pop('error', success.data['message']);
                    }
                },
                function(error) {
                    toaster.pop('error', error.data['message']);
                }
            );   
    };
   $scope.closeNav = function(){
        window.location.href = "#/";
    };
});