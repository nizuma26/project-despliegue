//ELEMENTOS PARA PERSONALIZAR
const body = document.body;
const btn_custom_interface = document.querySelector('.custom_interface');
const save_settings = document.querySelector('.save_settings');
const close_panel_control = document.querySelector('.close_panel_control');
const nav_sidebar = document.getElementById('nav_sidebar_control')
const navbar = document.getElementById('navbar_control')
const control_sidebar_content = document.getElementById('control-sidebar-content')
const main_color = document.getElementById('main_color')

//TEMAS
const sidebar_light = document.getElementById('sidebar_light')
const sidebar_dark = document.getElementById('sidebar_dark')
const nav_link = document.querySelectorAll('span.nav_link_color')
const theme_main = document.querySelectorAll('span.main_color')
const navbar_theme = document.querySelectorAll('a.header-theme')

//SIDEBAR
const nav_sidebar_legacy = document.getElementById('sidebar_nav_legacy')
const collap = document.getElementById('collap')
const sidebar_orientation = document.getElementById('sidebar_orientation')

let settings = {
    dataOne: {
        nav_link: 'theme_blue',
        sidebar_theme: 'sidebar-dark-primary',
        brand_logo_theme: '',
        navbar_theme: 'theme_blue',
        navbar_fixed: '',
        main_color: 'theme_blue',
    },
    dataTwo: {
        sidebar_options: {
            collapse: '',
            fixed: 'layout-fixed',
            flat: '',
            orientation: 'vtc',
            legacy: '',
            disable_hover: ''
        },
        small_text: {
            body: '',
            navbar: '',
            brand: '',
            sidebar_nav: '',
            footer: ''
        },
    }
}

function success(text, timer){
    Swal.fire({
        title: 'Genial!',
        text: text,
        icon: 'success',
        timer: timer,
        timerProgressBar: true,
        confirmButtonText: '<i class="fa fa-thumbs-up"></i> OK!',
        confirmButtonColor: '#289aff',
    })
}

const get_data = async () => {
    const data = new FormData();
    const my_id = document.getElementById('user_id')
    data.append("action", "get_settings");
    data.append("my_id", my_id.value);

    await fetch("/customize/interface/", {
        method: "POST",
        body: data,
      }).then(function (res) {
        return res.json();
      }).then(function (data) {
          if (data.value){
                //console.log('EXISTE')
                settings.dataOne.nav_link = data.nav_link_theme;
                settings.dataOne.sidebar_theme = data.sidebar_theme;
                settings.dataOne.navbar_theme = data.navbar_theme;
                settings.dataOne.brand_logo_theme = data.brand_logo_theme;
                settings.dataOne.main_color = data.main_color;
                settings.dataOne.navbar_fixed = data.navbar_fixed;
                settings.dataTwo.sidebar_options.collapse = data.sidebar_collapse;
                settings.dataTwo.sidebar_options.fixed = data.sidebar_fixed;
                settings.dataTwo.sidebar_options.flat = data.sidebar_flat;
                settings.dataTwo.sidebar_options.orientation = data.sidebar_orientation;
                settings.dataTwo.sidebar_options.legacy = data.sidebar_legacy;
                settings.dataTwo.sidebar_options.disable_hover = data.sidebar_disable_hover;
                settings.dataTwo.small_text.body = data.small_body;
                settings.dataTwo.small_text.navbar = data.small_navbar;
                settings.dataTwo.small_text.brand = data.small_sidebar_nav;
                settings.dataTwo.small_text.sidebar_nav = data.small_brand;
                settings.dataTwo.small_text.footer = data.small_footer;

            if (data.sidebar_orientation === 'hzt'){
                sidebar_orientation.checked = true
            }
        }
        // console.log('RESULTADO: ', data)
        // console.log('SETTINGS: ', settings)
      });
}

const save_data = async (user_id) => {
    const data = new FormData();
    data.append("action", "add_settings");
    data.append("settings", JSON.stringify(settings));
    data.append("my_id", user_id);

    await fetch("/customize/interface/", {
        method: "POST",
        body: data,
      }).then(function (res) {
        return res.json();
      }).then(function (data) {
          console.log(data)
          success('Configuración guardada con exito', 3000)
      })
}

let flag_get_data = false;
btn_custom_interface.addEventListener('click', () => {
    btn_custom_interface.classList.toggle('displace');
    control_sidebar_content.classList.remove('os-theme-light');
    if (flag_get_data === false){
        get_data();
        flag_get_data = true;
    }
})
close_panel_control.addEventListener('click', () => {
    btn_custom_interface.classList.toggle('displace')
})

navbar_theme.forEach((color)=>{
    color.addEventListener('click', () => {
        const nav_theme = color.getAttribute('header-theme')
        navbar.setAttribute('navbar-theme', nav_theme);
        settings.dataOne.navbar_theme = nav_theme;
    })
})
sidebar_orientation.addEventListener('change', function() {
    if (this.checked) {
      //body.classList.add('layout-fixed');
      settings.dataTwo.sidebar_options.orientation = 'hzt';
    } else {
      //body.classList.remove('layout-fixed');
      settings.dataTwo.sidebar_options.orientation = 'vtc';
    }
    console.log(settings.dataTwo.sidebar_options)
});
nav_link.forEach((color)=>{
    color.addEventListener('click', () => {
        const link = color.getAttribute('data-link');
        nav_sidebar.setAttribute('nav-link-theme', link);
        settings.dataOne.nav_link = link;
    })
})
theme_main.forEach((color)=>{
    color.addEventListener('click', () => {
        const theme = color.getAttribute('data-theme');
        main_color.setAttribute('main-color', theme);
        settings.dataOne.main_color = theme;
    })
})
sidebar_light.addEventListener('click', () => {
    nav_sidebar.setAttribute('nav-sidebar-theme', 'sidebar-light-primary');
    settings.dataOne.sidebar_theme = 'sidebar-light-primary'

})

sidebar_dark.addEventListener('click', () => {
    nav_sidebar.setAttribute('nav-sidebar-theme', 'sidebar-dark-primary');
    settings.dataOne.sidebar_theme = 'sidebar-dark-primary'
})
save_settings.addEventListener('click', () => {
    const user_id = document.getElementById('user_id')
    save_data(user_id);
    console.log('SEND: ', settings)
})