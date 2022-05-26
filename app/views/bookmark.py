from app.forms.bookmark import Bookmark_folder_form, Bookmark_form
from app.models.bookmark import Bookmark_folder
from app.views.common import *

def default(request):
    """ Main page """

    try:
        if not request.user.pk:
            return redirect("home")
    except Exception as e:
        debug_exception(e)
        data = {}
        return render(request, "error.html", {"data" : data})

def add(request):
    """ Add bookmark """


    try:
        postdata = json.loads(request.body.decode("utf-8")) if request.body.decode("utf-8") else {}
        
        bookmark_folder = postdata.get("folder")
        if not bookmark_folder:
            folder_name = postdata.get("name")

            data = {
                "user" : request.user.pk,
                "name" : folder_name
            }
            instance_form = Bookmark_folder_form(data)
            if instance_form.is_valid():
                instance_save = instance_form.save()
                bookmark_folder = instance_save.pk
            else:
                raise_error(beautify_form_errors(instance_form.errors))

        data = {
            "user" : request.user.pk,
            "folder" : bookmark_folder,
            "data" : postdata.get("data",{})
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