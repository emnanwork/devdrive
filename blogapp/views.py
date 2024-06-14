from django.shortcuts import render, redirect
#
from .models import Blog, Category
from django.contrib.auth.decorators import login_required
from .forms import CreateBlogForm
from django.utils.text import slugify
from django.contrib import messages

# Create your views here.
def index(request):
    featured_blog = Blog.objects.get(featured=True)
    blogs = Blog.objects.all()
    # blogs = Blog.objects.filter(featured=False)
    context = {
        "blog": blogs,
        "f_blog": featured_blog
    }
    # return render(request, "blogapp/index.html", context)
    categories = Category.objects.all()
    context = {"blogs":blogs, "cats": categories}
    # context = {"blogs":blogs, "msg":msg, "paginator": paginator, "cats": categories}
    return render(request, "blogapp/index.html", context)


def detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    context = {
        'blog': blog
    }
    return render(request, "blogapp/detail.html", context)


@login_required(login_url="signin")
def create_article(request):
    form=CreateBlogForm()
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.slug = slugify(request.POST["title"])
            blog.user=request.user
            blog.save()
            messages.success(request, "Article created successfully!")
            return redirect("profile")
    context = {"form": form}
    # context = {}
    return render(request, "blogapp/create.html", context)
    






