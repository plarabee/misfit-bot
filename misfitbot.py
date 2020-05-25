"""MisfitBot

This program is a Discord chat bot designed for entertainment
of the authors friends & family discord channel. In addition
to consuming the Discord API via the discord.py module, it 
also consumes several other APIs to provide features with
regular old requests.

Example usage:

    git clone https://github.com/plarabee/misfit-bot.git
    cd misfit-bot
    echo "BOT_CLIENT_KEY=VERY_SECRET_KEY" > .env
    echo "BLIZZARD_CLIENT_ID=VERY_SECRET_ID" >> .env
    echo "BLIZZARD_CLIENT_SECRET=ANOTHER_SECRET" >> .env
    docker build -t misfit-bot:1.1 .
    docker container run --detach --name bot misfit-bot:1.q
    
"""
import os
import json
import random

import discord
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from card import *
from deck import *
from poker import *

# Global Variable Definitions
RAIDBOTS_URL = 'https://www.raidbots.com/simbot'
MYTHIC_RANKINGS_URL = 'https://raider.io/mythic-plus-rankings/season-bfa-3/all/world/leaderboards-strict'
BLIZZ_OAUTH_URL = 'https://us.battle.net/oauth/token'
HS_SEARCH_URL = 'https://us.api.blizzard.com/hearthstone/cards?locale=en_US&textFilter='

# Disable unverified HTTPS request warnings from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_args(message):
    """
    Helper function to get arguments from a user's
    message. It takes in a message and returns
    a string containing the message following a
    command.
  """
    return message.split()[1]


def guide(spec):
    """
    Takes in a string, spec, that represents the class and specialization.
    Returns a string that represents the entire url of the class guide
  """
    iv_url_head = 'https://www.icy-veins.com/wow/'
    iv_url_tail = '-pve-dps-guide'
    return spec + ': ' + iv_url_head + spec + iv_url_tail + '\n'


def roll():
    """
    Returns a string with a random number between 1 and 100.
  """
    limit = 100
    return str(random.randint(1, limit))


def dadjoke():
    """
    Uses the icanhazdadjokes API to display a random dad jokes
  """
    url = 'https://icanhazdadjoke.com/'
    headers = {
        'User-Agent': 'Simple Discord Bot (https://github.com/plarabee)',
        'Accept': 'text/plain'
    }
    response = requests.get(url, headers=headers)
    return response.text


def insult():
    """
    Uses the insult api at https://insult.mattbas.org/api/ to return
    a string containing an insult. NSFW.
  """
    url = 'https://insult.mattbas.org/api/insult'
    headers = {
        'User-Agent': 'Simple Discord Bot (https://github.com/plarabee)',
        'Accept': 'text/plain'
    }
    response = requests.get(url, headers=headers)
    return response.text


