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
