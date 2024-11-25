# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .models import UserRecord
# import qrcode
# from io import BytesIO
# from django.core.files import File
# import random
# import string

# def generate_unique_code():
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Generates an 8-character random code
# def generate_qr(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         sex = request.POST.get('sex')

#         # Store user details in session
#         request.session['name'] = name
#         request.session['sex'] = sex

#         # Initialize user_record and unique_code
#         user_record = None
#         unique_code = None

#         try:
#             # Try to get the existing user record from the database
#             user_record = UserRecord.objects.get(name=name, sex=sex)
#             unique_code = user_record.unique_code  # Get the user's unique code

#             # Store the unique code in the session
#             request.session['unique_code'] = unique_code

#         except UserRecord.DoesNotExist:
#             # If user does not exist, create a new unique code
#             unique_code = generate_unique_code()
#             request.session['unique_code'] = unique_code  # Store new unique code in session

#         # Generate the QR code containing the unique code
#         qr = qrcode.QRCode(version=1, box_size=10, border=5)
#         qr.add_data(unique_code)  # Use the unique code
#         qr.make(fit=True)

#         # Create the image
#         img = qr.make_image(fill='black', back_color='white')

#         # Save the image to a BytesIO buffer
#         buffer = BytesIO()
#         img.save(buffer, format="PNG")

#         # If the user exists, save the QR code image to the user's record
#         if user_record:
#             file_name = f'{name}_qr.png'
#             buffer.seek(0)  # Move the buffer pointer to the beginning
#             user_record.qr_code.save(file_name, File(buffer), save=False)
#             user_record.save()

#         # Return the QR code and user_record to the template
#         return render(request, 'generate_qr.html', {'user_record': user_record, 'unique_code': unique_code})

#     return render(request, 'generate_qr.html')

   
# def verify_code(request):
#     if request.method == 'POST':
#         entered_code = request.POST.get('code')

#         # Retrieve the unique code from the session
#         session_unique_code = request.session.get('unique_code')

#         if session_unique_code and session_unique_code == entered_code:
#             # Fetch the user record based on the unique code
#             try:
#                 user_record = UserRecord.objects.get(unique_code=session_unique_code)
#                 return render(request, 'user_details.html', {'user_record': user_record})
#             except UserRecord.DoesNotExist:
#                 return HttpResponse('User record not found.')
#         else:
#             return HttpResponse('Invalid code. Please try again.')

#     return redirect('generate_qr')

# def error_page(request):
#     return render(request, 'error_page.html', {'message': 'User not found or invalid code.'})


from django.shortcuts import render, redirect
from django.http import HttpResponse

from barcode.forms import NewsletterSubscriptionForm
from .models import *
import qrcode
from io import BytesIO
import base64
import random
import string
from django.core.files import File


# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Certificate
import time
from django.views.decorators.csrf import csrf_protect

# @csrf_protect
# def certificate_check(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         certificate_number = request.POST.get('certificate number')
#         # Check if the certificate exists
#         time.sleep(2)
#         try:
#             certificate = Certificate.objects.get(name=name, certificate_number=certificate_number)
#             return JsonResponse({'found': True, 'message': 'Certificate found', 'certificate_url': f'/certificate/{certificate.id}'})
#         except Certificate.DoesNotExist:
#             return JsonResponse({'found': False, 'message': 'Certificate not found'})

#     return render(request, 'certificate_check.html')

# def view_certificate(request, certificate_id):
#     certificate = Certificate.objects.get(id=certificate_id)
#     return render(request, 'user_details.html', {'certificate': certificate})

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from .models import Certificate
import time, uuid
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache

