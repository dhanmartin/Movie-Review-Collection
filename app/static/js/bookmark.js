function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');


const mydata = JSON.parse(document.getElementById('mydata').textContent)
let current_record;
let bookmark_modal;

function refresh() {
    window.location.assign("/bookmark")
}

function remove_bookmark_modal(key,index) {
    current_record = mydata.records[key]["lists"][index]
    
    document.getElementById("remove_modal_label").innerHTML = "Remove "+current_record.display_title+"?"
    bookmark_modal = new bootstrap.Modal(document.getElementById('remove_bookmark_modal'))
    bookmark_modal.show()
}

function remove_bookmark() {
    let postdata = {
        "id" : current_record.bookmark
    }

    document.getElementById("remove_bookmark").disabled = true
    fetch("/bookmark/remove", {
        method: 'POST',
        credentials: 'same-origin',
        headers:{
            'Accept': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(postdata)
    })
    .then(response => {
            document.getElementById("remove_bookmark").disabled = false

            if (!response.ok) {
                return response.text().then(text => { 
                    throw new Error(text) 
                })
            }
            return response.text()
    })
    .then(data => {
        bookmark_modal.hide()
        refresh()
    })
    .catch(error => {
        alert(error.message)
    })

}

function load_review_page(key,index) {
    let record = mydata.records[key]["lists"][index]
    window.open(record.link.url);
}