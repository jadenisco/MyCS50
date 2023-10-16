from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    md_content = util.get_entry(title)
    mdc = Markdown()
    html_content = mdc.convert(md_content)
    return render(request, "encyclopedia/entry.html" , {
        "title": title,
        "content": html_content
    })
