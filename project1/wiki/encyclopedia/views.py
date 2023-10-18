from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util

class CreateForm(forms.Form):
    created_content = forms.CharField(label="Hello John")
#    priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)


def _list_entries(search_string=None):
    s_entries = []

    if search_string == None:
        return util.list_entries()
    
    for s in util.list_entries():
        if search_string.lower() in s.lower():
            s_entries.append(s)

    return s_entries


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form 
            })

    return render(request, "encyclopedia/create.html", {
        "form": CreateForm(),
    })

def index(request):
    search_string = None
    entries = []

    if 'q' in request.GET:
        search_string = request.GET['q']
        entries = _list_entries(search_string)
        # Brings you directly to the entry, not exactly the
        # assignment, but saves a step to get to the page.
        # remove these 2 lines for the exact assignment functionality
        if len(entries) == 1:
            return(title(request, entries[0]))
    else:
        entries = _list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "search_string": search_string
    })
def title(request, title):
    md_content = util.get_entry(title)
    mdc = Markdown()
    html_content = mdc.convert(md_content)
    return render(request, "encyclopedia/entry.html" , {
        "title": title,
        "content": html_content
    })
