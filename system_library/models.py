# importing required modules
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

# ----------- Library Management System Models ------------


class BookManager(models.Model):
    book_manager_name = models.CharField(max_length=50)

    
# Book model to store book details
class Book(models.Model):
    isbn = models.CharField(max_length=13,unique=True)
    book_name = models.CharField(max_length=150)
    author= models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    subject = models.CharField(max_length=2000)
    book_add_time = models.TimeField(default=timezone.now())
    book_add_date = models.DateField(default=date.today())
    pubulisher = models.CharField(max_length=200,default='')
    # 中外文图书，中外文杂志，论文
    # CHINESE,ENGLISH,EN_MAGZINE,CN_MAGZINE,THESIS = 0,1,2,3,4
    book_category = models.IntegerField(default=-1)
    # class Meta:
    #     unique_together = ("book_name", "author")

    def __str__(self):
        return self.book_name


# IssuedItem model to store issued book details
class IssuedItem(models.Model):
    book_id = models.ForeignKey(Book,on_delete=models.CASCADE)
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
        
class Student(models.Model):
    # junior,undergraduate,postgraduate,doctor = 0,1,2,3
    student_name = models.CharField(max_length=50)
    student_card = models.CharField(max_length=50,default=None)
    student_edu = models.IntegerField(default=0)
    lend_count = models.IntegerField(default=0)
    isbn = models.ForeignKey(Book, on_delete=models.CASCADE,default=None)
    
    def __str__(self):
        return (
            self.student_name
           
        )