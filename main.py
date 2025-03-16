from PIL import Image
import shutil
import os

shutil.rmtree("generated/", ignore_errors=True)
for path in [
    "generated/build/assets/",
    "generated/dist/",
    "generated/temp/",
    "generated/build/assets/1x/",
    "generated/build/assets/2x/"
]:
    os.makedirs(path, exist_ok=True)

final = []
config = ["local Config = {\nJokers = {\n"]
images = {}

for g in os.listdir("src/globals/"):
    name, _ = os.path.splitext(g)
    with open(os.path.join("src/globals", g), "r") as f:
        final.append(f"local {name} = (function()\n{f.read()}\nend)()")

print("Generating Jokers...")
for category in os.listdir("src/jokers/"):
    jokers = [j for j in os.listdir(os.path.join("src/jokers", category)) if j.endswith(".lua")]
    if not jokers:
        continue

    final_img = Image.new("RGBA", ((len(jokers) // 2) * 71, 95))
    final.append(f"if Config.Jokers.{category} then\nUtils.atlas(\"{category}\")")

    for i, joker in enumerate(jokers):
        print("\t", joker)
        base_name, _ = os.path.splitext(joker)

        joker_image = Image.open(os.path.join("src/jokers", category, base_name + ".png"))
        final_img.paste(joker_image, (i * 71, 0), joker_image)

        with open(os.path.join("src/jokers", category, joker), "r") as f:
            c = f.read().replace("atlas", f"pos = {{x = {i}, y = 0}},\natlas")
            final.append(f"local joker_{base_name} = (function()\n{c}\nend)()")

    final.append("end")
    images[f"{category}.png"] = final_img
    config.append(f"{category} = true,")

config.append("\n}\n}")

print("Generating decks...")
for deck in os.listdir("src/decks/"):
    print("\t", deck)
    name, _ = os.path.splitext(deck)
    with open(os.path.join("src/decks", deck), "r") as f:
        final.append(f"local deck_{name} = (function()\n{f.read()}\nend)()")

with open("src/hooks.lua", "r") as f:
    final.append(f"; (function()\n{f.read()}\nend)()")

shutil.copy("src/config.json", "generated/build/GustsUnfreeCards.json")

with open("generated/temp/raw.lua", "w+") as f:
    f.write("\n".join(final))
with open("generated/temp/raw_config.lua", "w+") as f:
    f.write("\n".join(config))

os.system("./luau-format generated/temp/raw.lua --output=generated/temp/formatted.lua --optimize")
os.system("./luau-format generated/temp/raw_config.lua --output=generated/temp/config.lua --optimize")

print("Generating images...")
for path, img in images.items():
    print("\t", path)
    img.save(os.path.join("generated/build/assets/1x", path))
    w, h = img.size
    img.resize((w * 2, h * 2), Image.Resampling.NEAREST).save(os.path.join("generated/build/assets/2x", path))

with open("generated/build/main.lua", "w+") as f_main:
    with open("src/header.lua", "r") as f_header, \
         open("generated/temp/config.lua", "r") as f_config, \
         open("src/after_config.lua", "r") as f_after_config, \
         open("generated/temp/formatted.lua", "r") as f_formatted:
        f_main.write("\n".join([
            f_header.read(),
            f_config.read(),
            f_after_config.read(),
            f_formatted.read()
        ]))
