from django.shortcuts import render,redirect
from .forms import MedicalRecordForm
from.models import MedicalRecord
from django.shortcuts import get_object_or_404
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def upload_record(request):
    profile=get_object_or_404(Profile,user=request.user)
    if request.method=="POST":
        form=MedicalRecordForm(request.POST,request.FILES)
        if form.is_valid():
            record=form.save(commit=False)
            record.profile=profile
            record.save()
            messages.success(request,"Record Added successfully!")
            return redirect("my_vault")
    return render(request,'core/record_upload.html',{'form':form})


def my_vault(request):
    profile=get_object_or_404(Profile,user=request.user)
    records=MedicalRecord.objects.filter(profile=profile).order_by("-uploaded_at")
    return render(request,'core/my_vault.html',{
        "records":records
    })


def delete_record(request,record_id:int):
    record=get_object_or_404(MedicalRecord,id=record_id,profile=request.user.profile)
    if record:
        record.file.delete()
    record.delete()
    messages.success(request,'Record Deleted Successfully')
    return redirect('my_vault')  


def view_record(request,record_id:int):
    record=MedicalRecord.objects.filter(id=record_id,profile=request.user.profile)
    return render(request, 'core/view_record.html', {'record': record})