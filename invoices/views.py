# from django.shortcuts import render, redirect
# from .forms import InvoiceForm
# from django.core.mail import EmailMessage
# from django.template.loader import render_to_string
# from xhtml2pdf import pisa
# from io import BytesIO
# from .models import Invoice

# def create_invoice(request):
#     if request.method == 'POST':
#         form = InvoiceForm(request.POST)
#         if form.is_valid():
#             invoice = form.save()
#             # Generate PDF
#             template_path = 'invoices/pdf_template.html'
#             context = {'invoice': invoice}
#             html = render_to_string(template_path, context)
#             result = BytesIO()
#             pisa_status = pisa.CreatePDF(html, dest=result)

#             if not pisa_status.err:
#                 # Email PDF
#                 email = EmailMessage(
#                     subject="Your Invoice",
#                     body="Please find your invoice attached.",
#                     from_email="your_email@gmail.com",
#                     to=[invoice.client_email],
#                 )
#                 email.attach('invoice.pdf', result.getvalue(), 'application/pdf')
#                 email.send()
#                 return redirect('success')
#     else:
#         form = InvoiceForm()
#     return render(request, 'invoices/create_invoice.html', {'form': form})

# def success(request):
#     return render(request, 'invoices/success.html')

from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render
from xhtml2pdf import pisa
from .models import Invoice
from .forms import InvoiceForm  # ✅ Don't forget this!

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
            response['Content-Disposition'] = 'inline; filename="invoice.pdf"'  # Or 'attachment' for download
            template = get_template(template_path)
            html = template.render(context)

            pisa_status = pisa.CreatePDF(html, dest=response)
            if pisa_status.err:
                return HttpResponse('Error generating PDF', status=500)

            return response  # ✅ Open PDF in browser

    else:
        form = InvoiceForm()

    # ❌ Was missing: render needs to be imported and called properly
    return render(request, 'invoices/create_invoice.html', {'form': form})
