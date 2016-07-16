var mainApp = angular.module("mainApp");
mainApp.service("homeService", function($http, $localStorage){
    var url = 'http://127.0.0.1:3434'
    token = localStorage['token'].replace(/['"]+/g, '')
    this.publish = function (message, channel) {
        console.log(message, channel)
        return $http.post(url + "/publish", {
            "message": message,
            "channel": channel
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.createChannel = function (name, type) {
        console.log(name, type)
        return $http.post(url + "/channel", {
            "channel_name": name,
            "type": type
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.fetch_message = function () {
        console.log()
        return $http.get(url + "/message", {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.get_user = function () {
        console.log()
        return $http.get(url + "/user", {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };
    
});