@csrf_protect
def certificate_check(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip().title()
        certificate_number = request.POST.get('certificate_number')
        # Check if the certificate exists
        time.sleep(2)
        try:
            certificate = Certificate.objects.get(name=name, certificate_number=certificate_number)
            
            # Generate a unique token
            token = str(uuid.uuid4())
            
            # Store token in cache with certificate id for a limited time (e.g., 10 minutes)
            cache.set(token, certificate.id, timeout=30)  # 600 seconds = 10 minutes
            
            certificate_image_url = certificate.image.url if certificate.image else None
            
            return JsonResponse({
                'found': True, 
                'message': 'Certificate found', 
                'title': certificate.title,
                'certificate_url': f'/certificate/{certificate.id}?token={token}',
                'name': certificate.name,
                'certificate_number': certificate_number,
                'start_date': certificate.start_date,  # Adjust according to your model field
                'end_date': certificate.end_date,  # Adjust according to your model field
                'issue_date': certificate.issue_date,  # Adjust according to your model field
                'certificate_image': certificate_image_url  # URL of the image
            })
        except Certificate.DoesNotExist:
            return JsonResponse({'found': False, 'message': 'Certificate not found'})

    return render(request, 'certificate_check.html')

# def view_certificate(request, certificate_id):
    token = request.GET.get('token')
    
    # Check if the token exists in the cache and matches the certificate_id
    if token and cache.get(token) == int(certificate_id):
        # Token is valid, so fetch and display the certificate
        certificate = get_object_or_404(Certificate, id=certificate_id)
        return render(request, 'user_details.html', {'certificate': certificate})
    else:
        # Invalid token or token expired
        return HttpResponseForbidden('Invalid or expired link.')

def view_certificate(request, certificate_id):
    token = request.GET.get('token')
    
    # Check if the token exists in the cache and matches the certificate_id
    if token and cache.get(token) == int(certificate_id):
        # Token is valid, so fetch and display the certificate
        certificate = get_object_or_404(Certificate, id=certificate_id)
        return render(request, 'user_details.html', {'certificate': certificate})
    else:
        # Invalid token or token expired, redirect to home with a message
        return redirect('home')

def download_certificate(request, certificate_id):
    certificate = get_object_or_404(Certificate, id=certificate_id)
    image_path = certificate.image.path  # Adjust based on your model

    # Open the file and return it as a response
    with open(image_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='image/jpeg')  # Change content_type if needed
        response['Content-Disposition'] = f'attachment; filename="{certificate.name}.jpg"'  # Use appropriate file extension
        return response

from django.conf import settings
import os

# def download_certificate(request, certificate_id):
#     certificate = get_object_or_404(Certificate, id=certificate_id)
    
#     # Assuming the certificate image is stored in the media directory
#     image_path = os.path.join(settings.MEDIA_ROOT, 'certificates', f'{certificate_id}.png')
    
#     # If the image exists, serve it as a file response
#     if os.path.exists(image_path):
#         with open(image_path, 'rb') as img_file:
#             response = HttpResponse(img_file.read(), content_type="image/png")
#             response['Content-Disposition'] = f'attachment; filename="certificate_{certificate_id}.png"'
#             return response
#     else:
#         return HttpResponse("Certificate image not found.", status=404)

# def download_certificate(request, certificate_id):
#     certificate = get_object_or_404(Certificate, id=certificate_id)
    
#     # Assuming the certificate image is stored in the media directory
#     image_path = os.path.join(settings.MEDIA_ROOT, 'certificates', f'{certificate.certificate_number}.png')
    
#     # If the image exists, serve it as a file response
#     if os.path.exists(image_path):
#         with open(image_path, 'rb') as img_file:
#             response = HttpResponse(img_file.read(), content_type="image/png")
#             response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.certificate_number}.png"'
#             return response
#     else:
#         return HttpResponse("Certificate image not found.", status=404)

# def download_certificate(request, certificate_id):
#     certificate = get_object_or_404(Certificate, id=certificate_id)
    
#     # Assuming the certificate image is stored in the media directory
#     image_path = os.path.join(settings.MEDIA_ROOT, 'certificates', f'{certificate.certificate_number}.png')
    
#     # Debugging statement to check the path
#     print(f"Image path for download: {image_path}")  # Debugging statement
    
#     # If the image exists, serve it as a file response
#     if os.path.exists(image_path):
#         with open(image_path, 'rb') as img_file:
#             response = HttpResponse(img_file.read(), content_type="image/png")
#             response['Content-Disposition'] = f'attachment; filename="certificate_{certificate.certificate_number}.png"'
#             return response
#     else:
#         return HttpResponse("Certificate image not found.", status=404)

def home(request):
    return render(request, 'index.html')

def about(request):
    myabout = True
    return render(request, 'about.html', {'myabout': myabout})

def contact(request):
    mycontact = True
    return render(request, 'contact.html', {'mycontact': mycontact})

from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

@csrf_exempt  # Optional: remove this if you send the CSRF token correctly
def contact_process(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Basic validation
        if not all([name, email, phone, message]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

        # Validate email
        try:
            validate_email(email)
            ContactMessage.objects.create(full_name=name, email=email, message=message, phone=phone)
            return JsonResponse({'status': 'success', 'message': 'Your message has been sent successfully!'})
        except ValidationError:
            return JsonResponse({'status': 'error', 'message': 'Invalid email address.'}, status=400)

    # If request method is not POST
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


@csrf_protect
def subscribe(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        email = request.POST.get('email')
        
        # Check if the email already exists
        if NewsletterSubscriber.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'You have already subscribed to the newsletter.'})

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'You have successfully subscribed to the newsletter!'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid email address.'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def generate_qr(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        sex = request.POST.get('sex')

        # Store user details in session
        request.session['name'] = name
        request.session['sex'] = sex

        # Initialize unique_code
        unique_code = None

        try:
            # Try to get the existing user record from the database
            user_record = UserRecord.objects.get(name=name, sex=sex)
            unique_code = user_record.unique_code  # Get the user's unique code
        except UserRecord.DoesNotExist:
            # If user does not exist, create a new unique code
            unique_code = generate_unique_code()

        # Store the unique code in the session
        request.session['unique_code'] = unique_code

        # Generate the QR code containing the unique code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(unique_code)
        qr.make(fit=True)

        # Create the image
        img = qr.make_image(fill='black', back_color='white')

        # Convert the image to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # If the user exists, save the QR code image to the user's record
        if 'user_record' in locals():
            file_name = f'{name}_qr.png'
            buffer.seek(0)
            user_record.qr_code.save(file_name, File(buffer), save=False)
            user_record.save()

        # Return the QR code and unique code to the template
        return render(request, 'generate_qr.html', {'unique_code': unique_code, 'qr_image_base64': img_str})

    return render(request, 'generate_qr.html')


def verify_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('code')

        # Retrieve the unique code from the session
        session_unique_code = request.session.get('unique_code')

        if session_unique_code and session_unique_code == entered_code:
            try:
                # Fetch the user record based on the unique code
                user_record = UserRecord.objects.get(unique_code=session_unique_code)
                return render(request, 'user_details.html', {'user_record': user_record})
            except UserRecord.DoesNotExist:
                # Render an error modal if the user does not exist
                return render(request, 'generate_qr.html', {'error': 'User not found.'})
        else:
            # Render an error modal for an invalid code
            return render(request, 'generate_qr.html', {'error': 'Invalid code. Please try again.'})
    return redirect('generate_qr')


from django.http import HttpResponse
import csv

def download_user_details(request, user_id):
    user_record = UserRecord.objects.get(id=user_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{user_record.name}_details.csv"'

    writer = csv.writer(response)
    writer.writerow(['Detail', 'Value'])
    writer.writerow(['Name', user_record.name])
    writer.writerow(['Sex', user_record.sex])
    writer.writerow(['Age', user_record.age])
    # Add more rows if needed

    return response

