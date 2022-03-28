import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None


def search_wiki(request):
    search_query = request.POST.get("q")
    list_of_matches = []
    flag = False
    for page in list_entries():
        if search_query.lower() == page.lower():
            flag = True
            break
        if search_query.lower() in page.lower():
            list_of_matches.append(page)

    return flag, page, list_of_matches


def check_duplicate_entry(title):
    """True if duplicate entry found, else False"""
    flag = False
    for entry in list_entries():
        if title.strip().lower() == entry.strip().lower():
            flag = True  # same entry exists
            return flag
