let DJANGODATA = util.loadTemplateData();
let current_record;
let bookmark_modal;

function refresh() {
    window.location.assign("/bookmark")
}

function remove_bookmark_modal(key,index) {
    current_record = DJANGODATA.records[key]["lists"][index]
    
    document.getElementById("remove_modal_label").innerHTML = "Remove "+current_record.display_title+"?"
    bookmark_modal = new bootstrap.Modal(document.getElementById('remove_bookmark_modal'))
    bookmark_modal.show()
}

function remove_bookmark() {
    let postdata = {
        "id" : current_record.bookmark
    }

    document.getElementById("remove_bookmark").disabled = true
    util.postRequest("/bookmark/remove", postdata).then(response => {
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
    let record = DJANGODATA.records[key]["lists"][index]
    window.open(record.link.url);
}