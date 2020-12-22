# -------------------- IMPORT DES LIBRAIRIES --------------------
#Librairie Discord
import discord
from discord.ext import commands

#Librairies nécessaires au scrap
import requests #Afin de pouvoir accéder à une page web avec une requête POST
from bs4 import BeautifulSoup #Scrapping simplifié
import re #Regex

#Librairie permettant l'accès aux variables d'environnement
import os

# -------------------- INITIALISATION DU BOT --------------------
bot = commands.Bot(command_prefix = "!", description = "Bot informatif sur les Space Invaders")
bot.remove_command('help')
api_token = os.environ['API_TOKEN']

# -------------------- FONCTIONS DE DEBUG --------------------
#Fonction appelée lorsque le bot est prêt
@bot.event
async def on_ready():
    print("Bot prêt !")

# -------------------- FONCTIONS UTILES --------------------
#Affichage de l'aide
@bot.command(aliases=['help', 'helpou', 'liste', 'commandes'])
async def aide(ctx):
    description_content = "Ce robot fonctionne sur le serveur mais aussi par message privé, vous pouvez simplement lui écrire et il vous répondra.\n\n"
    description_content += "**Liste des commandes :**\n\n"
    description_content += "**!infos_serveur** : affiche les informations du serveur\n"
    description_content += "**!aliases** : affiche les aliases des différentes commandes\n"
    description_content += "**!si VILLE_NUMERO** : affiche les informations d'un SI - exemple : !si PA_1200\n"
    description_content += "**!ville VILLE** : affiche les informations d'une ville - exemple : !ville Paris ou !ville PA\n"
    description_content += "**!mes_infos SERVICE PSEUDO** : met à jour mes informations - exemple : !mes_infos instagram Raphystole *!Confidentialité pour connaitre l'utlisation de tes données*\n"
    description_content += "*Vos informations ne seront pas divulguées hors de ce robot. Celles-ci sont conservées pendant une durée de 3 ans maximum et peuvent être détruites sur simple demande ou en utilisant la commande dédiée.*\n"
    embed=discord.Embed(color=0x04ff00, title="Fonctionnement du robot :", description=description_content)
    await ctx.send(embed=embed)

#Affichage des aliases
@bot.command(aliases=['alias'])
async def aliases(ctx):
    description_content = ""
    description_content += "**!aide** = !help, !helpou, !liste, !commandes\n" 
    description_content += "**!mes_infos** : !mesinfos, !mi, !maj, !modifier"
    embed=discord.Embed(color=0x04ff00, title="Liste des aliases :", description=description_content)
    await ctx.send(embed=embed)

#Mettre à jour ses données utilisateur
@bot.command(aliases=['mesinfos', 'modifier', 'mi', 'maj'])
async def mes_infos(ctx, account_type, username):
    account_type = account_type.lower()
    account_type = account_type.replace("flashinvaders", "flash_invaders").replace("site", "website").replace("webwebsite", "website").replace("spotter-invader", "spotter")
    if account_type in ["flash_invaders","website","instagram","flickr","spotter"]:
        url_api = "http://invaders.art.free.fr/botsi/users.php?controller=set_"+account_type+"&id_discord="+str(ctx.message.author.id)+"&"+account_type+"="+username+"&api_token="+api_token
        requests.get(url_api)
        account_type = account_type.replace("flash_invaders", "pseudo FlashInvaders").replace("instagram", "pseudo Instagram").replace("spotter", "pseudo Spotter-Invader").replace("flickr", "pseudo Flickr").replace("website", "site internet")
        await ctx.send("Ton "+account_type+" a bien été mis à jour !")
    else :
        await ctx.send("Ce service n'est pas pris en compte par le robot.\nServices pris en compte : FlashInvader, Instagram, Flickr, Spotter-Invader, Website.")

#Mettre à jour ses données utilisateur
@bot.command(aliases=['i'])
async def infos(ctx, user: discord.User):
    r = requests.get("http://invaders.art.free.fr/botsi/users.php?controller=get_all&id_discord="+str(user.id)+"&api_token="+api_token).json()
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
        embed=discord.Embed(color=0x04ff00, title="Informations sur "+str(user).rsplit("#",1)[0], description=embed_description)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

#Mettre à jour ses données utilisateur
@bot.command(aliases=['map', 'invasion_map','invasionmap'])
async def carte(ctx, map_number):
    r = requests.get("http://invaders.art.free.fr/botsi/maps.php?controller=get_map&map_number="+map_number).json()
    is_blank = True
    embed_description = ""
    if r["city"]:
        embed_description = "**Ville :** "+r["city"]+"\n"
        is_blank = False
    if r["release_date"]:
        embed_description += "**Date de sortie :** "+str(r["release_date"])+"\n"
        is_blank = False
    embed_description += "[Voir la carte complète](http://invaders.art.free.fr/botsi/maps?controller=map&map="+map_number+")"
    if is_blank :
        await ctx.send("Cette carte n'existe pas")
    else :
        embed=discord.Embed(color=0x04ff00, title="Informations sur la carte numéro : "+map_number, description=embed_description)
        embed.set_image(url=r["cover_img_link"])
        await ctx.send(embed=embed)

#Affichage des infos du serveur
@bot.command()
async def infos_serveur(ctx):
    server = ctx.guild
    numberOfTextChannels = len(server.text_channels)
    numberOfPeople = server.member_count
    serverName = server.name
    message = f"Le serveur **{serverName}** contient **{numberOfPeople} personnes** et possède **{numberOfTextChannels} salons textuels**."
    await ctx.send(message)

#Affichage des infos sur une ville
@bot.command()
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
@bot.command()
async def si(ctx, si):
    si_split = si.split("_")
    if len(si_split) != 2:
        await ctx.send("Le format du SI n'est pas bon")
    si_ville = si_split[0].upper()
    si_numero = si_split[1].lstrip("0")
    if si_ville == "PA":
        zfill_value = 4
    elif si_ville == "LDN" or si_ville == "HK" or si_ville == "LA" or si_ville == "NY" or si_ville == "TK":
        zfill_value = 3  
    else:
        zfill_value = 2
    si_numero = si_numero.zfill(zfill_value)
    if si_ville=="PA":
        data = dict(numero=si_numero,prs="on",toutparis="on",PA01="on",PA02="on",PA03="on",PA04="on",PA05="on",PA06="on",PA07="on",PA08="on",PA09="on",PA10="on",PA11="on",PA12="on",PA13="on",PA14="on",PA15="on",PA16="on",PA17="on",PA18="on",PA19="on",PA20="on",PA77="on",PA92="on",PA93="on",PA94="on")
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

# -------------------- DEMARRAGE DU BOT --------------------
bot.run(os.environ['TOKEN'])
