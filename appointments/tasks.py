from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from pets.models import Vaccination


@shared_task
def send_appointment_confirmation_email(appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)

        subject = f'Appointment Confirmation - {appointment.pet.name}'
        message = f"""
        Hello {appointment.owner.username},

        Your appointment has been booked successfully!

        Details:
        - Pet: {appointment.pet.name}
        - Date & Time: {appointment.appointment_date.strftime('%B %d, %Y at %H:%M')}
        - Reason: {appointment.reason}
        - Status: {appointment.get_status_display()}

        Thank you for using PetVet Diary!
        """

        recipient_email = appointment.owner.email

        if recipient_email:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            return f'Email sent to {recipient_email}'
        else:
            return 'No email address provided'

    except Appointment.DoesNotExist:
        return f'Appointment with id {appointment_id} does not exist'


@shared_task
def send_vaccination_reminders():
    today = timezone.now().date()
    upcoming_date = today + timedelta(days=7)

    upcoming_vaccinations = Vaccination.objects.filter(
        next_due_date__gte=today,
        next_due_date__lte=upcoming_date
    ).select_related('pet', 'pet__owner')

    sent_count = 0

    for vaccination in upcoming_vaccinations:
        owner = vaccination.pet.owner

        if owner.email:
            subject = f'Vaccination Reminder - {vaccination.pet.name}'
            message = f"""
            Hello {owner.username},

            This is a reminder that your pet {vaccination.pet.name} has an upcoming vaccination:

            Vaccine: {vaccination.vaccine_name}
            Due Date: {vaccination.next_due_date.strftime('%B %d, %Y')}

            Please schedule an appointment soon!

            Best regards,
            PetVet Diary Team
            """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [owner.email],
                fail_silently=True,
            )
            sent_count += 1

    return f'Sent {sent_count} vaccination reminders'