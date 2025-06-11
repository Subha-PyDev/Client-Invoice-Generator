from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from xhtml2pdf import pisa
from .models import Invoice
from .forms import InvoiceForm  

def success(request):
    return render(request, 'invoices/success.html')

def create_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()

            # Render PDF from template
            template_path = 'invoices/pdf_template.html'
            context = {'invoice': invoice}
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="invoice.pdf"'  
            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('Error generating PDF', status=500)

            return response 

    else:
        form = InvoiceForm()

    return render(request, 'invoices/create_invoice.html', {'form': form})
