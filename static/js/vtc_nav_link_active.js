//Para que las opciones del menú se activen al darle click
const url = window.location;
$('ul.nav-sidebar a').filter(function() {
    return this.href == url && !this.href.endsWith("#");
}).addClass('active');
$('ul.nav-treeview a').filter(function() {
    return this.href == url && !this.href.endsWith("#");
}).parentsUntil(".nav-sidebar > .nav-treeview").addClass('menu-open').prev('a').addClass('active');