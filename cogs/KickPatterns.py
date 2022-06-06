import discord
from discord.ext import commands, tasks
import copy
import re

class KickPattern(commands.Cog):
    """
    Simple example that can be worked in whichever direction.
    Actual ban logic is commented out in banLoop to test without
    doing any damage. The main functions are : 
    
    getMembers => returns a dictionary that's basically
                 'name #xxxx' => member
    matchingNames => returns a list of keys that fit some pattern for banning 
    ban => ... 
    
    After that, just some functions for interacting with the bot via discord,
    all with decorators specific roles. 

    """

    def __init__(self, bot):
        self.bot = bot
        self.patterns = []
        self.banLoop.start()

    async def getMembers(self):
        """
        returns {name + descrimator: member object, ....
       Just gets all server members in a dictionary
        :return: dictionary
        """
        dicMember = {}
        for guild in self.bot.guilds:
            for member in guild.members:
                # print(member.id) member ID
                # print(member) member name #0000
                dicMember[str(member)] = member
        return dicMember

    @tasks.loop(minutes=10)
    async def banLoop(self):
        """
        Create a deep copy of the ban patterns
        Get a copy of all the members of the server
        Compare members against the pattern list
        Send them to Valhalla
        :return:
        """
        # avoids async issues as size changes
        banPatterns = copy.deepcopy(self.patterns)
        # https://stackoverflow.com/questions/65808190/get-all-members-discord-py requires intents from bot
        serverMembers = await self.getMembers()
        banWorthy = self.matchingNames(serverMembers)

        # send them to valhalla, commented out for testing
        # for item in banWorthy:
        #     toBan = serverMembers[item]
        #     await self.ban(toBan)

    async def matchingNames(self, memberLst):
        """
        Create a list of display names
        regex match them against the pattern list
        return a list of keys for banning
        :param memberLst: list of display names as keys
        :return:
        """
        # create a list of keys from memberLst
        userNames = list(memberLst.keys())
        # regex for those items that match
        banMe = []
        for item in self.patterns:
            r = re.compile(item)
            tmp = list(filter(r.match, userNames))
            banMe.extend(tmp)
        return banMe

    async def ban(self, member : discord.Member, *, reason=None):
        """
        Simple kick command
        :param member:
        :param reason:
        :return:
        """
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_role('Admin') # < < < Set appropriate role for who can add, please be careful
    async def namePattern(self, ctx, arg):
        """
        command >namePattern *limited

        :param ctx: internal command for the channel the command is given in
        :param arg: pattern to add
        :return:
        """
        self.patterns.append(arg)

    @commands.command()
    @commands.has_role('Admin')
    async def getPatterns(self, ctx):
        """
        returns all the patterns saved
        :param ctx:
        :return:
        """
        await ctx.send(self.patterns)

    @commands.command()
    @commands.has_role('Admin')
    async def delPattern(self, ctx, arg):
        """
        removes a pattern from the list
        :param ctx:
        :param arg:
        :return:
        """
        if arg in self.patterns:
            self.patterns.remove(arg)
            await ctx.send(f"{arg} was removed")
        else:
            await ctx.send(f"{arg} was not found")

def setup(bot):
    bot.add_cog(KickPattern(bot))
