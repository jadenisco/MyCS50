from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util

class CreateEntryForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    content = forms.CharField(label="", widget=forms.Textarea)


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
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:index"))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form 
            })

    return render(request, "encyclopedia/create.html", {
        "form": CreateEntryForm(),
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
