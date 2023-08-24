from collections import defaultdict
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Egg, Chicken, EggShipment
from .forms import SignUpForm, AddEggForm, AddChickenForm, AddShipmentForm
from django.utils import timezone
from django.db.models import Count
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# get current user's latest month sales
def get_latest_month_sales():
    current_month = EggShipment.objects.filter(date_shipped__month=timezone.now().month)
    current_month_sales = sum(
        [shipment.get_total_sales() for shipment in current_month]
    )
    if current_month_sales == 0:
        return "N/A"
    else:
        return f"RM {round(current_month_sales, 2)}"


# get current user's analytics
def get_user_counts_and_sales(request):
    chicken_count = Chicken.objects.filter(owner=request.user).count()
    egg_count = (
        Egg.objects.filter(owner=request.user)
        .exclude(egg_shipment__isnull=False)
        .count()
    )
    shipment_count = EggShipment.objects.filter(owner=request.user).count()
    sales = get_latest_month_sales()

    count_dict = defaultdict(int)
    count_dict["chicken_count"] = chicken_count
    count_dict["egg_count"] = egg_count
    count_dict["shipment_count"] = shipment_count
    count_dict["sales"] = sales

    return count_dict


# Authentication
class IndexView(View):
    template = "crm/index.html"

    def get(self, request):
        if request.user.is_authenticated:
            count_dict = get_user_counts_and_sales(request)
            context = {"count_dict": count_dict}
            return render(request, self.template, context)
        else:
            return render(request, self.template)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            count_dict = get_user_counts_and_sales(request)
            context = {"count_dict": count_dict}
            messages.success(request, f"Hi {username}! Selamat Datang")
            return render(request, self.template, context)
        else:
            messages.error(request, "Kata Laluan atau/dan Nama Pengguna tidak sah")
            return redirect("crm:index")


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Anda telah berjaya log keluar")
        return redirect("crm:index")


class RegisterView(View):
    template = "crm/register.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template, {"form": form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Pendaftaran berjaya. Sila log masuk")
            return redirect("crm:index")
        else:
            return render(request, self.template, {"form": form})


# Egg


class EggView(LoginRequiredMixin, View):
    template_name = "crm/egg/view.html"

    def get(self, request, pk):
        egg = Egg.objects.filter(owner=pk).first()
        if request.user.id == pk:
            if not egg:
                messages.error(request, "Anda tidak mempunyai rekod telur")
                return render(request, self.template_name)
            egg_list = (
                Egg.objects.filter(
                    owner=request.user, collection_date__lte=timezone.now().date()
                )
                .values("collection_date")
                .annotate(count=Count("id"))
            )
            result = [
                {"collection_date": egg["collection_date"], "count": egg["count"]}
                for egg in egg_list
            ]
            return render(request, self.template_name, {"egg_list": result})
        else:
            messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
            return redirect("crm:egg_view", pk=request.user.id)


class EggDetail(LoginRequiredMixin, View):
    template_name = "crm/egg/detail.html"

    def get(self, request, date):
        egg = get_list_or_404(Egg, collection_date=date, owner=request.user)[0]

        if request.user == egg.owner:
            egg_list = (
                Egg.objects.filter(owner=request.user, collection_date=date)
                .values("size")
                .annotate(count=Count("id"))
            )
            result = [
                {"size": Egg.EGG_SIZE_CHOICES[egg["size"]][1], "count": egg["count"]}
                for egg in egg_list
            ]
            return render(
                request, self.template_name, {"collection_list": result, "date": date}
            )

        messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
        return redirect("crm:egg_detail", pk=request.user.id)


class EggAdd(LoginRequiredMixin, View):
    template_name = "crm/egg/add.html"

    def get(self, request):
        form = AddEggForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AddEggForm(request.POST)
        if form.is_valid():
            collection_date = timezone.now().date()
            owner = request.user
            for size_value, _ in Egg.EGG_SIZE_CHOICES:
                quantity = form.cleaned_data.get(f"quantity{size_value}")
                for _ in range(quantity):
                    Egg.objects.create(
                        owner=owner, collection_date=collection_date, size=size_value
                    )
            messages.success(request, "Rekod berjaya ditambah")
            return redirect("crm:egg_view", pk=request.user.id)

        messages.error(request, "Sila masukkan kuantiti telur sekurang-kurangnya 1")
        return redirect("crm:egg_add")


