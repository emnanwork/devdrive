from django.shortcuts import render, redirect
#
from .models import Blog, Category, Comment
from django.contrib.auth.decorators import login_required
from .forms import CreateBlogForm, CommentForm
from django.utils.text import slugify
from django.contrib import messages
from django.db.models import Q # use Q to filter
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def index(request):
    keyword = request.GET.get("search")
    msg=None
    paginator = None
    featured_blog = Blog.objects.get(featured=True)
    if keyword:
        blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(body__icontains=keyword) | 
                                    Q(category__title__icontains=keyword))
        
        if blogs.exists():
            # pass
            paginator = Paginator(blogs, 4)
            blogs = paginator.page(1)
        
        else:
            msg = "There is no article with the keyword"
            featured_blog = None
            
    else:
        blogs = Blog.objects.filter(featured=False)
        paginator = Paginator(blogs, 4)
        # blogs = paginator.page(1)
        page = request.GET.get("page")

        # blogs = paginator.page(page)
        
        try:
            blogs = paginator.page(page)
            
        except PageNotAnInteger:
            blogs = paginator.page(1)
        
        except EmptyPage:
            blogs = paginator.page(paginator.num_pages)
    
    # blogs = Blog.objects.all()
    # blogs = Blog.objects.filter(featured=False)
    # context = {
    #     "blog": blogs,
    #     "f_blog": featured_blog
    # }
    # return render(request, "blogapp/index.html", context)
    categories = Category.objects.all()
    # context = {"blogs":blogs, "cats": categories,"f_blog": featured_blog,"msg": msg}
    context = {"blogs":blogs, "msg":msg, "paginator": paginator, "cats": categories}
    return render(request, "blogapp/index.html", context)


def detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    # related_blogs = Blog.objects.filter(category__id=blog.category.id).exclude(id=blog.id)[:4]
    comments = Comment.objects.filter(blog=blog)
    # get comment form
    form = CommentForm()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user 
                comment.save()
                return redirect("detail", slug=blog.slug)
    # context = {
    #     'blog': blog
    # }
    context = {'blog': blog, "form": form, "comments": comments}
    # context = {'blog': blog, "form": form, "comments": comments, "r_blogs": related_blogs}
    
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
    


@login_required(login_url="signin")
def update_article(request, slug):
    update = True #allow us to change titles
    blog = Blog.objects.get(slug=slug)
    form=CreateBlogForm(instance=blog)
    if request.method == 'POST':
        form = CreateBlogForm(request.POST, request.FILES, instance=blog)
        blog = form.save(commit=False)
        blog.slug=slugify(request.POST["title"])
        blog.save()
        messages.success(request, "Article updated successfully")
        return redirect("profile")
    context={"update":update, "form":form}
    return render(request, "blogapp/create.html", context)




@login_required(login_url="signin")
def delete_article(request, slug):
    blog  = Blog.objects.get(slug=slug)
    blogs = Blog.objects.filter(user=request.user)
    delete_article = True
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Article deleted successfully")
        return redirect("profile")
    context = {"blog": blog, "del":delete_article, "blogs": blogs}
    return render(request, "core/profile.html", context)







