# on one EC-2 window, type the following:
sudo apt update
sudo apt install zip

# we want to install Java for Kafka and Spark
sudo apt install default-jre
sudo apt install default-jdk

# we want to install Miniconda to take care of all our Python problems without
# being the smothering idiot that Anaconda is
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
source ~/.bashrc

# let's install Kafka!
pip install kafka-python
wget http://apache-mirror.8birdsvideo.com/kafka/2.3.0/kafka_2.12-2.3.0.tgz
tar -xzf kafka_2.12-2.3.0.tgz

# ADD THE FOLLOWING TO YOUR ~/.bashrc:
# --------------
# for kafka installation
export PATH=/home/ubuntu/kafka_2.12-2.3.0/bin:$PATH
# --------------
source ~/.bashrc

# Set up is officially complete!

# Now let's start the project!

EC2-1:
zookeeper-server-start.sh config/zookeeper.properties &
kafka-server-start.sh config/server.properties &