class EggUpdate(LoginRequiredMixin, View):
    template_name = "crm/egg/update.html"

    def get(self, request, date):
        egg_list = (
            Egg.objects.filter(owner=request.user, collection_date=date)
            .values("size")
            .annotate(count=Count("id"))
        )
        result = [
            {"size": Egg.EGG_SIZE_CHOICES[egg["size"]][1], "count": egg["count"]}
            for egg in egg_list
        ]
        return render(request, self.template_name, {"egg_list": result, "date": date})

    def post(self, request, date):
        form = AddEggForm(request.POST)
        if form.is_valid():
            egg_records = get_list_or_404(Egg, collection_date=date, owner=request.user)
            for egg in egg_records:
                egg.delete()

            for size_value, _ in Egg.EGG_SIZE_CHOICES:
                quantity = form.cleaned_data.get(f"quantity{size_value}")
                for _ in range(quantity):
                    Egg.objects.create(
                        owner=request.user, collection_date=date, size=size_value
                    )

            messages.success(request, "Rekod berjaya dikemaskini")
            return redirect("crm:egg_detail", date)
        egg_list = (
            Egg.objects.filter(owner=request.user, collection_date=date)
            .values("size")
            .annotate(count=Count("id"))
        )
        result = [
            {"size": Egg.EGG_SIZE_CHOICES[egg["size"]][1], "count": egg["count"]}
            for egg in egg_list
        ]
        return render(request, self.template_name, {"egg_list": result, "date": date})


class EggDelete(LoginRequiredMixin, View):
    def post(self, request, date):
        egg_records = get_list_or_404(Egg, collection_date=date, owner=request.user)
        for egg in egg_records:
            egg.delete()
        messages.success(request, "Rekod berjaya dipadam")
        return redirect("crm:egg_view", pk=request.user.id)


# Chicken


class ChickenView(LoginRequiredMixin, View):
    template = "crm/chicken/view.html"

    def get(self, request, pk):
        # Get the chicken records of the user
        chicken_list = Chicken.objects.filter(owner=pk).order_by("-date_added")

        if not chicken_list:
            messages.error(request, "Tiada rekod ayam")
            return render(request, "crm/chicken/view.html")
        # Check if the user is the owner of the record
        if request.user == chicken_list[0].owner:
            return render(
                request, "crm/chicken/view.html", {"chicken_list": chicken_list}
            )

        messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
        return redirect("crm:chicken_view", pk=request.user.id)


class ChickenDetail(LoginRequiredMixin, View):
    template = "crm/chicken/detail.html"

    def get(self, request, pk):
        chicken = get_object_or_404(Chicken, id=pk)
        if not chicken:
            messages.error(request, "Maklumat ayam tidak wujud")
            return redirect("crm:chicken_view", pk=request.user.id)
        # Check if the user is the owner of the record
        if request.user != chicken.owner:
            messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
            return redirect(request, "crm:chicken/view.html", pk=request.user.id)
        return render(request, "crm/chicken/detail.html", {"chicken": chicken})


class ChickenAdd(LoginRequiredMixin, View):
    template = "crm/chicken/add.html"

    def get(self, request):
        today = timezone.now().date()
        form = AddChickenForm()
        return render(request, "crm/chicken/add.html", {"form": form, "today": today})

    def post(self, request):
        today = timezone.now().date()
        form = AddChickenForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            if form.date_added > today:
                messages.error(
                    request, "Tarikh ditambah tidak boleh melebihi tarikh hari ini"
                )
                return redirect("crm:chicken_add")
            form.owner = request.user
            form.save()
            messages.success(request, "Maklumat ayam berjaya ditambah")
            return redirect("crm:chicken_view", pk=request.user.id)


class ChickenUpdate(LoginRequiredMixin, View):
    template = "crm/chicken/update.html"

    def get(self, request, pk):
        current_chicken = get_object_or_404(Chicken, id=pk)
        if not current_chicken:
            messages.error(request, "Maklumat ayam tidak wujud")
            return redirect("crm:chicken_view", pk=request.user.id)
        if request.user != current_chicken.owner:
            messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
            return redirect(request, "crm:chicken/view.html", pk=request.user.id)
        form = AddChickenForm(instance=current_chicken)
        return render(request, "crm/chicken/update.html", {"form": form})

    def post(self, request, pk):
        current_chicken = get_object_or_404(Chicken, id=pk)
        form = AddChickenForm(request.POST, instance=current_chicken)
        if form.is_valid():
            form.save()
            messages.success(request, "Maklumat ayam berjaya dikemaskini")
            return redirect("crm:chicken_detail", pk=current_chicken.id)


class ChickenDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        if request.user != chicken.owner:
            messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
            return redirect(request, "crm:chicken/view.html", pk=request.user.id)

        chicken = get_object_or_404(Chicken, id=pk)
        if not chicken:
            messages.error(request, "Maklumat ayam tidak wujud")
            return redirect("crm:chicken_view", pk=request.user.id)
        chicken.delete()
        messages.success(request, "Maklumat ayam berjaya dipadam")
        return redirect("crm:chicken_view", pk=request.user.id)


# Egg Shipment


class EggShipmentView(LoginRequiredMixin, View):
    template_name = "crm/egg_shipment/view.html"

    def get(self, request, pk):
        # Get the egg shipment record of the user
        shipment_list = EggShipment.objects.filter(owner=pk).order_by("-date_shipped")

        if not shipment_list:
            messages.error(request, "Tiada rekod penghantaran telur")
            return render(request, self.template_name)

        if request.user == shipment_list[0].owner:
            return render(request, self.template_name, {"shipment_list": shipment_list})
        messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
        return redirect("crm:egg_shipment_view", pk=request.user.id)


class EggShipmentDetail(LoginRequiredMixin, View):
    template_name = "crm/egg_shipment/detail.html"

    def get(self, request, pk):
        shipment_detail = get_object_or_404(EggShipment, id=pk)
        if not shipment_detail:
            messages.error(request, "Maklumat penjualan telur tidak wujud")
            return redirect("crm:egg_shipment_view", pk=request.user.id)

        if request.user != shipment_detail.owner:
            messages.error(request, "Anda tidak dibenarkan mengakses halaman ini")
            return redirect("crm:egg_shipment_view", pk=request.user.id)

        return render(request, self.template_name, {"shipment_detail": shipment_detail})


class EggShipmentAdd(LoginRequiredMixin, View):
    template_name = "crm/egg_shipment/add.html"

    def get(self, request):
        form = AddShipmentForm(request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = AddShipmentForm(request.user, request.POST)
        if form.is_valid():
            egg_shipment = form.save(commit=False)
            egg_shipment.owner = request.user
            egg_shipment.save()
            quantity = form.cleaned_data["eggs_quantity"]
            shipment_quantity = quantity * 12
            # Check if the shipment is mixed size
            if form.cleaned_data["is_mixed_size"]:
                # Get egg record which is not in any shipment
                current_egg = (
                    Egg.objects.filter(owner=request.user, egg_shipment__isnull=True)
                    .order_by("size")
                    .order_by("collection_date")
                )
                # Check if all egg records are enough to fulfill the shipment
                if current_egg.count() < shipment_quantity:
                    messages.error(
                        request, "Tiada telur yang mencukupi untuk penghantaran"
                    )
                    egg_shipment.delete()
                    return redirect("crm:egg_shipment_add")
                for egg in current_egg:
                    egg.egg_shipment = egg_shipment
                    egg.save()
                    if (
                        Egg.objects.filter(egg_shipment=egg_shipment).count()
                        == shipment_quantity
                    ):
                        break
            else:
                # Get oldest egg record with the same size
                current_egg = Egg.objects.filter(
                    owner=request.user,
                    egg_shipment__isnull=True,
                    size=form.cleaned_data["size"],
                ).order_by("-collection_date")
                # Check if the egg record is enough to fulfill the shipment
                if current_egg.count() < shipment_quantity:
                    messages.error(
                        request, "Tiada telur yang mencukupi untuk penghantaran"
                    )
                    egg_shipment.delete()
                    return redirect("crm:egg_shipment_add")
                else:
                    for egg in current_egg:
                        egg.egg_shipment = egg_shipment
                        egg.save()
                        if (
                            Egg.objects.filter(egg_shipment=egg_shipment).count()
                            == shipment_quantity
                        ):
                            break

                messages.success(request, "Rekod berjaya ditambah")
                return redirect("crm:egg_shipment_view", pk=request.user.id)
            messages.error(request, "Rekod tidak berjaya ditambah")
            return redirect("crm:egg_shipment_add")
        form = AddShipmentForm(request.user)
        return render(request, self.template_name, {"form": form})


class EggShipmentDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        shipment_record = get_object_or_404(EggShipment, id=pk)
        if not shipment_record:
            messages.error(request, "Rekod tidak wujud")
            return redirect("crm:egg_shipment_view", pk=request.user.id)

        shipment_record.delete()
        messages.success(request, "Rekod berjaya dipadam")
        return redirect("crm:egg_shipment_view", pk=request.user.id)
