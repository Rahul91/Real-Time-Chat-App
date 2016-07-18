var mainApp = angular.module("mainApp");
mainApp.controller("homeController", function ($scope, toaster, $rootScope, $location, $document, $timeout, $interval, homeService) {
    
    $scope.channel_name = 'public';
    $scope.messageList = [];
    $scope.createNewChannel = false;
    $scope.displayChat = true;
    $document[0].body.style.backgroundColor = "white";

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
            console.log(error.data)          
            }
        );
    }
    $scope.get_user();

    $scope.fetch = function (channel_name) {
        var result = homeService.fetch_message(channel_name)
        result.then(function(response) {
            console.log(response.data);
            if (response.status ==  200){
                $scope.messageList = response.data;
                if ($scope.messageList.length > 0){
                    $scope.displayChat = true;
                }else{
                    $scope.channel_name = 'public'
                    $scope.displayChat = false;
                }
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        ); 
    }
    $scope.fetch('public');

    // $scope.listin = function(channel_name) {
    //     var result = homeService.streamFetch(channel_name)
    //     result.then(function(response) {
    //         console.log(response.data);
    //         if (response.status ==  200){
    //             $scope.messageList = response.data;
    //             if ($scope.messageList.length > 0){
    //                 $scope.displayChat = true;
    //             }else{
    //                 $scope.channel_name = 'public'
    //                 $scope.displayChat = false;
    //             }
    //         }else{
    //             toaster.pop('error', response.data['message'])
    //         }},
    //         function(error) {
    //             toaster.pop('error', error.data['message'])
    //             console.log(error.data)
    //         }
    //     );
    // }
    // $interval( function(){ $scope.listin($scope.channel_name); }, 20000);

    $scope.publish = function (message, channel) {
        var result = homeService.publish(message, channel)
        result.then(function(response) {
            console.log(response.data);
            if (response.status ==  200){
                // $scope.messageList.append({
                //                 'message_text': message,
                //                 'created_on': new Date(),
                //                 'published_by_name': $rootScope['first_name'],
                //                 'direction': "outgoing"
                //             });
                $scope.fetch(channel);
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        );
        $scope.message=''; 
    }

    $scope.close = function () {
        var modalClass = angular.element(document.querySelector('.modal'));
        modalClass.addClass('hide');
        $scope.displayChat = true;
        $scope.channel_name = 'public';
    }

    $scope.dismiss = function () {
        var channelModalClass = angular.element(document.querySelector('.channelModal'));
        channelModalClass.addClass('hide')
        $scope.displayChat = true;
        $scope.channel_name = 'public';
    }

    $scope.triggerChannelCreation = function () {
        $scope.createNewChannel = true;
        $scope.displayChat = false;
        var channelModalClass = angular.element(document.querySelector('.channelModal'));
        channelModalClass.removeClass('hide')
        var modalClass = angular.element(document.querySelector('.modal'));
        modalClass.addClass('hide');
    }

    // $scope.createNewChannel

    $scope.createChannel = function (name, type) {
        var channel = homeService.createChannel(name, type)
        channel.then(function(response) {
            console.log(response.data);
            if (response.status ==  200){
                $scope.channel_name = response.data['channel_name'];
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        );
     $scope.createNewChannel = false;
    }
});

mainApp.filter('reverse', function() {
    return function(items) {
    return items.slice().reverse();
    };
});

