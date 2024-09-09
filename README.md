<div>
    <h2 align="center">Real-time Facial Recognition Based Attendance and Activity Tracking System</h2>
</div>
<!--
<p align="center"><em>Abdisa Merga and Ephrata Zerfu</em></p>
<p align="center"></p>
-->
<h4><p align="Center">The Architecture</p></h4>
<div align="center">
    <a href="https://github.com/abdimk/facial_analysis/blob/main/Architecture"><img src="https://github.com/abdimk/facial_analysis/blob/main/Architecture/1.png" width="300" hight="400"></a>
</div>


<p align="center">
<a target="_blank" href="https://search.maven.org/artifact/com.webencyclop.core/mftool-java"><img src="https://img.shields.io/maven-central/v/com.webencyclop.core/mftool-java.svg?label=Maven%20Central"/></a> 
<a target="_blank" href="https://www.codacy.com/gh/ankitwasankar/mftool-java/dashboard?utm_source=github.com&utm_medium=referral&utm_content=ankitwasankar/mftool-java&utm_campaign=Badge_Coverage"><img src="https://app.codacy.com/project/badge/Coverage/0054db87ea0f426599c3a30b39291388" /></a>
<a href="https://www.codacy.com/gh/ankitwasankar/mftool-java/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ankitwasankar/mftool-java&amp;utm_campaign=Badge_Grade"><img src="https://app.codacy.com/project/badge/Grade/0054db87ea0f426599c3a30b39291388"/></a>
<a target="_blank" href="https://github.com/ankitwasankar/mftool-java/blob/master/license.md"><img src="https://camo.githubusercontent.com/8298ac0a88a52618cd97ba4cba6f34f63dd224a22031f283b0fec41a892c82cf/68747470733a2f2f696d672e736869656c64732e696f2f707970692f6c2f73656c656e69756d2d776972652e737667" /></a>
&nbsp <a target="_blank" href="https://www.linkedin.com/in/ankitwasankar/"><img height="20" src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
</p>
<p align="center">
  This repository contains the <strong>Setup and Configration</strong> for activity and facial recogniton attendance system.
    
  </p>

<p align="center">
<a href="#Introduction">Introduction</a> &nbsp;&bull;&nbsp;
<a href="#Installation">Installation</a> &nbsp;&bull;&nbsp;
<a href="#Usage">Usage</a> &nbsp;&bull;&nbsp;
<a href="#Documentation">Documentation</a> &nbsp;&bull;&nbsp;
<a href="#Issue">Issue?</a>
</p>




# Introduction
This <b>repository</b> provides simple APIs/functions/methods to work with svm facial recogniton You can:

- Reconize faces using svm Classification [Tensorflow](for Future)
- Able to take live stream feeds from multiple cameras at the same time using Kafka
- Fetch historic data on kibana
- Fetch assocated details from the sqlite database
- Generate Historical report using csv
- Able to run on distributed system/cluster nodes

# Face recognition Process using svm(support vector machine) clssification
<h4><p align="Center">Face Recognition Process </p></h4>
<div align="center">
    <a href="https://github.com/abdimk/facial_analysis/blob/main/Architecture"><img src="https://github.com/abdimk/facial_analysis/blob/main/Architecture/2.png" width="900"></a>
</div>

## System Dependencies

<strong> you need to Install those dependency for your os to run this system </strong> !

- Kafka - is a distributed event streaming platform used for building real-time data pipelines and streaming applications.
- ElasticSearch -is a distributed, RESTful search and analytics engine built on top of Apache Lucene.
- Kibana - Kibana is an open-source data visualization and exploration tool for Elasticsearch.

# Usage
clone the github repo 

```
git clone https://github.com/abdimk/facial_analysis
```
install the python libraries need 

```
pip3 install -r requirements.txt
```
<div align="center">
    <a href="#"><img src="https://github.com/abdimk/facial_analysis/blob/main/Assets/old.png" width="400"></a>
</div>

record a user using either [Register](https://github.com/abdimk/facial_analysis/blob/main/Register.py) or our new [customRegister](https://github.com/abdimk/facial_analysis/blob/main/customRegister.py)


run one of these apps using 

```
python3 customRegister.py
```

it capture 5 images for a singe individual and stores it on the DataBase folder

encode the face and thier names 

```
python3 Model/cpuModels/encode_faces.py
```


start the utilities as one 
```
python3 control/start.py
```
cd to the model

the run the main.py

```
python3 Model/main.py
```

# Installation
<p align="center">
<a href="#kafka">How do i install kafka</a> &nbsp;&bull;&nbsp;
<a href="#elastic">Elastic Search installtion</a> &nbsp;&bull;&nbsp;
<a href="#kibana">Kibana installation</a>
</p>



# kafka
installing kafka for ubuntu 22.04 > 

To update the system packages 
```
sudo apt get update
```
you can install OpenJDK 8 or OpenJDK 11
```
sudo apt install openjdk-8-jdk
```
or

```
sudo apt install openjdk-11-jdk
```

you also need to add java home to your path/bashrc file

```
sudo nano ~/.bashrc
```
then add this 
```
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 
export PATH=$PATH:/usr/lib/jvm/java-11-openjdk-amd64/bin 
```
update the path 
```
sudo source ~/.bashrc
```

### download kafka binary
To download the Kafka binary from offical website. Please use this <a href="https://kafka.apache.org/downloads">Kafka official download page</a> and to prompts to download page and you can download Kafka using wget

```
sudo wget https://downloads.apache.org/kafka/3.8.0/kafka_2.13-3.8.0.tgz
````

#### Step #1:Install Apache Kafka on Ubuntu 22.04 LTS
Now to un-tar or Unzip the archive file and move to another location:

```
sudo tar xzf kafka_2.13-3.8.0.tgz
```

```
sudo mv kafka_2.12-3.5.0 /opt/kafka
```
#### Step #2:Creating Zookeeper and Kafka Systemd Unit Files in Ubuntu 22.04 LTS

Create the systemd unit file for zookeeper service

```
sudo nano  /etc/systemd/system/zookeeper.service
```

paste the below lines

```
/etc/systemd/system/zookeeper.service
[Unit]
Description=Apache Zookeeper service
Documentation=http://zookeeper.apache.org
Requires=network.target remote-fs.target
After=network.target remote-fs.target

[Service]
Type=simple
ExecStart=/opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
ExecStop=/opt/kafka/bin/zookeeper-server-stop.sh
Restart=on-abnormal

[Install]
WantedBy=multi-user.target
```

Reload the daemon to take effect

```
sudo systemctl daemon-reload
```
Create the systemd unit file for kafka service

```
sudo nano /etc/systemd/system/kafka.service
```
paste the below lines
```
[Unit]
Description=Apache Kafka Service
Documentation=http://kafka.apache.org/documentation.html
Requires=zookeeper.service

[Service]
Type=simple
Environment="JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64"
ExecStart=/opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties
ExecStop=/opt/kafka/bin/kafka-server-stop.sh

[Install]
WantedBy=multi-user.target
```
Reload the daemon to take effect
```
sudo systemctl daemon-reload
```

#### Step #3:To Start ZooKeeper and Kafka Service and Check its Status
Lets start zookeeper service first
```
sudo systemctl start zookeeper
```

Check the status of  zookeeper service if it started

```
sudo systemctl status zookeeper
```

Start the kafka service

```
sudo systemctl start kafka
```

Check the status of  kafka service if it started
```
sudo systemctl status kafka
```
