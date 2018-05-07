import asyncio
import os
from datetime import datetime,time
import operator
import calendar

import random
import discord
from discord.ext import commands

from __main__ import send_cmd_help
from cogs.utils import checks

from .utils.dataIO import dataIO

from time import time
from math import floor
from random import randint

class fleur:
    """Des PATATES"""

    def __init__(self, bot):
        self.bot = bot
        self.settings_path = "data/patate/patate.json"
        self.flower = dataIO.load_json(self.settings_path)

    async def save_flower(self):
        dataIO.save_json(self.settings_path, self.flower)

    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def Pajouter(self,ctx, nombre, *, user: discord.Member=None):
        message = ctx.message

        if not user:
            await self.bot.say("Il faut préciser l'utilisateur")
            return
        if not nombre:
            await self.bot.say("Il faut préciser le nombre")
            return
        else:
            try: 
                int(''.join(nombre))
            except:
                await self.bot.say("Tu sais ce que c'est un nombre?")
                return
        if user.id not in self.flower[message.server.id]:
            self.flower[message.server.id][user.id] = {}
            self.flower[message.server.id][user.id]["coin"] = int(''.join(nombre))
            self.flower[message.server.id][user.id]["time"] = 0
            count = ''.join(nombre)
        else:
            self.flower[message.server.id][user.id]["coin"] += int(''.join(nombre))
            count = self.flower[message.server.id][user.id]["coin"]
        await self.save_flower()

        if count ==0:
            embed=discord.Embed(title="{} a adoré la patate sacrée {} fois".format(user.name, count),color=user.colour)
        else:
            embed=discord.Embed(title="{} a adoré la patate sacrée {} fois".format(user.name, count),color=user.colour)

        embed.set_thumbnail(url="https://transitionculture.org/wp-content/uploads/potato.jpg")

        await self.bot.say(embed=embed)
        
    @commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def Pfix(self, ctx, nombre, *, user: discord.Member=None):
        message = ctx.message

        if not user:
            await self.bot.say("Il faut préciser l'utilisateur")
            return
        if not nombre:
            await self.bot.say("Il faut préciser le nombre")
            return
        else:
            try: 
                int(''.join(nombre))
            except:
                await self.bot.say("Tu sais ce que c'est un nombre?")
                return
        if user.id not in self.flower[message.server.id]:
            self.flower[message.server.id][user.id] = {}
            self.flower[message.server.id][user.id]["coin"] = int(''.join(nombre))
            self.flower[message.server.id][user.id]["time"] = 0
            count = ''.join(nombre)
        else:
            self.flower[message.server.id][user.id]["coin"] = int(''.join(nombre))
            count = self.flower[message.server.id][user.id]["coin"]
        await self.save_flower()

        if count ==0:
            embed=discord.Embed(title="{} a adoré la patate sacrée {} fois".format(user.name, count),color=user.colour)
        else:
            embed=discord.Embed(title="{} a adoré la patate sacrée {} fois".format(user.name, count),color=user.colour)
        embed.set_thumbnail(url="https://transitionculture.org/wp-content/uploads/potato.jpg")
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, no_pm=True)
    async def rank(self,ctx,top:int=10):
        message= ctx.message
        server = message.server

        if top<1:
            top = 10

        member = {}

        for m in self.flower[server.id]:
            test= discord.utils.get(server.members, id=m)
            if test:
                member.update({m:self.flower[server.id][m]["coin"]})

        all=sorted(member.items(),key=operator.itemgetter(1),reverse=True)

        if len(all) < top:
            top = len(all)

        start = ""
        em = discord.Embed(title="**Leaderboard du serveur {}**\n\n".format(server.name),color=message.author.color)
        if server.icon_url:
            em.set_thumbnail(url=server.icon_url)

        for x in range(top):
            if x+1<10:
                nb = "{} ".format(str(x+1))
            else:
                nb = "{}".format(str(x+1))
            name = discord.utils.get(server.members, id=all[x][0])
            c = "**{}**     {}\n                Nombre d'adorations:  **{}**      ".format(nb,name.name,all[x][1])
            if x+1 == 1:
                c += ":first_place:"
            if x+1 == 2:
                c += ":second_place:"
            if x+1 == 3:
                c += ":third_place:"
            start += c + "\n"
            if len(start) > 1500:
                em.description = start
                await self.bot.say(embed=em)
                return
        em.description = start
        await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def adoration(self,ctx):
        message = ctx.message
        server = message.server
        user = message.author

        curr_time = time()

        if user.id not in self.flower[server.id]:
            self.flower[server.id][user.id] = {}
            self.flower[server.id][user.id]["coin"] = 1
            self.flower[server.id][user.id]["time"] = time()
            count = 1

        elif int(curr_time) - int(self.flower[server.id][user.id]["time"]) > 300:
            self.flower[server.id][user.id]["coin"] += 1
            count = self.flower[server.id][user.id]["coin"]
            self.flower[server.id][user.id]["time"] = curr_time
        else:
            total = int(curr_time) - int(self.flower[server.id][user.id]["time"])
            total = 300-total
            minute = 0
            while total>59:
                minute += 1
                total = total-60
            if minute != 0:
                embed=discord.Embed(title="{}, tu dois encore attendre {} minutes et {} secondes ".format(user.name,minute,total),color=user.colour)
            else:
                embed=discord.Embed(title="{}, tu dois encore attendre {} secondes ".format(user.name,total),color=user.colour)
            await self.bot.say(embed=embed)
            return

        embed=discord.Embed(title="{}, tu as adoré la patate sacrée {} fois".format(user.name, count),color=user.colour)
        embed.set_thumbnail(url="https://transitionculture.org/wp-content/uploads/potato.jpg")
        await self.bot.say(embed=embed)
        await self.save_flower()
        

    @commands.command(pass_context=True, no_pm=True)
    async def patate(self, ctx, *, user: discord.Member=None):
        message = ctx.message
        author = message.author

        if not message.server.id in self.flower:
            self.flower[message.server.id] = {}

        if not user:
            user = author

        if user.id not in self.flower[message.server.id]:
            self.flower[message.server.id][user.id] = {}
            self.flower[message.server.id][user.id]["coin"] = 0
            self.flower[message.server.id][user.id]["time"] = 0
            count = 0
        else:
            count = int(self.flower[message.server.id][user.id]["coin"])
        
        if count ==0:
            embed=discord.Embed(title="{} a adoré la patate sacrée {} fois".format(user.name, count),color=user.colour)
        else:
            embed=discord.Embed(title="{} a adoré la patate sacrée {} fois".format(user.name, count),color=user.colour)
        await self.save_flower()
        embed.set_thumbnail(url="https://transitionculture.org/wp-content/uploads/potato.jpg")
        await self.bot.say(embed=embed)
    
    """@commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def nombre(self, ctx):


        self.flower["nombre"] = int(ctx.message.content[8:])
        await self.save_flower()
        await self.bot.say("Tout les {}".format(self.flower["nombre"]))"""

    """@commands.command(pass_context=True, no_pm=True)
    @checks.admin_or_permissions(administrator=True)
    async def plant(self, ctx):
        message = ctx.message

        embed=discord.Embed(title="Une fleur est apparue", color=message.author.colour)
        embed.set_image(url="url")
        suppr = await self.bot.send_message(discord.Object(id='347455695890677762'), embed=embed)
        fl = 1

        while fl == 1:
            picked = await self.bot.wait_for_message(timeout = 6)
            if picked == None:
                embed=discord.Embed(title="Personne n'a eu la fleur.")
                await self.bot.send_message(message.channel, embed=embed)
                return
            if picked.content == "!pick":
                fl = 0
                if message.author.id not in self.flower:
                    self.flower[message.author.id] = "1"
                    count = 1
                else:
                    count = int(self.flower[message.author.id])
                    count += 1
                    self.flower[message.author.id] = count

                await self.bot.delete_message(suppr)
                embed=discord.Embed(title="{} a maintenant {} fleurs".format(message.author.name, count),color=picked.author.colour)
                await self.bot.send_message(picked.channel, embed=embed)
                await self.bot.delete_message(picked)
                    
                    
        await self.save_flower()"""




    def is_command(self, msg):
        if callable(self.bot.command_prefix):
            prefixes = self.bot.command_prefix(self.bot, msg)
        else:
            prefixes = self.bot.command_prefix
        for p in prefixes:
            if msg.content.startswith(p):
                return True
        return False

