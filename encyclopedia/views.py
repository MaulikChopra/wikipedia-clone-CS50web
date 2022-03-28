import markdown2
from django.shortcuts import redirect, render
from . import util


def index(request):
    if request.method == 'POST':
        flag, exact_match, list_of_matches = util.search_wiki(request)
        if flag == True:
            return redirect("specific entry", entry=exact_match)
        if flag == False and len(list_of_matches) != 0:
            return render(request, "encyclopedia/searchresult.html", {
                "matches": list_of_matches
            })
        return render(request, "encyclopedia/error.html", {
            "content": "No search result found",
            "title": "No search result found"
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def load_page(request, entry):
    entry = entry.strip()
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
        if util.check_duplicate_entry(title):
            content = f"""
            <div class="alert alert-danger" role="alert">
                Same page already exists, 
                <a href="/wiki/{title}/">{title}</a> 
            </div>
            """
            return render(request, "encyclopedia/newpage.html", {
                "content": content
            })
        else:
            content = request.POST.get("fcontent")
            util.save_entry(title, content)
            return redirect("specific entry", entry=title)

    return render(request, "encyclopedia/newpage.html")


def random_page(request):
    from random import choice
    content = markdown2.markdown(util.get_entry(choice(util.list_entries())))
    return render(request, "encyclopedia/randompage.html", {
        "content": content
    })
