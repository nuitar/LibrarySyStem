# importing required modules
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

# ----------- Library Management System Models ------------


class BookManager(models.Model):
    account = models.CharField(max_length=20)
    password = models.CharField(max_length=15)

    name = models.CharField(max_length=20)
    manage_card = models.CharField(max_length=13, unique=True)


class BookCategory(models.Model):
    category = models.CharField(max_length=10, unique=True)
    per_day_fine = models.IntegerField(default=10)

    def __str__(self):
        return self.category


class Book(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    book_name = models.CharField(max_length=150)
    author = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    book_add_datetime = models.DateTimeField(default=timezone.now())

    pubulisher = models.CharField(max_length=200, default='')
    # 中外文图书，中外文杂志，论文
    # CHINESE,ENGLISH,EN_MAGZINE,CN_MAGZINE,THESIS = 0,1,2,3,4
    book_category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.book_name


# IssuedItem model to store issued book details
class IssuedItem(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField(default=date.today(), blank=False)
    return_date = models.DateField(blank=True, null=True)

    # property to get book name
    @property
    def book_name(self):
        return self.book_id.book_name

    # property to get author name
    @property
    def username(self):
        return self.user_id.username

    def __str__(self):
        return (
            self.book_id.book_name
            + " issued by "
            + self.user_id.first_name
            + " on "
            + str(self.issue_date)
        )


class Education(models.Model):
    # junior,undergraduate,postgraduate,doctor = 0,1,2,3
    edu = models.CharField(max_length=10, unique=True)
    max_lend_count = models.IntegerField(default=0)
    max_lend_day = models.IntegerField(default=0)

    def __str__(self):
        return self.edu


class Person(models.Model):
    # junior,undergraduate,postgraduate,doctor = 0,1,2,3
    name = models.CharField(max_length=50)
    card = models.CharField(max_length=50, default=None, unique=True)
    specialty = models.CharField(max_length=50)
    education = models.ForeignKey(Education, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lend(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    lend_date = models.DateTimeField(default=timezone.now())

    class Meta:
        unique_together = ('person', 'book')

    def __str__(self):
        return ('[' + self.person.name +']' + ' 借 ' +'《' + self.book.book_name) + '》'
