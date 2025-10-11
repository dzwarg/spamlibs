from django.db import models

class IncomingMessage(models.Model):
    attachments = models.JSONField(default=list)
    headers = models.JSONField(default=dict)
    headerLines = models.JSONField(default=list)
    html = models.TextField(blank=True)
    text = models.TextField(blank=True)
    textAsHtml = models.TextField(blank=True)
    subject = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    to = models.JSONField(default=dict)
    from_field = models.JSONField(default=dict)
    messageId = models.CharField(max_length=255, blank=True)
    raw = models.TextField(blank=True)
    dkim = models.JSONField(default=dict)
    spf = models.JSONField(default=dict)
    arc = models.JSONField(default=dict)
    dmarc = models.JSONField(default=dict)
    bimi = models.JSONField(default=dict)
    recipients = models.JSONField(default=list)
    session = models.JSONField(default=dict)

    def __str__(self):
        return self.subject
