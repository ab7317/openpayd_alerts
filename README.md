# openpayd_alerts

# Server Setup 
- *https://github.com/ab7317/kraken_deposit_alerts*
- Is a link to the main script that is running on the server
- That script and this one are both on the same server
- Please follow that guide to build and maintain the serveR
- The link above will cover everything up till setup
  
  # Server specs
  - Here I will breifly outline what the specifications for the server are
  - **AWS EC2 Instance**
  - **Ubuntu AMI**

# Setup
- This section will cover setting up the code on the server
- This will use a different method from the other repo. Both methods are interchangeable
- In this method we will manually setup the code on the server
- This section assumes you have ssh access to your server
- First make sure you are in the corect directory
```
cd ~
```
```
mkdir openpayd_alerts
```
```
cd openpayd_alerts
```
```
mkdir config
```
```
sudo nano config/confi.py
```
- This will setup your main directory in the home. It will thenmove into the directory and create another directory inside called **config** the same as in the 
