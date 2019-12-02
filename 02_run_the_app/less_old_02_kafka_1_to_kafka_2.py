from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')


def predict(rdd):
    count = rdd.count()
    if (count > 0):
        counts = lines.map(lambda sentence: model.encode(sentence))
        return counts
    else:
        print('No data received!')


if __name__ == "__main__":
    sc = SparkContext(appName='PythonStreamingDirectKafkaTweet')
    sc.setLogLevel('ERROR')
    ssc = StreamingContext(sc, 1)  # 1 second for now

    brokers = 'localhost:9092'
    topic = 'sentence_to_kafka_1'

    kvs = KafkaUtils.createDirectStream(ssc, [topic], {'metadata.broker.list': brokers})
    lines = kvs.map(lambda x: x[1])
    lines.pprint()

    lines.foreachRDD(lambda rdd: predict(rdd))

    ssc.start()
    ssc.awaitTermination()
