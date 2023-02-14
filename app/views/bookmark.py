import json
from typing import OrderedDict

from django.shortcuts import (
    HttpResponse,
    redirect,
    render,
)

from app.forms.bookmark import (
    Bookmark_folder_form,
    Bookmark_form,
)
from app.models.bookmark import (
    Bookmark,
    Bookmark_folder,
)
from app.views.common import (
    beautify_form_errors,
    debug_exception,
    raise_error,
)


def default(request):
    """Main page"""

    try:
        if not request.user.pk:
            return redirect("home")

        records = read_bookmarks_group_per_folder(request)
        data = {
            "active_menu": "bookmark",
            "records": records,
        }
        return render(request, "bookmark.html", {"data": data})
    except Exception as e:
        debug_exception(e)
        data = {}
        return render(request, "error.html", {"data": data})


def read_bookmarks_group_per_folder(request) -> list:
    """Read bookmarks group per folder"""

    try:
        instances = Bookmark.objects.select_related("folder").filter(user=request.user.pk).order_by("folder__name")

        per_folder = OrderedDict()

        for instance in instances:
            key = instance.folder_id
            if key not in per_folder:
                per_folder[key] = {
                    "name": instance.folder.name,
                    "lists": [],
                }

            row = instance.data
            row["bookmark"] = instance.pk

            per_folder[key]["lists"].append(row)

        records = []
        for i in per_folder:
            record = per_folder[i]

            records.append(record)

        return records
    except Exception as e:
        debug_exception(e)
        raise e


def add(request):
    """Add bookmark"""

    try:
        postdata = json.loads(request.body.decode("utf-8")) if request.body.decode("utf-8") else {}

        bookmark_folder = postdata.get("folder")
        if not bookmark_folder:
            folder_name = postdata.get("name")

            data = {
                "user": request.user.pk,
                "name": folder_name,
            }
            instance_form = Bookmark_folder_form(data)
            if instance_form.is_valid():
                instance_save = instance_form.save()
                bookmark_folder = instance_save.pk
            else:
                raise_error(beautify_form_errors(instance_form.errors))

        data = {
            "user": request.user.pk,
            "folder": bookmark_folder,
            "data": postdata.get("data", {}),
        }

        instance_form = Bookmark_form(data)
        if instance_form.is_valid():
            instance_form.save()
        else:
            raise_error(beautify_form_errors(instance_form.errors))

        return HttpResponse("Success!")
    except Exception as e:
        debug_exception(e)
        return HttpResponse(str(e), status=400)


def remove(request):
    """Remove bookmark"""

    try:
        postdata = json.loads(request.body.decode("utf-8")) if request.body.decode("utf-8") else {}

        try:
            instance = Bookmark.objects.get(id=postdata["id"], user=request.user.pk)
        except Exception as e:
            raise_error("Bookmark not found!")

        bookmark_folder = instance.folder_id
        instance.delete()

        folder_not_empty = Bookmark.objects.filter(folder=bookmark_folder, user=request.user.pk).exists()
        if not folder_not_empty:
            Bookmark_folder.objects.filter(id=bookmark_folder).delete()

        return HttpResponse("Success!")
    except Exception as e:
        debug_exception(e)
        return HttpResponse(str(e), status=400)
