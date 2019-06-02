from confluent_kafka import Consumer, KafkaException
import sys
import json
import logging
from pprint import pformat

"""
twitter-kafka-consumer

This is a basic python consumer that reads twitter data from a kafka topic.

Usage:
- Operation requires a running instance of kafka
- "twitter-kafka-producer" reads/filters tweets from the twitter's streaming API
- "twitter-kafka-consumer" reads tweets from the corresponding kafka topic

"""

__author__ = "wak2116@columbia.edu"
__license__ = 'MIT'
__version__ = '0.0.1'
__status__ = 'Development'

broker = "localhost:9092"
group = 1
topics = ["twitter-topic"]

print("Hello World: twitter-kafka-consumer")

def stats_cb(stats_json_str):
    stats_json = json.loads(stats_json_str)
    print('\nKAFKA Stats: {}\n'.format(pformat(stats_json)))


def print_usage_and_exit(program_name):
    sys.stderr.write('Usage: %s [options..] <bootstrap-brokers> <group> <topic1> <topic2> ..\n' % program_name)
    options = '''
 Options:
  -T <intvl>   Enable client statistics at specified interval (ms)
'''
    sys.stderr.write(options)
    sys.exit(1)

# Consumer configuration
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
conf = {'bootstrap.servers': broker, 'group.id': group, 'session.timeout.ms': 6000,
            'auto.offset.reset': 'earliest'}

# Enable client statistics at specified interval (ms)
#conf['stats_cb'] = stats_cb
#conf['statistics.interval.ms'] = 10000

# Create logger for consumer (logs will be emitted when poll() is called)
logger = logging.getLogger('consumer')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
logger.addHandler(handler)

# Create Consumer instance
# Hint: try debug='fetch' to generate some log messages
c = Consumer(conf, logger=logger)

def print_assignment(consumer, partitions):
    print('Assignment:', partitions)

# Subscribe to topics
c.subscribe(topics, on_assign=print_assignment)

# Read messages from Kafka, print to stdout
try:
    while True:
        msg = c.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            raise KafkaException(msg.error())
        else:
            # Proper message
            sys.stderr.write('%% %s [%d] at offset %d with key %s:\n' %
                             (msg.topic(), msg.partition(), msg.offset(),
                              str(msg.key())))
            print(msg.value())

except KeyboardInterrupt:
    sys.stderr.write('%% Aborted by user\n')

finally:
    # Close down consumer to commit final offsets.
    c.close()

