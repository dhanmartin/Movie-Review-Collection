from django.urls import path
from app.import_views import *

urlpatterns = [
    path('', index.default, name='home'),
    path('page/<int:page_no>', index.default),
    path('bookmark', bookmark.default),
    path('bookmark/add', bookmark.add),
]