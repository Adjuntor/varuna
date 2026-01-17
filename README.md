# How to run
```
git clone https://github.com/Adjuntor/varuna.git
cd shiva
pip install --no-cache-dir -r requirements.txt
```
Edit with the correct values the config file.
Run the bot.
```
python3 main.py
```

# Docker Image
Requires docker to be installed.
```
git clone https://github.com/Adjuntor/varuna.git
cd varuna
```
Edit with the correct values the config file.
```
docker build -t varuna .
docker run -d --name=varuna -v <volume-name>:/usr/src/app/config --restart=always varuna
```

# Docker Compose
Requires docker and docker compose to be installed.
Edit the Volume location on the compose.
```
git clone https://github.com/Adjuntor/varuna.git
cd varuna
```
Edit with the correct values the config file.
```
docker-compose up -d
```

# Delete Docker Container
```
docker stop varuna
docker rm varuna
```

# Updating
To update the bot use the command below.
```
git pull
```
