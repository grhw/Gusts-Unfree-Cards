from PIL import Image
import shutil
import os

final = []
config = []
images = {}
shutil.rmtree("generated/")
os.makedirs("generated/build/assets/")
os.makedirs("generated/dist/")
os.makedirs("generated/temp/")

for g in os.listdir("src/globals/"):
    with open("src/globals/" + g,"r") as f:
        final.append(f"local {g.split(".")[0]} = (function()\n{f.read()}\nend)()")

config.append("local Config = {\nJokers = {\n")

print("Generating Jokers...")
for joker_category in os.listdir("src/jokers/"):
    i = 0
    jokers = os.listdir("src/jokers/" + joker_category)
    final_img = Image.new("RGBA",((len(jokers)//2)*71,95))
    final.append(f"if Config.Jokers.{joker_category} then")
    final.append(f"Utils.atlas(\"{joker_category}\")")
    for joker in jokers:
        if joker.endswith(".lua"):
            print("\t",joker)
            joker_image = Image.open("src/jokers/" + joker_category + "/" + joker.replace(".lua",".png"))
            final_img.paste(joker_image,(i*71,0),joker_image)
            
            with open("src/jokers/" + joker_category + "/" + joker,"r") as f:
                c = f.read()
                c = c.replace("atlas","pos = {" f"x = {i}, y = {0}" "},\natlas")
                final.append(f"local joker_{joker.split(".")[0]} = (function()\n{c}\nend)()")
            i += 1
    final.append("end")
    images[joker_category + ".png"] = final_img
    config.append(joker_category + " = true,")

config.append("\n}\n}")
print("Generating decks...")

for deck in os.listdir("src/decks/"):
    print("\t",deck)
    with open("src/decks/" + deck,"r") as f:
        final.append(f"local deck_{g.split(".")[0]} = (function()\n{f.read()}\nend)()")

with open("src/hooks.lua", "r") as f:
    final.append(f"; (function()\n{f.read()}\nend)()")
shutil.copy("src/config.json","generated/build/GustsUnfreeCards.json")

with open("generated/temp/raw.lua","w+") as f:
    f.write("\n".join(final))
with open("generated/temp/raw_config.lua","w+") as f:
    f.write("\n".join(config))
os.system("./luau-format generated/temp/raw.lua --output=generated/temp/formatted.lua --optimize")
os.system("./luau-format generated/temp/raw_config.lua --output=generated/temp/config.lua --optimize")

print("Generating images...")

os.makedirs("generated/build/assets/1x/")
os.makedirs("generated/build/assets/2x/")

for path in images.keys():
    print("\t",path)
    images[path].save("generated/build/assets/1x/" + path)
    w,h = images[path].size
    images[path].resize((w*2,h*2),Image.Resampling.NEAREST).save("generated/build/assets/2x/" + path)

with open("generated/build/main.lua","w+") as f:
    with open("src/header.lua","r") as header:
        with open("src/after_config.lua","r") as after_config:
            with open("generated/temp/formatted.lua","r") as formatted:
                with open("generated/temp/config.lua","r") as config:
                    f.write("\n".join([header.read(),config.read(),after_config.read(),formatted.read()]))