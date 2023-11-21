const showNotification = document.getElementById('btnNot')
const containerNotify = document.querySelector('.Menu_NOtification_Wrap')
const btnSend = document.querySelector('.btn_notify')
const bodyNotification = document.querySelector('.Notification_body')
const unread_notifications = document.querySelector('.number_ntf')
const btn_all = document.querySelector('.btn_all')
const btn_unread = document.querySelector('.btn_unread')
const btn_read = document.querySelector('.btn_read')

//Dropdown
let notiActive = false;
let num_notifications = 0;

function popup_notification() {
  const Toast = Swal.mixin({
    toast: true,
    position: 'top',
    customClass: {
      popup: 'colored-toast'
    },
    showClass: {
      popup: 'fade_down_animation'
    },
    showConfirmButton: false,
    timer: 3600,
  })
  Toast.fire({
    icon: 'info',
    title: 'Tienes una nueva notificación'
  })
}

function scrollToBottomNotify() {
  bodyNotification.scrollTop = bodyNotification.scrollHeight;
}

//CONEXION CON WEBSOCKET
let notifySocket = new WebSocket(`ws://${window.location.host}/ws/notification/`);
notifySocket.onmessage = function (e) {
  console.log("onMessage");
  onNotification(JSON.parse(e.data));
};
notifySocket.onopen = function (e) {
  console.log("CONNECTION ESTABLISHED");
};
notifySocket.onclose = function (e) {
  console.log("CONNECTION LOST");
};
notifySocket.onerror = function (e) {
  console.log(e);
};

async function get_notification() {
  const data = new FormData();
  const my_id = document.getElementById('user_id')
  data.append("action", "get_notification");
  data.append("id", my_id.value);

  await fetch("/notificacion/list/", {
    method: "POST",
    body: data,
  }).then(function (res) {
    return res.json();
  }).then(function (data) {
    let li = ''
    let notification = data
    num_notifications = notification.unread;
    num_notifications !== 0 ? unread_notifications.textContent = num_notifications : unread_notifications.textContent = ''
    notification.notify.map((notify) => {
      li += `<div class="contains_id" id-notify="${notify.id}">
      <div class="content_notify redirect" data-read="${notify.read}">
          <div class="single_notify d-flex align-items-center position-relative redirect">
            <div class="notify_thumb">
              <img src="${notify.image}" class="redirect" alt="">
            </div>
            <div class="notify_content redirect">
              <p class="redirect">${notify.message} - ${notify.title}</p>
            </div>
            <span class="timesince_notify redirect">hace ${notify.created_at}</span>
          </div>
        <div class="custom-dropdown">
      </div>
          <span class="delete_notification choices_notification">
            <i class="fas fa-ellipsis-v choices_notification"></i>                  
          </span>
          <ul class="dropdown__menu dropdown__choices" data-id="${notify.id}">
            ${notify.read !== true ?
          `<li class="dropdown__item notify__read">
                <a class="dropdown__name notify__read">  <i class="fas fa-check"></i> Marcar como leída</a>
              </li>` : ''}
            <li class="dropdown__item notify__delete">
              <a class="dropdown__name notify__delete"><i class="fas fa-trash"></i> Eliminar</a>
            </li>
          </ul>
        </div>
      </div>`;
      bodyNotification.innerHTML = li;
    })
  });
}
get_notification()
const onNotification = (data) => {
  if (data.type === 'new_notification') {
    console.log(data)
    const my_id = document.getElementById('user_id').value
    let firstNotification = bodyNotification.firstChild;
    data.user_receptor.some(user_id => {
      if (my_id == user_id.id) {
        num_notifications += 1
        unread_notifications.textContent = num_notifications;
        const newNotification = document.createElement("div");
        newNotification.classList.add("content_notify");
        newNotification.setAttribute("data-read", "false");
        newNotification.innerHTML = `
                <a href="${data.url}">
                <div class="single_notify d-flex align-items-center position-relative">
                  <div class="notify_thumb">
                    <img src="${data.image}" alt="">
                  </div>
                  <div class="notify_content">
                    <p>${data.message} - ${data.title}</p>
                  </div>
                  <span class="timesince_notify">hace ${data.created_at}</span>
                </div>                
              </a>
              <div class="custom-dropdown">
                <span class="delete_notification choices_notification">
                      <i class="fas fa-ellipsis-v choices_notification"></i>                  
                </span>
                <ul class="dropdown__menu dropdown__choices" data-id="${data.id}">
                  <li class="dropdown__item notify__read">
                    <a class="dropdown__name notify__read">  <i class="fas fa-check"></i> Marcar como leida</a>
                  </li>
                  <li class="dropdown__item notify__delete">
                    <a class="dropdown__name notify__delete"><i class="fas fa-trash"></i> Eliminar</a>
                  </li>
                </ul>             
              </div>
            `
        popup_notification();
        return bodyNotification.insertBefore(newNotification, firstNotification);
      }
    });
  }
}
//PARA FILTRAR LAS NOTIFICACIONES
btn_all.addEventListener('click', function () {
  const notificacions_all = document.querySelectorAll('.content_notify')
  notificacions_all.forEach((all) => {
    all.style.display = "block";
  })
  document.querySelector('button.tab_active').classList.remove('tab_active')
  btn_all.classList.add('tab_active')
})
btn_unread.addEventListener('click', function () {
  const notificacions_all = document.querySelectorAll('.content_notify')
  Array.from(notificacions_all).filter(read => {
    if (read.getAttribute("data-read") !== "true") {
      read.style.display = "block";
    } else {
      read.style.display = "none";
    }
  });
  document.querySelector('button.tab_active').classList.remove('tab_active')
  btn_unread.classList.add('tab_active')
})
btn_read.addEventListener('click', function () {
  const notificacions_all = document.querySelectorAll('.content_notify')
  Array.from(notificacions_all).filter(read => {
    if (read.getAttribute("data-read") !== "false") {
      read.style.display = "block";
    } else {
      read.style.display = "none";
    }
  });
  document.querySelector('button.tab_active').classList.remove('tab_active')
  btn_read.classList.add('tab_active')
})

