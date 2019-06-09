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
3.2) sudo chown -R your_username:your_username /data  
3.3) touch /data/zookeeper/myid  
3.4) echo '1' >> /data/zookeeper/myid  
3.5) cd ~/zookeeper/conf   
3.6) cp zoo_sample.cfg zoo.cfg   
3.7) Use your favorite text editor to set the following properties to "zoo.cfg" file  
[ Note: replace x.x.x.x with the cooresponding IP addresses obtained in Step 5 ]  
dataDir=/data/zookeeper  
server.1=x.x.x.x:2888:3888  
4) Next step
