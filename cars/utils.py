from .models import * 
from django.db.models import Count
from django.core.cache import cache


menu = [{'title': 'About website', 'url_name': 'about'},
        {'title': 'Add a post', 'url_name': 'add_post'},
        {'title': 'Contact us', 'url_name': 'contact'},
        ]


class DataMixin:
    paginate_by = 20
    
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Categories.objects.annotate(Count('get_posts'))
 
            
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        
        context['menu'] = user_menu
        
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context