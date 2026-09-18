import discord
from discord import app_commands
import random

intents = discord.Intents.default()
intents.guilds = True

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        await self.tree.sync()
        print(f'تم تشغيل البوت بنجاح باسم: {self.user}')

bot = MyBot()

# قوائم الرول بلاي
categories = ["جندي", "ضابط", "مسعف", "طبيب", "قائد", "ملازم", "رائد", "محقق", "مواطن", "رجل أعمال", "ميكانيكي", "عضو", "رئيس"]
departments = ["المطافئ", "الشرطة", "الجيش", "القوات الخاصة", "المستشفى", "العصابة", "البلدية", "الأمن العام", "المخابرات"]
ranks = ["أول", "مبتدئ", "متقدم", "متدرب", "خبير", "سابق", "احتياطي", "عام"]

def generate_rp_name():
    cat = random.choice(categories)
    dept = random.choice(departments)
    rank = random.choice(ranks)
    style = random.randint(1, 3)
    if style == 1:
        return f"{cat} - {dept}"
    elif style == 2:
        return f"{cat} {rank}"
    else:
        return f"{cat} {dept} ({rank})"

# 1. أمر إنشاء الرتب العشوائية للرول بلاي
@bot.tree.command(name="generate_roles", description="إنشاء 100 رتبة رول بلاي عشوائية وغير مكررة")
@app_commands.checks.has_permissions(manage_roles=True)
async def generate_roles(interaction: discord.Interaction):
    await interaction.response.send_message("⏳ جاري إنشاء 100 رتبة رول بلاي عشوائية، انتظر قليلاً...")
    guild = interaction.guild
    created_count = 0
    used_names = set()

    while created_count < 100:
        role_name = generate_rp_name()
        if role_name in used_names:
            continue
        used_names.add(role_name)
        random_color = discord.Color(random.randint(0, 0xFFFFFF))
        
        try:
            await guild.create_role(name=role_name, color=random_color)
            created_count += 1
        except discord.Forbidden:
            await interaction.followup.send("❌ ليس لدي صلاحية إدارة الرتب (Manage Roles).")
            return
        except discord.HTTPException:
            await interaction.followup.send("❌ السيرفر امتلأ بالرتب أو حدث خطأ بالاتصال.")
            return

    await interaction.followup.send(f"✅ تم إنشاء {created_count} رتبة رول بلاي منوعة بنجاح!")

# 2. الأمر الجديد: حذف جميع الرتب في السيرفر تنظيف كامل
@bot.tree.command(name="delete_all_roles", description="⚠️ حذف جميع رتب السيرفر التي يستطيع البوت حذفها لتنظيف السيرفر")
@app_commands.checks.has_permissions(administrator=True) # هذا الأمر متاح فقط للأدمن لحماية السيرفر
async def delete_all_roles(interaction: discord.Interaction):
    await interaction.response.send_message("⏳ جاري تنظيف السيرفر وحذف جميع الرتب المتاحة، انتظر قليلاً...")
    
    guild = interaction.guild
    deleted_count = 0
    
    # الحصول على رتبة البوت الأعلى لتجنب محاولة حذف رتب أعلى منه
    bot_member = guild.get_member(bot.user.id)
    bot_top_role = bot_member.top_role

    for role in list(guild.roles):
        # تخطي رتبة @everyone، ورتبة البوت نفسه، والرتب التابعة للبوتات الأخرى أو الإضافات
        if role.is_default() or role.managed or role >= bot_top_role:
            continue
            
        try:
            await role.delete()
            deleted_count += 1
        except discord.Forbidden:
            continue # تخطي أي رتبة يفشل في حذفها بسبب الصلاحيات
        except discord.HTTPException:
            continue

    await interaction.followup.send(f"🗑️ تم حذف {deleted_count} رتبة بنجاح وتنظيف السيرفر!")

bot.run('MTU0OTA3OTk3NTY4NzIzMzYxNg.GjkqEQ.ZrdN2nRMQnxZraYhh8deW2Zk8AfN6jtSC5HKP8')