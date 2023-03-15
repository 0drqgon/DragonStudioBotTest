import discord
from discord.utils import get
from discord.ext import commands

TOKEN = 'lkajhgfjahstjhtasonkaohsj'
GUILD = '1085193543905181737'
EMOJI_BELL = '🔔'
EMOJI_GIVEAWAY = '🎉'
ROLE_BELL_ID = 1085193543905181740
ROLE_GIVEAWAY_ID = 1085193543905181739


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(intents=intents, command_prefix="!")


@client.event
async def on_ready():
    guild = get(client.guilds, name=GUILD)
    print(f'{client.user} has connected to Discord!')


# Category
category_id = 1085193544362364995

# message in the ticket creation embed
ticket_message = "Click the button below to create a new ticket."

# emoji for the ticket button
ticket_emoji = '🎫'

# color of the ticket creation embed
ticket_color = discord.Color.blue()

# the role that will be able to view the ticket channels
support_role_id = 1085193543926173706

# the function that will create the ticket channel
async def create_ticket_channel(guild, member):
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True),
        member: discord.PermissionOverwrite(read_messages=True),
        guild.get_role(support_role_id): discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(f'ticket-{member.display_name}', overwrites=overwrites, category=guild.get_channel(category_id))
    return channel

# the function that will create the ticket creation embed
def create_ticket_embed():
    embed = discord.Embed(title="Support Ticket", description=ticket_message, color=ticket_color)
    return embed

# the function that will handle the ticket button click
async def handle_ticket_button(interaction):
    member = interaction.author
    guild = interaction.guild
    channel = await create_ticket_channel(guild, member)
    await interaction.message.delete()
    await member.send(f"Your ticket has been created in {channel.mention}.")

# the function that will add the ticket button to the ticket creation embed
async def add_ticket_button(embed):
    button = discord.Button(label="Create Ticket", emoji=ticket_emoji, style=discord.ButtonStyle.blurple)
    button.callback = handle_ticket_button
    embed.set_footer(text="Click the button below to create a new ticket.")
    embed.add_field(name="Instructions", value=f"Click the {ticket_emoji} button to create a new ticket.")
    return embed

# the command that will send the ticket creation embed
@client.command()
async def ticket(ctx):
    embed = create_ticket_embed()
    embed = await add_ticket_button(embed)
    message = await ctx.send(embed=embed)

# Reaction Role function
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