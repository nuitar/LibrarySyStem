from django.contrib import admin
from .models import Person,Book,BookManager,BookCategory,Education,Lend,Reserve

# Register your models here.



# class PersonInline(admin.StackedInline):
#     model = Person
#     extra = 3


class LendAdmin(admin.ModelAdmin):  
    fieldsets = [
        ("Person information", {"fields": ["person"]}),
        ("Book information", {"fields": ["book"]}),
    ]
    readonly_fields = ("person_name","get_person_card")
    
    list_display = ('get_person_name', 'book_title', 'lend_date')
    def person_name(self, obj):
        return obj.person.name
    person_name.short_description = 'Person Name'  # 设置列的标题

    def book_title(self, obj):
        return obj.book.book_name
    book_title.short_description = 'Book Name'  # 设置列的标题
    
class EducationAdmin(admin.ModelAdmin):      
    list_display = ('edu', 'obj_max_lend_count', 'obj_max_lend_day')
    def obj_max_lend_count(self, obj):
        return obj.max_lend_count
    obj_max_lend_count.short_description = '最大借书数量'  # 设置列的标题

    def obj_max_lend_day(self, obj):
        return obj.max_lend_day
    obj_max_lend_day.short_description = '最大借书天数'  # 设置列的标题
    

class BookAdmin(admin.ModelAdmin):      
    list_display = ('book_name', 'isbn', 'publisher',"quantity")


class BookCategoryAdmin(admin.ModelAdmin):      
    list_display = ('category', 'per_day_fine')

class PersonAdmin(admin.ModelAdmin):      
    list_display = ('name', 'card','specialty','education')

class ReserveAdmin(admin.ModelAdmin):      
    list_display = ('person', 'book','reserve_date')

class BookManagerAdmin(admin.ModelAdmin):      
    list_display = ('account', 'name','manage_card')


admin.site.register(Person,PersonAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(BookManager,BookManagerAdmin)
admin.site.register(BookCategory,BookCategoryAdmin)
admin.site.register(Education,EducationAdmin)
admin.site.register(Lend,LendAdmin)
admin.site.register(Reserve,ReserveAdmin)    
