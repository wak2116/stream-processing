This readme describes the process to deploy a three node kafka cluster on the Google Cloud Platorm (GCP)

1) Open the Google Cloud Platform console ( https://console.cloud.google.com )
2) Create a new project
3) Use the menu in the upper left corner to access the "Compute Engine" page
4) Under "VM instances", use "CREATE INSTANCE" to create three VMs with the following attributes:  
   Region: us-east4 (Northern Virginia)  
   Zone: us-east4-c  
   Machine type: small  
   Boot disk: Ubuntu 18.04 LTS  
   "Allow HTTP traffic" is checked  
   "Allow HTTPS traffic" is checked  
5) In the Google console, note the "Internal IP" addresses for each VM instance
6) In the Google console, note the "External IP" addresses for each VM instance
7) Select the first VM instance and launch an SSH seesion
8) Download and install Apache Zookeeper
  : wget https://www.apache.org/dist/zookeeper/KEYS  
  : gpg --import KEYS  
  : wget http://mirror.cc.columbia.edu/pub/software/apache/zookeeper/zookeeper-3.5.5/apache-zookeeper-3.5.5.tar.gz  
  : wget https://www-eu.apache.org/dist/zookeeper/zookeeper-3.5.5/apache-zookeeper-3.5.5.tar.gz.asc  
  : gpg --verify apache-zookeeper-3.5.5.tar.gz.asc apache-zookeeper-3.5.5.tar.gz  
  [ Note: verify that signature is good before proceeding ]  
  : tar -xzf apache-zookeeper-3.5.5.tar.gz  
  : ln -sfn apache-zookeeper-3.5.5 zookeeper  
  : rm KEYS apache-zookeeper-3.5.5.tar.gz apache-zookeeper-3.5.5.tar.gz.asc  
9) Download and install Apache Kafka
  : wget https://www.apache.org/dist/kafka/KEYS  
  : gpg --import KEYS  
  : wget http://mirrors.ocf.berkeley.edu/apache/kafka/2.2.0/kafka_2.12-2.2.0.tgz  
  : wget https://www-eu.apache.org/dist/kafka/2.2.0/kafka_2.12-2.2.0.tgz.asc  
  : gpg --verify kafka_2.12-2.2.0.tgz.asc kafka_2.12-2.2.0.tgz  
  [ Note: verify that signature is good before proceeding ]  
  : tar -xzf kafka_2.12-2.2.0.tgz  
  : ln -sfn kafka_2.12-2.2.0 kafka  
  : rm KEYS kafka_2.12-2.2.0.tgz kafka_2.12-2.2.0.tgz.asc  
10) Install Java
  : sudo add-apt-repository ppa:webupd8team/java  
  : sudo apt update  
  : sudo apt install default-jre   
  : java --version  
11) Verify that your favorate text editor is installed
  To install emacs on Ubuntu  
  : sudo apt-get update  
  : sudo apt-get install emacs  
12) Configure zookeeper as a three node cluster
  Create zookeeper myid file  
  [ Note: set myid to '1' for node 1, set myid to '2' for node 2, ... ]  
  : mkdir /tmp/zookeeper/ -p  
  : touch /tmp/zookeeper/myid  
  : echo '1' >> /tmp/zookeeper/myid  
  Create "zookeeper.properties" file  
  : cd zookeeper/conf  
  : touch zookeeper.properties  
  Use your favorite text editor to add the following properties to "zookeeper.properties" file  
  [ Note: replace x.x.x.x with the cooresponding IP addresses obtained in Step 5 ]  
      dataDir=/tmp/zookeeper  
      clientPort=2181  
      maxClientCnxns=200  
      tickTime=2000  
      server.1=x.x.x.x:2888:3888  
      server.2=x.x.x.x:2888:3888   
      server.3=x.x.x.x:2888:3888  
      initLimit=20  
      syncLimit=10  
13) Congfigure kafka as a three node cluser
  : cd ~/kafka/config  
  : cp server.properties server.properties.orig  
  Use your favorite text editor to set the following properties to "server.properties" file  
  [ Note: set broker.id to 1 for node 1, set broker.id to 2 for node 2, ... ]  
  [ Note: replace x.x.x.x with the cooresponding IP addresses obtained in Step 5 ]  
  [ Note: replace y.y.y.y with the cooresponding IP address obtained in Step 6 ]  
      broker.id=1  
      advertised.listeners=PLAINTEXT://y.y.y.y:9092  
      zookeeper.connect=x.x.x.x:2181,x.x.x.x:2181,x.x.x.x:2181  
14) Start zookeeper  
   : cd ~/zookeeper  
   : bin/zkServer.sh start conf/zookeeper.properties  
   : bin/zkServer.sh status conf/zookeeper.properties   
15) Start kafka   
   : cd ~/kafka  
   : bin/kafka-server-start.sh -daemon config/server.properties
16) Repeat steps 8-15 on the remaining two VM instances
