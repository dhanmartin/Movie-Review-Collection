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