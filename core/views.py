from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import Bookform,UserForm
from .models import Book

# Create your views here.
def home(request):
    return render(request, 'home.html')
 

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username,password= password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm(request, data=request.POST)

    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,'Your account has been created successfully')
            return redirect("login")

        else:
            print(form.errors)

    else:
        form = UserForm()

    return render(request, "register.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "You have logout successfully")
    return redirect("home")

@login_required
def list_books(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "list_books.html", context)


@login_required
def add_book(request):
    if request.method == 'POST':
        form = Bookform(request.POST)
        if form.is_valid():
            book = form.save(commit=False) # create a book but dont save it
            book.user = request.user
            book.save()
            messages.success(request, "Book Added Successfully")
            return redirect("my_profile")
    else:
        form = Bookform()

    return render(request, 'add_mod_book.html', {
        "form": form,
        "title": "Add Book"
    })

@login_required
def edit_book(request, pk):
    book = Book.objects.get(pk=pk)
    if request.method == 'POST':
        form = Bookform(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book modified successfully")
            return redirect("list_books")
    else:
        form = Bookform(instance=book)

    return render(request, "add_mod_book.html", {
        "form": form,
        "title": "Edit Book"
    })

@login_required
def delete_book(request,pk):
    books = Book.objects.get(pk=pk)
    if request.method == 'POST':
        books.delete()
        messages.success(request,'Book deleted successfully')
        return redirect('list_book')

    return render(request,'delete_book.html',{'books': books})

@login_required
def my_profile(request):
    books=request.user.book_set.all()
    print(books)
    return render(request, "my_profile.html",{'books': books})

@login_required
def user_profile(request ):
    return render(request, "user_profile.html")
