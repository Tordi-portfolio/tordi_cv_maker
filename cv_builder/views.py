# cv_builder/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CVForm
from .models import CV

@login_required
def create_cv(request):
    # Safety check: ensure we only query if the user is actually authenticated
    cv = None
    if request.user.is_authenticated:
        try:
            cv = CV.objects.get(user=request.user)
        except CV.DoesNotExist:
            cv = None

    if request.method == 'POST':
        form = CVForm(request.POST, instance=cv)
        if form.is_valid():
            new_cv = form.save(commit=False)
            new_cv.user = request.user
            new_cv.save()
            return redirect('create_cv')
    else:
        form = CVForm(instance=cv)
        
    return render(request, 'cv_form.html', {'form': form, 'cv': cv})

# cv_builder/views.py
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CVForm, CustomUserCreationForm

# Make sure to import your new form
from .forms import CVForm, CustomUserCreationForm 

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Optional: auto-login after registration
            return redirect('create_cv')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')



from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.http import HttpResponse

@login_required
def generate_pdf(request):
    cv = CV.objects.get(user=request.user)
    html_string = render_to_string('cv_pdf.html', {'cv': cv})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="CV_{cv.full_name}.pdf"'

    # Create PDF
    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Errors occurred', status=500)
    return response


# cv_builder/views.py
from django.shortcuts import render
from .models import CV

@login_required
def all_cvs_view(request):
    # This now allows anyone to view the list of CVs
    cvs = CV.objects.all()
    return render(request, 'all_cvs.html', {'cvs': cvs})


from django.shortcuts import get_object_or_404

@login_required
def cv_detail_view(request, pk):
    cv = get_object_or_404(CV, pk=pk)
    return render(request, 'cv_detail.html', {'cv': cv})\
    

# cv_builder/views.py
def home_view(request):
    return render(request, 'home.html')


# cv_builder/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def delete_cv_view(request, pk):
    cv = get_object_or_404(CV, pk=pk)
    
    # Check if the user is the owner or staff
    if request.user == cv.user or request.user.is_staff:
        cv.delete()
        messages.success(request, "CV deleted successfully.")
    else:
        messages.error(request, "You don't have permission to delete this.")
        
    return redirect('all_cvs')