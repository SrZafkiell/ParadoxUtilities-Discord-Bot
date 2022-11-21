#Special thanks file
***
In the making of this discord bot project from scratch without having previous python experience, the following
sites were key to help me reach my goal.

Documentation used: 
[Discord](https://discord.com/developers/docs/intro),
[Twitch](https://dev.twitch.tv/docs/api/),
[Discord.py](https://discordpy.readthedocs.io/en/stable/),
[](),
[](),
[]()

~~If im stealing someone's code, at least i will try to understand it first and learn from it~~ o.O

***

1. Having Runtime Warning with extension loading [splunktool.com](https://splunktool.com/runtimewarning-coroutine-botbaseloadextension-was-never-awaited-after-updating-discordpy)

**Cogs file side**
~~~python
async def setup(bot):
   await bot.add_cog(YourCog(bot))
~~~
**Client side (Bot side for me -> main.py)**
~~~python
async def load_extensions():
    for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        # cut off the.py from the file name
        await client.load_extension(f "cogs.{filename[:-3]}")
~~~
In their page it was bad formatted but very understandable. Thanks a lot.

2. Understanding a little more about slash commands
* [sanamo (YouTube)](https://youtu.be/1geg9VTKhDE) This video made me understand a little more about the documentation of discord.py (Not enough yet :C)
* [cmoorelabs (YouTube)](https://youtu.be/1EW-oSga5k4) Made me want to learn more about the post made by [AbstractUmbra](https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f) about slash commands.

With this information i wasn't able to make a very professional slash command implementation but got me started in it. I will try to improve the more i dive into making discord bots. **Thanks a lot for your resources for people like me**

3. 

***