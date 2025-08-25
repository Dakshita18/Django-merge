from django import forms 
from .models import *
from .forms import *
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required




def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    print(posts)
    for tag in posts:
        print(tag)

    context = {'posts':posts}
    return render(request, 'blog/post_list.html',context)

def category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    print(category,"cccccccccccccccccc")
    posts = Post.objects.all(category=category)
    print(posts,"pppppppppppppppppppp")

    context = {'posts':posts}


    return render(request, 'blog/post_list.html',context)

def TAG(request, pk):
    TAG = get_object_or_404(Tag, pk=pk)
    print(category,"cccccccccccccccccc")
    posts = Post.objects.filter(tag =TAG )
    print(posts,"EEEEEEEEEEEEEE")

    context = {'posts':posts}

    return render(request, 'blog/post_list.html',context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    comments = Comment.objects.filter(post=post, parent=None).order_by('-id')  # only top-level comments

    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        text = request.POST.get('comment')
        reply_text = request.POST.get('reply')
        parent_id = request.POST.get('parent_id')

        parent_comment = Comment.objects.filter(id=parent_id).first() if parent_id else None

        if reply_text and parent_comment:
            Comment.objects.create(name=name, email=email, text=reply_text, post=post, parent=parent_comment)
        elif text:
            Comment.objects.create(name=name, email=email, text=text, post=post)

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'categories': categories,
        'tags': tags,
        'comments': comments,
    })
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        print(form,"fffffffffffffffffffffffffffffffffffffff")
        if form.is_valid():
            post = form.save(commit=False)
            print(post,"))))))))))))))))))))))))))))))))))))")
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})



def signup(request):
    print('inside signup')
    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        password = request.POST.get('password')
        print(password)
        phonenumber =request.POST.get('phonenumber')
        print(phonenumber)
        email = request.POST.get('email')
        print(email)
        city = request.POST.get('city')
        print(city)
        state =request.POST.get('state')
        print(state)
        country =request.POST.get('country')
        print(country)
        Address =request.POST.get('Address')
        print(Address)
        profileimagerrrrrrr =request.FILES.get('profileimageeeeeeeeee')
        print(profileimagerrrrrrr,"????????????????????????????????????????????????????????????????????????????????????")


        user = User.objects.create_user(username=username, password=password,phone_number=phonenumber,email=email,city=city,state=state,country=country,address=Address,profile_picture=profileimagerrrrrrr)
        print(user,'uuuuuuuuuuuuuuuuuuuu')
        messages.success(request, "Account created successfully! You can now log in.")
        print('account created succesfully')
        return redirect('post_list') 
       

    return render(request, 'blog/signup.html')
            


def login_view(request):
    print('inside login')
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
    
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect("post_list")
        else:
            return HttpResponse("fail")

    return render(request=request, template_name="blog/login.html")

def logout_view(request):
        logout(request)
       
        return redirect('post_list')   

@login_required
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'blog/profile.html', context)

def EditProfile(request):
    user = request.user
    context = {'user': user}
    if request.method == 'POST':

        username = request.POST.get('user_name')
        print(username)
        password = request.POST.get('password')
        print(password)
        phonenumber =request.POST.get('phonenumber')
        print(phonenumber)
        email = request.POST.get('email')
        print(email)
        city = request.POST.get('city')
        print(city)
        state =request.POST.get('state')
        print(state)
        country =request.POST.get('country')
        print(country)
        Address =request.POST.get('Address')
        print(Address)
        profileimage =request.POST.get('profileimages')
        print(profileimage)

        user.username =username
        user.email =email
        user.city =city
        user.state =state
        user.country =country
        user.address =Address
        user.phone_number=phonenumber
        
        user.save()
        
    return render(request, 'blog/edit profile.html', context)

    