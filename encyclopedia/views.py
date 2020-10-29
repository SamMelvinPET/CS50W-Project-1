from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def viewpage(request, name):
    pagedata = util.get_entry(name)

    if pagedata == None:
        return render(request, "encyclopedia/entrynotfound.html")
    
    return render(request, "encyclopedia/entry.html", {
        "pagedata": markdown(pagedata),
        "pagetitle": name
        })



