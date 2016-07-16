var mainApp = angular.module("mainApp");
mainApp.controller("logoutController", function ($scope, $localStorage, toaster, $location) {
    localStorage.token = ""
    window.location.href = "#/"
});