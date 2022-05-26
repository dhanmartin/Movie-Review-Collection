const mydata = JSON.parse(document.getElementById('mydata').textContent)
function search() {
    let url = build_url(1)
    window.location.assign(url)
}

function next() {
    let url = build_url(mydata.next_page)
    window.location.assign(url)
}

function previous() {
    let url = build_url(mydata.previous_page)
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
        page_no = mydata.current_page
    }
    let url = "/page/"+page_no+get_url_for_search()
    return url
}

function show_modal(index) {
    let record = mydata.records[index]
    let myModal = new bootstrap.Modal(document.getElementById('myModal'))
    document.getElementById("modal_movie_title").innerHTML = record.display_title
    document.getElementById("modal_movie_description").innerHTML = record.summary_short
    myModal.show()
}

function load_review_page(index) {
    let record = mydata.records[index]
    window.open(record.link.url);
}

let input = document.getElementById("search_box");
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        search()
    }
});