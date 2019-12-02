from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


if __name__ == "__main__":
    sc = SparkContext(appName='PythonStreamingDirectKafkaTweet')
    sc.setLogLevel('ERROR')
    ssc = StreamingContext(sc, 1)  # 1 second for now

    brokers = 'localhost:9092'
    topic = 'sentence_to_kafka_1'

    kvs = KafkaUtils.createDirectStream(ssc, [topic], {'metadata.broker.list': brokers})
    lines = kvs.map(lambda x: x['sentence_to_encode'])
    lines.pprint()

    counts = lines.map(lambda word: (word, 1))
    counts.pprint()

    ssc.start()
    ssc.awaitTermination()
