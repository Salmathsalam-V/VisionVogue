from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from Category. models import Category
from Store . models import Product, Variation
from carts.models import Coupon
from . models import SalesReport
from . forms import CategoryForm, CouponForm, ImageGalleryFormSet, ProductForm, VariationForm
from Accounts . models import Account
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
import re
from Orders . models import Order, OrderProduct, Payment, Return
from .forms import OrderStatusForm
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
import io
import csv
import xlwt
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import datetime
from django.views.generic import ListView, UpdateView, DeleteView


def admin_dashboard(request):
    category_count = Category.objects.count()
    product_count = Product.objects.count()
    recent_products = Product.objects.order_by('-id')[:5]

    context = {
        'category_count': category_count,
        'product_count': product_count,
        'recent_products': recent_products,
    }
    return render(request, 'admin/dashboard.html', context)

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            brand_name = form.cleaned_data.get('brand_name') 
            if not re.match("^[A-Za-z0-9 ]*$", brand_name):
                form.add_error('brand_name', 'Brand name cannot contain special symbols.')
            else:
                if Category.objects.filter(Q(brand_name__iexact=brand_name)).exists():
                    form.add_error('brand_name', 'Brand name already exists.')
                else:
                    form.save()
                    return redirect('myadmin:category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES,instance=category)
        if form.is_valid():
            brand_name = form.cleaned_data.get('brand_name') 
            if not re.match("^[A-Za-z0-9 ]*$", brand_name):
                form.add_error('brand_name', 'Brand name cannot contain special symbols.')
            else:
                if Category.objects.filter(Q(brand_name__iexact=brand_name)).exclude(id=category.id).exists():
                    form.add_error('brand_name', 'Brand name already exists.')
                else:
                    form.save()
                    return redirect('myadmin:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.is_delete=True
        category.save()
        return redirect('myadmin:category_list')
    return render(request, 'admin/category_confirm_delete.html', {'category': category})

# Product Views

def product_list(request):
    products=Product.objects.all()
    return render(request, 'admin/product_list.html',{'products':products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_name = form.cleaned_data.get('product_name') 
            if not re.match("^[A-Za-z0-9 ]*$", product_name):
                form.add_error('product_name', 'Brand name cannot contain special symbols.')
            else:
                if Product.objects.filter(Q(product_name__iexact=product_name)).exists():
                    form.add_error('product_name', 'product name already exists.')
                else:
                    form.save()
                    return redirect('myadmin:product_list')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_name = form.cleaned_data.get('product_name') 
            if not re.match("^[A-Za-z0-9 ]*$", product_name):
                form.add_error('product_name', 'Brand name cannot contain special symbols.')
            else:
                if Product.objects.filter(Q(product_name__iexact=product_name)).exclude(id=product.id).exists():
                    form.add_error('product_name', 'product name already exists.')
                else:
                    form.save()
                    return redirect('myadmin:product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form})


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_delete=True
        product.save()
        return redirect('myadmin:product_list')
    return render(request, 'admin/product_confirm_delete.html', {'product': product})


def user_list(request):
    users = Account.objects.filter(is_superadmin=False)
    return render(request, 'admin/user_list.html', {'users': users})


def user_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myadmin:user_list')
    else:
        form = UserCreationForm()
    return render(request, 'admin/user_form.html', {'form': form})


def user_update(request, pk):
    user = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if 'block' in request.POST:
                user.is_block = True
                user.save()
            elif 'unblock' in request.POST:
                user.is_block = False
                user.save()
        return redirect('myadmin:user_list')
    else:
        form = UserChangeForm(instance=user)
    return render(request, 'admin/user_form.html', {'form': form})


def user_delete(request, pk):
    user = get_object_or_404(Account, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('myadmin:user_list')
    return render(request, 'admin/user_confirm_delete.html', {'user': user})

def variation_list(request):
    variations = Variation.objects.all()
    context = {
        'variations': variations,
    }
    return render(request, 'admin/variation_list.html', context)

def add_variation(request):
    if request.method == 'POST':
        variation_form = VariationForm(request.POST)
        formset = ImageGalleryFormSet(request.POST, request.FILES)
        
        if variation_form.is_valid() and formset.is_valid():
            variation = variation_form.save()
            # Save images from formset
            for form in formset:
                image = form.save(commit=False)
                image.variation = variation
                image.save()
            return redirect('myadmin:variation_list')  # Redirect to a success page or variation list

    else:
        variation_form = VariationForm()
        formset = ImageGalleryFormSet()

    return render(request, 'admin/add_variation.html', {
        'variation_form': variation_form,
        'formset': formset,
    })
# List View
def variation_list(request):
    variations = Variation.objects.all()
    context = {
        'variations': variations,
    }
    return render(request, 'admin/variation_list.html', context)

# Update Variation
def update_variation(request, pk):
    variation = get_object_or_404(Variation, pk=pk)
    if request.method == 'POST':
        form = VariationForm(request.POST, request.FILES, instance=variation)
        formset = ImageGalleryFormSet(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            for form in formset:
                image = form.save(commit=False)
                image.variation = variation
                image.save()
            messages.success(request, 'Variation updated successfully.')
            return redirect('myadmin:variation_list')
    else:
        form = VariationForm(instance=variation)
        formset = ImageGalleryFormSet()

    context = {
        'form': form,
        'formset': formset,
        'variation': variation,
    }
    return render(request, 'admin/variation_form.html', context)

# Delete Variation
def delete_variation(request, pk):
    variation = get_object_or_404(Variation, pk=pk)
    if request.method == 'POST':
        variation.delete()
        messages.success(request, 'Variation deleted successfully.')
        return redirect('myadmin:variation_list')
    context = {
        'variation': variation,
    }
    return render(request, 'admin/variation_confirm_delete.html', context)

  # order 
def view_orders(request):
    if request.user in Account.objects.filter(is_admin=True):
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')  # Redirect to a suitable page

    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'admin/view_orders.html', {'orders': orders})

def update_order_status(request, order_id):
    if request.user in Account.objects.filter(is_admin=True):
        messages.error(request, "You do not have permission to update this order.")
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            previous_status = order.status
            updated_order = form.save(commit=False)

            # Check if the status is being updated to 'Accepted'
            if updated_order.status == 'Accepted' and previous_status != 'Accepted':
                updated_order.delivery_date = timezone.now() + timedelta(days=10)
            
            updated_order.save()
            messages.success(request, 'Order status updated successfully!')
            return redirect('myadmin:view_orders')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'admin/update_order_status.html', {'form': form, 'order': order})

def order_product_details(request, order_id):
    if request.user in Account.objects.filter(is_admin=True):
        payment = Payment.objects.filter(payment_id = order_id.order_number)
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home', payment)

    order = get_object_or_404(Order, id=order_id)
    order_products = OrderProduct.objects.filter(order=order)

    return render(request, 'admin/order_product_details.html', {'order': order, 'order_products': order_products})


def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'admin/coupon_list.html', {'coupons': coupons})

def coupon_create(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('myadmin:coupon_list')
    else:
        form = CouponForm()
    return render(request, 'admin/coupon_form.html', {'form': form})

def coupon_update(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('myadmin:coupon_list')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'admin/coupon_form.html', {'form': form})

def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        return redirect('myadmin:coupon_list')
    return render(request, 'admin/coupon_confirm_delete.html', {'coupon': coupon})


def sales_report(request):
    # Filter parameters
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    period = request.GET.get('period')
    orders = Order.objects.all()
    
    # Custom date filtering
    if period == '' and start_date and end_date:
        try:
            # Parse the start and end dates to ensure they are in the correct format
            start_date = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
            end_date = timezone.make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
            orders = orders.filter(created_at__range=[start_date, end_date])
        except ValueError:
            raise ValidationError("Invalid date format. Dates must be in YYYY-MM-DD format.")
    
    # Aggregation based on period
    if period == 'daily':
        orders = orders.filter(created_at__date=timezone.now().date())
    elif period == 'weekly':
        orders = orders.filter(created_at__gte=timezone.now() - timedelta(days=7))
    elif period == 'monthly':
        orders = orders.filter(created_at__month=timezone.now().month)
    else:
        # Custom date range already handled above
        pass

    # Aggregate the data based on filtered orders
    data = orders.values('orderproduct__product__product_name').annotate(
        total_quantity=Sum('orderproduct__quantity'),
        total_sales=Sum(F('orderproduct__quantity') * F('orderproduct__product_price')),
        total_discount=Sum('discount_amount'),
        sub_total=Sum('sub_total')
    ).order_by('orderproduct__product__product_name')
  
    total_sales = data.aggregate(Sum('total_sales'))['total_sales__sum'] or 0
    total_orders = orders.count()
    total_discount = orders.aggregate(Sum('discount_amount'))['discount_amount__sum'] or 0
    sub_total = orders.aggregate(Sum('sub_total'))['sub_total__sum'] or 0

    context = {
        'data': data,
        'orders': orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_discount': total_discount,
        'sub_total': sub_total,
        'period': period,
        'start_date': start_date if start_date else None,
        'end_date': end_date if end_date else None,
    }
    
    if 'export_pdf' in request.GET:
        return generate_pdf('admin/sales_report_pdf.html', context)
    elif 'export_excel' in request.GET:
        return generate_excel(data)
    
    return render(request, 'admin/sales_report.html', context)

def generate_pdf(template_src, context):
    print(context)
    template = get_template(template_src)
    html = template.render(context)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_excel(data):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="sales_report.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales Report')

    # Sheet header
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    # Define the columns for the Excel sheet
    columns = ['Item Name', 'Quantity Sold', 'Total Discount', 'Total Sales', 'Sub Total']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body
    font_style = xlwt.XFStyle()

    # Writing data from the sales report
    for item in data:
        row_num += 1
        ws.write(row_num, 0, item['orderproduct__product__product_name'], font_style)
        ws.write(row_num, 1, item['total_quantity'], font_style)
        ws.write(row_num, 2, item['total_discount'], font_style)
        ws.write(row_num, 3, item['total_sales'], font_style)
        ws.write(row_num, 4, item['sub_total'], font_style)

    wb.save(response)
    return response

def view_saved_reports(request):
    reports = SalesReport.objects.all()
    return render(request, 'admin/saved_reports.html', {'reports': reports})

def return_list(request):
    returns = Return.objects.all()  # Fetch all Return objects
    return render(request, 'admin/return_list.html', {'returns': returns})