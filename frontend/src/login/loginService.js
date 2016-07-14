var mainApp = angular.module("mainApp");
mainApp.service("loginService", function($http){
    var url = 'http://127.0.0.1:3434'
    this.validate = function (username, password) {
        console.log(username, password)
        return $http.post(url + "/auth", {
        "username": username,
        "password": password
        }); 
    };
});