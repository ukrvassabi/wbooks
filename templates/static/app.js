(function() {
  "use strict";

  angular
    .module("wbooks", ["ui.router"])
    .config(function($stateProvider, $urlRouterProvider) {

      $urlRouterProvider.otherwise("/");

      $stateProvider
          .state("home", {
            url: "/",
            template:
              "<wbooks-navigation></wbooks-navigation>" +
              "<h1 class='text-center m-top-100'>Welcome to Wbooks app!</h1>" +
              "<div class='text-center m-top-100'>" +
                "<button class='btn btn-primary' ui-sref='books'>Go to Books</button>" +
              "</div>"
          })
          .state("books", {
            url: "/books",
            templateUrl: "static/books.tpl.html",
            controller: "BooksController",
            controllerAs: "books"
          });
    });
})();
