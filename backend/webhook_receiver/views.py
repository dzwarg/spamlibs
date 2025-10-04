import json
import logging
from datetime import datetime

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import IncomingMessage

logger = logging.getLogger(__name__)

@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        logger.info(f"Webhook received from {request.META.get('REMOTE_ADDR')}")
        logger.info(f"Headers: {request.headers}")
        logger.info(f"Raw Body: {request.body.decode('utf-8', errors='ignore')}")

        try:
            payload = json.loads(request.body)
            logger.info(f"Parsed JSON Payload: {payload}")
        except json.JSONDecodeError as e:
            logger.error(f"Malformed JSON payload: {e}")
            return JsonResponse({'error': 'Malformed JSON payload'}, status=400)

        required_fields = ['subject', 'from', 'text']
        missing_fields = [field for field in required_fields if field not in payload]
        if missing_fields:
            return JsonResponse({'error': f'Missing required fields: {", ".join(missing_fields)}'}, status=400)

        date_str = payload.get('date')
        date_obj = None
        if date_str:
            try:
                # Replace 'Z' with '+00:00' for fromisoformat
                if date_str.endswith('Z'):
                    date_str = date_str[:-1] + '+00:00'
                date_obj = datetime.fromisoformat(date_str)
            except ValueError:
                logger.warning(f"Could not parse date: {date_str}")

        message = IncomingMessage(
            attachments=payload.get('attachments', []),
            headers=payload.get('headers', {}),
            headerLines=payload.get('headerLines', []),
            html=payload.get('html', ''),
            text=payload.get('text', ''),
            textAsHtml=payload.get('textAsHtml', ''),
            subject=payload.get('subject', ''),
            date=date_obj,
            to=payload.get('to', {}),
            from_field=payload.get('from', {}),
            messageId=payload.get('messageId', ''),
            raw=payload.get('raw', ''),
            dkim=payload.get('dkim', {}),
            spf=payload.get('spf', {}),
            arc=payload.get('arc', {}),
            dmarc=payload.get('dmarc', {}),
            bimi=payload.get('bimi', {}),
            recipients=payload.get('recipients', []),
            session=payload.get('session', {}),
        )
        message.save()

        return HttpResponse(status=200)
    else:
        logger.warning(f"Webhook received with unsupported method: {request.method}")
        return HttpResponse(status=405)
