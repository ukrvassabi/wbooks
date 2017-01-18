(function() {
  "use strict";

  angular
      .module("wbooks")
      .factory("UserService", function($http) {
        return {
          getUser: function() {
            return $http.get("/api/v1/wunderlist/user");
          }
        }
      })
      .factory("BooksService", function($q, $http) {
        return {
          getList: function (data) {
            if (data && data.limit) {
              return $q.all([
                  $http.get("/api/v1/book?limit=" + data.limit),
                  $http.get("/api/v1/bookwbook"),
                  $http.get("/api/v1/wunderlist/book")
              ]);
            }
            return $q.all([
                $http.get("/api/v1/book"),
                $http.get("/api/v1/bookwbook"),
                $http.get("/api/v1/wunderlist/book")
            ]);
          },
          addToWunderlist: function(book) {
            return $http.post("/api/v1/wunderlist/book",
                {
                  id: book.id,
                  title: book.title,
                  link: book.link,
                  category: book.category.name
                });
          }
        }
      })
})();
