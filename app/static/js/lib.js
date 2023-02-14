class Utility {
    loadTemplateData() {
        return JSON.parse(document.getElementById('DJANGODATA').textContent);
    }

    getCookie(name) {
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

    postRequest(url, data) {
        return fetch(url, {
            method: 'POST',
            credentials: 'same-origin',
            headers:{
                'Accept': 'application/json',
                'X-CSRFToken': this.getCookie('csrftoken'),
            },
            body: JSON.stringify(data)
        })
    }
}

const util = new Utility()
