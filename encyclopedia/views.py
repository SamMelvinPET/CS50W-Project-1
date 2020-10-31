from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from markdown2 import markdown
from random import choice
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search": SearchBar()
    })

def viewpage(request, name):
    pagedata = util.get_entry(name)

    if pagedata == None:
        return render(request, "encyclopedia/entrynotfound.html", {
            "search": SearchBar()
            })
    
    return render(request, "encyclopedia/entry.html", {
        "pagedata": markdown(pagedata),
        "pagetitle": name,
        "search": SearchBar()
        })


class SearchBar(forms.Form):
    search = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search'})
        )


def search(request):
    if request.method == "POST":
        form = SearchBar(request.POST)
        if form.is_valid():
            searched = form.cleaned_data["search"]
            entries = util.list_entries()
            partials = [entry for entry in entries if searched.lower() in entry.lower()]
            if searched.lower() in [entry.lower() for entry in entries]:
                return HttpResponseRedirect(f"wiki/{searched}")
            else:
                return render(request, "encyclopedia/searchresults.html", {
                              "entries": partials,
                              "search": SearchBar()
                              })


def randompage(request):
    entry = choice(util.list_entries())
    return HttpResponseRedirect(f"wiki/{entry}")
