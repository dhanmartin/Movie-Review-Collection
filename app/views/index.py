import requests
from django.conf import settings
from app.models.bookmark import Bookmark, Bookmark_folder
from app.views.common import *

def default(request, page_no=1):
    """ Main page """

    try:
        keyword = request.GET.get("q")
        response = read_reviews(request,page_no,keyword)

        bookmark_folders = read_bookmark_folders(request)

        data = {
            "active_menu" : "home",
            "records" : response["records"],
            "next_page" : page_no + 1,
            "previous_page" : page_no - 1,
            "current_page" : page_no,
            "q" : keyword if keyword else "",
            "bookmark_folders" : bookmark_folders,
        }

        data["previous_disabled"] = "disabled" if data["previous_page"] == 0 else ""
        data["next_disabled"] = "disabled" if not response["has_more"] else ""

        return render(request, "index.html", {"data" : data})
    except Exception as e:
        debug_exception(e)
        data = {}
        return render(request, "error.html", {"data" : data})

def read_reviews(request,page_no=0,keyword=None) -> dict:
    """ Read reviews """

    try:
        max_record = 10
        offset = (page_no - 1) * max_record
        api_key = settings.NYTIMES_API_KEY
        
        query = ""
        if keyword:
            query = f"&query={keyword}"
        
        url = f"https://api.nytimes.com/svc/movies/v2/reviews/search.json?api-key={api_key}&offset={offset}{query}"
        response = requests.get(url)
        data = response.json()
        records = data.pop("results",None)
        if not records:
            records = []
        records = records[0:max_record]

        bookmarks = Bookmark.objects.filter(user=request.user.pk)
        bookmark_keys = {}
        for bookmark in bookmarks:
            key = f"{ bookmark.data.get('byline') }{ bookmark.data.get('display_title') }{ bookmark.data.get('publication_date') }"
            bookmark_keys[key] = bookmark.pk

        for record in records:
            key = f"{ record.get('byline') }{ record.get('display_title') }{ record.get('publication_date') }"
            record["bookmark"] = bookmark_keys.get(key)

        results = {
            "records" : records,
            "has_more" : data.get("has_more")
        }
        return results
    except Exception as e:
        debug_exception(e)
        raise e

def read_bookmark_folders(request) -> list:
    """ Read bookmark folders of current user """

    try:
        folders = []
        if request.user.pk:
            folders = list(Bookmark_folder.objects.filter(user=request.user.pk).order_by("name").values("id","name"))

        return folders
    except Exception as e:
        debug_exception(e)
        raise e