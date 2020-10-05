# This is my production project, whose has written with Python3, PyQT5 and MySQL
This is instruction for UNIX-systems. I'm sure, that's work on Debian and Ubuntu. You can try GIT BASH for Windows. 

First of all you need to clone project to local computer. 
```git   
git clone https://github.com/S0GGeR/DesktopWishList 
```    
The next step is initialize the virtual enviroment. I recomend you to use Python 3.8.2
```ssh   
python -m venv venv
```      

Activate your venv:
```ssh   
source venv/bin/activate
```      

After this, you need to install all requirments. The command is:    
```python3    
python manage.py -r req.txt
```    

If everything is okay, we need to set up our MySQL:
```ssh 
sudo apt-get install -y mysql-server                                   #installing MySQL server 
sudo mysql -u root                                                     #openning the database control panel    
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';           #creating some user with some password.  
\q                                                                     #exiting control panel
```   
Open the main.py file and enter your host(127.0.0.1), username and password, which you entered when creating the database. Now everything should work
