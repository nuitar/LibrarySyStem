# Importing required libraries
from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import Book, IssuedItem, Person, BookManager, BookCategory, Education, Lend,Reserve
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from datetime import date
from django.core.paginator import Paginator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

import json
import os
# ----------------- Library Management System Views -----------------

# Home view


def home(request):
    return render(request, "home.html")


# Login view to login user
def login(request):

    # If request is post then get username and password from request
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Authenticate user
        user = auth.authenticate(username=username, password=password)

        # If user is authenticated then login user
        if user is not None:
            auth.login(request, user)

            # Redirect to home page
            return redirect("/")
        else:

            # If user is not authenticated then show error message
            # and redirect to login page
            messages.info(request, "Invalid Credential")
            return redirect("login")
    else:

        # If request is not post then render login page
        return render(request, "login.html")


# Register view to register user
def register(request):

    # If request is post then get user details from request
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # Check if password and confirm password matches
        if password1 == password2:

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exist")
                return redirect("register")

            # Check if email already exists
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already registered")
                return redirect("register")

            # If username and email does not exists then create user
            else:

                # Create user
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password1,
                )

                # Save user
                user.save()

                # Redirect to login page
                return redirect("login")
        else:

            # If password and confirm password does not matches then show error message
            messages.info(request, "Password not matches")
            return redirect("register")
    else:

        # If request is not post then render register page
        return render(request, "register.html")


# Logout view to logout user
def logout(request):

    # Logout user and redirect to home page
    auth.logout(request)
    return redirect("/")


# Issue view to issue book to user
@login_required(login_url="login")
def issue(request):

    # If request is post then get book id from request
    if request.method == "POST":
        book_id = request.POST["book_id"]
        current_book = Book.objects.get(id=book_id)
        book = Book.objects.filter(id=book_id)
        issue_item = IssuedItem.objects.create(
            user_id=request.user, book_id=current_book
        )
        issue_item.save()
        book.update(quantity=book[0].quantity - 1)

        # Show success message and redirect to issue page
        messages.success(request, "Book issued successfully.")

    # Get all books which are not issued to user
    my_items = IssuedItem.objects.filter(
        user_id=request.user, return_date__isnull=True
    ).values_list("book_id")
    books = Book.objects.exclude(id__in=my_items).filter(quantity__gt=0)

    # Return issue page with books that are not issued to user
    return render(request, "issue_item.html", {"books": books})


# History view to show history of issued books to user
@login_required(login_url="login")
def history(request):

    # Get all issued books to user
    my_items = IssuedItem.objects.filter(
        user_id=request.user).order_by("-issue_date")

    # Paginate data
    paginator = Paginator(my_items, 10)

    # Get page number from request
    page_number = request.GET.get("page")
    show_data_final = paginator.get_page(page_number)

    # Return history page with issued books to user
    return render(request, "history.html", {"books": show_data_final})


# Return view to return book to library
@login_required(login_url="login")
def return_item(request):

    # If request is post then get book id from request
    if request.method == "POST":

        # Get book id from request
        book_id = request.POST["book_id"]

        # Get book object
        current_book = Book.objects.get(id=book_id)

        # Update book quantity
        book = Book.objects.filter(id=book_id)
        book.update(quantity=book[0].quantity + 1)

        # Update return date of book and show success message
        issue_item = IssuedItem.objects.filter(
            user_id=request.user, book_id=current_book, return_date__isnull=True
        )
        issue_item.update(return_date=date.today())
        messages.success(request, "Book returned successfully.")

    # Get all books which are issued to user
    my_items = IssuedItem.objects.filter(
        user_id=request.user, return_date__isnull=True
    ).values_list("book_id")

    # Get all books which are not issued to user
    books = Book.objects.exclude(~Q(id__in=my_items))

    # Return return page with books that are issued to user
    params = {"books": books}
    return render(request, "return_item.html", params)


