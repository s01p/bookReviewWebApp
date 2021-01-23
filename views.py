from django.shortcuts import render,redirect, get_object_or_404
from .models import Book,Comment,Record
# Create your views here.
from tablib import Dataset
from django.contrib.auth.decorators import login_required
from .resourse import BookResource
from django.http import HttpResponse
from django.db.models import Q
from django.http import Http404
import requests
import json
from .forms import CommentForm,SignUpForm
from django.contrib.auth import login, authenticate,logout
from .forms import SignUpForm
from django.core.exceptions import PermissionDenied



def export(request):
    book_resource = BookResource()
    dataset = book_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="book.csv"'
    return render(request,'book/temp.html',{'response' : response})

def simple_upload(request):
    if request.method == 'POST':
        person_resource = BookResource()
        dataset = Dataset()
        new_persons = request.FILES['myfile']

        imported_data = dataset.load(new_persons.read().decode('utf-8'),format='csv')
        result = person_resource.import_data(imported_data, dry_run=True)  # Test the data import
                                                     
        if not result.has_errors():
            person_resource.import_data(imported_data, dry_run=False)  # Actually import now

        return render(request, 'book/index.html')
    else:
        return render(request,'book/import.html')
def remove_900(request):
    obj = Book.objects.all()
    obj.delete()

    return render(request,'book/index.html')   


def search(request):
    if request.method == "POST":
        data = request.POST["searchdata"]
        search_result = list(Book.objects.filter(Q(isbn__startswith=data)|Q(title__startswith=data)| Q(author__startswith=data)))

        if not search_result:
            raise Http404("search not found")                                      
          
        return render(request,'book/display.html',{'search_result' : search_result})

    else:
        return render(request,'book/search_form.html',)


def Book_detail(request,pk):
    book = get_object_or_404(Book, pk=pk) 
    print(book.isbn)
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": " hBgLy1KiSdCC4E47fsUw", "isbns": "9781632168146"})
    
    
    data = res.json()    
    print(res.json())
    return render(request,'book/book_detail.html',{'book':book,'data1':data['books'][0]["average_rating"],'data2':data['books'][0]['work_reviews_count']})
@login_required
def add_comment_to_post(request, pk):
    book = get_object_or_404(Book, pk=pk)
    print(request.user)
    
    #data = request.user
     #Record.objects.filter(book_key = book).
    record = Record.objects.filter(author = request.user).filter(book_key = book) 
    print(record)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
           if not record:
                 comment = form.save(commit=False)
                 comment.book = book
                 comment.save()
                 t = Record()
                 t.commented = True
                 t.book_key = book
                 t.author = request.user
                 t.save()
                 return redirect('Book_detail', pk=book.pk)
           else:
                return HttpResponse("Can not comment more than once!")
            
    else:
        form = CommentForm()
    return render(request, 'book/add_comment_to_post.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('search')
    else:
        form = SignUpForm()
    return render(request, 'book/signup.html', {'form': form})   