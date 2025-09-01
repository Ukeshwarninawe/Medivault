import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Vault, MedicalRecord
from .forms import MedicalRecordForm
from django.urls import reverse
@login_required
def create_vault(request):
    # Check if vault exists to prevent duplicate vaults
    if Vault.objects.filter(owner=request.user.profile).exists():
        messages.info(request, "Vault already exists, please authenticate.")
        return redirect('authenticate_vault')

    if request.method == "POST":
        name = request.POST.get("vault_name")
        pw = request.POST.get("vault_password")
        vault = Vault(name=name, owner=request.user.profile)
        vault.set_password(pw)
        vault.save()
        messages.success(request, "Vault created successfully! Please authenticate to continue.")
        return redirect('authenticate_vault')

    return render(request, 'core/create_vault.html')


@login_required
def authenticate_vault(request):
    vault = get_object_or_404(Vault, owner=request.user.profile)

    if request.method == "POST":
        pw = request.POST.get("password")
        if vault.check_password(pw):
            request.session[f'vault_auth_{vault.id}'] = True
            messages.success(request, "Vault authenticated successfully!")
            return redirect('view_vault')
        messages.error(request, "Incorrect password")

    return render(request, 'core/authenticate_vault.html', {'vault': vault})

def view_vault(request):
    vault = get_object_or_404(Vault, owner=request.user.profile)

    if not request.session.get(f'vault_auth_{vault.id}', False):
        return redirect('authenticate_vault')

    records = vault.medical_records.order_by('-uploaded_at')
    return render(request, 'core/my_vault.html', {'vault': vault, 'records': records})


@login_required
def access_vault_by_qr(request, qr_secret):
    vault = get_object_or_404(Vault, qr_secret=qr_secret, owner=request.user.profile)
    request.session[f'vault_auth_{vault.id}'] = True
    return redirect('view_vault')
@login_required
def upload_record(request):
    profile = request.user.profile

    # Try to get user's vault, redirect to create vault if not found
    try:
        vault = Vault.objects.get(owner=profile)
    except Vault.DoesNotExist:
        messages.info(request, "You need to create a vault first.")
        return redirect('create_vault')

    # Check if vault is authenticated in this session
    if not request.session.get(f'vault_auth_{vault.id}', False):
        messages.info(request, "Please authenticate your vault before uploading records.")
        return redirect('authenticate_vault', vault_id=vault.id)

    if request.method == "POST":
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.vault = vault
            record.save()
            messages.success(request, "Record uploaded successfully!")
            return redirect('view_vault')
    else:
        form = MedicalRecordForm()

    return render(request, 'core/record_upload.html', {'form': form, 'vault': vault})
@login_required
def delete_record(request, record_id):
    vault=get_object_or_404(Vault,owner=request.user.profile)
    rec = get_object_or_404(MedicalRecord, id=record_id,vault=vault)
    if rec.file and os.path.isfile(rec.file.path):
        rec.file.delete()
    rec.delete()
    messages.success(request, "Record deleted successfully.")
    return redirect('my_vault')

@login_required
def view_record(request, record_id):
    vault=get_object_or_404(Vault,owner=request.user.profile)
    rec = get_object_or_404(MedicalRecord, id=record_id,vault=vault)
    if rec.vault.owner != request.user.profile:
        messages.error(request, "Not authorized")
        return redirect('my_vault')
    return render(request, 'core/view_record.html', {'record': rec})

@login_required
def my_vault(request):
    profile = request.user.profile
    try:
        vault = Vault.objects.get(owner=profile)
    except Vault.DoesNotExist:
        vault = None
    records = vault.medical_records.order_by('-uploaded_at') if vault else []
    return render(request, 'core/my_vault.html', {'vault': vault, 'records': records})


@login_required
def show_qr(request):
    profile = request.user.profile
    vault = get_object_or_404(Vault, owner=profile)

    # Generate internal access URL (e.g., /vault/qr/<uuid>/)
    qr_path = reverse('access_vault_by_qr', args=[str(vault.qr_secret)])

    # Full URL (if you want it to work from mobile scanner too)
    full_qr_url = request.build_absolute_uri(qr_path)

    return render(request, 'core/show_qr.html', {
        'vault': vault,
        'qr_url': full_qr_url
    })