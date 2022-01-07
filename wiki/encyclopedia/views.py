from re import template
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
from django import forms
import random
import markdown2
from markdown2 import Markdown
markdowner = Markdown()




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
            'entry': markdowner.convert(util.get_entry(title)),
            'title' : title.capitalize()
        })

def search(request):
    search_term = request.POST['q'].lower()
    entries = util.list_entries()
    entries = map(lambda x: x.lower(), entries)
    if util.get_entry(search_term) == None:
        return render(request, 'encyclopedia/search_results.html', {
            "entries": entries,
            "search_term": search_term
        })
    else:
        return redirect(f'wiki/{search_term}')

def new_page(request):
    print(request.method)
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        # if entry does not already exist
        if util.get_entry(title) != None:
            print('exists already error')
            messages.info(request, f"Entry for '{title}' already exists! If this is for another topic, please change the title.")
            print(messages)
            return render(request, 'encyclopedia/new_page.html', {
                "title": title,
                "content": content
            })
        # if entry exists
        else:
            util.save_entry(title, content)
            return redirect(f'wiki/{title}')
            
    elif request.method == 'GET':
        return render(request, 'encyclopedia/new_page.html')


def edit_page(request):
    # unable to use PUT method in form so created hidden input with value either PUT/POST
    #if method is PUT, send back uneditable title and edited content, save entry
    if request.POST['_method'] == 'PUT':
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return redirect(f'wiki/{title}')
    # if post, send form with textarea with editable content
    elif request.POST['_method'] == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        return render(request, 'encyclopedia/edit.html', {
            'title' : title,
            'content': util.get_entry(title)
        })

def random_page(request):
    entries = util.list_entries()
    randompage = random.choice(entries)
    return redirect(f'wiki/{randompage}')
    
        


