
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import *
from .forms import *
from .utils import *

menu = [{'title': 'About website', 'url_name': 'about'},
        {'title': 'Add a post', 'url_name': 'add_post'},
        {'title': 'Contact us', 'url_name': 'contacts'},
        {'title': 'Sign in', 'url_name': 'login'},
        ]


class CarsHome(DataMixin, ListView):
    model = Cars
    template_name = 'cars/index.html'
    context_object_name = 'posts'
    
    
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_queryset(self): #return only published posts
        return Cars.objects.filter(is_published=True).select_related('cat')
    
    
def about(request):
    return render(request, 'cars/about.html', {'menu': menu, 'title': 'About website'})


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'cars/add_post.html'
    success_url = reverse_lazy('home') # return to home page after successuflly adding a post
    login_url = reverse_lazy('home')
    raise_exception = True
    
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Adding a post')
        return dict(list(context.items()) + list(c_def.items()))
    
#def add_post(request):
    #if request.method == 'POST':
        #form = AddPostForm(request.POST, request.FILES)
        #if form.is_valid():
            #print(form.cleaned_data)
            #form.save() # save data from connecting to database form
            #return redirect('home') 

    #else:
        #form = AddPostForm()
        
    #return render(request, 'cars/add_post.html', {'form': form, 'menu': menu, 'title':'Adding a post'})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'cars/contact.html'
    success_url = reverse_lazy('home')
    
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Contact us')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')
    

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found!</h1>')


class ShowPost(DataMixin, DetailView):
    model = Cars
    template_name = 'cars/post.html'
    slug_url_kwarg = 'post_slug' # for slug 
    #pk_url_kwarg = 'post_pk' # for id 
    context_object_name = 'post'
    
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))
    
    
#def show_post(request, post_slug):
    #post = get_object_or_404(Cars, slug=post_slug)
    
    #context = {
        #'post': post,
        #'menu': menu,
        #'title': post.title,
        #'cat_selected': post.cat_id,
    #}
    #return render(request, 'cars/post.html', context=context)


class CarsCategories(DataMixin, ListView):
    model = Cars
    template_name = 'cars/index.html'
    context_object_name = 'posts'
    allow_empty = False

    
    def get_queryset(self):
        return Cars.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Categories.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

#def show_category(request, cat_slug):
    #category = get_object_or_404(Categories, slug=cat_slug)
    #posts = Cars.objects.filter(cat=category)
    
    #if len(posts) == 0:
        #raise Http404()
    
    #context = {
        #'posts': posts,
        #'menu': menu,
        #'title': 'Categories views',
        #'cat_selected': cat_slug,
        
    #}
    
    #return render(request, 'cars/index.html', context=context)
    
    
class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'cars/register.html'
    success_url = reverse_lazy('login')
    
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')         
    
        
class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'cars/login.html'
    
    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Authentication')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
    
    