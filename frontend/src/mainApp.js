var mainApp = angular.module("mainApp", ['ngRoute', 'ngStorage']);
mainApp.config(function($routeProvider) {
    $routeProvider.
    when('/auth', {
        templateUrl: 'src/login/login.html',
        controller: 'loginController'
    }).
    when('/signup', {
        templateUrl: 'src/signup/signup.html',
        controller: 'signupController'
    }).
    when('/home', {
        templateUrl: 'src/auth/auth.html'
    }).
    when('/', {
        controller: 'indexController'
    }).
    otherwise({
        redirectTo: '/'
    });
});


mainApp.controller("indexController", function () {
    $scope.closeNav = function () {
        document.getElementById("mySidenav").style.width = "0";
        document.getElementById("main").style.marginLeft= "0";
        document.body.style.backgroundColor = "white";
    };
    $scope.openNav = function () {
        document.getElementById("mySidenav").style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
        document.body.style.backgroundColor = "rgba(0,0,0,0.4)";
    };

});
