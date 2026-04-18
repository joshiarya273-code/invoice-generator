from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Invoice, Customer, Product
from .forms import InvoiceForm, InvoiceItemFormSet, CustomerForm


def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        formset = InvoiceItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            invoice = form.save()
            formset.instance = invoice
            formset.save()
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
        formset = InvoiceItemFormSet()

    return render(request, 'invoice_app/create_invoice.html', {
        'form': form,
        'formset': formset,
    })


def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    items = invoice.items.select_related('product').all()
    return render(request, 'invoice_app/invoice_detail.html', {
        'invoice': invoice,
        'items': items,
    })


def invoice_list(request):
    invoices = Invoice.objects.select_related('customer').all().order_by('-date')
    return render(request, 'invoice_app/invoice_list.html', {'invoices': invoices})


def get_product_price(request, product_id):
    """AJAX endpoint — returns price of a product as JSON."""
    product = get_object_or_404(Product, pk=product_id)
    return JsonResponse({'price': product.price})
