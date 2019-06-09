This file documents the installation process to run a standalone kafka + spark streaming pipeline from the command line
1) Install Java  
(1.1) sudo apt update  
(1.2) sudo apt install default-jre  
(1.3) java --version  
2) Download and install Apache Zookeeper
(2.1) wget https://www.apache.org/dist/zookeeper/KEYS  
(2.2) gpg --import KEYS  
(2.3) wget https://www-eu.apache.org/dist/zookeeper/zookeeper-3.5.5/apache-zookeeper-3.5.5-bin.tar.gz  
(2.4) wget https://www-eu.apache.org/dist/zookeeper/zookeeper-3.5.5/apache-zookeeper-3.5.5-bin.tar.gz.asc  
(2.5) gpg --verify apache-zookeeper-3.5.5-bin.tar.gz.asc apache-zookeeper-3.5.5-bin.tar.gz  
(2.6) Note: verify that signature is good before proceeding  
(2.7) tar -xzf apache-zookeeper-3.5.5-bin.tar.gz  
(2.8) ln -sfn apache-zookeeper-3.5.5-bin zookeeper  
(2.9) rm KEYS apache-zookeeper-3.5.5-bin.tar.gz apache-zookeeper-3.5.5-bin.tar.gz.asc  
3) Configure zookeeper as a standalone instance  
3.1) sudo mkdir /data/zookeeper/ -p
3.2) Note: In the next step, replace "your_username" with your username    
3.2) sudo chown -R your_username:your_username /data  
3.3) touch /data/zookeeper/myid  
3.4) echo '1' >> /data/zookeeper/myid  
3.5) cd ~/zookeeper/conf   
3.6) cp zoo_sample.cfg zoo.cfg   
3.7) Use your favorite text editor to set the following properties to "zoo.cfg" file  
Note: In this step, replace "x.x.x.x" with the internally facing IP addresss for the server you are ssh'd into    
  dataDir=/data/zookeeper  
  server.1=x.x.x.x:2888:3888  
4) Start zookeeper  
(4.1) ~/zookeeper/bin/zkServer.sh start ~/zookeeper/conf/zoo.cfg
5) Download and install Apache Kafka  
(5.1) cd ~  
(5.2) wget https://www.apache.org/dist/kafka/KEYS   
(5.3) gpg --import KEYS  
(5.4) wget http://mirrors.ocf.berkeley.edu/apache/kafka/2.2.0/kafka_2.12-2.2.0.tgz  
(5.5) wget https://www-eu.apache.org/dist/kafka/2.2.0/kafka_2.12-2.2.0.tgz.asc  
(5.6) gpg --verify kafka_2.12-2.2.0.tgz.asc kafka_2.12-2.2.0.tgz  
(5.7) Note: verify that signature is good before proceeding  
(5.8) tar -xzf kafka_2.12-2.2.0.tgz  
(5.9) ln -sfn kafka_2.12-2.2.0 kafka  
(5.10) rm KEYS kafka_2.12-2.2.0.tgz kafka_2.12-2.2.0.tgz.asc  
6) Configure kafka as a standalone instance  
(6.1) cd ~/kafka/config  
(6.2) cp server.properties server.properties.orig   
(6.3) Use your favorite text editor to set the following properties to "server.properties" file  
Note: In this step, replace "x.x.x.x" with the internally facing IP addresss for the server you are ssh'd into  
Note: In this step replace "y.y.y.y" with the externally facing IP addresss for the server you are ssh'd into  
  broker.id=1  
  advertised.listeners=PLAINTEXT://y.y.y.y:9092  
  zookeeper.connect=x.x.x.x:2181  
7) Start kafka  
(7.1) ~/kafka/bin/kafka-server-start.sh -daemon ~/kafka/config/server.properties &
8) Download spark
(8.0) cd ~   
(8.1) wget https://www.apache.org/dist/spark/KEYS  
(8.2) gpg --import KEYS  
(8.3) wget http://mirror.cc.columbia.edu/pub/software/apache/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz 
(8.4) wget   
(8.5) gpg --verify apache-zookeeper-3.5.5-bin.tar.gz.asc apache-zookeeper-3.5.5-bin.tar.gz  
(8.6) Note: verify that signature is good before proceeding  
(8.7) tar -xzf apache-zookeeper-3.5.5-bin.tar.gz  
(8.8) ln -sfn apache-zookeeper-3.5.5-bin zookeeper  
(8.9) rm KEYS apache-zookeeper-3.5.5-bin.tar.gz apache-zookeeper-3.5.5-bin.tar.gz.asc