class BookData:
    def __init__(self) -> None:
        self.json = []

    def appendBook(self, book: Book):
        self.json.append(self.to_json(book))
    
    @staticmethod
    def to_json(book:Book):
        return {"isbn": book.isbn,
                          "name": book.book_name,
                          "date": book.book_add_datetime,
                          "author": book.author,
                          'quantity': book.quantity,
                          'publisher': book.pubulisher,
                          'category': book.book_category.category}

class PersonData:
    def __init__(self) -> None:
        self.json = []

    def appendPerson(self, person: Person):
        self.json.append(self.to_json(person))

    @staticmethod
    def to_json(person:Person):
        return {"name": person.name,
                          "card": person.card,
                          'specialty':person.specialty,
                          'education': person.education.edu}
class LendData:
    def __init__(self) -> None:
        self.json = []

    def appendLend(self, lend: Lend):
        self.json.append(self.to_json(lend))
    
    @staticmethod
    def to_json(lend:Lend):
        return {"person": PersonData.to_json(lend.person),
                          "book": BookData.to_json(lend.book),
                          'lend_date':lend.lend_date}
        
@csrf_exempt
def query_book_all(request):
    books = Book.objects.all()
    bookdata = BookData()
    for book in books:
        if book.book_name == "None":
            continue
        bookdata.appendBook(book)

    # 返回前端json
    return JsonResponse(data=bookdata.json, safe=False,status=200)


@csrf_exempt
def query_book(request):
    try:
        isbn =request.GET['isbn']
        
        # author = post_json['author']
        book = Book.objects.get(isbn=isbn)
    except:
        return JsonResponse(data=[], safe=False)
    # 返回前端json
    return JsonResponse(data=[BookData.to_json(book)], safe=False)

@csrf_exempt
def query_person(request):
    try:
        card = request.GET['card']
        person = Person.objects.get(card=card)
    except:
        return JsonResponse(data=[], safe=False,status=400)
    # 返回前端json
    return JsonResponse(data=[PersonData.to_json(person)], safe=False,status=200)

@csrf_exempt
def query_lend_all(request):
    lends = Lend.objects.all()
    lend_data = LendData()
    for lend in lends:
        lend_data.appendLend(lend)
    # 返回前端json
    return JsonResponse(data=lend_data.json, safe=False,status=200)

@csrf_exempt
def person_query_lend(request):
    try:
        card = request.GET['card']
        person = Person.objects.get(card=card)
        lends = Lend.objects.filter(person=person)
        book_data = BookData()
        for lend in lends:
            book_data.appendBook(lend.book)
    except:
        return JsonResponse(data=[], safe=False,status=400)
    # 返回前端json
    return JsonResponse(data=book_data.json, safe=False,status=200)


@csrf_exempt
def add_person(request):
    try:
        post_json = json.loads(request.body)        
        name = post_json['name']
        card =post_json['card']
        specialty = post_json['specialty']
        education_char = post_json['education'] # 本科 研究生 老师等
        education = Education.objects.get(edu=education_char)
        person = Person(name=name,card=card,specialty=specialty,education=education)
        person.save()
    except:
        return JsonResponse(data=[{'status':False}], safe=False,status=400)
    # 返回前端json
    return JsonResponse(data=[{'status':True}], safe=False,status=200)


@csrf_exempt
def add_book(request: HttpRequest):
    try:
        post_json = json.loads(request.body)
         
        isbn = post_json['isbn']
        name = post_json['book_name']
        author = post_json['author']
        pubulisher = post_json['publisher']
        try:
            quantity = post_json['quantity']
        except:
            quantity = 1
        char_category = post_json['category']
        book_category = BookCategory.objects.get(category=char_category)

        book = Book(isbn=isbn, book_name=name, author=author, quantity=quantity,
                    pubulisher=pubulisher, book_category=book_category)
        book.save()
    except:
        return JsonResponse(data=[], safe=False,status=400)
    # 返回前端json
    return JsonResponse(data=[], safe=False,status=200)


