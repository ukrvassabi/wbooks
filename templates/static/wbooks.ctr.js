(function() {
  "use strict";

  angular
      .module("wbooks")
      .controller("BooksController", function($rootScope, BooksService) {

        var vm = this;
        $rootScope.$broadcast("blockSpinner:show");

        BooksService.getList().then(function(responses) {
          vm.booksList = [];
          var books = responses[0].data, bookswbooks = responses[1].data, wbooks = responses[2].data;
          angular.forEach(books, function(book) {
            angular.forEach(bookswbooks, function(wbook) {
              if (book.id === wbook.book_id) highlightBook(book);
            });
            angular.forEach(wbooks, function (wbook) {
              if (book.title == wbook.title) highlightBook(book);
            });
            vm.booksList.push(book);
          });
          $rootScope.$broadcast("blockSpinner:hide");
        });

        vm.addToWunderlist = function(book) {
          $rootScope.$broadcast("blockSpinner:show");
          BooksService.addToWunderlist(book).then(function() {
            highlightBook(book);
            $rootScope.$broadcast("blockSpinner:hide");
          });
        };

        function highlightBook(book) {
          book.wbook = true;
          book.highlight = "success";
        }
      });
})();
