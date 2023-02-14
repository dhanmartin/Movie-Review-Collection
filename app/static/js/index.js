let DJANGODATA = util.loadTemplateData();
let current_index;
let bookmark_modal;

function refresh() {
    let url = build_url()
    window.location.assign(url)
}

function search() {
    let url = build_url(1)
    window.location.assign(url)
}

function next() {
    let url = build_url(DJANGODATA.next_page)
    window.location.assign(url)
}

function previous() {
    let url = build_url(DJANGODATA.previous_page)
    window.location.assign(url)
}

function get_url_for_search() {
    let keyword = document.getElementById("search_box").value
    let url = ""
    if (keyword) {
        url = "?q="+keyword
    }

    return url
}

function build_url(page_no) {
    if (!page_no) {
        page_no = DJANGODATA.current_page
    }
    let url = "/page/"+page_no+get_url_for_search()
    return url
}

function show_modal(index) {
    current_index = index
    let record = DJANGODATA.records[index]
    document.getElementById("submit_bookmark").disabled = false
    document.getElementById("modal_movie_title").innerHTML = record.display_title
    document.getElementById("modal_movie_description").innerHTML = record.summary_short
    let bookmark_folder = document.getElementById("bookmark_folder")
    bookmark_folder.value = ''
    bookmark_folder_change(bookmark_folder)
    document.getElementById("bookmark_folder_name").value = ''
    bookmark_modal = new bootstrap.Modal(document.getElementById('myModal'))
    bookmark_modal.show()
}

function bookmark_folder_change(element) {
    let new_folder = document.getElementById("new_folder_name")
    if (!element.value) {
        new_folder.style.display = ""
    }
    else {
        new_folder.style.display = "none"
    }
}

function add_bookmark() {
    let record = DJANGODATA.records[current_index]

    let postdata = {
        "name" : document.getElementById("bookmark_folder_name").value,
        "folder" : document.getElementById("bookmark_folder").value,
        "data" : record,
    }

    document.getElementById("submit_bookmark").disabled = true
    util.postRequest("/bookmark/add", postdata).then(response => {
        document.getElementById("submit_bookmark").disabled = false

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

function remove_bookmark_modal(index) {
    current_index = index
    let record = DJANGODATA.records[index]

    document.getElementById("remove_modal_label").innerHTML = "Remove "+record.display_title+"?"
    bookmark_modal = new bootstrap.Modal(document.getElementById('remove_bookmark_modal'))
    bookmark_modal.show()
}

function remove_bookmark() {
    let record = DJANGODATA.records[current_index]

    let postdata = {
        "id" : record.bookmark
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

function load_review_page(index) {
    let record = DJANGODATA.records[index]
    window.open(record.link.url);
}

let input = document.getElementById("search_box");
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        search()
    }
});
