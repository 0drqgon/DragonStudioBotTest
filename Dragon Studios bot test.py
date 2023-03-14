import discord
from discord.utils import get
from discord.ext import commands

TOKEN = 'MTA4NTE3ODc2MDk5MjY1MzM4NA.GPpG5l.A5K0sdyEDdsOqYYezgA1kGfE595P0zQFP4Hm4I'
GUILD = '1085193543905181737'
EMOJI_BELL = '🔔'
EMOJI_GIVEAWAY = '🎉'
ROLE_BELL_ID = 1085193543905181740
ROLE_GIVEAWAY_ID = 1085193543905181739
TICKET_CATEGORY_NAME = "Support"  # Name of the ticket category
TICKET_EMOJIS = ["🎫", "🆘"]
TICKET_CHANNELS = []

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(intents=intents, command_prefix="!")


# Ticket system functionality
@client.event
async def on_raw_reaction_add(payload):
    if str(payload.emoji) in TICKET_EMOJIS:
        channel = client.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await client.fetch_user(payload.user_id)
        if str(payload.emoji) == "🎫":
            category = discord.utils.get(channel.guild.categories, name=TICKET_CATEGORY_NAME)
            if not category:
                category = await channel.guild.create_category(TICKET_CATEGORY_NAME)
            ticket_name = f"{user.name}-ticket"
            ticket_channel = await category.create_text_channel(name=ticket_name)
            TICKET_CHANNELS.append(ticket_channel)
            await ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
            await message.remove_reaction(payload.emoji, user)
            ticket_embed = discord.Embed(
                title=f"Ticket for {user.name}", description="Please state your issue.", color=0x00ff00
            )
            await ticket_channel.send(embed=ticket_embed)
        elif str(payload.emoji) == "🆘":
            category = discord.utils.get(channel.guild.categories, name=TICKET_CATEGORY_NAME)
            if category:
                for channel in category.channels:
                    if channel.name.startswith(user.name):
                        await channel.delete()
                        TICKET_CHANNELS.remove(channel)

@client.event
async def on_raw_reaction_remove(payload):
    pass

# Command to start a new ticket channel with a button
@client.command()
async def newticket(ctx):
    if ctx.message.content == "!newticket":
        category = discord.utils.get(ctx.guild.categories, name=TICKET_CATEGORY_NAME)
        if not category:
            category = await ctx.guild.create_category(TICKET_CATEGORY_NAME)

        ticket_name = f"{ctx.author.name}-ticket"
        ticket_channel = await category.create_text_channel(name=ticket_name)
        TICKET_CHANNELS.append(ticket_channel)
        await ticket_channel.set_permissions(ctx.author, read_messages=True, send_messages=True)

        ticket_embed = discord.Embed(title=f"Ticket for {ctx.author.name}", description="Please state your issue.", color=0x00ff00)
        message = await ctx.send(
        "Click the button below to start a new ticket channel.",
        components=[
            [discord.ui.Button(style=discord.ButtonStyle.green, label="Open ticket", custom_id="new_ticket")]
        ]
    )

    while True:
        interaction = await client.wait_for("button_click")
        if interaction.custom_id == "new_ticket":
            await message.delete()
            await interaction.respond(type=6)
            await ticket_channel.send(embed=ticket_embed)
            break

#Ping system functionality
@client.event
async def on_ready():
    guild = get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == EMOJI_BELL:
        guild = client.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_BELL_ID)
        await payload.member.add_roles(role)
    elif payload.emoji.name == EMOJI_GIVEAWAY:
        guild = client.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_GIVEAWAY_ID)
        await payload.member.add_roles(role)
@client.event
async def on_raw_reaction_remove(payload):
    if payload.emoji.name == EMOJI_BELL:
        guild = client.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_BELL_ID)
        member = await guild.fetch_member(payload.user_id)
        if role.id in [_role.id for _role in member.roles]:
            await member.remove_roles(role)
    elif payload.emoji.name == EMOJI_GIVEAWAY:
        guild = client.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_GIVEAWAY_ID)
        member = await guild.fetch_member(payload.user_id)
        if role.id in [_role.id for _role in member.roles]:
            await member.remove_roles(role)


@client.command()
async def generate(ctx):
    if ctx.message.content == "!generate":
        embed = discord.Embed()
        embed.colour = discord.Colour(0xE2340F)
        embed.description = "To get roles related to different pings in this discord, check the emoji related to the role!\n" \
                            "\n" \
                            "\n" \
                            "Announcements: :bell:\n" \
                            "\n" \
                            "Giveaways: :tada:"
        message = await ctx.send(embed=embed)
        await message.add_reaction(EMOJI_BELL)
        await message.add_reaction(EMOJI_GIVEAWAY)


client.run(token=TOKEN)