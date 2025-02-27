import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

user_ids_to_delete = set()
allowed_role = None  # Роль, которой разрешено использовать команды
bot_running = False


@bot.event
async def on_ready():
    print(f'Бот {bot.user} успешно запущен.')


@bot.command()
async def start(ctx):
    global bot_running
    if not check_permissions(ctx):
        return await ctx.send("У вас нет прав для использования этой команды.")
    bot_running = True
    await ctx.send("Бот запущен! Теперь он удаляет сообщения от указанных пользователей.")

@bot.command()
async def stop(ctx):
    global bot_running
    if not check_permissions(ctx):
        return await ctx.send("У вас нет прав для использования этой команды.")
    bot_running = False
    await ctx.send("Бот остановлен. Сообщения больше не удаляются.")


@bot.command()
async def addid(ctx, user_id: int):
    """Добавляет ID пользователя в список для удаления сообщений."""
    if not check_permissions(ctx):
        return await ctx.send("У вас нет прав для использования этой команды.")
    user_ids_to_delete.add(user_id)
    await ctx.send(f"Добавлен ID {user_id} в список удаления сообщений.")


@bot.command()
async def delid(ctx, user_id: int):
    """Удаляет ID пользователя из списка."""
    if not check_permissions(ctx):
        return await ctx.send("У вас нет прав для использования этой команды.")
    if user_id in user_ids_to_delete:
        user_ids_to_delete.remove(user_id)
        await ctx.send(f"ID {user_id} удалён из списка.")
    else:
        await ctx.send(f"ID {user_id} не найден в списке.")


@bot.command()
async def listid(ctx):
    """Выводит список ID, чьи сообщения удаляются."""
    if not check_permissions(ctx):
        return await ctx.send("У вас нет прав для использования этой команды.")
    if user_ids_to_delete:
        await ctx.send(f"Список ID для удаления сообщений: {', '.join(map(str, user_ids_to_delete))}")
    else:
        await ctx.send("Список пуст.")


@bot.command()
async def addrole(ctx, role: discord.Role):
    """Добавляет роль, которая сможет использовать команды. Только владелец сервера может это делать."""
    global allowed_role
    if ctx.author == ctx.guild.owner:
        allowed_role = role
        await ctx.send(f"Роль {role.mention} теперь может использовать команды бота.")
    else:
        await ctx.send("Только владелец сервера может использовать эту команду.")


@bot.event
async def on_message(message):
    if bot_running and message.author.id in user_ids_to_delete:
        await message.delete()
    await bot.process_commands(message)


def check_permissions(ctx):
    """Проверяет, есть ли у пользователя разрешённая роль."""
    if ctx.author == ctx.guild.owner:
        return True
    if allowed_role and allowed_role in ctx.author.roles:
        return True
    return False


bot.run("YOURBOTTOKEN")
