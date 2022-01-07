# -------------------- IMPORT DES LIBRAIRIES --------------------
#Librairie Discord
import discord
from discord.ext import commands
from discord_slash import SlashCommand, ButtonStyle
from discord_slash.utils.manage_commands import create_option, create_choice, remove_all_commands
from discord_slash.utils.manage_components import *

#Librairies nécessaires au scrap
import requests #Afin de pouvoir accéder à une page web avec une requête POST
from bs4 import BeautifulSoup #Scrapping simplifié
import re #Regex
import json #JSON

#Librairie permettant l'accès aux variables d'environnement
import os

# -------------------- INITIALISATION DU BOT --------------------
bot = commands.Bot(command_prefix = "!", description = "Bot informatif sur les Space Invaders")
slash = SlashCommand(bot, sync_commands = True)
bot.remove_command('help')
api_token = os.environ['API_TOKEN']
cities_list = ["FKF","KLN","BRL","MLB","PRT","WN","DHK","ANVR","BXL","CHAR","RDU","BT","GRU","SP","HK","DJN","BRC","BBO","MLGA","MEN","LA","MIA","NY","SD","AIX","AVI","BTA","CAPF","CLR","CON","CAZ","DIJ","FRQ","GRN","LCT","LIL","LBR","LY","MARS","MTB","MPL","NA","NIM","PA","PAU","PRP","RN","TLS","VMRL","VRS","LDN","MAN","NCL","VRN","ELT","RA","ROM","TK","MBSA","MRAK","RBA","CCU","KAT","AMS","NOO","RTD","FAO","LJU","SPACE","HALM","VSB","ANZR","BSL","BRN","GNV","LSN","GRTI","BGK","DJBA","IST","POTI"]

# -------------------- FONCTIONS DE DEBUG --------------------
#Fonction appelée lorsque le bot est prêt
@bot.event
async def on_ready():
    print("Bot prêt !")

# -------------------- FONCTIONS UTILES --------------------
#Affichage de l'aide
@slash.slash(name="aide", guild_ids=[730904034608676907], description="Aide à propos des commandes disponibles")
async def aide(ctx):
    description_content = "Ce robot fonctionne sur le serveur mais aussi par message privé, vous pouvez simplement lui écrire et il vous répondra.\n"
    description_content += "Les commandes se pré-remplissent, il vous suffit de taper le début de la commande et du ou des paramètre(s) afin de les compléter.\n\n"
    description_content += "**Liste des commandes :**\n\n"
    description_content += "**/infos_serveur** : affiche les informations du serveur\n"
    description_content += "**/si VILLE_NUMERO** : affiche les informations d'un SI - exemple : !si PA_1200\n"
    description_content += "**/ville VILLE** : affiche les informations d'une ville - exemple : !ville Paris ou !ville PA\n"
    description_content += "**/mes_infos COMPTE PSEUDO** : met à jour mes informations - exemple : !mes_infos instagram Raphystole *!Confidentialité pour connaitre l'utlisation de tes données*\n"
    description_content += "**/infos @UTILISATEUR** : affiche les informations d'un utilisateur - exemple : !infos @Raphystole\n"
    description_content += "*Vos informations ne seront pas divulguées hors de ce robot. Celles-ci sont conservées pendant une durée de 3 ans maximum et peuvent être détruites sur simple demande ou en utilisant la commande dédiée.*\n"
    embed=discord.Embed(color=0x04ff00, title="Fonctionnement du robot :", description=description_content)
    await ctx.send(embed=embed)

