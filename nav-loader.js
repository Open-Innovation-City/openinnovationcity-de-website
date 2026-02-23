(function () {
  var isEnglish = /\/en(\/|$)/.test(window.location.pathname);
  fetch(isEnglish ? '/nav-en.html' : '/nav-de.html')
    .then(function (r) { return r.text(); })
    .then(function (html) {
      var el = document.getElementById('site-header');
      if (el) {
        el.outerHTML = html;
        if (window.jQuery && window.Foundation) {
          $(document).foundation();
        }
      }
    });
})();