showNotification.addEventListener('click', function () {
  containerNotify.classList.toggle("active");
})
document.addEventListener('click', function (event) {
  if (!containerNotify.contains(event.target) && !showNotification.contains(event.target)) {
    containerNotify.classList.remove('active');
    //notiActive = false;      
  }
});

async function manageNotification(action, id) {
  const data = new FormData();
  const my_id = document.getElementById('user_id').value
  data.append("notification_id", id);
  data.append("user_id", my_id);

  action ? data.append("action", "read") : data.append("action", "delete");

  await fetch("/notificacion/list/", {
    method: "POST",
    body: data,
  })
    .then(function (res) {
      return res.json();
    })
    .then(function (data) {
      if (data.notify == false) {
        num_notifications -= 1;
        if (num_notifications === 0) {
          return unread_notifications.textContent = ''
        }
        unread_notifications.textContent = num_notifications
      }
    });
}

const read_notify = async (id) => {
  console.log(id)
  const data = new FormData();
  const my_id = document.getElementById('user_id').value
  data.append("notification_id", id);
  data.append("user_id", my_id);
  data.append("action", "read")

  await fetch("/notificacion/list/", {
    method: "POST",
    body: data,
  })
    .then(function (res) {
      return res.json();
    })
    .then(function (data) {
      location.href = data.url
      console.log(data)
    });
}

bodyNotification.addEventListener('click', function (event) {
  let event_target = event.target
  if (event_target.classList.contains('choices_notification')) {

    let choicesContent = event.target.closest('div')
    choicesContent.classList.toggle('show-dropdown')

  } if (event_target.classList.contains('notify__delete')) {
    event.stopPropagation();
    let id_delete = event_target.closest('ul').getAttribute("data-id")
    let element = event_target.closest('div.content_notify')
    element.remove();
    let action = false;
    manageNotification(action, id_delete)

  } else if (event_target.classList.contains('notify__read')) {
    event.stopPropagation();
    let id_read = event_target.closest('ul').getAttribute("data-id")
    event_target.closest('div.content_notify').setAttribute("data-read", "true")
    let li = event_target.closest('li.notify__read')
    li.remove();
    let action = true;
    manageNotification(action, id_read)
  }
  else if (event_target.classList.contains('redirect')) {
    let id_read = event_target.closest('div.contains_id').getAttribute("id-notify")
    read_notify(id_read)
    //console.log(event_target.closest('div.contains_id').getAttribute("id-notify"))
  }
});

// let dropdownActive = false;
// choicesButton.forEach((btn)=>{
//   btn.addEventListener("click", ()=>{
//     console.log('asdasdsad')
//     if (dropdownActive == false) {
//       choicesContent.classList.add('show-dropdown')
//       dropdownActive = true;
//     } else if (dropdownActive) {
//       choicesContent.classList.remove("show-dropdown");
//         dropdownActive = false;
//     }
//   })
// })

// choicesButton.addEventListener('click', () => {
//     if (dropdownActive == false) {
//         choicesContent.classList.add('show-dropdown')
//         dropdownActive = true;
//     } else if (dropdownActive) {
//       choicesContent.classList.remove("show-dropdown");
//         dropdownActive = false;
//     }
// })
// document.addEventListener('click', function (event) {
//     if (dropdownActive && !choicesContent.contains(event.target) && !dropdownButton.contains(event.target)) {
//       choicesContent.classList.remove('show-dropdown');
//         dropdownActive = false;
//     }
// });

