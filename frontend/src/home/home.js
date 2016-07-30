var mainApp = angular.module("mainApp");
mainApp.controller("homeController", function ($scope, toaster, $rootScope, $location, $document, $timeout, $interval, homeService) {
    $scope.channel_name = 'public';
    $scope.messageList = [];
    $scope.InvitationList = [];
    $scope.createNewChannel = false;
    $scope.showunsubscribechannel = false;
    $scope.invitationRequestModal = false;
    $scope.showdeletechannel = false;
    $scope.showInviteUser = false;
    $scope.displayChat = true;
    $scope.autoRefresh = true;
    $scope.fetchingChat = true;
    $scope.page_num = 0
    $scope.requestedChannelName = ''
    $scope.requsterName = ''
    $document[0].body.style.backgroundColor = "white";
    
    $scope.get_user = function () {
        var userInfo = homeService.get_user()
        userInfo.then(function (response) {
            if (response.status ==  200){
                $rootScope.username = response.data['username'],
                $rootScope.first_name = response.data['first_name']
                $scope.get_pending_request_for_user();
            }else{
                toaster.pop('error', response.data['message'])
            }
        },function (error) {
            toaster.pop('error', error.data['message'])
            }
        );
    }
    
    $scope.get_user();

    $scope.get_pending_request_for_user = function () {
        var userInfo = homeService.get_pending_request_for_user()
        userInfo.then(function (response) {
            if (response.status ==  200){
                $scope.InvitationList = response.data;
            }else{
                toaster.pop('error', response.data['message'])
            }
        },function (error) {
            toaster.pop('error', error.data['message'])
            }
        );
    }
    // $scope.get_pending_request_for_user();

    $scope.get_channel_by_name = function (channel_name) {
        var result = homeService.get_channel_by_name(channel_name)
        result.then(function(response) {
            if (response.status ==  200){
                if (response.data == null){
                    $scope.createChannel('public', 'public')
                }else{
                    $scope.get_all_channels();
                }
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
            }
        );
    }

    $scope.get_channel_by_name($scope.channel_name);

    $scope.get_chat_by_channel_name = function (channel_name, page_num) {
        var result = homeService.get_chat_by_channel_name(channel_name, page_num)
        result.then(function(response) {
            $scope.channel_name = channel_name;
            if (response.status ==  200){
                $scope.fetchingChat = false;
                $scope.messageList = response.data;
                if ($scope.messageList.length > 0){
                    $scope.displayChat = true;
                    $scope.channel_name = channel_name;
                }else{
                    $scope.channel_name = channel_name;
                    // toaster.pop('warning', 'No chat found, start a conversation');
                }
                $scope.displayChat = true;
            }else{
                $scope.fetchingChat = false;
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                $scope.fetchingChat = false;
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        ); 
    }

    $scope.get_chat_by_channel_name($scope.channel_name, $scope.page_num);
    $scope.fetchMessage = $interval(function () {
        if ($scope.autoRefresh == true){
            $scope.get_chat_by_channel_name($scope.channel_name, $scope.page_num);
        }
    }, 10000);


    if ($rootScope.showWelcomeMessage == true){
        $scope.welcomeMessage = true;
        $rootScope.showWelcomeMessage = false;
    }

    $scope.get_all_channels = function () {
        var result = homeService.get_all_channels()
        result.then(function(response) {
            if (response.status ==  200){
                $scope.channelList = response.data;
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        );
    }

    $scope.fetchChannel = $interval(function () {
        $scope.get_pending_request_for_user();
        $scope.get_all_channels();
    }, 120000);
    // $scope.get_all_channels();

    $scope.publish = function (message, channel_name) {
        var result = homeService.publish(message, channel_name)
        result.then(function(response) {
            if (response.status ==  200){
                $scope.messageList.unshift({
                                'message_text': message,
                                'created_on': new Date(),
                                'published_by_name': $rootScope['first_name'],
                                'direction': "outgoing"
                            });
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
            }
        );
        $scope.message=''; 
    }

    $scope.close = function () {
        var modalClass = angular.element(document.querySelector('.modal'));
        modalClass.addClass('hide');
        $scope.displayChat = true;
        $scope.autoRefresh = true;
        $scope.welcomeMessage = false;
    }

    $scope.dismiss = function () {
        var channelModalClass = angular.element(document.querySelector('.channelModal'));
        channelModalClass.addClass('hide')
        $scope.displayChat = true;
        $scope.autoRefresh = true;
        $scope.showdeletechannel = false;
        $scope.showunsubscribechannel = false;
    }

    $scope.triggerChannelCreation = function () {
        $scope.autoRefresh = false;
        $scope.createNewChannel = true;
        $scope.displayChat = false;
        var channelModalClass = angular.element(document.querySelector('.channelModal'));
        channelModalClass.removeClass('hide')
        var modalClass = angular.element(document.querySelector('.modal'));
        modalClass.addClass('hide');
    }

    $scope.triggerChannelUnsubscription = function () {
        $scope.showunsubscribechannel = true;
        $scope.autoRefresh = false;
        $scope.displayChat = false;
    }

    $scope.triggerChatDeletion = function () {
        $scope.showdeletechannel = true;
        $scope.autoRefresh = false;
        $scope.displayChat = false;
    }

    $scope.triggerAcceptInvitation = function (requestedChannelName, requsterName) {
        $scope.displayChat = false;
        $scope.invitationRequestModal = true;
        $scope.requestedChannelName = requestedChannelName;
        $scope.requsterName = requsterName;
        $scope.autoRefresh = false;
    }
    
    $scope.triggerInviteUsers = function () {
        $scope.showInviteUser = true;
        $scope.autoRefresh = false;
        $scope.displayChat = false;
    }

    $scope.dismissInviteUser = function () {
        $scope.displayChat = true;
        $scope.autoRefresh = true;
        $scope.showInviteUser = false;
        $scope.showunsubscribechannel = false;
    }

    $scope.dismissDelete = function () {
        $scope.displayChat = true;
        $scope.autoRefresh = true;
        $scope.showdeletechannel = false;
        $scope.showunsubscribechannel = false;
    }

    $scope.dismissUnsubscribe = function () {
        $scope.displayChat = true;
        $scope.autoRefresh = true;
        $scope.showdeletechannel = false;
        $scope.showunsubscribechannel = false;
    }

    $scope.laterInvitation = function(){
        $scope.invitationRequestModal = false;
        $scope.displayChat = true;
        $scope.autoRefresh = true;
    }

    $scope.fetchPreviousChat = function () {
        $scope.page_num +=1;
        $scope.autoRefresh = false;
        $scope.get_chat_by_channel_name($scope.channel_name, $scope.page_num);
    }

    $scope.createChannel = function (channelName, type) {
        $scope.displayChat = true;
        var channel = homeService.createChannel(channelName, type)
        $scope.fetchingChat = true;
        channel.then(function(response) {
            if (response.status ==  200){
                console.log(response.data);
                toaster.pop('success', channelName + ': ' + response.data['message']);
                if (response.data['message'] == 'Created'){
                    $scope.channel_name = response.data['channel_name'];
                    $scope.get_all_channels();
                    $scope.get_chat_by_channel_name($scope.channel_name, $scope.page_num);
                }
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
            }
        );
     $scope.createNewChannel = false;
     $scope.fetchingChat = false;
     $scope.autoRefresh = true;
    }

    $scope.inviteUser = function (user_name, channel_name) {
        $scope.displayChat = true;
        if (channel_name == 'public'){
            toaster.pop('warning', 'You cannnot send invitation for Public channel');
        }else{
            var channel = homeService.inviteUser(user_name, channel_name)
            $scope.fetchingChat = true;
            channel.then(function(response) {
                if (response.status ==  200){
                    toaster.pop('success',  'Inviation to: ' + user_name +  ' sent successfully');
                }else{
                    toaster.pop('error', response.data['message'])
                }},
                function(error) {
                    toaster.pop('error', error.data['message'])
                }
            );
        }
     $scope.createNewChannel = false;
     $scope.showInviteUser = false;
     $scope.fetchingChat = false;
     $scope.autoRefresh = true;
    }

    $scope.deleteChat = function (channelName) {
        $scope.displayChat = true;
        var channel = homeService.deleteChat(channelName)
        channel.then(function(response) {
        if (response.status ==  200){
            toaster.pop('success', 'Chats deleted');
            $scope.get_chat_by_channel_name(channelName, 0);
        }else{
            toaster.pop('error', response.data['message'])
        }},
        function(error) {
            toaster.pop('error', error.data['message'])
            console.log(error.data)
        });
         $scope.invitationRequestModal = false;
         $scope.showdeletechannel = false;
         $scope.showunsubscribechannel = false;
         $scope.displayChat = true;
         $scope.fetchingChat = false;
         $scope.autoRefresh = true;
    }

    $scope.joinChannelResponse = function (channelName, response) {
        $scope.displayChat = true;
        var channel = homeService.save_user_invitation_response(channelName, response)
        channel.then(function(response) {
        if (response.status ==  200){
            if (response.data.user_preference == 'accepted'){
                $scope.get_chat_by_channel_name(channelName, 0);
                $scope.get_all_channels();
            }
        }else{
            toaster.pop('error', response.data['message'])
        }},
        function(error) {
            toaster.pop('error', error.data['message'])
            console.log(error.data)
        });
         $scope.showdeletechannel = false;
         $scope.showunsubscribechannel = false;
         $scope.invitationRequestModal = false;
         $scope.fetchingChat = false;
         $scope.autoRefresh = true;
         $scope.get_pending_request_for_user();
    }

    $scope.unsubscibeChannel = function (channelName) {
        $scope.displayChat = true;
        if (channelName == 'public'){
            toaster.pop('warning', 'You cannnot unsubscribe Public channel');
        }else{
            var channel = homeService.unsubscribeChannel(channelName)
            $scope.fetchingChat = true;
            channel.then(function(response) {
            if (response.status ==  200){
                toaster.pop('success', channelName + ' Successfully Unsuscribed');
                $scope.get_chat_by_channel_name('public', 0);
                $scope.get_all_channels();
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            });
        }
        $scope.displayChat = true;
        $scope.showunsubscribechannel = false;
        $scope.fetchingChat = false;
        $scope.autoRefresh = true;
    }

    var destoryScope = $scope.$on('$locationChangeSuccess', function() {
        $interval.cancel($scope.fetchMessage);
        destoryScope();
    });

});

mainApp.filter('reverse', function() {
    return function(items) {
    return items.slice().reverse();
    };
});


mainApp.filter('timezone', function(){

 return function (val, offset) {
        if (val != null && val.length > 16) {
    return val.substring(0, 26)
}    
return val;
    };
});

mainApp.directive('scrollBottom', function($timeout) {
    return {
        scope: {
            scrollBottom: "="
        },
        link: function(scope, element) {
            scope.$watchCollection('scrollBottom', function(newValue, oldValue) {
                if (newValue) {
                    $timeout(function() {
                        $(element).scrollTop($(element)[0].scrollHeight);
                    }, 10);
                }
            });
        }
    };
})

