from markdown2 import Markdown
from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib import messages
from django.shortcuts import redirect
from django.core.files.storage import default_storage
from django.core.validators import RegexValidator
import markdown2
import re
import random

from . import util




class CreatePageForm(forms.Form):
    title = forms.CharField(label="Enter a title", max_length=30,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control mb-4'}),
                            validators=[RegexValidator('^[a-zA-Z0-9 -]{1,30}$', message="Title must be between 1 to 30 characters, contain only Latin letters, digits, dashes and spaces")])
    description = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', "rows": "17"}), label="Enter a description", max_length=1000)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def greet(request, name):
    md = Markdown()
    greetPage = util.get_entry(name)
    if (greetPage is None):
        return render(request, "encyclopedia/error.html", {
            "title": name
        })
    else :
        return render(request, "encyclopedia/greet.html", {
            "greetTitle" : name, 
            "content" : md.convert(greetPage),
        })


def search(request):
    query = request.GET.get("q", "")
    if query is None or query == "":
        return render(request, "encyclopedia/search.html", {
            "found": "",
            "query" : query
        })
    else:

        entries = util.list_entries();
        found = [
                valid_entry
                for valid_entry in entries
                if query.lower() in valid_entry.lower()
            ]

        return render(request, "encyclopedia/search.html", {
            "found": found, 
            "query": query
            })




def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html", {
            "form": CreatePageForm()
        })
    if request.method == "POST":
        form = CreatePageForm(request.POST)
        if not form.is_valid():
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
        title = form.cleaned_data["title"]
        content = form.cleaned_data["description"]

        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            messages.add_message(request, messages.ERROR,
                                 'Entry already exists with the provided title!')
            return render(request, "encyclopedia/new_page.html", {
                "form": form
            })
        else:
            util.save_entry(title, content)
            return redirect("greet", title)





def edit_page(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "content": content})

    if request.method == "POST":
        content = request.POST.get("description")
        util.save_entry(title, content)
        return redirect("greet", title)


def random_(request):
    list = util.list_entries()
    choice = random.choice(list)
    return redirect("greet", choice)





def login(request):
    return render(request, "encyclopedia/login.html")



