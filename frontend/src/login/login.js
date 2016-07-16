var mainApp = angular.module("mainApp");
mainApp.controller("loginController", function ($scope, $rootScope, loginService, $localStorage, $location, toaster) {
    $scope.index = false;
    $scope.login = function (username, password) {
        var result = loginService.validate(username, password)
        result.then(function(response) {
            if (response.status == 200){
                localStorage.token = response.data["access_token"];
                console.log(localStorage.token);
                toaster.pop('success', 'LOGGED-IN');
                // $timeout(function() {
                //     window.location.href='#/home'
                // }, 50)
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