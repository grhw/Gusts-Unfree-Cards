from PIL import Image
import shutil
import json
import os

def setup_directories():
    shutil.rmtree("generated/", ignore_errors=True)
    paths = [
        "generated/build/assets/",
        "generated/dist/",
        "generated/temp/",
        "generated/build/assets/1x/",
        "generated/build/assets/2x/"
    ]
    for path in paths:
        os.makedirs(path, exist_ok=True)

def load_globals():
    globals_code = []
    for g in os.listdir("src/globals/"):
        name, _ = os.path.splitext(g)
        with open(os.path.join("src/globals", g), "r") as f:
            globals_code.append(f"local {name} = (function()\n{f.read()}\nend)()")
    return globals_code

def process_generic(category_type, config_name, final_code, images, config):
    base_path = f"src/{category_type}/"
    print(f"Generating {config_name}...")
    
    for category in os.listdir(base_path):
        items = [f for f in os.listdir(os.path.join(base_path, category)) if f.endswith(".lua")]
        if not items:
            continue
        
        final_img = Image.new("RGBA", (len(items) * 71, 95))
        final_code.append(f"if Config.{config_name}.{category} then\nUtils.atlas(\"{category}\")")
        
        for i, item in enumerate(items):
            print("\t", item)
            base_name, _ = os.path.splitext(item)
            
            image_path = os.path.join(base_path, category, base_name + ".png")
            if os.path.exists(image_path):
                item_image = Image.open(image_path)
                final_img.paste(item_image, (i * 71, 0), item_image)
            
            with open(os.path.join(base_path, category, item), "r") as f:
                c = f.read().replace("atlas", f"pos = {{x = {i}, y = 0}},\natlas")
                final_code.append(f"local {category_type}_{base_name} = (function()\n{c}\nend)()")
        
        final_code.append("end")
        images[f"{category}.png"] = final_img
        config.append(f"{category} = true,")

def process_decks(final_code):
    print("Generating decks...")
    for deck in os.listdir("src/decks/"):
        print("\t", deck)
        name, _ = os.path.splitext(deck)
        with open(os.path.join("src/decks", deck), "r") as f:
            final_code.append(f"local deck_{name} = (function()\n{f.read()}\nend)()")

def generate_lua_files(final_code, config):
    with open("generated/temp/raw.lua", "w+") as f:
        f.write("\n".join(final_code))
    with open("generated/temp/raw_config.lua", "w+") as f:
        f.write("\n".join(config))
    os.system("./luau-format generated/temp/raw.lua --output=generated/temp/formatted.lua --optimize")
    os.system("./luau-format generated/temp/raw_config.lua --output=generated/temp/config.lua --optimize")

def generate_images(images):
    print("Generating images...")
    for path, img in images.items():
        print("\t", path)
        img.save(os.path.join("generated/build/assets/1x", path))
        w, h = img.size
        img.resize((w * 2, h * 2), Image.Resampling.NEAREST).save(os.path.join("generated/build/assets/2x", path))

def assemble_main_lua():
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

def package_mod():
    os.makedirs("generated/temp/package/")
    print("Done. Packaging mod...")
    with open("src/config.json","r") as f:
        v = json.loads(f.read())["version"]
    print("Version v" + v)
    shutil.copytree("generated/build/", f"generated/temp/package/GustsUnfreeCards-v{v}")
    os.system(f'cd ./generated/temp/package/ && zip -r "../../dist/GustsUnfreeCards-{v}.zip" ./')

setup_directories()

final_code = load_globals()
config = ["local Config = {\nJokers = {\n"]
images = {}

process_generic("jokers", "Jokers", final_code, images, config)
process_generic("tarots", "TarotCards", final_code, images, config)

config.append("\n}\n}")
process_decks(final_code)

with open("src/hooks.lua", "r") as f:
    final_code.append(f"; (function()\n{f.read()}\nend)()")

shutil.copy("src/config.json", "generated/build/GustsUnfreeCards.json")
generate_lua_files(final_code, config)
generate_images(images)
assemble_main_lua()
package_mod()
