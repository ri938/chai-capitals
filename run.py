import click

from chai_py import TRoom

import bot


@click.group(chain=False)
def cli():
    pass


@cli.command()
def usa():
    quizbot = bot.USAStatesQuizBot()
    t_room = TRoom([quizbot])
    t_room.chat()


@cli.command()
def europe():
    quizbot = bot.EuropeanCapitalsQuizBot()
    t_room = TRoom([quizbot])
    t_room.chat()


@cli.command()
def world():
    quizbot = bot.WorldCapitalsQuizBot()
    t_room = TRoom([quizbot])
    t_room.chat()


if __name__ == '__main__':
    cli()
