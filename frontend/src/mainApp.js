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
    otherwise({
        redirectTo: '/'
    });
});
