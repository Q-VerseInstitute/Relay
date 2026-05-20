import discord
from discord import app_commands
from discord.ext import commands
from utils.config import load_config, save_config

config = load_config()
ALLOWED_POST_ROLES = config["allowed_post_roles"]

class BroadcastModal(discord.ui.Modal, title="QVI Log"):
    header = discord.ui.TextInput(
        label="Header",
        default="[QVI::LOG]",
        max_length=64,
    )
    body = discord.ui.TextInput(
        label="Message",
        style=discord.TextStyle.paragraph,
        max_length=4000,
    )
    status = discord.ui.TextInput(
        label="Layer status",
        default="Stable",
        max_length=64,
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        channel_id = config["channels"]["notification_channel_id"]
        channel = interaction.client.get_channel(channel_id)

        if not channel or channel is None:
            await interaction.response.send_message(
                "Please specify notifications channel first.",
                ephemeral=True,
            )
            return

        color = discord.Color.ash_embed()

        if self.header.value == "[QVI::LOG]":
            color = discord.Color.dark_gray()
        elif self.header.value == "[QVI::WARNING]" or self.header.value == "[QVI::WARN]":
            color = discord.Color.dark_red()
        elif self.header.value == "[QVI::UPDATE]":
            color = discord.Color.blue()
        elif self.header.value == "[QVI::CRITICAL]":
            color = discord.Color.dark_red()
        else:
            color = discord.Color.ash_embed()

        embed = discord.Embed(
                title=self.header.value,
                description=f"```{self.body.value}```",
                color=color,
            )
        
        embed.set_footer(text=f"QVI Notification System • Layer Status: {self.status.value}")
        embed.timestamp = discord.utils.utcnow()

        await channel.send(
            embed=embed
        )
        await interaction.response.send_message(
            "Notification sent.",
            ephemeral=True,
        )

class Messages(commands.Cog):
    post_group = app_commands.Group(name="broadcast", description="Broadcast commands")
    access_group = app_commands.Group(name="access", description="Notification access commands", parent=post_group)
    channel_group = app_commands.Group(name="channel", description="Notification channel control commands", parent=post_group)

    def __init__(self, bot):
        self.bot = bot
    
    async def cog_load(self):
        print("Messages cog loaded.")

    async def cog_unload(self):
        print("Messages cog unloaded.")

    @post_group.command(name="upload", description="Broadcast to specified channel")
    @app_commands.guild_only()
    async def post(self, interaction: discord.Interaction):
        role_ids = [role.id for role in interaction.user.roles]

        if not any(role in ALLOWED_POST_ROLES for role in role_ids):
            await interaction.response.send_message(
                "Access denied: you don't have permission to use this command.",
                ephemeral=True,
            )

            return
        
        await interaction.response.send_modal(BroadcastModal())

    @access_group.command(name="grant", description="Grant broadcast permission to a specific role")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def post_role_add(self, interaction: discord.Interaction, role: discord.Role):
        if not role.id in config["allowed_post_roles"]:
            config["allowed_post_roles"].append(role.id)
            save_config(config)

            await interaction.response.send_message(
                f"Permission granted for the {role.mention} role.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"Permission cannot be granted: the role {role.mention} already has it.",
                ephemeral=True,
            )

            return
        
    @access_group.command(name="revoke", description="Revoke a specific role's broadcast permission")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def post_role_remove(self, interaction: discord.Interaction, role: discord.Role):
        role_id = role.id

        if role_id in config["allowed_post_roles"]:
            config["allowed_post_roles"].remove(role_id)
            save_config(config)

            await interaction.response.send_message(
                f"Broadcast permission for the {role.mention} role has been revoked.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                f"The permission cannot be revoked: the role {role.mention} does not have it.",
                ephemeral=True,
            )

            return

    @channel_group.command(name="set", description="Link the channel to the broadcast")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def post_channel_set(self, interaction: discord.Interaction, channel: discord.abc.GuildChannel):

        if isinstance(channel, discord.channel.TextChannel):
            config["channels"]["notification_channel_id"] = channel.id
            save_config(config)

            await interaction.response.send_message(
                f"Broadcast channel set: {channel.mention}.",
                ephemeral=True,
            )
        else:
            await interaction.response.send_message(
                "Only text channels can be set.",
                ephemeral=True,
            )

    @channel_group.command(name="remove", description="Remove the channel's link to the broadcast")
    @app_commands.guild_only()
    @app_commands.checks.has_permissions(manage_guild=True)
    async def post_channel_remove(self, interaction: discord.Interaction):
        config["channels"]["notification_channel_id"] = None
        save_config(config)

        await interaction.response.send_message(
            f"Broadcast channel removed.",
            ephemeral=True,
        )



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Messages(bot))
