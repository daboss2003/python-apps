import random
from django.http import HttpResponse
from django.shortcuts import redirect, render
from difflib import SequenceMatcher
from django.core.files.storage import default_storage
import os
from . import util
import markdown2



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    }) 
    
    
def entry_name(request,name):
    data = util.get_entry(name)
    if data != None:
        html = markdown2.markdown(data)
        return render(request,"encyclopedia/entry.html",{
            "title": name,
            "entries": html
            
        } )
        
    return render(request, "encyclopedia/error.html",{
            "name":name
        })
    
def search(request):
    if request.method == 'POST':
        query = request.POST.get('q')
        if query =="":
            return HttpResponse("search Empty")
        data = util.get_entry(query)
        if data :
            html = markdown2.markdown(data)
            return render(request,"encyclopedia/entry.html",{
                "entries":html,
                "title":query
            })
        else:
            filenames = "entries"
            match = []
            for files in os.listdir(filenames):
                file_title = os.path.splitext(files)[0]
                similar_result = SequenceMatcher(None,query.lower(),file_title.lower()).ratio()
                if similar_result > 0.1:
                    match.append(files)
            return render(request,"encyclopedia/search.html",{
                "entries":match,
                "title":query
            })
                    
def create_new(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title == "":
            return HttpResponse("error, can't process an empty form")
        filenames = "entries"
        for files in os.listdir(filenames):
            file_title = os.path.splitext(files)[0]
            if file_title.lower() == title.lower():
                return HttpResponse("error, entry already exist")
        content = request.POST.get('content')
        if content == "":
            return HttpResponse("error, can't process an empty form")
        util.save_entry(title, content)
        data = util.get_entry(title)
        html = markdown2.markdown(data)
        return render(request,"encyclopedia/entry.html",{
            "entries":html,
            "title":title
            
        } )
    return render(request,"encyclopedia/creat.html")
        
        
      
def edit_page(request,name):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title == "":
            return HttpResponse("error, can't process an empty form")
        content = request.POST.get('content')
        if content == "":
            return HttpResponse("error, can't process an empty form")
        util.save_entry(title, content)
        data = util.get_entry(title)
        html = markdown2.markdown(data)
        return render(request,"encyclopedia/entry.html",{
            "entries":html,
            "title":title
        } )
    else:
        data = util.get_entry(name)
        return render(request,"encyclopedia/edit.html",{
        "title":name,
        "entries":data
    })
        


def random_page(request):
    random_en = []
    filenames = "entries"
    for files in os.listdir(filenames):
        file_title = os.path.splitext(files)[0]
        random_en.append(file_title)
    random_entry = random.choice(random_en)
    data = util.get_entry(random_entry)
    html = markdown2.markdown(data)
    return render(request,"encyclopedia/entry.html",{
            "title": random_entry,
            "entries": html
            
        } )
    
