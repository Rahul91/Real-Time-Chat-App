var mainApp = angular.module("mainApp");
mainApp.service("signupService", function($http){
    var url = 'http://127.0.0.1:3434'
    this.signup = function (username, password, first_name, last_name) {
        console.log(username, password, first_name, last_name)
        return $http.post(url + "/signup", {
            "username": username,
            "password": password,
            "firstname": first_name,
            "lastname":  last_name
        }); 
    };
});