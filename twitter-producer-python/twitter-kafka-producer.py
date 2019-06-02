import tweepy
from confluent_kafka import Producer
import sys
import datetime

"""
twitter-kafka-producer

This is a basic python producer that streams twitter data to a kafka topic.

Usage:
- Operation requires a running instance of kafka
- "twitter-kafka-producer" reads/filters tweets from the twitter's streaming API
- "twitter-kafka-consumer" reads tweets from the corresponding kafka topic

To run an installed instance of kafka locally from the command line: 
1) start zookeeper
    MacOS: /usr/local/bin/zkServer start 
2) start kafka
    MacOS (foreground): kafka-server-start /usr/local/etc/kafka/server.properties
    
To read messages with the generic kafka command line consumer
    MacOS: kafka-console-consumer --bootstrap-server localhost:9092 --topic twitter-topic --from-beginning
 
"""

__author__ = "wak2116@columbia.edu"
__license__ = 'MIT'
__version__ = '0.0.1'
__status__ = 'Development'

# set twitter attributes
consumer_token = "0u0otpx8210Aq9xsOCk9nAZz9"
consumer_secret = "7EjAzixmA7Boncir8gwO3imPrzp4N18nYcpzPUaWm6igVw1d2G"
access_key = "1099110306591199233-nXHUGDsoz6VUqbtF1YG0m1wZd0JDVl"
access_secret = "y7suFGLDoQkpGpOqefXZsPSWqSRCo9v4WUxNEIzjmEzfS"
auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

# Columbia COSMOS Testbed
geofence = [-73.962266, 40.809294, -73.952029, 40.820262]

# set kafka attributes
broker = "localhost:9092"
topic = "twitter-topic"

# check python environment
# print("Hello World: twitter-kafka-producer")

# Create kafka producer instance
# See https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md
conf = {'bootstrap.servers': broker}
p = Producer(**conf)

# Kafka functions
# Optional per-message delivery callback (triggered by poll() or flush())
# when a message has been successfully delivered or permanently
# failed delivery (after retries).
def delivery_callback(err, msg):
    if err:
        sys.stderr.write('%% Message failed delivery: %s\n' % err)
    else:
        sys.stderr.write('%% Message delivered to %s [%d] @ %d\n' %
                         (msg.topic(), msg.partition(), msg.offset()))

# Tweepy functions
# create class to support streaming Twitter connection
# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        # convert GMT to NYC time
        tweet_dtc = str(status.created_at)
        dt_index = datetime.datetime.strptime(tweet_dtc, '%Y-%m-%d %H:%M:%S')
        dt_index -= datetime.timedelta(seconds=(60 * 60 * 4))
        nyc_datetime = dt_index.strftime('%Y-%m-%d-%H-%M-%S')

        data = status.text

        message = '[' + nyc_datetime + "]," + str(geofence) + ',[' + data + ']'
        #print(message)

        # Publish message to Kafka
        try:
            # Produce line (without newline)
            p.produce(topic, message, callback=delivery_callback)

        except BufferError:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                             len(p))

        # Serve delivery callback queue.
        # NOTE: Since produce() is an asynchronous API this poll() call
        #       will most likely not serve the delivery callback for the
        #       last produced message.
        p.poll(0)

        # Wait until all messages have been delivered
        sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
        p.flush()

    def on_error(self, status_code):
        if status_code == 420:
            print("402")
            # returning False in on_data disconnects the stream
            return False

    def on_timeout(self):
        print('Timeout...')
        return True  # Don't kill the stream

try:

    # connect to twitter and publish messages to kafka
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    # filter the tweets
    myStream.filter(locations=geofence)

except KeyboardInterrupt:
    sys.stderr.write('%% Aborted by user\n')

finally:
    p.flush()