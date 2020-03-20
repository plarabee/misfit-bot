# misfit-bot

A basic gamer discord bot written in
python.

## Requirements
+ git
+ docker (or podman)
+ a discord bot key
+ a blizzard client id and app secret

## Usage
```
git clone https://github.com/plarabee/misfit-bot.git
cd misfit-bot
echo "BOT_CLIENT_KEY=VERY_SECRET_KEY" > .env
echo "BLIZZARD_CLIENT_ID=VERY_SECRET_ID" >> .env
echo "BLIZZARD_CLIENT_SECRET=ANOTHER_SECRET" >> .env
docker build -t misfit-bot:1.1 .
docker container run --detach --name bot misfit-bot:1.1
```