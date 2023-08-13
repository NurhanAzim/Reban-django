from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Egg, Chicken
from .forms import SignUpForm, AddEggForm, UpdateEggForm, AddChickenForm
from django.utils import timezone
from django.shortcuts import get_object_or_404, get_list_or_404

# Authentication
def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Hi {username}! Selamat Datang')
            return redirect("crm:index")
        else:
            messages.error(request, "Kata Laluan atau/dan Nama Pengguna tidak sah")
            return redirect("crm:index")
    return render(request, "crm/index.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Log Keluar berjaya")
    return redirect("crm:index")

def register_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pendaftaran berjaya. Sila log masuk")
            return redirect("crm:index")
    else:
        form = SignUpForm()
        return render(request, "crm/register.html", {'form': form})
    
# Egg
def egg_view(request, pk):

    # Get the first egg records of the user
    egg = get_list_or_404(Egg, owner=pk)[0]
    if not egg:
        messages.error(request, "Anda tidak mempunyai rekod telur")
        return redirect("crm:index")
    # Check if the user is the owner of the record
    if request.user == egg.owner:
        # Get daily collection list today and before
        egg_list = Egg.objects.filter(owner=request.user, collection_date__lte=timezone.now().date()).order_by('-collection_date')

        # Combine the daily collection list into a dictionary
        existing_record = defaultdict(int)
        for egg in egg_list:
            existing_record[egg.collection_date] += egg.quantity

        result = [{'id': id, 'collection_date': date, 'quantity': quantity} for id, (date, quantity) in enumerate(existing_record.items())]

        return render(request, 'crm/egg_view.html', {'egg_list': result})
    messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
    return redirect("crm:egg_view", pk=request.user.id)

def egg_detail(request, date):
    egg = get_list_or_404(Egg, collection_date=date, owner=request.user)[0]

    # Check if the user is the owner of the record
    if request.user == egg.owner:
        collection_list = Egg.objects.filter(owner=request.user, collection_date=date)
        return render(request, 'crm/egg_detail.html', {'collection_list': collection_list, 'date': date})
    messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
    return redirect("crm:egg_detail", pk=request.user.id)

def egg_add(request):
    if request.method == "POST":
        form = AddEggForm(request.POST)
        if form.is_valid():
            # add information for owner and collection_date column
            new_egg = form.save(commit=False)
            new_egg.owner = request.user
            new_egg.collection_date = timezone.now().date()

            # check if the user has already added eggs today with the same size
            # if yes, update the quantity and id to the existing record
            if Egg.objects.filter(owner=request.user, collection_date=new_egg.collection_date, size=new_egg.size).exists():
                new_egg.quantity += Egg.objects.get(owner=request.user, collection_date=new_egg.collection_date, size=new_egg.size).quantity
                new_egg.id = Egg.objects.get(owner=request.user, collection_date=new_egg.collection_date, size=new_egg.size).id
            new_egg.save()
            messages.success(request, "Rekod berjaya ditambah")
            return redirect("crm:egg_view", pk=request.user.id)
    form = AddEggForm()
    return render(request, 'crm/egg_add.html', {'form': form})

def egg_update(request, pk):
    # Get the eggs collected on date
    current_egg = get_object_or_404(Egg, id=pk)
    if request.method == "POST":
        form = UpdateEggForm(request.POST, instance=current_egg)
        if form.is_valid():
            form.save()
            messages.success(request, "Rekod berjaya dikemaskini")
            return redirect("crm:egg_detail", date=current_egg.collection_date)
    form = UpdateEggForm(instance=current_egg)
    return render(request, 'crm/egg_update.html', {'form': form, 'size': current_egg.get_size_display,})

def egg_delete(request, date):
    egg_records = get_list_or_404(Egg, collection_date=date, owner=request.user)
    for egg in egg_records:
        egg.delete()
    messages.success(request, "Rekod berjaya dipadam")
    return redirect("crm:egg_view", pk=request.user.id)
    
# Chicken

def chicken_view(request, pk):
    # Get the chicken records of the user
    chicken_list = get_list_or_404(Chicken, owner=pk)

    if not chicken_list:
        messages.error(request, "Maklumat ayam tidak wujud")
        return redirect("crm:index")
    # Check if the user is the owner of the record
    if request.user == chicken_list[0].owner:
        return render(request, 'crm/chicken_view.html', {'chicken_list': chicken_list})
    messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
    return redirect("crm:chicken_view", pk=request.user.id)

def chicken_detail(request, pk):
    chicken = get_object_or_404(Chicken, id=pk)
    if not chicken:
        messages.error(request, "Maklumat ayam tidak wujud")
        return redirect("crm:chicken_view", pk=request.user.id)
    # Check if the user is the owner of the record
    if request.user == chicken.owner:
        return render(request, 'crm/chicken_detail.html', {'chicken': chicken})
    else:
        messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
        return redirect(request, 'crm:chicken_view.html', pk=request.user.id)

def chicken_add(request):
    today = timezone.now().date()
    if request.method == "POST":
        form = AddChickenForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if form.date_added > today:
                messages.error(request, "Tarikh ditambah tidak boleh melebihi tarikh hari ini")
                return redirect('crm:chicken_add')
            form.owner = request.user
            form.save()
            messages.success(request, "Maklumat ayam berjaya ditambah")
            return redirect('crm:chicken_view', pk=request.user.id)
    form = AddChickenForm()
    return render(request, 'crm/chicken_add.html', {'form': form, 'today': today})

def chicken_update(request, pk):
    current_chicken = get_object_or_404(Chicken, id=pk)
    if not current_chicken:
        messages.error(request, "Maklumat ayam tidak wujud")
        return redirect("crm:chicken_view", pk=request.user.id)
    if request.method == "POST":
        form = AddChickenForm(request.POST, instance=current_chicken)
        if form.is_valid():
            form.save()
            messages.success(request, "Maklumat ayam berjaya dikemaskini")
            return redirect('crm:chicken_detail', pk=current_chicken.id)
    
    form = AddChickenForm(instance=current_chicken)
    return render(request, 'crm/chicken_update.html', {'form': form})

def chicken_delete(request, pk):
    chicken = get_object_or_404(Chicken, id=pk)
    if not chicken:
        messages.error(request, "Maklumat ayam tidak wujud")
        return redirect("crm:chicken_view", pk=request.user.id)
    chicken.delete()
    messages.success(request, "Maklumat ayam berjaya dipadam")
    return redirect("crm:chicken_view", pk=request.user.id)

