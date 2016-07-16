var mainApp = angular.module("mainApp");
mainApp.controller("landingController", function ($scope, $rootScope, loginService, $localStorage, $location, $document) {
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
});