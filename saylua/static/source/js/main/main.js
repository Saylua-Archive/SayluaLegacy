window.addEventListener('load', function () {
  window.addEventListener('scroll', fixNavbar);

  // Form Validation
  FormValidation.bind('.validated-form');
});

// Make navigation bar stay at the top
function fixNavbar () {
  var top = document.getElementById("banner").offsetHeight;
  if (document.body.scrollTop > top ||
    document.documentElement.scrollTop > top) {
    addClass(document.getElementById("navbar"), "fixed");
  } else {
    removeClass(document.getElementById("navbar"), "fixed");
  }
}
