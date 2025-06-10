#__________________Alzak bot V2.0__________________#

import discord
from discord.ext import commands
import asyncio
import datetime

#variables
x=datetime.datetime.now()
intents = discord.Intents.default()
intents.message_content = True  
intents.members = True  
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot pripojený ako {bot.user}')
    
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    #ak user napise na zaciatok alzak zacne pocuvat
    if message.content.lower().startswith("!alzak"):
        guild = message.guild

        #ak user nevyberie koho mutnuť 
        if not message.mentions:
            await message.channel.send("Prosím, označ používateľa, ktorého chceš mutnúť. Príklad: `!alzak @meno`")
            return

        member_to_mute = message.mentions[0]
        member_muter=message.author.name


        category = discord.utils.get(guild.categories, name="Trading")
        channel = None
        if category:
            channel = discord.utils.get(category.text_channels, name="trading")

        mute_role = discord.utils.get(guild.roles, name="Muted")
        if not mute_role:
            try:
                mute_role = await guild.create_role(name="Muted")
                for ch in guild.channels:
                    await ch.set_permissions(mute_role, send_messages=False)
            except discord.Forbidden:
                await message.channel.send("Bot nemá oprávnenie vytvoriť rolu 'Muted'.")
                return

        # Pridanie role + zakázanie písania
        await member_to_mute.add_roles(mute_role)
        await channel.set_permissions(member_to_mute, send_messages=False)
        await message.channel.send(f'{member_to_mute.mention} bol mutnutý.')
        print(f'Bol mutnutý používateľ: {member_to_mute.name}')
        with open("AlzakBot.log","a") as f:
            f.write( "\n" +str(x.strftime("%Y-%m-%d %H:%M:%S")) + " Muted -> by: " +  str(member_muter)   + " -> who: " + str(member_to_mute.name))
        

        await asyncio.sleep(300)

        y=datetime.datetime.now()
        await member_to_mute.remove_roles(mute_role)
        await channel.set_permissions(member_to_mute, send_messages=True)
        await message.channel.send(f'{member_to_mute.mention} bol odmutnutý.')
        print(f'Bol odmutnutý používateľ: {member_to_mute.name}')
        with open("AlzakBot.log","a") as f:
            f.write("\n" +str(y.strftime("%Y-%m-%d %H:%M:%S")) +" unmuted -> who: " + str(member_to_mute.name))


bot.run('')