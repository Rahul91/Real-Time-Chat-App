var mainApp = angular.module("mainApp");
mainApp.service("signupService", function($http, $rootScope, appConfig){
    // var url = 'http://127.0.0.1:3434'
    var apiendpoint = appConfig[appConfig.env].api_url;
    var apiendpointport = appConfig[appConfig.env].api_url_port;

    var url = apiendpoint + ':' + apiendpointport
    // var end_point_url = $rootScope.apiUrl
    this.signup = function (username, password, first_name, last_name) {
        console.log(username, password, first_name, last_name)
        return $http.post(url + "/signup", {
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name":  last_name
        }); 
    };
});