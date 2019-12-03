# Step Zero: Prep Your Environment!

## Get an EC2 instance
I recommend selecting a **Ubuntu 18.04 Amazon Machine Image (AMI)** of type **t3a.xlarge** with at least **16GB** of storage.

## Prep the EC2 instance
SSH into your EC2 instance, then type the following line-by-line:
```bash
sudo apt update
sudo apt install zip
sudo apt-get install gcc

# we want to install Java for Kafka and Spark
sudo apt install default-jre
sudo apt install default-jdk

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

Then run the following to make sure that `$PATH` adjustment actually applies:
```bash
source ~/.bashrc
```

Use a guide such as [this](https://cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries) to set up your Google credentials.
