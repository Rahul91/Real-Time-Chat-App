var mainApp = angular.module("mainApp");
mainApp.service("loginService", function($http, appConfig){
    // var url = 'http://127.0.0.1:3434'
    var apiendpoint = appConfig[appConfig.env].api_url;
    var apiendpointport = appConfig[appConfig.env].api_url_port;

    var url = apiendpoint + ':' + apiendpointport
    this.validate = function (username, password) {
        console.log(username, password)
        return $http.post(url + "/auth", {
        "username": username,
        "password": password
        }); 
    };
});