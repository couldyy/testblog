from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.http import HttpResponse
from django.db.models import F
from django.core.mail import send_mail
from .forms import *

# Create your views here.

class HomePage(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

class GetCategory(ListView):
    # extra_context = {'categories': Category.objects.all()}
    model = Post
    template_name = 'blog/category.html'
    context_object_name = 'post'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

class ShowSingleNews(DetailView):
    model = Post
    template_name = 'blog/single_news.html'
    context_object_name = 'post'

    form = CommentForm

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            form.instance.user_created_comment = request.user
            form.instance.post_of_comment = post
            commrepl = request.POST.get("commentID")
            form.instance.comm_to_repl_id = commrepl
            form.save()
        else:
            print("some error with form happened")
            print(form.errors.as_data())

        return redirect(reverse("single_news", kwargs={
            "slug": self.get_object().slug,
        }))


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Post.objects.get(slug=self.kwargs['slug'])
        context['form'] = self.form
        context['comments'] = Comment.objects.filter(post_of_comment=self.get_object(), comm_to_repl=None)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()

        return context



class GetNewsByTag(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости по тегу: ' + str(Tags.objects.get(slug=self.kwargs['slug']))
        return context

    def get_queryset(self):
        return Post.objects.filter(tag__slug=self.kwargs['slug'])


class Search(ListView):
    template_name = 'blog/search_posts.html'
    context_object_name = 'post'
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

def registration(request):
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CreateUser()
    return render(request, 'blog/registration.html', {"form": form, "title": 'Регистрация'})


def loginn(request):
    if request.method == 'POST':
        form = LoginUser(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginUser()
    return render(request, 'blog/login.html', {"form": form, "title": 'Авторизация'})

def logoutt(request):
    logout(request)
    return redirect('home')



def like(request, slug, comment_id):
    result = ''
    post = Post.objects.get(slug=slug)
    comment = Comment.objects.get(id=comment_id)
    user = request.user
    print(comment)
    if user in comment.likes.all():
        comment.likes.remove(user)
        comment.like_count -= 1
        result = Comment.like_count
        comment.save()
    else:
        comment.likes.add(user)
        comment.like_count += 1
        comment.save()
    return redirect(reverse("single_news", kwargs={
        "slug": post.slug,
    }))