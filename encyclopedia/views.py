from django.http import HttpResponse
from httplib2 import Http
import markdown2
from django.shortcuts import render
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def load_page(request, entry):
    page = util.get_entry(entry)
    if page is not None:
        content = markdown2.markdown(page)
        return render(request, "encyclopedia/specificpage.html", {
            "content": content
        })
    return render(request, "encyclopedia/specificpage.html", {
        "content": "404: Page not found"
    })


def create_new_page(request):
    return render(request, "encyclopedia/newpage.html")


def random_page(request):
    from random import choice
    content = markdown2.markdown(util.get_entry(choice(util.list_entries())))
    return render(request, "encyclopedia/randompage.html", {
        "content": content
    })
