const url = window.location;
$('ul.navbar_sidebar_top li.nav-item a').filter(function () {
    return this.href == url && !this.href.endsWith("#");
}).addClass('active');
$('ul.nav_dropdown a').filter(function () {
    return this.href == url && !this.href.endsWith("#");
}).parentsUntil(".navbar_sidebar_top > .nav_dropdown").addClass('menu-open').prev('a').addClass('active');