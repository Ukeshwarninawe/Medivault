from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import OCRDocumentForm
from .models import OCRDocument
from .ocr_utils import run_ocr
from accounts.models import Profile  # Make sure you import the Profile model
from django.contrib import messages


@login_required
def upload_document(request):
    profile = get_object_or_404(Profile, user=request.user)
    document = None

    if request.method == 'POST':
        form = OCRDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.profile = profile 
            document.save()

            # Run OCR and save results
            try:
                text = run_ocr(document.file.path)
                document.ocr_result = text
                document.processed = True
                document.save()
                messages.success(request, "OCR processing complete.")
            except Exception as e:
                messages.error(request, f"OCR processing failed: {str(e)}")

            return render(request, 'ocr/upload.html', {
                'form': OCRDocumentForm(),  # empty form for next upload
                'document': document
            })
    else:
        form = OCRDocumentForm()

    return render(request, 'ocr/upload.html', {'form': form})


@login_required
def my_uploads(request):
    profile = get_object_or_404(Profile, user=request.user)
    uploads = OCRDocument.objects.filter(profile=profile).order_by('-uploaded_at')
    return render(request, 'ocr/my_upload.html', {'uploads': uploads})




@login_required
def view_uploads(request, document_id: int):
    profile = get_object_or_404(Profile, user=request.user)
    document = get_object_or_404(OCRDocument, id=document_id, profile=profile)

    return render(request, 'ocr/view_upload.html', {'document': document})


from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
# @require_POST
def delete_uploads(request, document_id: int):
    profile = get_object_or_404(Profile, user=request.user)
    document = get_object_or_404(OCRDocument, id=document_id, profile=profile)

    document.file.delete(save=False)
    document.delete()  

    messages.success(request, "Document deleted successfully.")
    return HttpResponseRedirect(reverse('my_uploads'))
