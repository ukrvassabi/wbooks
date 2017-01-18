(function() {
  "use strict";

  angular
      .module("wbooks")
      .filter('searchTitle', function () {
        return function (items, search) {
          var filtered = [],
              searchMatch = new RegExp(search, 'i');
          if (items && items.length > 0) {
            for (var i = 0; i < items.length; i++) {
              if (searchMatch.test(items[i].title)) {
                filtered.push(items[i]);
              }
            }
          }
          return filtered;
        };
      });
})();