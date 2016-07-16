var mainApp = angular.module("mainApp");
mainApp.controller("homeController", function ($scope, toaster, $rootScope, $location, $timeout, $interval, homeService) {
    // $scope.listin = function() {
    //     console.log("$scope.callAtInterval - Interval occurred");

    // }
    // $interval( function(){ $scope.listin(); }, 3000);
    $scope.channel_name = 'public';
    $scope.messageList = [];
    $scope.createNewChannel = false;
    $scope.displayChat = true;

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

    $scope.fetch = function () {
        var result = homeService.fetch_message()
        result.then(function(response) {
            console.log(response.data);
            if (response.status ==  200){
                $scope.messageList = response.data;
                if ($scope.messageList.length > 0){
                    $scope.displayChat = true;
                }else{
                    $scope.channel_name = 'public'
                    $scope.displayChat = false;
                    //     toaster.pop({
                    //     type: 'warning',
                    //     title: 'No Channel Found',
                    //     body: 'We found no channel, Send a message and a public channel will be created for you',
                    //     showCloseButton: true,
                    //     timeout: 10000
                    // });
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
    $scope.fetch();


    $scope.publish = function (message, channel) {
        var result = homeService.publish(message, channel)
        result.then(function(response) {
            console.log(response.data);
            if (response.status ==  200){
                $scope.messageList.push({
                                'message_text': message,
                                'created_on': new Date(),
                                'published_by': $rootScope['first_name'],
                                'direction': "outgoing"
                            });
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        ); 

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
        var modalClass = angular.element(document.querySelector('.modal'));
        modalClass.addClass('hide');
        $scope.createNewChannel = true;
    }

    // $scope.createNewChannel

    $scope.createChannel = function (name, type) {
        var channel = homeService.createChannel(name, type)
        channel.then(function(response) {
            console.log(response.data);
            if (response.status ==  200){
                $scope.channel_name = response.data['channel_name'];
                $scope.displayChat = true;
            }else{
                toaster.pop('error', response.data['message'])
            }},
            function(error) {
                toaster.pop('error', error.data['message'])
                console.log(error.data)
            }
        );
     var channelModalClass = angular.element(document.querySelector('.channelModal'));
    channelModalClass.addClass('hide') 
    }
});