from kafka import KafkaConsumer
import json
from app.api.send_email import consumer_sendmail

bootstrap_servers = ['localhost:9092']

cons = KafkaConsumer(
    'test-topics',
    group_id='group1',
    bootstrap_servers=bootstrap_servers,
    enable_auto_commit=True)

for message in cons:
    data = json.loads(message.value.decode('utf-8'))
    from mail10minutes import app
    with app.app_context():
        consumer_sendmail(data=data)
