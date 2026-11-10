import discord
from discord.ext import commands
import os

# Nastavení intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Fialovo-černý styl (barva pro embedy: tmavě fialová)
EMBED_COLOR = discord.Color.from_rgb(111, 44, 145)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} je online a připraven pro Flow SMP!")
    await bot.change_presence(activity=discord.Game(name="Flow SMP | !help"))

# 1. Uvítací zprávy
@bot.event
async def on_member_join(member):
    for channel in member.guild.text_channels:
        if channel.name == "vitejte" or channel.name == "welcome":
            embed = discord.Embed(
                title="Vítej na Flow SMP!",
                description=f"Ahoj {member.mention}, vítej na našem serveru! Užij si hraní.",
                color=EMBED_COLOR
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            await channel.send(embed=embed)
            break

# 4. Jednoduchá automatická moderace (zakázaná slova)
BAD_WORDS = ["spatneslovo1", "spatneslovo2"] # Zde si můžeš doplnit vlastní slova

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    msg_lower = message.content.lower()
    for word in BAD_WORDS:
        if word in msg_lower:
            await message.delete()
            await message.channel.send(f"{message.author.mention} Toto slovo není na serveru povoleno!", delete_after=5)
            return

    await bot.process_commands(message)

# 6. Základní admin příkaz pro promazání zpráv
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    await ctx.channel.purge(limit=amount + 1)
    embed = discord.Embed(
        title="Promázáno",
        description=f"Úspěšně smazáno {amount} zpráv.",
        color=0x9b59b6 # případně tvoje barva
    )
    await ctx.send(embed=embed, delete_after=5)

# Spuštění bota pomocí tokenu z Discloudu
bot.run(os.getenv("TOKEN"))
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

class VerificationView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Ověřit se / Verify", style=discord.ButtonStyle.green, custom_id="verify_button")
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Tady si můžeš doplnit název role, kterou uživatel dostane (např. "Hráč" nebo "Member")
        role = discord.utils.get(interaction.guild.roles, name="Verifed")
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Úspěšně jsi se ověřil/a!", ephemeral=True)
        else:
            await interaction.response.send_message("Role 'Hráč' neexistuje na tomto serveru.", ephemeral=True)

@bot.event
async def on_ready():
    bot.add_view(VerificationView())
    print(f"Bot {bot.user} je připraven!")

@bot.command()
@commands.has_permissions(administrator=True)
async def verify(ctx):
    view = VerificationView()
    await ctx.send("Kliknutím na tlačítko níže potvrdíš, že nejsi bot:", view=view)

# Sem doplň svůj token nebo nechej načítání z Railway variables
import os
bot.run(os.getenv("TOKEN"))
