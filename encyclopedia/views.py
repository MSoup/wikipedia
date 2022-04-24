from distutils import file_util
from xmlrpc.client import ResponseError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
import markdown2
import random 
from . import util


def index(request):
    queryStringValue = request.GET.get('q')

    # No query string, return default index page
    allEntries = util.list_entries()
    if not queryStringValue:
        return render(request, "encyclopedia/index.html", {
        "entries": allEntries
    })

    # Query string entered, find exact match
    if queryStringValue in allEntries:
        return title(request, queryStringValue)
    
    # No exact match, find partial matches
    matches = []

    for entry in allEntries:
        if queryStringValue.lower() in entry.lower():
            matches.append(entry)

    if matches:
        return render(request, "encyclopedia/search_results.html", {
        "entries": matches
    })

    else:
        return render(request, "encyclopedia/search_results.html", {
        "entries": allEntries,
        "no_matches_notification": True,
    })

def display_contents(request, title):
    """
    displays the content of a file
    title is the part in wiki/{title}, and corresponds to a md file within the entries directory
    """
    file = util.get_entry(title)
    if file:
        file_to_html = markdown2.markdown(file)
        return render(request, "encyclopedia/display_entry.html", {
            "entry_title": title.capitalize(),
            "contents": file_to_html,
        })
    else:
        return HttpResponseNotFound("Not found")

def new_page(request):
    if request.method == "POST":
        form = util.NewPost(request.POST)
        file_exists = False

        title = request.POST['title']
        content = request.POST['body']

        if form.is_valid():
            try:
                util.save_entry(title, content)
                return display_contents(request, title)
            except:
                file_exists = True
                pass

        # Form not valid, OR title exists
        print(form)
        return render(request, 'encyclopedia/new_page.html', {
            "form": form,
            "file_exists": file_exists,
            "title": title,
            "content": content,
        })

    return render(request, "encyclopedia/new_page.html")

def random_page(request):
    allEntries = util.list_entries()

    select_page = random.choice(allEntries)
    return display_contents(request, select_page)