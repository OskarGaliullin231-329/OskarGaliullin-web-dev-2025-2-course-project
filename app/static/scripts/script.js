let del_mes = document.getElementById('del-mes');

let del_btn = document.getElementById('del-btn');

del_btn.addEventListener('click', function() {
    del_mes.style='display: block;';
});

let yes_btn = document.getElementById('yes-btn');
let no_btn = document.getElementById('no-btn');

// yes_btn.addEventListener('click', function() {});
no_btn.addEventListener('click', function() {
    del_mes.style = 'display: none;';
});
