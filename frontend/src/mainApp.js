var mainApp = angular.module("mainApp", ['ngRoute', 'ngStorage']);
mainApp.config(function($routeProvider) {
    $routeProvider.
    when('/auth', {
        templateUrl: 'src/login/login.html',
        controller: 'loginController'
    }).
    when('/signup', {
<<<<<<< HEAD
        templateUrl: 'src/signup/signup.html',
        controller: 'signupController'
=======
        templateUrl: 'src/signup/signup.html'
        // controller: 'loginController'
>>>>>>> 7e6f01308adefe85755bff38039fc5258241e1f8
    }).
    otherwise({
        redirectTo: '/'
    });
});
