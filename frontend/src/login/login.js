var mainApp = angular.module("mainApp");
mainApp.controller("loginController", function ($scope, appConfig, $rootScope, loginService, $localStorage, $location, toaster) {
    $scope.index = false;
    $scope.login = function (username, password) {
        var result = loginService.validate(username, password)
        result.then(function(response) {
            if (response.status == 200){
                localStorage.token = response.data["access_token"];
                toaster.pop('success', 'LOGGED-IN');
                window.location.href='#/home'
            }else{
                toaster.pop('error', response['statusText']);
            }
        },function(error) {}
    );   
};

    $scope.closeNav = function(){
        window.location.href = "#/";
    };
});