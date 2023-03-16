import pika

# Set connection parameters
credentials = pika.PlainCredentials('reader', 'reader')
parameters = pika.ConnectionParameters('108.143.79.237',
                                       5672,
                                       '/',
                                       credentials)

# Connect to RabbitMQ server
connection = pika.BlockingConnection(parameters)

# Create a channel
channel = connection.channel()

# Declare an exclusive queue
result = channel.queue_declare(queue='', exclusive=True)

# Get the queue name
queue_name = result.method.queue

# Bind the queue to the exchange
channel.queue_bind(exchange='toll', queue=queue_name, routing_key='my_key')


# Define a callback function to handle incoming messages
def callback(ch, method, properties, body):
    # Decode from bytes to normal string
    decoded_response = body.decode()

    # Convert from string to dictionary
    message_dict = eval(decoded_response)

    # Get separate variables for passing to functions
    lat = message_dict.get('lat')
    lon = message_dict.get('lon')
    license_plate = message_dict.get('licenseplate')
    toll_gate_id = message_dict.get('id')
    time = message_dict.get('time')

    # Just a test print
    print(lat, lon, license_plate, toll_gate_id, time)


# Start consuming messages from the queue
channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

# Start the event loop
channel.start_consuming()
