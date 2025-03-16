from PIL import Image
import shutil
import os

final = []
category_images = {}
config = []
shutil.rmtree("generated/")
os.makedirs("generated/build/assets/")
os.makedirs("generated/dist/")
os.makedirs("generated/temp/")

for g in os.listdir("src/globals/"):
    with open("src/globals/" + g,"r") as f:
        final.append(f"local {g.split(".")[0]} = (function()\n{f.read()}\nend)()")

config.append("local Config = {\nJokers = {\n")

for joker_category in os.listdir("src/jokers/"):
    i = 0
    category_images[joker_category] = []
    final.append(f"if Config.Jokers.{joker_category} then")
    for joker in os.listdir("src/jokers/" + joker_category):
        if joker.endswith(".lua"):
            with open("src/jokers/" + joker_category + "/" + joker,"r") as f:
                c = f.read()
                c = c.replace("atlas","pos = {" f"x = {i}, y = {0}" "},\natlas")
                final.append(f"local joker_{joker.split(".")[0]} = (function()\n{c}\nend)()")
            i += 1
            
            category_images[joker_category].append(Image.open("src/jokers/" + joker_category + "/" + joker.replace(".lua",".png")))
    final.append("end")
    config.append(joker_category + " = true,")

config.append("\n}\n}")

for category in category_images.keys():
    final_img = Image.new("RGBA",(len(category_images[category])*71,95))
    for i,joker_image in enumerate(category_images[category]):
        final_img.paste(joker_image,(i*71,0),joker_image)
    
    final_img.save("generated/build/assets/" + category + ".png")

for deck in os.listdir("src/decks/"):
    with open("src/decks/" + deck,"r") as f:
        final.append(f"local deck_{g.split(".")[0]} = (function()\n{f.read()}\nend)()")

with open("src/hooks.lua", "r") as f:
    final.append(f"; (function()\n{f.read()}\nend)()")
shutil.copy("src/config.json","generated/build/Gusts_Unfree_Cards.json")

with open("generated/temp/raw.lua","w+") as f:
    f.write("\n".join(final))
with open("generated/temp/raw_config.lua","w+") as f:
    f.write("\n".join(config))
os.system("./luau-format generated/temp/raw.lua --output=generated/temp/formatted.lua --optimize")
os.system("./luau-format generated/temp/raw_config.lua --output=generated/temp/config.lua --optimize")

with open("generated/build/main.lua","w+") as f:
    with open("src/header.lua","r") as header:
        with open("src/after_config.lua","r") as after_config:
            with open("generated/temp/formatted.lua","r") as formatted:
                with open("generated/temp/config.lua","r") as config:
                    f.write("\n".join([header.read(),config.read(),after_config.read(),formatted.read()]))