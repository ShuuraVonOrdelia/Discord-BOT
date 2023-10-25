from discord.ext import commands
import discord
import random
import urllib
import json
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 160100364987662336  # Change to your discord id
limit_message = 5
time_limit = 1
flood_control = False

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1,6))

@bot.event
async def on_message(message):
    global flood_control
    if message.content.lower() == 'salut tout le monde':
        await message.channel.send(f'Salut tout seul, {message.author.mention}')

    if flood_control and message.author != bot.user:
        user_messages = [msg for msg in bot.cached_messages if (message.created_at - msg.created_at).total_seconds() <= time_limit * 60 and not msg.content.startswith('!')]
        
        if len(user_messages) > limit_message:
            await message.channel.send(f'{message.author.mention}, flood detected :eyes:')

    await bot.process_commands(message)

@bot.command()
async def admin(ctx, member: discord.Member):
    admin_role = discord.utils.get(ctx.guild.roles, name='Admin')
    if admin_role is None:
        permissions = discord.Permissions(
            manage_channels=True,
            kick_members=True,
            ban_members=True
        )
        admin_role = await ctx.guild.create_role(name='Admin', permissions=permissions)

    await member.add_roles(admin_role)
    await ctx.send(f'{member.mention} is now an Admin')

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    if reason is None:
        funny_reasons = ['J\'ai glissé chef', 'Oh c\'est con ça', 'Vous savez, je ne pense pas qu\'il y ait de bonne ou mauvaise situation']
        reason = random.choice(funny_reasons)
    await ctx.send(f'{member.mention} banned: {reason}')

@bot.command()
async def flood(ctx):
    global flood_control
    flood_control = not flood_control

    if flood_control:
        await ctx.send('Flood control activated.')
    else:
        await ctx.send('Flood control deactivated.')

@bot.command()
async def xkcd(ctx):
    response = urllib.request.urlopen('https://xkcd.com/info.0.json')
    data = json.load(response)
    max = data['num']
    get = json.load(urllib.request.urlopen(f'https://xkcd.com/{random.randint(1, max)}/info.0.json'))
    await ctx.send(get['img'])

@bot.command()
async def poll(ctx, *, question):
    poll = await ctx.send(f"@here {question}")
    await poll.add_reaction('👍')
    await poll.add_reaction('👎')
    timeout = 30
    await asyncio.sleep(30)
    poll = await ctx.channel.fetch_message(poll.id)
    thumbs_up = discord.utils.get(poll.reactions, emoji='👍')
    thumbs_down = discord.utils.get(poll.reactions, emoji='👎')
    if thumbs_up.count > thumbs_down.count:
        result = f'YES win!'
    elif thumbs_up.count < thumbs_down.count:
        result = f'No win!'
    else:
        result = f'It\'s a tie!'

    await ctx.send(f'Poll Result: {question}\n👍: {thumbs_up.count - 1}\n👎: {thumbs_down.count - 1}' + result)
    await poll.delete()

token = "<TOKEN>"
bot.run(token)  # Starts the bot