cd ../

git pull

sudo docker rm $(sudo docker ps -aq)

echo "> Build Docker Image"
sudo docker build -t comfortchat .

echo "> Run Docker Container"
sudo docker run --name api -p 80:80 comfortchat