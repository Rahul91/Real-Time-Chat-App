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
    // when('/login', {
    //     // templateUrl: 'src/auth/auth.html#login'
    // }).
    otherwise({
        redirectTo: '/'
    });
});
