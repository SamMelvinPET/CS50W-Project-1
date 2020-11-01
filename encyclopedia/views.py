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


class NewPageForm(forms.Form):
    newtitle = forms.CharField(
        label="New Entry Title:"
        )
    pagecontent = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={'placeholder':'Page content goes here'})
        )
    editpage = forms.BooleanField(
        label="",
        widget=forms.HiddenInput(),
        initial=False,
        required=False
        )



def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        print(form.errors)
        if form.is_valid():
            newtitle = form.cleaned_data["newtitle"]
            pagecontent = form.cleaned_data["pagecontent"]
            editpage = form.cleaned_data["editpage"]
            entries = util.list_entries()
            if not(editpage):
                if util.get_entry(newtitle) != None:
                    return render(request, "encyclopedia/newpage.html", {
                        "title":"New Entry",
                        "search": SearchBar(),
                        "form": NewPageForm(initial={'newtitle':newtitle, 'pagecontent':pagecontent}),
                        "alert": True
                        })
            
            util.save_entry(newtitle, pagecontent)
            return HttpResponseRedirect(f"wiki/{newtitle}")
        else:
            return HttpResponse('Form not valid')

    else:
        return render(request, "encyclopedia/newpage.html", {
            "title":"New Entry",
            "search": SearchBar(),
            "form": NewPageForm(),
            "alert": False
            })

def editpage(request, name):
    return render(request, "encyclopedia/newpage.html", {
        "title":"Edit Entry",
        "search": SearchBar(),
        "form": NewPageForm(initial={'newtitle':name, 'pagecontent':util.get_entry(name), 'editpage':True}),
        "alert": False
        })
