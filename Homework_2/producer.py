from faker import Faker
import json
import logging
import pika
from models import Contact
from mongoengine import connect, Document, StringField, BooleanField

connect('homework_8_2')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

# Створення обміну для sms_queue
channel.exchange_declare(exchange='sms_queue', exchange_type='direct')

channel.queue_declare(queue='email_queue', durable=True)
channel.queue_declare(queue='sms_queue', durable=True)

fake = Faker()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(nums: int):
    logger.info("Starting producer...")
    for _ in range(nums):
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
            phone_number=fake.phone_number(),
            preferred_contact_method=fake.random_element(elements=('SMS', 'Email'))
        )
        contact.save()

        message = {'contact_id': str(contact.id)}

        json_message = json.dumps(message)

        if contact.preferred_contact_method == 'SMS':
            # Надсилання повідомлення до обміну 'sms_queue'
            channel.basic_publish(exchange='sms_queue', routing_key='', body=json_message,
                                  properties=pika.BasicProperties(delivery_mode=2))
            logger.info(f"Message sent to SMS queue: {json_message}")
        else:
            # Надсилання повідомлення до обміну 'email_queue'
            channel.basic_publish(exchange='', routing_key='email_queue', body=json_message,
                                  properties=pika.BasicProperties(delivery_mode=2))
            logger.info(f"Message sent to Email queue: {json_message}")

    connection.close()
    logger.info("Producer stopped.")

if __name__ == '__main__':
    main(10)
