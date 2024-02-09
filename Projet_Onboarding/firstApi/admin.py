from django.contrib import admin
from .models import ProjectVersion, Event 
from django.contrib.auth.models import User

admin.site.register(ProjectVersion)

class FeaturesAdmin(admin.ModelAdmin):
    # Cette ligne détermine quels champs sont affichés dans la vue liste
    list_display = ('name',) # Assurez-vous que ces champs existent dans votre modèle

class CategoryAdmin(admin.ModelAdmin):
    # Idem pour Category
    list_display = ('name',) # Assurez-vous que ces champs existent dans votre modèle



   
class EventAdmin(admin.ModelAdmin):
        
        actions = ['delete_selected']

        list_display = ('user', 'user_group', 'event', 'created', 'feature', 'action_type')
        list_filter = ('user', 'user_group', 'event', 'feature', 'action_type')
        search_fields = ('user__username', 'user_group', 'event', 'feature', 'action_type')
        date_hierarchy = 'created'
    
        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == 'user':
                kwargs['empty_label'] = '(None)'
                kwargs['queryset'] = User.objects.all()
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Event, EventAdmin)