#Mettre à jour ses données utilisateur
@slash.slash(name="mes_informations", guild_ids=[730904034608676907], description="Mettre à jour mes informations", options=[
    create_option(name="compte", description="Numéro de la ville", option_type=3, required=True, choices=[
        create_choice(name="Flash Invaders", value="flash_invaders"),
        create_choice(name="Site internet", value="website"),
        create_choice(name="Instagram", value="instagram"),
        create_choice(name="Flickr", value="flickr"),
        create_choice(name="Spotter Invader", value="spotter")
    ]),
    create_option(name="nom", description="Username ou pseudo", option_type=3, required=True)
])
async def mes_infos(ctx, compte, nom):
    print(ctx.author_id)
    compte = compte.lower()
    compte = compte.replace("flashinvaders", "flash_invaders").replace("site", "website").replace("webwebsite", "website").replace("spotter-invader", "spotter")
    if compte in ["flash_invaders","website","instagram","flickr","spotter"]:
        url_api = "http://invaders.art.free.fr/botsi/users.php?controller=set_"+compte+"&id_discord="+str(ctx.author_id)+"&"+compte+"="+nom+"&api_token="+api_token
        requests.get(url_api)
        compte = compte.replace("flash_invaders", "pseudo FlashInvaders").replace("instagram", "pseudo Instagram").replace("spotter", "pseudo Spotter-Invader").replace("flickr", "pseudo Flickr").replace("website", "site internet")
        await ctx.send("Ton "+compte+" a bien été mis à jour !")
    else :
        await ctx.send("Ce service n'est pas pris en compte par le robot.\nServices pris en compte : FlashInvaders, Instagram, Flickr, Spotter-Invader, Website.")

#Mettre à jour ses données utilisateur
@slash.slash(name="infos", guild_ids=[730904034608676907], description="Rechercher des informations sur un utilisateur", options=[
    create_option(name="utilisateur", description="Utilisateur du serveur Discord", option_type=6, required=True)
])
@bot.command(aliases=['i'])
async def infos(ctx, utilisateur: discord.User):
    response = requests.get("http://invaders.art.free.fr/botsi/users.php?controller=get_all&id_discord="+str(utilisateur.id)+"&api_token="+api_token)
    try:
        r=response.json()
        is_blank = True
        embed_description = ""
        if r["flash_invaders"]:
            embed_description = "**FlashInvaders :** ["+r["flash_invaders"]+"](https://www.decrocher-la-lune.com/invader/user/"+r["flash_invaders"].replace(" ","%20")+")\n"
            is_blank = False
        if r["instagram"]:
            embed_description += "**Instagram :** ["+r["instagram"]+"](https://www.instagram.com/"+r["instagram"]+")\n"
            is_blank = False
        if r["spotter"]:
            embed_description += "**Spotter-Invader :** "+r["spotter"]+"\n"
            is_blank = False
        if r["flickr"]:
            embed_description += "**Flickr :** "+r["flickr"]+"\n"
            is_blank = False
        if r["website"]:
            embed_description += "**Site internet :** "+"["+r["website"]+"]("+r["website"]+")\n"
            is_blank = False
        if is_blank :
            await ctx.send("Aucunes données pour cet utilisateur")
        else :
            embed_description = embed_description[:-1]
            embed=discord.Embed(color=0x04ff00, title="Informations sur "+str(utilisateur).rsplit("#",1)[0], description=embed_description)
            embed.set_thumbnail(url=utilisateur.avatar_url)
            await ctx.send(embed=embed)
    except:
        await ctx.send("Aucunes données pour cet utilisateur")

