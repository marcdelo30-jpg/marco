import os
import random
import discord
from discord import app_commands
from discord.ext import commands

# Configuration des intents (nécessaire pour lire les messages et gérer le bot)
intents = discord.Intents.default()
intents.message_content = True


class Marcobot(commands.Bot):

  def __init__(self):
    super().__init__(command_prefix="!", intents=intents)

  


bot = Marcobot()


@bot.event
async def on_ready():
  print(f"🤖 {bot.user} est connecté et prêt 24/7 !")

async def setup_hook(self):
      # Remplace TON_ID_DE_SERVEUR par l'ID de ton serveur Discord (ex: 123456789012345678)
      GUILD_ID = discord.Object(id=1359606058922017001)
      self.tree.copy_global_to(guild=GUILD_ID)
      await self.tree.sync(guild=GUILD_ID)
      print("Commandes slash synchronisées instantanément sur le serveur !")

# ---------------------------------------------------------
# 1. SECTION QUIZ (Commande classique !quiz)
# ---------------------------------------------------------
QUIZ_QUESTIONS = [
    {
        "question": "Quelle est la capitale de la France ?",
        "reponse": "paris",
    },
    {
        "question": "Combien font 5 x 6 ?",
        "reponse": "30",
    },
    {
        "question": "Quel est l'océan le plus grand du monde ?",
        "reponse": "pacifique",
    },
]


@bot.command(name="quiz")
async def quiz(ctx):
  """Pose une question de quiz aléatoire."""
  q = random.choice(QUIZ_QUESTIONS)
  await ctx.send(f"❓ **Quiz :** {q['question']}")

  def check(m):
    return m.channel == ctx.channel and not m.author.bot

  try:
    msg = await bot.wait_for("message", check=check, timeout=30.0)
    if msg.content.strip().lower() == q["reponse"]:
      await ctx.send(
          f"🎉 Bravo {msg.author.mention} ! C'est la bonne réponse !"
      )
    else:
      await ctx.send(
          f"❌ Dommage ! La bonne réponse était : **{q['reponse']}**."
      )
  except TimeoutError:
    await ctx.send(
        f"⏰ Temps écoulé ! La réponse était : **{q['reponse']}**."
    )


# ---------------------------------------------------------
# 2. SECTION QUÊTES (Commande slash /quete)
# ---------------------------------------------------------
QUETES = [
    {
        "titre": "Chasse aux gobelins",
        "recompense": "100 pièces d'or",
        "xp": 50,
    },
    {
        "titre": "Récupérer l'épée perdue dans la caverne",
        "recompense": "250 pièces d'or",
        "xp": 120,
    },
    {
        "titre": "Explorer la forêt maudite",
        "recompense": "150 pièces d'or",
        "xp": 80,
    },
    {
        "titre": "Livrer la potion au mage",
        "recompense": "75 pièces d'or",
        "xp": 40,
    },
]


@bot.tree.command(
    name="quete",
    description="Accepte une quête aléatoire pour gagner de l'or et de l'XP !",
)
async def quete(interaction: discord.Interaction):
  q = random.choice(QUETES)

  embed = discord.Embed(
      title=f"📜 Quête acceptée : {q['titre']}",
      description=(
          f"Bonne chance, **{interaction.user.display_name}** ! Tu t'es lancé"
          " dans cette aventure."
      ),
      color=discord.Color.blurple(),
  )
  embed.add_field(name="💰 Récompense", value=q["recompense"], inline=True)
  embed.add_field(name="✨ Expérience", value=f"{q['xp']} XP", inline=True)
  embed.set_footer(
      text="Tape /quete à nouveau pour tenter une autre aventure !"
  )

  await interaction.response.send_message(embed=embed)


# Lancement du bot via le token sécurisé sur Railway
bot.run(os.environ["DISCORD_TOKEN"])
