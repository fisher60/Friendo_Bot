from asyncio import sleep
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command
from bot import settings


def convert_time(time, period) -> int:
    """Converts the given time and period (i.e 10 minutes) to seconds"""

    result = None
    try:
        time = int(time)
        if "sec" in period:
            result = time
        elif "min" in period:
            result = time * 60
        elif "hour" in period:
            result = time * (60 ** 2)
    except ValueError:
        pass
    return result


class Utilities(Cog):
    """Simple, useful commands that offer some sort of service or benefit to users."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.index = 0
        self.drink_tasks = {}
        self.reminder_tasks = {}

    async def reminder_wrapper(
        self, time, period, ctx, msg="Reminder!", task_type="reminder", reason=None
    ):
        """Wrapper function for reminders to allow the task to be created on function call"""

        seconds = convert_time(time, period)

        if task_type == "drink":
            self.drink_tasks[ctx.author.id] += 1
        elif task_type == "reminder":
            self.reminder_tasks[ctx.author.id] += 1

        @tasks.loop(count=1)
        async def create_reminder():
            """sets a delay for the reminder to complete"""

            await sleep(seconds)

        @create_reminder.after_loop
        async def after_create_reminder():
            """
            After the delay is complete, this function will execute.
            Used for both regular reminders and the special 'drink' reminder\
            """

            completion_message = msg
            if task_type == "drink":
                self.drink_tasks[ctx.author.id] -= 1
            elif task_type == "reminder":
                completion_message = (
                    f"{ctx.author.mention}, Reminder for: {reason if reason else ''}"
                )
                self.reminder_tasks[ctx.author.id] -= 1
            await ctx.send(completion_message)

        if seconds:
            create_reminder.start()
        else:
            msg = "Please enter a valid time and period (i.e .reminder 5 minutes)"
            await ctx.send(msg)

    @command(brief="Returns Friendo's Version")
    async def version(self, ctx):
        msg = f"Version is {settings.VERSION}"
        await ctx.send(msg)
        return msg

    @command(brief="[number] [unit (seconds/minutes/hours)] [reason for reminder]")
    async def reminder(self, ctx, time, period="minutes", *, reason=None):
        """creates a reminder for the user"""

        if ctx.author.id not in self.reminder_tasks:
            self.reminder_tasks[ctx.author.id] = 0
        if self.reminder_tasks[ctx.author.id] < 1:
            await self.reminder_wrapper(
                ctx=ctx, time=time, period=period, task_type="reminder", reason=reason
            )
            if period in ["second", "seconds", "minute", "minutes", "hour", "hours"]:
                await ctx.send(
                    f"{ctx.author.mention} I will set a reminder for you in {time} {period}"
                )
        return

    @command(brief="Starts a 10 minute drink session to stay hydrated")
    async def drink(self, ctx):
        """Sets multiple reminders for a user to remind them to drink water and pace their drinking."""
        if ctx.author.id not in self.drink_tasks:
            self.drink_tasks[ctx.author.id] = 0
        if self.drink_tasks[ctx.author.id] < 1:
            await ctx.send(f"{ctx.author.mention} I got you, mate.")
            base_msg = f"OY! {ctx.author.mention} drink some water, mate."
            await self.reminder_wrapper(
                ctx=ctx,
                time=5,
                period="minutes",
                msg=base_msg,
                task_type="drink",
                reason="drinking",
            )
            await self.reminder_wrapper(
                ctx=ctx,
                time=10,
                period="minutes",
                msg=base_msg
                + "\n\nYou can run this command and have another if you'd like.",
                task_type="drink",
                reason="drinking",
            )
        else:
            msg = f"{ctx.author.mention} You are already drinking!"
            await ctx.send(msg)

    @command()
    async def ping(self, ctx):
        await ctx.send(f"Ping is {round(self.bot.latency * 1000)}ms")
        return self.bot.latency


def setup(bot: Bot) -> None:
    """Load the Utilities cog."""
    bot.add_cog(Utilities(bot))
