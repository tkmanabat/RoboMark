import discord
from discord.ext import commands
import googletrans
from googletrans import Translator


class translate(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command(name="translate", help="Visit https://py-googletrans.readthedocs.io/en/latest/ for languages supported")
    async def translate(self, ctx, lang_to, *args):
        lang_to = lang_to.lower()
        if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
            raise commands.BadArgument("Sorry lods di pwede yang gawa gawa mong language")

        text = ' '.join(args)
        translator = googletrans.Translator()
        text_translated = translator.translate(text, dest=lang_to).text
        await ctx.send(text_translated)

def setup(client):
    client.add_cog(translate(client))