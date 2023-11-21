//ELEMENTOS PARA PERSONALIZAR
const body = document.body;
const btn_custom_interface = document.querySelector('.custom_interface');
const save_settings = document.querySelector('.save_settings');
const close_panel_control = document.querySelector('.close_panel_control');
const sidebar = document.getElementById('sidebar_control')
const navbar = document.getElementById('navbar_control')
const brand_logo = document.getElementById('brand_logo')
const control_sidebar_content = document.getElementById('control-sidebar-content')
const nav_sidebar = document.querySelector('ul.nav-sidebar')
const main_color = document.getElementById('main_color')
//OPCIONES DEL PANEL DE CONTROL

//SIDEBAR
const collapse = document.getElementById('sidebar_collapse');
const sidebar_fixed = document.getElementById('sidebar_fixed');
const sidebar_nav_flat = document.getElementById('sidebar_nav_flat')
const sidebar_nav_legacy = document.getElementById('sidebar_nav_legacy')
const sidebar_orientation = document.getElementById('sidebar_orientation')

//TEMAS
const sidebar_light = document.getElementById('sidebar_light')
const sidebar_dark = document.getElementById('sidebar_dark')
const theme_main = document.querySelectorAll('span.main_color')
const nav_link = document.querySelectorAll('span.nav_link_color')
const navbar_theme = document.querySelectorAll('a.header-theme')
const brand_logo_theme = document.querySelectorAll('a.logo-theme')

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
                console.log('ES DIFERENTE')
                settings.dataOne.nav_link = data.nav_link_theme;
                settings.dataOne.sidebar_theme = data.sidebar_theme;
                settings.dataOne.navbar_theme = data.navbar_theme;
                settings.dataOne.brand_logo_theme = data.brand_logo_theme;
                settings.dataOne.navbar_fixed = data.navbar_fixed;
                settings.dataOne.main_color = data.main_color;
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
    
            if (data.sidebar_collapse != '' && data.sidebar_collapse !== undefined){
                collapse.checked = true
            }
            if (data.sidebar_fixed != '' && data.sidebar_fixed !== undefined){
                sidebar_fixed.checked = true
            }
            if (data.sidebar_flat != '' && data.sidebar_flat !== undefined){
                sidebar_nav_flat.checked = true
            }
            if (data.sidebar_legacy != '' && data.sidebar_legacy !== undefined){
                sidebar_nav_legacy.checked = true
            }
            if (data.sidebar_orientation === 'hzt'){
                sidebar_orientation.checked = true
            }
            }
        //console.log('RESULTADO: ', data)
        //console.log('SETTINGS: ', settings)
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
nav_link.forEach((color)=>{
    color.addEventListener('click', () => {
        const link = color.getAttribute('data-link');
        sidebar.setAttribute('nav-link-theme', link);
        settings.dataOne.nav_link = link;
    })
})
navbar_theme.forEach((color)=>{
    color.addEventListener('click', () => {
        const nav_theme = color.getAttribute('header-theme')
        navbar.setAttribute('navbar-theme', nav_theme);
        settings.dataOne.navbar_theme = nav_theme;
    })
})
brand_logo_theme.forEach((color)=>{
    color.addEventListener('click', () => {
        const logo_theme = color.getAttribute('logo-theme');
        brand_logo.setAttribute('brand-logo-theme', logo_theme);
        settings.dataOne.brand_logo_theme = logo_theme;

    })
})

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

collapse.addEventListener('change', function() {
    if (this.checked) {
      body.classList.add('sidebar-collapse');
      settings.dataTwo.sidebar_options.collapse = 'sidebar-collapse';
    } else {
      body.classList.remove('sidebar-collapse');
      settings.dataTwo.sidebar_options.collapse = '';
    }
});
sidebar_fixed.addEventListener('change', function() {
    if (this.checked) {
      body.classList.add('layout-fixed');
      settings.dataTwo.sidebar_options.fixed = 'layout-fixed';
    } else {
      body.classList.remove('layout-fixed');
      settings.dataTwo.sidebar_options.fixed = '';
    }
});
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
sidebar_nav_flat.addEventListener('change', function() {
    if (this.checked) {
        nav_sidebar.classList.add('nav-flat');
      settings.dataTwo.sidebar_options.flat = 'nav-flat';
    } else {
        nav_sidebar.classList.remove('nav-flat');
      settings.dataTwo.sidebar_options.flat = '';
    }
});
sidebar_nav_legacy.addEventListener('change', function() {
    if (this.checked) {
        nav_sidebar.classList.add('nav-legacy');
      settings.dataTwo.sidebar_options.legacy = 'nav-legacy';
    } else {
        nav_sidebar.classList.remove('nav-legacy');
      settings.dataTwo.sidebar_options.legacy = '';
    }
});
sidebar_light.addEventListener('click', () => {
    sidebar.classList.remove('sidebar-dark-primary')
    sidebar.classList.add('sidebar-light-primary')
    settings.dataOne.sidebar_theme = 'sidebar-light-primary'

})
sidebar_dark.addEventListener('click', () => {
    sidebar.classList.remove('sidebar-light-primary')
    sidebar.classList.add('sidebar-dark-primary')
    settings.dataOne.sidebar_theme = 'sidebar-dark-primary'
})
theme_main.forEach((color)=>{
    color.addEventListener('click', () => {
        const theme = color.getAttribute('data-theme');
        main_color.setAttribute('main-color', theme);
        settings.dataOne.main_color = theme;
    })
})
save_settings.addEventListener('click', () => {
    const user_id = document.getElementById('user_id')
    save_data(user_id);
    console.log('SEND: ', settings)
})









// Asignar valores aleatorios a los atributos
    // settings.dataOne.nav_link = 'Inicio';
    // settings.dataOne.sidebar_theme = 'oscuro';
    // settings.dataOne.brand_logo_theme = 'logo.png';
    // settings.dataOne.navbar_theme = 'claro';
    // settings.dataTwo.sidebar_options.collapse = 'true';
    // settings.dataTwo.sidebar_options.legacy = 'legaaa';
    
    // let nuevoObjeto = {
    //     theme: {},
    //     sidebar_options: {},
    //     small_text: {}
    // };
    // if (settings.dataOne != {}){
    //     for (let key in settings.dataOne) {
    //         if (settings.dataOne.hasOwnProperty(key) && settings.dataOne[key] !== undefined && settings.dataOne[key] !== "") {
    //             nuevoObjeto.theme[key] = settings.dataOne[key];
    //         }
    //     }
    // }
    // if (settings.dataTwo.sidebar_options != {}){
    //     for (let key in settings.dataTwo.sidebar_options) {
    //         if (settings.dataTwo.sidebar_options.hasOwnProperty(key) && settings.dataTwo.sidebar_options[key] !== undefined && settings.dataTwo.sidebar_options[key] != "") {
    //             nuevoObjeto.sidebar_options[key] = settings.dataTwo.sidebar_options[key];
    //         }
    //     }
    // }
    // if (settings.dataTwo.small_text != ''){
    //     for (let key in settings.dataTwo.small_text) {
    //         if (settings.dataTwo.small_text.hasOwnProperty(key) && settings.dataTwo.small_text[key] !== undefined && settings.dataTwo.small_text[key] != "") {
    //             nuevoObjeto.small_text[key] = settings.dataTwo.small_text[key];
    //         }
    //     }
    // }
    // Crear nuevo objeto con atributos no vacíos
    