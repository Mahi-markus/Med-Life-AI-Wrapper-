from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Patient, Prescription, Medicine
from .utils import  ocr_extract_prescription
from PyPDF2 import PdfReader   # <-- ADD THI

@csrf_exempt
def process_prescription(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=400)
    print("REQUEST FILES:", request.FILES)
    uploaded_file = request.FILES.get("file")
    
    if not uploaded_file:
        return JsonResponse({"error": "No file provided"}, status=400)

    # only pdf for now
    if uploaded_file.content_type != "application/pdf":
        return JsonResponse({"error": "Only PDF files are supported"}, status=400)
    # Extract text from PDF
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        extracted_text += page.extract_text() + "\n"
    print("EXTRACTED TEXT:", extracted_text)

    # Call OCR LLM
    ocr_json_str = ocr_extract_prescription(extracted_text)
    print("test:", type(ocr_json_str))
    
    
    import json
    ocr_data = json.loads(ocr_json_str)

    # Save patient
    patient_data = ocr_data["patient"]
    patient, _ = Patient.objects.get_or_create(
        email=patient_data["email"],
        defaults={"name": patient_data["name"]}
    )

    # Save prescription
    prescription = Prescription.objects.create(
        patient=patient,
        prescrip_analogy=ocr_data["prescription"]["analogy"]
    )

    # Save medicines
    medicine_list = []
    for med in ocr_data["medicines"]:
        medicine = Medicine.objects.create(
            name=med["name"],
            expire_date=med["expire_date"],
            dosage=med["dosage"],
            instruction=med["instruction"],
            number_of_pills_in_day=med["number_of_pills_in_day"],
            part_of_day=med["part_of_day"]
        )
        medicine_list.append(medicine)

    prescription.medicine_info.set(medicine_list)

    return JsonResponse({
        "message": "Prescription processed successfully",
        "patient_id": patient.patient_id,
        "prescription_id": prescription.prescrip_id
    })
