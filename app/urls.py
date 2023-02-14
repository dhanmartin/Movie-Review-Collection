from django.urls import path

from app.views import (
    bookmark,
    index,
)


urlpatterns = [
    path("", index.default, name="home"),
    path("page/<int:page_no>", index.default),
    path("bookmark", bookmark.default),
    path("bookmark/add", bookmark.add),
    path("bookmark/remove", bookmark.remove),
]
