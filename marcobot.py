import os
import discord
from discord.ext import commands
from discord import app_commands

# Configuration des identifiants (staff et animateurs)
STAFF_IDS = [123456789012345678]  # Remplace par les vrais IDs du staff
ANIMATEURS_IDS = [987654321098765432]  # Remplace par les vrais IDs des animateurs

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

class QuizView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Vue persistante

    @discord.ui.button(label="Répondre A", style=discord.ButtonStyle.primary, custom_id="quiz_btn_a")
    async def btn_a(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Logique de la bonne réponse
        await interaction.response.send_message("Bonne réponse ! Notification envoyée au staff.", ephemeral=True)
        
        # Notification DM staff / animateurs
        destinataires = set(STAFF_IDS + ANIMATEURS_IDS)
        for user_id in destinataires:
            try:
                user = await client.fetch_user(user_id)
                if user:
                    await user.send(f"Le quiz a été réussi par {interaction.user.name} !")
            except Exception:
                pass

@client.event
async def on_ready():
    # Enregistrement de la vue persistante au démarrage
    client.add_view(QuizView())
    print(f"Connecté en tant que {client.user} (ID: {client.user.id})")

@client.tree.command(name="quiz", description="Lance un quiz permanent")
async def quiz(interaction: discord.Interaction):
    view = QuizView()
    await interaction.response.send_message("Question du quiz : Choisissez une option !", view=view)

@quiz.error
async def quiz_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.errors.MissingPermissions):
        await interaction.response.send_message("❌ Tu n'as pas les permissions d'administrateur pour utiliser cette commande.", ephemeral=True)

# Lancement sécurisé du bot via la variable d'environnement
client.run(os.getenv("DISCORD_TOKEN"))