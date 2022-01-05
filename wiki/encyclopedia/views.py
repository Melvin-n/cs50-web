from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# takes title which is typed into url bar and returns an entry using get_entry function
def entry_page(request, title):
    if util.get_entry(title) == None:
        return render(request, 'encyclopedia/not_found.html', {
            'title': title
        })
    else:
        return render(request, 'encyclopedia/entry.html', {
            'entry': util.get_entry(title),
            'title' : title.capitalize()
        })