#Mettre à jour ses données utilisateur
@slash.slash(name="carte", guild_ids=[730904034608676907], description="Rechercher la carte d'une ville", options=[
    create_option(name="carte", description="Numéro (ex : 1), nom (ex: Paris) ou acronyme (ex: PA) de la ville", option_type=3, required=True)
])
async def carte(ctx, carte):
    carte = str(carte).zfill(2).lower()
    carte = carte.replace("paris1", "01").replace("pa1", "01").replace("montpellier", "02").replace("mpl", "02").replace("grenoble", "03").replace("grn", "03").replace("berne", "04").replace("brn", "04").replace("avignon", "05").replace("avi", "05").replace("genève", "06").replace("gnv", "06").replace("lyon", "07").replace("ly", "07").replace("rotterdam", "08").replace("rtd", "08").replace("tokyo", "09").replace("tk", "09").replace("perth", "10").replace("prt", "10").replace("new-york", "11").replace("ny", "11").replace("los angeles", "12").replace("la", "12").replace("manchester", "13").replace("man", "13").replace("bastia", "14").replace("bta", "14").replace("vienne", "15").replace("wn", "15").replace("côte d'azur", "16").replace("caz", "16").replace("bilbao", "17").replace("bbo", "17").replace("kathmandou", "18").replace("kat", "18").replace("rome", "19").replace("rom", "19").replace("paris2", "20").replace("pa2", "20").replace("saõ paulo", "21").replace("sp", "21").replace("bruxelles", "22").replace("bxl", "22").replace("miami", "23").replace("mia", "23").replace("ravenne", "24").replace("ra", "24").replace("djerba", "25").replace("djba", "25").replace("marseille", "26").replace("mars", "26")
    r = requests.get("http://invaders.art.free.fr/botsi/maps.php?controller=get_map&map_number="+carte).json()
    is_blank = True
    embed_description = ""
    if r["city"]:
        embed_description = "**Ville :** "+r["city"]+"\n"
        is_blank = False
    if r["release_date"]:
        embed_description += "**Date de sortie :** "+str(r["release_date"])+"\n"
        is_blank = False
    if r["copies"]:
        embed_description += "**Nombre de copies :** "+str(r["copies"])
        if r["signed_copies"]:
            embed_description += " (et "+str(r["signed_copies"])+" signées)"
        embed_description += "\n"
        is_blank = False
    if r["format"]:
        embed_description += "**Format :** "+str(r["format"])+"\n"
        is_blank = False
    if r["source"]:
        embed_description += "**Source :** "+str(r["source"])+"\n"
        is_blank = False
    embed_description += "[Voir la carte complète](http://invaders.art.free.fr/botsi/maps?controller=map&map="+carte+")"
    if is_blank :
        await ctx.send("Cette carte n'existe pas", hidden=True)
    else :
        embed=discord.Embed(color=0x04ff00, title="Informations sur la carte numéro : "+carte, description=embed_description)
        embed.set_image(url=r["cover_img_link"])
        await ctx.send(embed=embed)

