var mainApp = angular.module("mainApp");
mainApp.service("homeService", function($http, $localStorage, appConfig){
    var apiendpoint = appConfig[appConfig.env].api_url;
    var apiendpointport = appConfig[appConfig.env].api_url_port;
    var url = apiendpoint + ':' + apiendpointport
    
    var token = localStorage['token'].replace(/['"]+/g, '')
    
    this.get_all_channels = function () {
        return $http.get(url + "/channel", {
            "headers": {
            "Authorization": 'JWT ' + localStorage['token'].replace(/['"]+/g, '')
            }
        }); 
    };

    this.get_channel_by_name = function (channel_name) {
        return $http.get(url + "/channel/" + channel_name, {
            "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.createChannel = function (name, type) {
        return $http.post(url + "/channel/create", {
            "channel_name": name,
            "type": type
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.deleteChat = function (channel_name) {
        return $http.post(url + "/message/delete", {
            "channel_name": channel_name,
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.inviteUser = function (user_name, channel_name) {
        return $http.post(url + "/channel/invite", {
            "channel_name": channel_name,
            "invited_user_name": user_name,
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.unsubscribeChannel = function (channel_name) {
        return $http.post(url + "/channel/unsubscribe", {
            "channel_name": channel_name,
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };
    

    this.get_chat_by_channel_name = function (channel_name, page_num) {
        return $http.post(url + "/message", {
            "channel_name": channel_name,
            "page_num": page_num
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.publish = function (message, channel) {
        return $http.post(url + "/message/publish", {
            "message": message,
            "channel_name": channel
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };

    this.streamFetch = function (channel_name) {
        return $http.post(url + "/stream", {
            "channel_name": channel_name,
            }, {
         "headers": {
            "Authorization": 'JWT ' + token
            }
        }); 
    };
    
    this.get_user = function () {
        return $http.get(url + "/user", {
         "headers": {
            "Authorization": 'JWT ' + localStorage['token'].replace(/['"]+/g, '')
            }
        }); 
    };

    this.get_pending_request_for_user = function () {
        return $http.get(url + "/channel/pending", {
         "headers": {
            "Authorization": 'JWT ' + localStorage['token'].replace(/['"]+/g, '')
            }
        }); 
    };
    
});