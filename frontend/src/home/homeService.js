var mainApp = angular.module("mainApp");
mainApp.service("homeService", function($http, $localStorage, appConfig){
    var apiendpoint = appConfig[appConfig.env].api_url;
    var apiendpointport = appConfig[appConfig.env].api_url_port;
    var url = apiendpoint + ':' + apiendpointport
    
    token = localStorage['token'].replace(/['"]+/g, '')
    this.publish = function (message, channel) {
        console.log(message, channel)
        return $http.post(url + "/publish", {
            "message": message,
            "channel_name": channel
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

    this.deleteChat = function (channel_name) {
        console.log(name, type)
        return $http.post(url + "/channel/delete", {
            "channel_name": channel_name
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.fetch_message = function (channel_name, page_num) {
        console.log(channel_name)
        return $http.post(url + "/message", {
            "channel_name": channel_name,
            "page_num": page_num
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.streamFetch = function (channel_name) {
        console.log(channel_name)
        return $http.post(url + "/stream", {
            "channel_name": channel_name,
            }, {
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