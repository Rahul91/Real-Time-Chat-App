var mainApp = angular.module("mainApp", ['ngRoute', 'ngStorage', 'ngAnimate', 'toaster', "ngModal"]);

mainApp.factory('myInterceptor', myInterceptor);

mainApp.config(function($routeProvider, $httpProvider) {
    $routeProvider.
    when('/login', {
        templateUrl: 'src/login/login.html',
        controller: 'loginController'
    }).
    when('/logout', {
        templateUrl: 'src/landing/landing.html',
        controller: 'logoutController'
    }).
    when('/signup', {
        templateUrl: 'src/signup/signup.html',
        controller: 'signupController'
    }).
    when('/home', {
        templateUrl: 'src/home/home.html',
        controller: 'homeController'
    }).
    when('/', {
        templateUrl: 'src/landing/landing.html',
        controller: 'landingController'
    }).
    otherwise({
        redirectTo: '/'
    });
    $httpProvider.interceptors.push('myInterceptor');

    // $rootScope.urlEndPoint = 'http://127.0.0.1:3434'
});

function myInterceptor() {
  return {
    // request: function(config) {
    //   console.log('in request');
    //   return config;
    // },

    // requestError: function(config) {
    //     console.log('in request error');
    //   return config;
    // },

    // response: function(res) {
    //     console.log('in response');
    //   return res;
    // },

    responseError: function(res) {
        console.log('in responseError: ', res);
        // toaster.pop('error', res.data['message']);
        return res;
    }
  }
}
