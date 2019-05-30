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
7) Add firewall exceptions to support internal communication between VM instances
8) Add firewall exceptions to support client connections to VM instances
9) Select the first VM instance and launch an SSH seesion
10) Install Java  
  : sudo apt-get update  
  : sudo apt-get install default-jre   
  : java --version  
11) Download and install Apache Zookeeper  
  : wget https://www.apache.org/dist/zookeeper/KEYS  
  : gpg --import KEYS  
  : wget https://www-eu.apache.org/dist/zookeeper/zookeeper-3.5.5/apache-zookeeper-3.5.5-bin.tar.gz   
  : wget https://www-eu.apache.org/dist/zookeeper/zookeeper-3.5.5/apache-zookeeper-3.5.5-bin.tar.gz.asc  
  : gpg --verify apache-zookeeper-3.5.5-bin.tar.gz.asc apache-zookeeper-3.5.5-bin.tar.gz  
  [ Note: verify that signature is good before proceeding ]  
  : tar -xzf apache-zookeeper-3.5.5-bin.tar.gz  
  : ln -sfn apache-zookeeper-3.5.5-bin zookeeper  
  : rm KEYS apache-zookeeper-3.5.5-bin.tar.gz apache-zookeeper-3.5.5-bin.tar.gz.asc
12) Verify that your favorate text editor is installed
  To install emacs on Ubuntu    
  : sudo apt-get update    
  : sudo apt-get install emacs    
13) Configure zookeeper as a three node cluster
  Create zookeeper myid file  
  [ Note: set myid to '1' for node 1, set myid to '2' for node 2, ... ]  
  : sudo mkdir /data/zookeeper/ -p. 
  : sudo chown -R your_username:your_username /data   
  : touch /data/zookeeper/myid  
  : echo '1' >> /data/zookeeper/myid   
  Create "zoo.cfg" file  
  : cd ~/zookeeper/conf  
  : cp zoo_sample.cfg zoo.cfg  
  Use your favorite text editor to set the following properties to "zoo.cfg" file  
  [ Note: replace x.x.x.x with the cooresponding IP addresses obtained in Step 5 ]  
      dataDir=/data/zookeeper  
      server.1=x.x.x.x:2888:3888  
      server.2=x.x.x.x:2888:3888   
      server.3=x.x.x.x:2888:3888   
14) Start zookeeper  
   : cd ~/zookeeper  
   : bin/zkServer.sh start conf/zoo.cfg  
   : bin/zkServer.sh status conf/zoo.cfg   
15) Repeat steps 10 through 14 for the other VM instances
16) Download and install Apache Kafka  
  : cd ~  
  : wget https://www.apache.org/dist/kafka/KEYS  
  : gpg --import KEYS  
  : wget http://mirrors.ocf.berkeley.edu/apache/kafka/2.2.0/kafka_2.12-2.2.0.tgz  
  : wget https://www-eu.apache.org/dist/kafka/2.2.0/kafka_2.12-2.2.0.tgz.asc  
  : gpg --verify kafka_2.12-2.2.0.tgz.asc kafka_2.12-2.2.0.tgz  
  [ Note: verify that signature is good before proceeding ]  
  : tar -xzf kafka_2.12-2.2.0.tgz  
  : ln -sfn kafka_2.12-2.2.0 kafka  
  : rm KEYS kafka_2.12-2.2.0.tgz kafka_2.12-2.2.0.tgz.asc  
17) Congfigure kafka as a three node cluser  
  : cd ~/kafka/config  
  : cp server.properties server.properties.orig  
  Use your favorite text editor to set the following properties to "server.properties" file  
  [ Note: set broker.id to 1 for node 1, set broker.id to 2 for node 2, ... ]  
  [ Note: replace x.x.x.x with the cooresponding IP addresses obtained in Step 5 ]  
  [ Note: replace y.y.y.y with the cooresponding IP address obtained in Step 6 ]  
      broker.id=1  
      advertised.listeners=PLAINTEXT://y.y.y.y:9092  
      zookeeper.connect=x.x.x.x:2181,x.x.x.x:2181,x.x.x.x:2181  
18) Start kafka   
   : cd ~/kafka  
   : sudo bin/kafka-server-start.sh -daemon config/server.properties
19) Repeat steps 16 through 18 for the other VM instances