#Affichage des infos du serveur
@slash.slash(name="serveur", guild_ids=[730904034608676907], description="Rechercher des informations sur une ville")
async def serveur(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfPeople = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contient **{numberOfPeople} personnes** et possède **{numberOfTextChannels} salons textuels**."
    await ctx.send(message)

#Affichage des infos sur une ville
#@bot.command()
@slash.slash(name="ville", guild_ids=[730904034608676907], description="Rechercher des informations sur une ville", options=[
    create_option(name="ville", description="Nom de la ville", option_type=3, required=True)
])
async def ville(ctx, ville):
    ville = ville.lower()
    ville = ville.replace("francfort","frankfurt").replace("vienne","vienna").replace("wien","vienna").replace("saopaulo","sao-paulo").replace("hongkong","hong-kong").replace("barcelona","barcelone")
    convert_spotter_spaceinvaders = {"aix":"aix-en-provence","ams":"amsterdam","anvr":"anvers","anzr":"anzere","avi":"avignon","bgk":"bangkok","brc":"barcelone","bsl":"basel","bta":"bastia","brl":"berlin ","brn":"bern","bt":"bhutan","bbo":"bilbao","bxl":"bruxelles","ccu":"cancun","capf":"capferret","caz":"caz","char":"charleroi","clr":"clermont-ferrand","kln":"cologne","con":"contis-les-bains","djn":"daejeon","dhk":"dakha","cij":"dijon","djba":"djerba","elt":"eilat","fao":"faro","frq":"forcalquier","fkf":"frankfurt","gnv":"geneve","grn":"grenoble","gru":"grude","grti":"grumeti","halm":"halmstad","hk":"hong-kong","ist":"istanbul","kat":"katmandou","lct":"la-ciotat","lsn":"lausanne","lil":"lille","lju":"ljubjana","ldn":"london","la":"los-angeles","lbr":"luberon","ly":"lyon","mlga":"malaga","man":"manchester","mrak":"marrakech","mars":"marseille","mlb":"melbourne","men":"menorca","mia":"miami","mbsa":"mombasa","mtb":"montauban","mpl":"montpellier","na":"nantes","ncl":"newcastle","ny":"new-york","nim":"nimes"," oo":"noordwijk","pa":"paris","pau":"pau","prp":"perpignan","prt":"perth","rba":"rabat","ra":"ravenna","rdu":"redu","rn":"rennes","rom":"rome","rtd":"rotterdam","sd":"san-diego","sp":"sao-paulo","tk":"tokyo","tls":"toulouse","vlmo":"valmorel","vrn":"varanasi","vrs":"versailles","wn":"vienna","vsb":"visby"}
    convert_spaceinvaders_spotter = dict((reversed(item) for item in convert_spotter_spaceinvaders.items()))
    if ville in convert_spotter_spaceinvaders.keys():
        ville_spotter = ville
        ville_spaceinvaders = convert_spotter_spaceinvaders[ville]
    else:
        ville_spotter = convert_spaceinvaders_spotter[ville]
        ville_spaceinvaders = ville
    r = requests.get("https://space-invaders.com/world/"+ville_spaceinvaders)
    soup = BeautifulSoup(r.content, 'html.parser') #Parsing de la page récupérée
    regex_1 = re.compile('^titre') #Définition du regex
    infos_1 = soup.find_all('div', attrs={'class': regex_1})
    for div in infos_1:
            ville_nom =  div.h2.getText()
            ville_stats = []
            for h3 in div.find_all("h3"):
                    ville_stats.append(h3.getText().replace("WAVES: ", "").replace("INVADERS: ", "").replace("SCORE: ", "").replace(" PTS", ""))
    ville_invasions = ville_stats[0]
    ville_invaders =ville_stats[1]
    ville_score = ville_stats[2]
    embed=discord.Embed(color=0x04ff00, title=ville_nom, description="Invasions : "+ville_invasions+"\nInvaders : "+ville_invaders+"\nScore : "+ville_score+" pts\n[SPOTTER](http://invaders.art.free.fr/invaderspotter_rechercheville.php?ville="+ville_spotter+") / [SPACE-INVADERS](https://www.space-invaders.com/world/"+ville_spaceinvaders+")")
    print("Affichage de "+ville_nom)
    await ctx.send(embed=embed)

#Affichage des infos sur un SI
@slash.slash(name="si", guild_ids=[730904034608676907], description="Rechercher des informations sur un SI", options=[
    create_option(name="si", description="Nom du SI (par exemple : PA_0001)", option_type=3, required=True)
])
async def si(ctx, si):
    si_split = si.split("_")
    si_ville = si_split[0].upper()
    si_numero = si_split[1].lstrip("0")
    #Gestion des erreurs
    if si.upper() == "DSK_2806":
        await ctx.send(":underage:")
        return
    if len(si_split) != 2:
        await ctx.send("Le format du SI n'est pas bon")
        return
    if si_ville == "DK":
        await ctx.send("Nous n'avons pas encore la prétention d'être des envahisseurs de l'espace...")
        return
    if si_ville not in cities_list:
        await ctx.send(f"La ville \"{si_ville}\" n'a pas été envahie")
        return
    #Formattage des chiffres
    if si_ville == "PA":
        zfill_value = 4
    elif si_ville == "LDN" or si_ville == "HK" or si_ville == "LA" or si_ville == "NY" or si_ville == "TK":
        zfill_value = 3  
    else:
        zfill_value = 2
    si_numero = si_numero.zfill(zfill_value)
    #Formattage de la ville
    if si_ville=="PA":
        data = dict(numero=si_numero,prs="on",toutparis="on",PA01="on",PA02="on",PA03="on",PA04="on",PA05="on",PA06="on",PA07="on",PA08="on",PA09="on",PA10="on",PA11="on",PA12="on",PA13="on",PA14="on",PA15="on",PA16="on",PA17="on",PA18="on",PA19="on",PA20="on",PA77="on",PA92="on",PA93="on",PA94="on",PA95="on")
    else:
        data = {}
        data[si_ville] = "on"
        data["numero"] = si_numero
    r = requests.post("http://invader.spotter.free.fr/listing.php", data=data, allow_redirects=True) #Requête sur le site avec la variable précédente en méthode POST (page)
    soup = BeautifulSoup(r.content, 'html.parser') #Parsing de la page récupérée
    regex_1 = re.compile('^haut') #Définition du regex
    infos_1 = soup.find_all('tr', attrs={'class': regex_1}) #Enregistrement de l'ensemble des blocs <tr> dans une liste
    #Pour chaque bloc, on trie les données :
    for tr in infos_1:
        #points -------------------------------- Points que rapporte le SI
        si_points =  tr.b.getText().split('[')[1].split(' pts]')[0]
        #condition -------------------------------------------- Etat du SI
        si_condition = tr.font.getText().split('connu :  ')[1].split('Date')[0]
        #image ----------------------------------------------- Image du SI
        si_image=[]
        for td in tr.find_all("td"): #Il y a 3 colonnes
            if len(td.find_all("img"))!=0:
                if td.find_all("img")[0].has_attr('class'):
                    if td.find_all("img")[0]['class'][0] != "banniere":
                        si_image.append(td.find_all("img")[0]['src'])
                else:
                    si_image.append(td.find_all("img")[0]['src'])
    si_spotter = si_ville+"_"+si_numero
    if len(infos_1)==0:
        await ctx.send("Ce SI n'existe pas ou n'est pas répertorié ("+si_spotter+")")
        return
    si_instagram = si_ville+"_"+si_numero.lstrip("0").zfill(2)
    if si_condition == "OK" or si_condition == "Un peu dégradé" :
        color_value = 0x00ff00
    elif si_condition == "Dégradé" :
        color_value = 0xffaa00
    elif si_condition == "Très dégradé" or si_condition == "Détruit !" :
        color_value = 0xff0000
    else :
        color_value = 0xb1b1b1
    embed=discord.Embed(color=color_value, title=si_spotter, description="Condition : "+si_condition+"\nPoints : "+si_points+" pts\n[SPOTTER](http://invaders.art.free.fr/invaderspotter_recherchesi.php?si="+si_spotter+") [INSTAGRAM](https://www.instagram.com/explore/tags/"+si_instagram+")")
    embed.set_thumbnail(url="http://invader.spotter.free.fr/"+si_image[0])
    print("Affichage de "+si_spotter)
    await ctx.send(embed=embed)

# -------------------- FONCTIONS INUTILES --------------------
@bot.command()
async def coucou(ctx):
    await ctx.send("Coucou !")
@bot.command()
async def bienvenue(ctx):
    await ctx.send("Merci "+ctx.author.mention+" !")

'''@slash.slash(name="quiz", guild_ids=[730904034608676907], description="Quiz de test")
async def quiz(ctx):
    select = create_select(
        options=[
            create_select_option("Haha tRoP mArRaNt lOl", value="1", emoji="😂"),
            create_select_option("...", value="2", emoji="😏"),
            create_select_option("friendzone", value="3", emoji="💛"),
            create_select_option("renard", value="4", emoji="🦊"),        await choice_ctx.send("Bonne réponse ! 🦊")
    else:
        message = ctx.message
        await message.delete()
        await choice_ctx.send("Mauvaise réponse... 😒")
'''

# -------------------- DEMARRAGE DU BOT --------------------
bot.run(os.environ['TOKEN'])
