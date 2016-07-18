var mainApp = angular.module("mainApp", ['ngRoute', 'ngStorage', 'ngAnimate', 'toaster']);

mainApp.factory('myInterceptor', myInterceptor);

mainApp.constant('appConfig', {
        env: 'development',
        development: {
            api_url: 'http://localhost',
            api_url_port: '3434'
        }
    });

// mainApp.constant("myConfig", {
//         "url": "http://localhost",
//         "port": "3434"
//     })

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

// mainApp.factory('mySocket', function (socketFactory) {
//   var mySocket = socketFactory();
//   mySocket.forward('error');
//   return mySocket;
// });

