import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        # Log all incoming content
        logger.info(f"Webhook received from {request.META.get('REMOTE_ADDR')}")
        logger.info(f"Headers: {request.headers}")
        logger.info(f"Raw Body: {request.body.decode('utf-8', errors='ignore')}")

        payload = None
        try:
            payload = json.loads(request.body)
            logger.info(f"Parsed JSON Payload: {payload}")
        except json.JSONDecodeError as e:
            logger.error(f"Malformed JSON payload: {e}")
            # Continue processing even with malformed JSON as per FR-007

        # Process the payload (for now, just acknowledge)
        # Further processing logic would go here

        return HttpResponse(status=200)
    else:
        logger.warning(f"Webhook received with unsupported method: {request.method}")
        return HttpResponse(status=405)
