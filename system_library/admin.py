from django.contrib import admin
from .models import Person,Book,BookManager,BookCategory,Education,Lend

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
    
    
admin.site.register(Person)
admin.site.register(Book)
admin.site.register(BookManager)
admin.site.register(BookCategory)
admin.site.register(Education)
admin.site.register(Lend)