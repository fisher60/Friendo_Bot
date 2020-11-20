from . import settings
from bot.bot import Friendo

if __name__ == "__main__":
    bot = Friendo(command_prefix=settings.COMMAND_PREFIX, help_command=None)

    # load help command
    bot.load_extension("bot.cogs.help")

    # load in basic commands
    bot.load_extension("bot.cogs.greetings")
    bot.load_extension("bot.cogs.utilities")
    bot.load_extension("bot.cogs.source")

    # load in image segmentation commands
    bot.load_extension("bot.cogs.image_segmentation")

    # load in Meme commands
    bot.load_extension("bot.cogs.memes")

    # load in Admin commands
    bot.load_extension("bot.cogs.admin")

    # load in Fun commands
    bot.load_extension("bot.cogs.fun")

    # load in randomcase command
    bot.load_extension("bot.cogs.randomcase")

    # load in Event command
    bot.load_extension("bot.cogs.events")

    # load in Todo List command
    bot.load_extension("bot.cogs.todo_list")

    # load in wolfram command
    bot.load_extension("bot.cogs.wolfram")

    # load covid stats
    bot.load_extension("bot.cogs.covid_stats")

    # load music cogs
    bot.load_extension("bot.cogs.last_fm")

    # load wonder twins cog
    bot.load_extension("bot.cogs.wonder_twins")

    # loads the weather cog
    bot.load_extension("bot.cogs.weather")
    
    # loads the animals cog
    bot.load_extension("bot.cogs.animals")

    bot.run(settings.TOKEN)
