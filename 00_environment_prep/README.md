# Step Zero: Prep Your Environment!

## Prep the EC-2 instance
SSH into your EC-2 instance, then type the following line-by-line:
```bash
sudo apt update
sudo apt install zip
sudo apt-get install gcc

# we want to install Java for Kafka and Spark
sudo apt install default-jre
sudo apt install default-jdk

# ... and I guess Scala...
sudo apt-get install scala

# we want to install Miniconda to take care of all our Python problems without
# being the smothering idiot that Anaconda is
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

# let's install Kafka!
wget http://apache-mirror.8birdsvideo.com/kafka/2.3.0/kafka_2.12-2.3.0.tgz
tar -xzf kafka_2.12-2.3.0.tgz
```

Add the following to your `~/.bashrc` file:
```bash
# for kafka installation
export PATH=/home/ubuntu/kafka_2.12-2.3.0/bin:$PATH
```

Installing PySpark is a bit more difficult. First, navigate to [Maven Cental's website](https://search.maven.org/search?q=spark-streaming-kafka-0-8-assembly) and download ` spark-streaming-kafka-0-8-assembly_2.11-2.4.4.jar`. `scp` this file to your EC-2 instance.
```bash
wget https://archive.apache.org/dist/spark/spark-2.4.4/spark-2.4.4-bin-hadoop2.7.tgz
tar -xzf spark-2.4.4-bin-hadoop2.7.tgz
```

Add the following to your `~/.bashrc` file:
```bash
# for Spark installation
export SPARK_HOME='/home/ubuntu/spark-2.4.4-bin-hadoop2.7'
export PATH=$SPARK_HOME:$PATH
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
```

Then run the following to make sure that `$PATH` adjustment actually applies:
```bash
source ~/.bashrc
```

## Grab the code
Use a guide such as [this](https://medium.com/digitalcrafts/how-to-set-up-an-ec2-instance-with-github-node-js-and-postgresql-e363cb771826) to establish your Github credentials on the EC-2 instance, then run the following command to grab the code:
```bash
git clone https://github.com/nathancooperjones/python-kafka-spark-kafka-bigquery-trump.git
cd python-kafka-spark-kafka-bigquery-trump/
pip install -r requirements.txt
```

Use a guide such as [this] (https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries) to set up your Google credentials.


## Run the code
You will need four EC2 windows open, either by making new tabs or using `tmux`. We will refer to these windows as EC2-1, EC2-2, EC2-3, and EC2-4.

**EC2-1:**
```bash
zookeeper-server-start.sh config/zookeeper.properties &
# press *Enter* until prompt returns
kafka-server-start.sh config/server.properties &
# press *Enter* until prompt returns
```

**EC2-2:**
```bash
python kafka_1_to_kafka_2.py
```

**EC2-3:**
```bash
python kafka_2_to_bigquery.py
```

**EC2-4:**
```bash
python user_to_kafka_1.py
```
