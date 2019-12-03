# Step Two: Run the App!

The hard part is done - everything is installed and downloaded. Let's have some fun now!

Ensure you configured `config.py` with your own information.

To properly run this application, it is recommended you have four EC2 windows open, either through new tabs or a tool like `tmux`. We will refer to these windows as **EC2-1**, **EC2-2**, **EC2-3**, and **EC2-4**.

### EC2-1:
```bash
zookeeper-server-start.sh config/zookeeper.properties &
# press *Enter* until prompt returns
kafka-server-start.sh config/server.properties &
# press *Enter* until prompt returns
```

### EC2-2:
```bash
python 02_kafka_1_to_kafka_2.py
```

### EC2-3:
```bash
python 03_kafka_2_to_bigquery.py
```

### EC2-4:
```bash
python 01_user_to_kafka_1.py
```

You can enter text into and view your Trump results on **EC2-4**. Enjoy!
