from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Category, Product

def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            messages.error(
                request,
                'Invalid username or password.'
            )

    return render(
        request,
        'products/login.html'
    )
@login_required
def logout_view(request):

    logout(request)

    return redirect('login')
@login_required
def dashboard(request):

    total_products = Product.objects.count()

    active_products = Product.objects.filter(
        status='active'
    ).count()

    inactive_products = Product.objects.filter(
        status='inactive'
    ).count()

    low_stock_products = Product.objects.filter(
        stock__lte=5
    ).count()

    context = {
        'total_products': total_products,
        'active_products': active_products,
        'inactive_products': inactive_products,
        'low_stock_products': low_stock_products,
    }

    return render(
        request,
        'products/dashboard.html',
        context
    )
@login_required
def product_list(request):

    products = Product.objects.select_related(
        'category'
    ).all()

    search = request.GET.get(
        'search',
        ''
    ).strip()

    category_id = request.GET.get(
        'category',
        ''
    )

    status = request.GET.get(
        'status',
        ''
    )

    if search:

        products = products.filter(
            name__icontains=search
        )

    if category_id:

        products = products.filter(
            category_id=category_id
        )

    if status:

        products = products.filter(
            status=status
        )

 
    products = products.order_by(
        '-created_at'
    )

    paginator = Paginator(
        products,
        5
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    categories = Category.objects.all().order_by(
        'name'
    )

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
        'selected_status': status,
    }

    return render(
        request,
        'products/productList.html',
        context
    )

@login_required
def product_add(request):

    if request.method == 'POST':

        form = ProductForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Product added successfully.'
            )

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm()

    context = {
        'form': form,
        'page_title': 'Add Product',
        'button_text': 'Save Product',
    }

    return render(
        request,
        'products/productForm.html',
        context
    )
@login_required
def product_edit(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Product updated successfully.'
            )

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm(
            instance=product
        )

    context = {
        'form': form,
        'page_title': 'Edit Product',
        'button_text': 'Update Product',
        'product': product,
    }

    return render(
        request,
        'products/productForm.html',
        context
    )
@login_required
def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    context = {
        'product': product,
    }

    return render(
        request,
        'products/productDetails.html',
        context
    )
@login_required
def product_delete(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.method == 'POST':

        product.delete()

        messages.success(
            request,
            'Product deleted successfully.'
        )

        return redirect(
            'product_list'
        )

    return render(
        request,
        'products/productDetails.html',
        {
            'product': product,
            'delete_confirmation': True,
        }
    )