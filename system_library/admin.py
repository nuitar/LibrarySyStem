from django.contrib import admin
from .models import Student,Book

# Register your models here.



# class StudentInline(admin.StackedInline):
#     model = Student
#     # extra = 3


# class BookAdmin(admin.ModelAdmin):
#     # fieldsets = [
#     #     (None, {"fields": ["question_text"]}),
#     #     ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
#     # ]
#     inlines = [StudentInline]
    
    
admin.site.register(Student)
admin.site.register(Book)