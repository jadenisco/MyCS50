from django.http import HttpResponse
from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    t = util.get_entry(title)
    print(t)
    return HttpResponse(f"Contents: {t}!")
