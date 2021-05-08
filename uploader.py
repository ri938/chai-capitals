import click
import os

from chai_py import Metadata, package, upload_and_deploy, wait_for_deployment
from chai_py.auth import set_auth
from chai_py.deployment import advertise_deployed_bot

import bot

# set authentication
DEVELOPER_UID = os.environ['CHAI_DEVELOPER_UID']
DEVELOPER_KEY = os.environ['CHAI_DEVELOPER_KEY']
set_auth(DEVELOPER_UID, DEVELOPER_KEY)


@click.group(chain=False)
def cli():
    pass


@cli.command()
def usa():
    url = 'https://images-ext-1.discordapp.net/external/aZyKNr7xHa3CpCgupuF8YuW' \
          'XtMLLpv7JDczx1SziPm8/https/blog.tcea.org/wp-content/uploads/2020/06/' \
          'eagle.jpg?width=999&height=666'

    upload_bot(
        name='American State Capitals',
        image_url=url,
        description='Guess the state capitals',
        bot=bot.USAStatesQuizBot,
        bot_uid=None
    )


@cli.command()
def europe():
    url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9G' \
          'cR9xNkNiQXRPTsTpa5wf69hTnem33QoGZRkaw&usqp=CAU'

    upload_bot(
        name='European Capitals',
        image_url=url,
        description='Guess the European capital cities',
        bot=bot.EuropeanCapitalsQuizBot,
        bot_uid=None
    )


@cli.command()
def world():
    url = 'https://upload.wikimedia.org/wikipedia/commons' \
          '/6/6f/Earth_Eastern_Hemisphere.jpg'

    upload_bot(
        name='World Capitals',
        image_url=url,
        description='Guess the world capital cities',
        bot=bot.WorldCapitalsQuizBot,
        bot_uid=None
    )


def upload_bot(name, image_url, description, bot, bot_uid):
    package(
        Metadata(
            name=name, image_url=image_url,
            color="f1a2b3",
            description=description,
            input_class=bot
        ),
        requirements=[
            'fuzzywuzzy'
        ]
    )
    uid = upload_and_deploy("_package.zip", bot_uid=bot_uid)
    wait_for_deployment(uid)
    bot_url = advertise_deployed_bot(uid)
    print('bot available at', bot_url)


if __name__ == '__main__':
    cli()
