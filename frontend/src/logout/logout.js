var mainApp = angular.module("mainApp");
mainApp.controller("logoutController", function ($scope, $localStorage, toaster, $window, $rootScope, $location) {
    localStorage.token = "";
    $rootScope.username = "";
    $rootScope.first_name = "";
    $rootScope.showWelcomeMessage = false;
    window.location.href = "#/"
});