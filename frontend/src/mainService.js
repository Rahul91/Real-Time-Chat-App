mainApp.service('mainService', function($http){
    var url = 'http://127.0.0.1:3434'
    this.callindex = function () {
        data =  $http.get(url + "/home");
        return data;
    };
})