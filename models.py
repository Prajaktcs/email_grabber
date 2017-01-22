from datetime import datetime

from elasticsearch_dsl import Date, DocType, Text, Text


class EmailMsg(DocType):
    class Meta:
        index = 'emails'

    created_at = Date()
    subject = Text()
    from_user = Text()
    to_user = Text()
    cc_user = Text()
    msg_num = Text()
    body = Text()
    received_date = Date()

    def save(self, *args, **kwargs):
        if not self.created_at or 'override_created' in kwargs:
            self.created_at = datetime.now()
        super().save(*args, **kwargs)