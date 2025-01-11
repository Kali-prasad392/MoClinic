from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from .models import PatientDetails, PatientQueue, Medicines, Tests, Prescription
import json

def register_patient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient = PatientDetails.objects.create(
            user_id=data.get('user_id'),
            weight=data.get('weight'),
            height=data.get('height'),
            temperature=data.get('temperature'),
            blood_pressure=data.get('blood_pressure'),
            BMI=data.get('BMI'),
            cholesterol=data.get('cholesterol'),
            blood_sugar=data.get('blood_sugar'),
            date_visited=data.get('date_visited'),
            date_treated=data.get('date_treated')
        )
        return JsonResponse({"message": "Patient registered successfully", "patient_id": str(patient.patient_ID)}, status=201)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def enqueue_patient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient = get_object_or_404(PatientDetails, patient_ID=data.get('patient_id'))
        PatientQueue.objects.create(
            patient=patient,
            queue_position=data.get('queue_position')
        )
        return JsonResponse({"message": "Patient added to queue"}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def dequeue_patient(request):
    if request.method == 'POST':
        queue_entry = PatientQueue.objects.order_by('queue_position').first()
        if queue_entry:
            queue_entry.delete()
            return JsonResponse({"message": "Patient dequeued", "patient_id": str(queue_entry.patient.patient_ID)}, status=200)
        return JsonResponse({"error": "Queue is empty"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def call_patient(request):
    if request.method == 'GET':
        queue_entry = PatientQueue.objects.order_by('queue_position').first()
        if queue_entry:
            return JsonResponse({"message": "Patient called", "patient_id": str(queue_entry.patient.patient_ID)}, status=200)
        return JsonResponse({"error": "Queue is empty"}, status=404)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def get_patient_details(request):
    if request.method == 'GET':
        patient_id = request.GET.get('patient_id')
        patient = get_object_or_404(PatientDetails, patient_ID=patient_id)
        patient_data = {
            "user_id": patient.user_id,
            "weight": patient.weight,
            "height": patient.height,
            "temperature": patient.temperature,
            "blood_pressure": patient.blood_pressure,
            "BMI": patient.BMI,
            "cholesterol": patient.cholesterol,
            "blood_sugar": patient.blood_sugar,
            "date_visited": patient.date_visited,
            "date_treated": patient.date_treated,
        }
        return JsonResponse(patient_data, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)


def prescribe(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        patient = get_object_or_404(PatientDetails, patient_ID=data.get('patient_id'))
        prescription = Prescription.objects.create(
            patient=patient,
            medicine=data.get('medicine'),
            dosage=data.get('dosage'),
            instructions=data.get('instructions')
        )
        return JsonResponse({"message": "Prescription added successfully", "prescription_id": str(prescription.prescription_ID)}, status=200)
    return JsonResponse({"error": "Invalid request method"}, status=400)