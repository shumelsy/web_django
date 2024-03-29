mv web_django/web ./
mv web_django/init.sh ./
rm -rf web_django

chmod +x init.sh
#chmod +x web/etc/hello.py
#ln -s /home/box/web/etc/hello.py /home/box/web/

sudo ln -s /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/test.conf
sudo unlink /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart

sudo /etc/init.d/mysql start
mysql -uroot -e "create database ask;"
mysql -uroot -e "create user box@'localhost' identified by 'au7emeer2GeeSee';"
mysql -uroot -e "grant all privileges on ask.* to box@'localhost';"
mysql -uroot -e "flush privileges;"

#sudo ln -s /home/box/web/etc/gunicorn.conf /etc/gunicorn.d/test
#sudo /etc/init.d/gunicorn restart
#sudo /etc/init.d/gunicorn stop
#cd /home/box/web/etc/
#sudo gunicorn -c gunicorn.conf hello:app &
#sudo gunicorn --bind='0.0.0.0:8080' hello:app &

#don't forget to change hello.py!

cd /home/box/web/ask/
sudo gunicorn --bind='0.0.0.0:8000' ask.wsgi:application &
#sudo gunicorn -c /home/box/web/etc/gunicorn_ask.conf ask.wsgi:application &

