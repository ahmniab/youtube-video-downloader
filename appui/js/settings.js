const settings_form = document.querySelector('.w-50.p-3')
const spinner = document.getElementById('spinner')
const dl_path_inpt = document.getElementById('download_path')
const port_inpt = document.getElementById('port')


var xhr = new XMLHttpRequest();
xhr.open("GET", `http://${HOST_NAME}/change-settings`);

xhr.onload = function () {
    if (xhr.status >= 200 && xhr.status < 300) {
        let response = JSON.parse(xhr.responseText);
        console.log(response)
        dl_path_inpt.value = response.download_path
        port_inpt.value = response.port
        spinner.classList.add('hidden')
        settings_form.classList.remove('hidden')
        
    } else {
        console.error("Request failed with status:", xhr.status);
    }
};

xhr.onerror = function () {
    console.error("Request failed");
};

xhr.send();

function save_settings() {
    // if (!Number.isInteger(port_inpt.value)) 
    //     return
    
    xhr.open("POST", `http://${HOST_NAME}/change-settings`, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            let response = JSON.parse(xhr.responseText);
            console.log("Success:", response);
            alert('settings updated')
        } else {
            console.error("Request failed with status:", xhr.status);
            alert('faild to update settings')
        }
    };

    xhr.onerror = function (e) {
        console.error(e);
        alert('faild to update settings')
    };

    var data = JSON.stringify({
        port: parseInt(port_inpt.value),
        download_path: dl_path_inpt.value
    });
    xhr.send(data);
}

