from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, CategoryItem,CategoryItemForm
from django.shortcuts import get_object_or_404

# Create your views here.
@login_required(login_url="signin")
def edit_item(request, item_id):
    item = get_object_or_404(CategoryItem, id=item_id)
    if request.method == 'POST':
        # Update item data
        item.title = request.POST.get('title')
        item.save()
        return redirect("detail", slug=item.category.slug)
    context = {"item": item}
    return render(request, "edit_item.html", context)

@login_required(login_url="signin")
def delete_item(request, item_id):
    item = get_object_or_404(CategoryItem, id=item_id)
    if request.method == 'POST':
        # Delete item
        category_slug = item.category.slug
        item.delete()
        return redirect("detail", slug=category_slug)
    context = {"item": item}
    return render(request, "delete_item.html", context)

@login_required(login_url="signin")
def update_item(request, item_id):
    item = get_object_or_404(CategoryItem, id=item_id)
    if request.method == 'POST':
        form = CategoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("detail", slug=item.category.slug)
    else:
        form = CategoryItemForm(instance=item)
    context = {"form": form, "item": item}
    return render(request, "edit_item.html", context)

def index(request):
    categories = Category.objects.all()
    context = {"categories":categories}
    return render(request, "index.html", context)

@login_required(login_url="signin")
def detail(request, slug):
    category = Category.objects.get(slug=slug)
    categories = CategoryItem.objects.filter(category=category)
    
    msg = None
    
    if request.user.is_authenticated:
        if category.voters.filter(id=request.user.id).exists():
            msg = "voted"
            
    
    if request.method == 'POST':
        selected_id = request.POST.get("category_item")
        print(selected_id)
        item = CategoryItem.objects.get(id=selected_id)
        item.total_vote += 1
        
        item_category = item.category 
        item_category.total_vote += 1
        
        item.voters.add(request.user)
        item_category.voters.add(request.user)
        
        item.save()
        item_category.save()
        
        return redirect("result", slug=category.slug)
        
    
    context = {"category": category, "categories": categories, "msg": msg}
    return render(request, "detail.html", context)

def result(request, slug):
    category = Category.objects.get(slug=slug)
    items = CategoryItem.objects.filter(category=category)
    context = {"category": category, "items": items}
    return render(request, "result.html", context)

def signin(request):
    msg = ""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            
            else:
            
                return redirect("index")
        else:
            msg = "Invalid Credentials"
            
    context = {"msg":msg}
    return render(request, "signin.html", context)

def signup(request):

    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            # login starts here
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            
            
    context = {"form":form}
    return render(request, "signup.html", context)



def signout(request):
    logout(request)
    return redirect("index")

@login_required(login_url="signin")
def update_item(request, item_id):
    item = CategoryItem.objects.get(pk=item_id)
    if request.method == 'POST':
        form = CategoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('result', slug=item.category.slug)
    else:
        form = CategoryItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})