@csrf_exempt
def update_book_isbn(request: HttpRequest):
    try:
        post_json = json.loads(request.body)
         
        isbn = post_json['isbn']
        name = post_json['book_name']
        author = post_json['author']
        pubulisher = post_json['publisher']
        try:
            quantity = post_json['quantity']
        except:
            quantity = 1

        char_category = post_json['category']
        book_category = BookCategory.objects.get(category=char_category)

        book = Book.objects.get(isbn=isbn)
        book.book_name = name
        book.author = author
        book.publisher = pubulisher
        book.quantity = quantity
        book.book_category = book_category
        book.save()
    except:
        return JsonResponse(data=[], safe=False,status=400)
    # 返回前端json
    return JsonResponse(data=[], safe=False,status=200)


@csrf_exempt
def delete_book_isbn(request):
    try:
        post_json = json.loads(request.body)
        isbn = post_json['isbn']
        book = Book.objects.get(isbn=isbn)
        book.delete()
    except:
        return JsonResponse(data=[], safe=False,status=400)
    # 返回前端json
    return JsonResponse(data=[], safe=False,status=200)


@csrf_exempt
def lend_book(request):
    try:
        post_json = json.loads(request.body)
         
        isbn = post_json['isbn']
        card = post_json['card']
        person = Person.objects.get(card=card)
        book = Book.objects.get(isbn=isbn)
        if (Lend.objects.filter(person=person).count() == person.education.max_lend_count
                or book.quantity == 0):
            raise OverflowError
        try:
            reserve = Reserve.objects.get(person=person, book=book)
            reserve.delete()
            lend = Lend(person=person, book=book)
            lend.save()
        except:
            lend = Lend(person=person, book=book)
            lend.save()
            
            book.quantity -= 1
            book.save()

    except:
        return JsonResponse(data=[], safe=False,status=400)

    # 返回前端json
    return JsonResponse(data=[], safe=False,status=200)


@csrf_exempt
def return_book(request):
    try:
        post_json = json.loads(request.body)

        card = post_json['card']
        isbn = post_json['isbn']

        person = Person.objects.get(card=card)
        book = Book.objects.get(isbn=isbn)

        lend = Lend.objects.get(person=person, book=book)
        lend_days = (timezone.now() - lend.lend_date).days - \
            person.education.max_lend_day

        if lend_days > 0:
            fine = book.book_category.per_day_fine*lend_days
            return JsonResponse(data=[{'fine': fine}], safe=False,status=400)
        book.quantity += 1
        book.save()
        lend.delete()
    except:
        return JsonResponse(data=[{'fine': 0}], safe=False,status=400)
    
    # 返回前端json
    return JsonResponse(data=[{'fine': 0}], safe=False,status=200)

@csrf_exempt
def reserve_book(request:HttpRequest):
    try:
        post_json = json.loads(request.body)
         
        isbn = post_json['isbn']
        card = post_json['card']
        person = Person.objects.get(card=card)
        book = Book.objects.get(isbn=isbn)
        if (Lend.objects.filter(person=person).count() == person.education.max_lend_count
                or book.quantity == 0):
            raise OverflowError
        reserve = Reserve(person=person, book=book)
        reserve.save()
        
        book.quantity -= 1
        book.save()

    except:
        return JsonResponse(data=[], safe=False,status=400)

    # 返回前端json
    return JsonResponse(data=[], safe=False,status=200)
        

@csrf_exempt
def img_read(request: HttpRequest, img_name: str):
    try:
        with open(f'system_library/static/system_library/images/{img_name}', 'rb') as f:
            img_data = f.read()
    except:
        return HttpResponse(None, content_type="image/png",status=400)
    return HttpResponse(img_data, content_type="image/png",status=200)


@csrf_exempt
def img_save(request: HttpRequest, img_name: str):
    try:
        print(request.POST['username'])
        img = request.FILES['file']

        with open(f'system_library/static/system_library/images/{img_name}', 'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
    except:
        return JsonResponse([],status=400)
    return JsonResponse([],status=200)
