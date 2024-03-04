import json
import os
import sys
import pika
from models import Contact
from mongoengine import connect

connect('homework_8_2')

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue', durable=True)

def main():
    def callback(ch, method, properties, body):
        message = json.loads(body)
        contact_id = message['contact_id']
        contact = Contact.objects(id=contact_id).first()
        if contact:
            send_email(contact.email)

            contact.message_sent = True
            contact.save()
            print(f"Email sent to {contact.email}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='email_queue', on_message_callback=callback)

    print(' [*] Waiting for messages from email_queue. To exit press CTRL+C')
    channel.start_consuming()

def send_email(email):
    print(f"Sending email to {email}")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