def chucknorris():
    """
    Uses the icndb API to return a random joke
  """
    url = 'http://api.icndb.com/jokes/random'
    headers = {
        'User-Agent': 'Simple Discord Bot (https://github.com/plarabee)',
        'Accept': 'text/json'
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    return data['value']['joke']


def get_blizzard_auth(client_id, secret):
    """
    Makes a post request to Blizzard OAuth2 with
    basic HTTP auth and returns a bearer token
    for use in future API calls.
  """
    response = requests.post(BLIZZ_OAUTH_URL,
                             verify=False,
                             auth=HTTPBasicAuth(client_id, secret),
                             data={'grant_type': 'client_credentials'})

    data = json.loads(response.text)

    return data['access_token']


def get_hs_cards(token, search_term):
    """
    Makes an API call to the official Hearthstone API.
    Requires a OAuth2 Bearer token and a search_term.
    Returns result in raw JSON.
  """
    auth = 'Bearer ' + token

    headers = {'Authorization': auth}
    response = requests.get(HS_SEARCH_URL + search_term, headers=headers)

    return json.loads(response.text)

def random_card():
    """
    Creates a new deck object, shuffles it, and prints
    the rank/suit of the card. Used like roll for random
    contests
  """
    deck = Deck()
    deck.shuffle()
    card = deck.draw()
    return card.rank, card.suit

def poker_hand():
    """
    Creates a new deck object, shuffles it, and returns
    an array of five card objects.
  """
    hand = []
    deck = Deck()
    deck.shuffle()

    for i in range(0, 5):
        hand.append(deck.draw())

    ranking, is_high_card = rank_hand(hand)    
    return hand, ranking, is_high_card 


def main():
    """
    Main function. Initializes the bot and declares all of its commands and functions
  """
    # get secrets from .env
    load_dotenv()
    bot_client_key = os.getenv('BOT_CLIENT_KEY')
    blizz_client_id = os.getenv('BLIZZARD_CLIENT_ID')
    blizz_secret = os.getenv('BLIZZARD_CLIENT_SECRET')

    # initialize discord client
    client = discord.Client()

    # provides console feedback that client is logged in
    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client:  # prevent bot from replying to itself
            return

        if message.content.startswith('!help'):  # !help
            await message.channel.send(
                " Bot Commands: \n"
                "# !help - this dialog\n"
                "# !roll - rolls a random number 1 - 100\n"
                "# !chucknorris - tells a random Chuck Norris joke\n"
                "# !dadjoke - tells a random Dad Joke\n"
                "# !mythic+ - links the mythic+ leaderboard\n"
                "# !raidbots - links raidbots, site to sim your gear\n"
                "# !{CLASS} - displays icyveins guide for all specs of that class\n"
                "# !hearthstone {NAME} - displays data about matching HS cards\n"
            )

        if message.content.startswith('!classic'):  # !classic
            await message.channel.send('No one cares about Classic.')

        if 'good bot' in message.content:  # good bot
            await message.channel.send(
                'https://tenor.com/view/thumbs-up-robot-good-gif-15533559')

        if 'bad bot' in message.content:  # bad bot
            await message.channel.send(
                'https://tenor.com/view/sad-r2d2-robot-beep-star-wars-gif-5812746'
            )

        if message.content.startswith('!roll'):  # !roll
            roll_result = roll()
            await message.channel.send(
                f'{ message.author.name } rolls a { roll_result }')

        if message.content.startswith('!chucknorris'):  # !chucknorris
            chucknorris_result = chucknorris()
            await message.channel.send(chucknorris_result)

        if message.content.startswith('!dadjoke'):  # !dadjoke
            dadjoke_result = dadjoke()
            await message.channel.send(dadjoke_result)

        if message.content.startswith('!insult'):  # !insult
            insult_result = insult()
            await message.channel.send(insult_result)

        if message.content.startswith('!mythic+'):  # !mythic+
            await message.channel.send('Mythic + Rankings Here: ' +
                                       MYTHIC_RANKINGS_URL)

        if message.content.startswith('!raidbots'):  # !raidbots
            await message.channel.send('Sim your gear here: ' + RAIDBOTS_URL)

        # Class guides begin here.

        if message.content.startswith('!deathknight'):  # !deathknight
            await message.channel.send(
                guide('blood-death-knight') + guide('frost-death-knight') +
                guide('unholy-death-knight'))

        if message.content.startswith('!demonhunter'):  # !demonhunter
            await message.channel.send(
                guide('havoc-demon-hunter') + guide('vengeance-demon-hunter'))

        if message.content.startswith('!druid'):  # !druid
            await message.channel.send(
                guide('balance-druid') + guide('feral-druid') +
                guide('guardian-druid') + guide('restoration-druid'))

        if message.content.startswith('!hunter'):  # !hunter
            await message.channel.send(
                guide('beast-mastery-hunter') + guide('marksmanship-hunter') +
                guide('survival-hunter'))

        if message.content.startswith('!mage'):  # !mage
            await message.channel.send(
                guide('arcane-mage') + guide('fire-mage') +
                guide('frost-mage'))

        if message.content.startswith('!monk'):  # !monk
            await message.channel.send(
                guide('brewmaster-monk') + guide('mistweaver-monk') +
                guide('windwalker-monk'))

        if message.content.startswith('!paladin'):  # !paladin
            await message.channel.send(
                guide('holy-paladin') + guide('protection-paladin') +
                guide('retribution-paladin'))

        if message.content.startswith('!priest'):  # !priest
            await message.channel.send(
                guide('discipline-priest') + guide('holy-priest') +
                guide('shadow-priest'))

        if message.content.startswith('!rogue'):  # !rogue
            await message.channel.send(
                guide('assassination-rogue') + guide('outlaw-rogue') +
                guide('subtlety-rogue'))

        if message.content.startswith('!shaman'):  # !shaman
            await message.channel.send(
                guide('elemental-shaman') + guide('enhancement-shaman') +
                guide('restoration-shaman'))

        if message.content.startswith('!warlock'):  # !warlock
            await message.channel.send(
                guide('affliction-warlock') + guide('demonology-warlock') +
                guide('destruction-warlock'))

        if message.content.startswith('!warrior'):  # !warrior
            await message.channel.send(
                guide('arms-warrior') + guide('fury-warrior') +
                guide('protection-warrior'))
        
        if message.content.startswith('!draw'):
            rank, suit = random_card()
            await message.channel.send(f'{message.author.name} drew a {rank} of {suit}')
        
        if message.content.startswith('!poker'):
            hand, ranking, is_high_card  = poker_hand()
            resp = f'{message.author.name} draws a poker hand:\n\n'

            for card in hand:
                resp += f'{card.rank} of {card.suit}\n'

            if is_high_card:
                resp += f'\nHigh Card of {ranking}'
            else:
                resp += f'\n{ranking}'

            await message.channel.send(resp)


        if message.content.startswith('!hearthstone'):  # !hearthstone

            # make api call
            token = get_blizzard_auth(blizz_client_id, blizz_secret)
            search_term = get_args(message.content)
            cards = get_hs_cards(token, search_term)

            # check to make sure we don't have too many results
            if len(cards['cards']) > 8:
                await message.channel.send(
                    'Woah there! Too many results. Try a more specific search.'
                )

            else:

                bot_message = '#############################################\n'

                # print the cards
                for i in range(0, len(cards['cards'])):

                    # skip if the search term doesn't match part of name
                    if search_term.lower() in cards['cards'][i]['name'].lower(
                    ):

                        bot_message += 'Name: ' + cards['cards'][i][
                            'name'] + '\n'

                        if 'manaCost' in cards['cards'][i]:
                            bot_message += 'Mana: ' + str(
                                cards['cards'][i]['manaCost']) + '\n'

                        if 'attack' in cards['cards'][i]:
                            bot_message += 'ATK: ' + str(
                                cards['cards'][i]['attack']) + '\n'

                        if 'health' in cards['cards'][i]:
                            bot_message += 'HP: ' + str(
                                cards['cards'][i]['health']) + '\n'

                        bot_message += 'Text: ' + cards['cards'][i][
                            'text'] + '\n'

                        bot_message += '######################################################\n'

                await message.channel.send(bot_message)


    client.run(bot_client_key)


main()
