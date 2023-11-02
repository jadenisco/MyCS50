from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from markdown2 import Markdown
import html2markdown
import random

from . import util

class SaveEntryForm(forms.Form):
    entry = forms.CharField(label="Entry", max_length=100)
    content = forms.CharField(label="", widget=forms.Textarea)
    overwrite = forms.CharField(widget=forms.HiddenInput)

class CreateEntryForm(forms.Form):
    entry = forms.CharField(label="Entry", max_length=100)
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
        if 'overwrite' in request.POST:
            form = SaveEntryForm(request.POST)
        else:
            form = CreateEntryForm(request.POST)

        if form.is_valid():
            entry = form.cleaned_data["entry"]
            content = form.cleaned_data["content"]
            if 'overwrite' not in form.cleaned_data:
                if entry in util.list_entries():
                    message = f'The entry "{entry}" is being used, please choose a different title.'
                    return(render(request, "encyclopedia/create.html",
                                {"form": form,
                                "alert_message": message}))

            util.save_entry(entry, content)
            return HttpResponseRedirect(reverse("wiki:entry",
                                                kwargs={'title': entry}))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form 
            })

    form = CreateEntryForm()
    form.fields['entry'].initial = 'Entry Name Here'
    form.fields['content'].initial = 'Entry Content Here'
    return render(request, "encyclopedia/create.html", {
        "form": form
    })


def edit(request):
    form = CreateEntryForm(request.POST)
    if form.is_valid():
        new_form = CreateEntryForm()
        new_form.fields['entry'].initial = form.cleaned_data['entry']
        content = html2markdown.convert(form.cleaned_data["content"])
        new_form.fields['content'].initial = content
        return(render(request, "encyclopedia/edit.html",{
            "form": new_form}))

    message = "The edited form is not valid!"
    return render(request, "encyclopedia/edit.html", {
            "form": form,
            "alert_message": message})


def entry(request, title):
    md_content = util.get_entry(title)
    if md_content:
        mdc = Markdown()
        html_content = mdc.convert(md_content)
    else:
        html_content = None

    return render(request, "encyclopedia/entry.html" , {
        "entry": title,
        "content": html_content,
    })


def random_page(request):
    entries = util.list_entries()
    entry_page = entries[random.randint(0, len(entries)-1)] 
    return(entry(request, entry_page))


def index(request):
    search_string = None
    entries = []

    if 'q' in request.GET:
        search_string = request.GET['q']
        entries = _list_entries(search_string)
    else:
        entries = _list_entries()

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "search_string": search_string
    })
