import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix=',', intents=intents)

load_dotenv()

Discord_token = os.getenv("discord_token")

# Canais com comandos personalizados. Se for testar em seu servidor, troque os id (os números dos canais)
canal_bemvindo = 1341553085474148362
mensagem_bemvindos_ID = 1345093888150605854

# Cargos
orfao = 1345121188417900697
filhos = 1341551322549456917

@bot.event
async def on_ready():
    global staff_novosmembros
    staff_novosmembros = bot.get_channel(1341552178418155550)
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.event
async def on_member_join(member):
    orfao_role = member.guild.get_role(orfao)
    await member.add_roles(orfao_role)
    print(f"O cargo 'orfao' foi adicionado ao membro {member.name}.")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == mensagem_bemvindos_ID:
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        
        if member is None:
            return

        if any(role.id == orfao for role in member.roles):
            button = Memberbutton(member)
            view = View()
            view.add_item(button)
            message = await staff_novosmembros.send(f"O membro {member.name}, quer entrar no server.", view=view)
            button.message = message
        else:
            print(f'Canal staff_novos_membros não encontrado ou o cargo não está com este membro')

class Memberbutton(Button):
    def __init__(self, member):
        super().__init__(label="Incorporar usuário", style=discord.ButtonStyle.primary)
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        orfao_role = guild.get_role(orfao)
        novo_cargo = guild.get_role(filhos)
        
        if orfao_role in self.member.roles:
            await self.member.remove_roles(orfao_role)
            await self.member.add_roles(novo_cargo)
        if self.message:
            await self.message.edit(content=f"O usuário {self.member.name} foi incorporado.", view=None)

bot.run(Discord_token)
