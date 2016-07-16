var mainApp = angular.module("mainApp");
mainApp.service("signupService", function($http, $rootScope){
    var url = 'http://127.0.0.1:3434'
    var end_point_url = $rootScope.apiUrl
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