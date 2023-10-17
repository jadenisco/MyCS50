from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown

from . import util

def _list_entries(search_string=None):
    s_entries = []

    if search_string == None:
        return util.list_entries()
    
    for s in util.list_entries():
        if search_string.lower() in s.lower():
            s_entries.append(s)

    return s_entries

def index(request):
    search_string = None
    entries = []

    if 'q' in request.GET:
        entries = _list_entries(request.GET['q'])
        if len(entries) == 1:
            return(title(request, entries[0]))
    else:
        entries = _list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def title(request, title):
    md_content = util.get_entry(title)
    mdc = Markdown()
    html_content = mdc.convert(md_content)
    return render(request, "encyclopedia/entry.html" , {
        "title": title,
        "content": html_content
    })
