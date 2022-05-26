import requests
from app.views.common import *

def default(request, page_no=1):
    """ Main page """

    try:
        keyword = request.GET.get("q")
        response = read_reviews(page_no,keyword)

        data = {
            "records" : response["records"],
            "next_page" : page_no + 1,
            "previous_page" : page_no - 1,
            "current_page" : page_no,
            "q" : keyword if keyword else "",
        }

        data["previous_disabled"] = "disabled" if data["previous_page"] == 0 else ""
        data["next_disabled"] = "disabled" if not response["has_more"] else ""

        return render(request, "index.html", {"data" : data})
    except Exception as e:
        debug_exception(e)
        data = {}
        return render(request, "error.html", {"data" : data})

def read_reviews(page_no=0,keyword=None) -> dict:
    """ Read reviews """

    try:
        max_record = 10
        offset = (page_no - 1) * max_record
        api_key = "mIq3gHXGmWLJb9cP2m3VTcvomwh8M4j0"
        query = ""
        if keyword:
            query = f"&query={keyword}"
        url = f"https://api.nytimes.com/svc/movies/v2/reviews/search.json?api-key={api_key}&offset={offset}{query}"
        response = requests.get(url)
        data = response.json()
        records = data.pop("results",None)[0:max_record]
        results = {
            "records" : records,
            "has_more" : data.get("has_more")
        }
        return results
    except Exception as e:
        debug_exception(e)
        raise e
