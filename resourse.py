from import_export import resources
from .models import Book

class BookResource(resources.ModelResource):
    #delete = fields.Field(widget=widgets.BooleanWidget())
    
   # def for_delete(self, row, instance):
        #return self.fields['delete'].clean(row)
    
    class Meta:
        model = Book