import argparse
import os
import json
from colorthief import ColorThief
import climage

CONFIG_PATH = os.path.expanduser("~/.colourpeek_config.json")


def rgb_to_ansi(r, g, b):
    return f"\033[48;2;{r};{g};{b}m  \033[0m"


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)


def ask_truecolor_support():
    print("🌈 Does your terminal support true color (24-bit)?")
    print("If you're not sure, test at https://www.nordtheme.com/docs/ports/terminal-usage")
    while True:
        ans = input("Type 'y' for yes or 'n' for no: ").strip().lower()
        if ans in ['y', 'n']:
            return ans == 'y'


def main():
    parser = argparse.ArgumentParser(description="Preview image and extract dominant colors.")
    parser.add_argument("image", help="Path to the image file")
    parser.add_argument("-n", "--num", type=int, default=8, help="Number of colors to extract")
    parser.add_argument("--truecolor", choices=["yes", "no", "ask"], help="Manually set truecolor")
    parser.add_argument("--remember", action="store_true", help="Remember terminal setting after this run")
    parser.add_argument("--forget", action="store_true", help="Forget saved setting")
    args = parser.parse_args()

    config = {} if args.forget else load_config()
    supports_truecolor = None

    if args.truecolor == "yes":
        supports_truecolor = True
    elif args.truecolor == "no":
        supports_truecolor = False
    elif args.truecolor == "ask":
        supports_truecolor = ask_truecolor_support()
    elif "truecolor" in config:
        supports_truecolor = config["truecolor"]
    else:
        supports_truecolor = ask_truecolor_support()

    image_path = os.path.expanduser(args.image)

    # Try preview
    try:
        output = climage.convert(
            image_path,
            is_unicode=True,
            is_truecolor=supports_truecolor,
            is_256color=not supports_truecolor,
            is_8color=False
        )
        print(output)
    except Exception as e:
        print(f"⚠️  Image preview failed: {e}\n")

    # Always show color palette
    print("🎨 Color previews:")
    try:
        ct = ColorThief(image_path)
        palette = ct.get_palette(color_count=args.num)
        for (r, g, b) in palette:
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            block = rgb_to_ansi(r, g, b) if supports_truecolor else ""
            print(f"  {block} {hex_color} (RGB: {r}, {g}, {b})")
    except Exception as e:
        print(f"Could not extract palette: {e}")

    # Ask to remember setting if not already saved and not forced
    if "truecolor" not in config and not args.forget and not args.truecolor:
        remember = input("\n❓ Do you want to remember this setting for future runs? (y/n): ").strip().lower()
        if remember == "y" or args.remember:
            config["truecolor"] = supports_truecolor
            save_config(config)
            print("✅ Setting saved.")
        else:
            print("ℹ️  Will ask again next time.")


if __name__ == "__main__":
    main()

