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

// File upload functionality
document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('files');
    const fileList = document.getElementById('file-list');
    
    if (fileInput && fileList) {
        fileInput.addEventListener('change', function() {
            fileList.innerHTML = '';
            
            for (let i = 0; i < this.files.length; i++) {
                const file = this.files[i];
                const fileItem = document.createElement('div');
                fileItem.className = 'file-preview-item';
                fileItem.innerHTML = `
                    <span>${file.name}</span>
                    <span class="file-size">(${(file.size / 1024).toFixed(1)} KB)</span>
                `;
                fileList.appendChild(fileItem);
            }
        });
    }
});
