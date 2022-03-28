import markdown2
from django.shortcuts import redirect, render
from . import util


def index(request):
    if request.method == 'POST':
        search_query = request.POST.get("q")
        for page in util.list_entries():
            if search_query.lower() == page.lower():
                return redirect("specific entry", entry=page)
        # implement proper search mentioned on cs50 website.
        return render(request, "encyclopedia/error.html", {
            "content": "No search result found",
            "title": "No search result found"
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def load_page(request, entry):
    page = util.get_entry(entry)
    if request.method == "POST":
        if request.POST.get("Edit") == "":
            return render(request, "encyclopedia/editpage.html", {
                "oldcontent": page,
                "title": "Edit page: " + entry
            })

        elif request.POST.get("Ncontent") != "":
            newcontent = request.POST.get("Ncontent")
            util.save_entry(entry, newcontent)
            return redirect("specific entry", entry=entry)
    if page is not None:
        content = markdown2.markdown(page)
        return render(request, "encyclopedia/specificpage.html", {
            "content": content,
            "title": entry
        })

    return render(request, "encyclopedia/error.html", {
        "content": "404: Page not found",
        "title": "404 error"
    })


def create_new_page(request):
    if request.method == "POST":
        title = request.POST.get("fname")
        content = request.POST.get("fcontent")
        if title not in util.list_entries():
            util.save_entry(title, content)
            return redirect("specific entry", entry=title)
        else:
            content = f"""
            <div class="alert alert-danger" role="alert">
                Same page already exists, 
                <a href="/wiki/{title}/">{title}</a> 
            </div>
            """
            return render(request, "encyclopedia/newpage.html", {
                "content": content
            })
    return render(request, "encyclopedia/newpage.html")


def random_page(request):
    from random import choice
    content = markdown2.markdown(util.get_entry(choice(util.list_entries())))
    return render(request, "encyclopedia/randompage.html", {
        "content": content
    })
