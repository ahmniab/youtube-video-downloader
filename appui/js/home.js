const link_box           = document.getElementById('link');
const video_formats_area = document.getElementById('video_formats');
const audio_formats_area = document.getElementById('audio_formats');
const download_btn       = document.getElementById('download_btn');

link_box.value = '';
let format_id = 1;

function add_video_format(format){
    let format_id_string = `format${format_id++}`;
    let video_format = document.createElement('div');
    video_format.classList.add('form-check');
    video_format.innerHTML = `
        <input class="form-check-input" type="radio" name="id" id="${format_id_string}" value="${format.id}">
        <label class="form-check-label" for="${format_id_string}">
                ${format.resolution} - ${(format.filesize / 1048576).toFixed(2)}MB - ${format.ext} 
        </label>
    `;
    video_formats_area.appendChild(video_format);

} 
function add_audio_format(format){
    let format_id_string = `format${format_id++}`;
    let audio_format = document.createElement('div');
    audio_format.classList.add('form-check');
    audio_format.innerHTML = `
        <input class="form-check-input" type="radio" name="id" id="${format_id_string}" value="${format.id}">
        <label class="form-check-label" for="${format_id_string}">
                ${format.resolution} - ${format.ext} 
        </label>
    `;
    audio_formats_area.appendChild(audio_format);
}

function add_to_formats_area(formats) {
    video_formats_area.innerHTML = '<h3>Video</h3>';
    audio_formats_area.innerHTML = '<h3>Audio</h3>';
    formats.video.forEach(format => {
            add_video_format(format);
    });
    formats.audio.forEach(format => {
            add_audio_format(format);
    });
}

link_box.addEventListener('change', (e)=> {
    var xhr = new XMLHttpRequest();

    xhr.open("POST", "http://localhost:8087/vid-info", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            let response = JSON.parse(xhr.responseText);
            add_to_formats_area(response);
            download_btn.classList.remove('disabled');
            console.log("Success:", response);
        } else {
            console.error("Request failed with status:", xhr.status);
        }
    };

    xhr.onerror = function () {
        console.error("Request failed");
    };

    var data = JSON.stringify({
        link: link_box.value,
    });
    xhr.send(data);

});
 