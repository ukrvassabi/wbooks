(function() {
  "use strict";

  angular
      .module("wbooks")
      .directive("wbooksNavigation", function($rootScope, $state, UserService) {
        return {
          restrict: "E",
          replace: true,
          templateUrl: "static/navigation.tpl.html",
          link: function (scope) {
            scope.showSearch = $state.is("books");
            $rootScope.$on("$stateChangeSuccess", function() {
              scope.showSearch = $state.is("books");
            });

            UserService.getUser().then(function(response) {
              scope.user = response.data.name;
            });
          }
        }
      })
      .directive("wbooksSpinner", function($rootScope) {
        return {
          restrict: "E",
          replace: true,
          template: "<div class='spinner-bg' ng-show='showSpinner'>" +
                      "<div class='spinner'>Loading...</div>" +
                    "</div>",
          link: function (scope) {
            $rootScope.$on("blockSpinner:show", function() {
              scope.showSpinner = true;
            });
            $rootScope.$on("blockSpinner:hide", function() {
              scope.showSpinner = false;
            });
          }
        }
      });
})();
