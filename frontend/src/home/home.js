var mainApp = angular.module("mainApp");
mainApp.controller("homeController", function ($scope, toaster, $rootScope, $location, $document, $timeout, $interval, homeService) {
    
    $scope.channel_name = 'public';
    $scope.messageList = [];
    $scope.createNewChannel = false;
    $scope.showunsubscribechannel = false;
    $scope.showdeletechannel = false;
    $scope.displayChat = true;
    $scope.autoRefresh = true;
    $scope.page_num = 0
    $document[0].body.style.backgroundColor = "white";
    
    $scope.openNav = function(){
        $document[0].getElementById("mySidenav").style.width = "250px";
        $document[0].getElementById("main").style.marginLeft = "250px";
        $document[0].body.style.backgroundColor = "rgba(0,0,0,0.4)";
    };
    
    $scope.closeNav = function(){
        $document[0].getElementById("mySidenav").style.width = "0";
        $document[0].getElementById("main").style.marginLeft= "0";
        $document[0].body.style.backgroundColor = "white";
    };
    
    $scope.get_user = function () {
        var userInfo = homeService.get_user()
        userInfo.then(function (response) {
            if (response.status ==  200){
                $rootScope.username = response.data['username'],
                $rootScope.first_name = response.data['first_name']
            }else{
                toaster.pop('error', response.data['message'])
            }
        },function (error) {
            toaster.pop('error', error.data['message'])
            }
        );
    }
    $scope.get_user();

    $scope.get_channel_by_name = function (channel_name) {
        var result = homeService.get_channel_by_name(channel_name)
        result.then(function(response) {
            if (response.status ==  200){
                if (response.data.length == 0){
                    $scope.createChannel('public', 'public')
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
            if (response.status ==  200){
                $scope.messageList = response.data;
                if ($scope.messageList.length > 0){
                    $scope.displayChat = true;
                }else{
                    $scope.channel_name = channel_name;
                    toaster.pop('warning' + 'No chat found');
                }
                $scope.displayChat = true;
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        ); 
    }
    $scope.get_chat_by_channel_name($scope.channel_name, $scope.page_num);

    $interval(function () {
        if ($scope.autoRefresh == true){
            $scope.get_chat_by_channel_name($scope.channel_name, $scope.page_num);
        }
    }, 20000);

    if ($rootScope.showWelcomeMessage == true){
        $scope.welcomeMessage = this;
        $rootScope.showWelcomeMessage = false;
    }

    $scope.get_all_channels = function () {
        var result = homeService.get_all_channels()
        result.then(function(response) {
            if (response.status ==  200){
                $scope.channelList = response.data
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        );
    }
    $scope.get_all_channels();

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
        // $scope.channel_name = 'public';
    }

    $scope.dismiss = function () {
        var channelModalClass = angular.element(document.querySelector('.channelModal'));
        channelModalClass.addClass('hide')
        $scope.displayChat = true;
        $scope.autoRefresh = true;
        $scope.showdeletechannel = false;
        $scope.showunsubscribechannel = false;
        // $scope.channel_name = 'public';
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
        // var unsubscribechannelmodal = angular.element(document.querySelector('.unsubscribechannelmodal'));
        // unsubscribechannelmodal.removeClass('hide')
    }

    $scope.triggerChatDeletion = function () {
        $scope.showdeletechannel = true;
        $scope.autoRefresh = false;
        $scope.displayChat = false;
        // var deletechannelmodal = angular.element(document.querySelector('.deletechannelmodal'));
        // deletechannelmodal.removeClass('hide')
        // var modalClass = angular.element(document.querySelector('.modal'));
        // modalClass.addClass('hide');
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

    $scope.loadMore = function () {
        $scope.page_num +=1;
        $scope.autoRefresh = false;
        $scope.get_chat_by_channel_name(channelName, $scope.page_num);
        // $scope.channel_name = 'public';
    }

    $scope.createChannel = function (name, type) {
        var channel = homeService.createChannel(name, type)
        channel.then(function(response) {
            if (response.status ==  200){
                $scope.channel_name = response.data['channel_name'];
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
            }
        );
     $scope.createNewChannel = false;
    }

    $scope.deleteChat = function (channelName) {
        var channel = homeService.deleteChat(channelName)
        channel.then(function(response) {
        if (response.status ==  200){
            $scope.get_chat_by_channel_name(channelName, 0);
        }else{
            toaster.pop('error', response.data['message'])
        }},
        function(error) {
            toaster.pop('error', error.data['message'])
            console.log(error.data)
        });
         $scope.showdeletechannel = false;
         $scope.displayChat = true;
    }

    $scope.unsubscibeChannel = function (channelName) {
        if (channelName == 'public'){
            toaster.pop('warning', 'You cannnot unsubscribe Public channel');
        }else{
            var channel = homeService.unsubscribeChannel(channelName)
            channel.then(function(response) {
            if (response.status ==  200){
                toaster.pop('success', channelName + 'Successfully Unsuscribed')
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
    }

});

mainApp.filter('reverse', function() {
    return function(items) {
    return items.slice().reverse();
    };
});

