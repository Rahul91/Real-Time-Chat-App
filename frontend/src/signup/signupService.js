var mainApp = angular.module("mainApp");
mainApp.service("signupService", function($http){
    var url = 'http://127.0.0.1:3434'
    this.signup = function (username, password, firstname, lastname) {
        console.log(username, password, firstname, lastname)
        return $http.post(url + "/signup", {
            "username": username,
            "password": password,
            "firstname": firstname,
            "lastname":  lastname
        }); 
    };
});