"""
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if self.is_command(message):
            return
        if self.flower["msg"] > self.flower["nombre"]:
            self.flower["msg"] = 0
        a = self.flower["msg"]
        a += 1
        self.flower["msg"] = a
        if a == self.flower["nombre"]:
            embed=discord.Embed(title="Une patate est apparue", color=0xffa505)
            embed.set_image(url="http://transitionculture.org/wp-content/uploads/potato.jpg")
            suppr = await self.bot.send_message(discord.Object(id='347455695890677762'), embed=embed)
            fl = 1

            while fl == 1:
                picked = await self.bot.wait_for_message(timeout = 60)
                if picked.content == "!pick":
                    fl = 0
                    print(fl)
                    if message.author.id not in self.flower:
                        self.flower[message.author.id] = "1"
                        count = 1
                    else:
                        count = int(self.flower[message.author.id])
                        count += 1
                        self.flower[message.author.id] = count

                    await self.bot.delete_message(suppr)
                    embed=discord.Embed(title="{} a maintenant {} patates".format(message.author.name, count),color=0xffa505)
                    await self.bot.send_message(picked.channel, embed=embed)
                    await self.bot.delete_message(picked)
                    
                    
        await self.save_flower()"""



def check_folders():
    folder = "data/pate"
    if not os.path.exists(folder):
        print("Creating {} folder...".format(folder))
        os.makedirs(folder)


def check_files():
    default = {"channels_enabled": {}}
    if not dataIO.is_valid_json("data/patate/patate.json"):
        print("Creating default flower.json...")
        dataIO.save_json("data/patate/patate.json", default)

def setup(bot):
    bot.add_cog(fleur(bot))