import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    #clear messages
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        #if (ctx.message.author.permissions_in(ctx.message.channel).manage_messages):
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"Removed {amount} message(s)", delete_after=5)

    #kick members
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason = reason)
        await ctx.send(f"{member.mention} has been kicked.")

    #ban members
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason = reason)
        await ctx.send(f"{member.mention} has been banned.")

    #unban members
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users =  await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}.")
                return

    #add role perms
    #TODO, remove role if target had roles alr
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, role: discord.Role, member: discord.Member=None):
        member = member or ctx.message.author
        if role not in member.roles:
            await member.add_roles(role)
            await ctx.send(f"Role '{role}' has been added to {member}")
        else:
            await member.remove_roles(role)
            await ctx.send(f"Role '{role}' has been removed from {member}")

def setup(client):
    client.add_cog(Admin(client))
