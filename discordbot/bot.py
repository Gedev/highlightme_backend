import asyncio
import re
from typing import Final, Dict, Any
import os

import discord
from PIL import ImageDraw, Image, ImageFont, ImageFilter
from dotenv import load_dotenv
import requests
from discord import Intents, Client, Message, File, app_commands, Interaction

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

print(TOKEN)

intents: Intents = Intents.default()
intents.message_content = True  # NOQA
intents.guilds = True


def run_bot():
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    client.run(TOKEN)



class MyClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = app_commands.CommandTree(self)

client: MyClient = MyClient(intents=intents)

@client.tree.command(name="ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(client.latency * 1000)}ms")

# Function to extract the WarcraftLogs code from the URL
def extract_code_from_url(url: str) -> str:
    match = re.search(r'warcraftlogs.com/reports/([a-zA-Z0-9]+)', url)
    return match.group(1) if match else None

@app_commands.command(name="highlight", description="Create the highlight for a Warcraftlogs report")
@app_commands.describe(report="URL (www.warcraftlogs.com/reports/ZQdNmfwyWPgkAYF9) Or code (ZQdNmfwyWPgkAYF9)")
async def highlight(interaction: discord.Interaction, report: str = None) -> None:
    discord_pseudo = interaction.user.name
    print(discord_pseudo)
    if report.startswith("http") or report.startswith("www"):
        code = extract_code_from_url(report)
    else:
        code = report

    if not code:
        await interaction.response.send_message("You must provide either a valid WarcraftLogs code or URL.", ephemeral=True)
        return

    # Check if highlights already exist
    existing_data = check_existing_highlights(code)

    if existing_data.get('status') == 'exists':
        frontend_url = existing_data.get('url')
        response = f"Highlights for the report {code} already exist.\n[View Full Report]({frontend_url})"
        await interaction.response.send_message(response)
        return

    await interaction.response.send_message("Processing your request, this may take a few seconds...")
    initial_message = await interaction.original_response()

    # Loading animation
    loading_messages = ["Processing your request",
                        "Processing your request..",
                        "Processing your request...",
                        ]

    for i in range(1):
        for message in loading_messages:
            await initial_message.edit(content=message)
            await asyncio.sleep(0.5)

    backend_data = send_to_backend(code, discord_pseudo)

    # loading_messages2 = [
    #     "Need more time processing",
    #     "No worries, the app can handle it",
    #     "But it's quite unusual...",
    #     "Have you played the game before ?",
    #     "Goddamit, what is that ?",
    #     "Nevermind, It's almost finished",
    # ]
    #
    # for i in range(1):
    #     for message in loading_messages2:
    #         await initial_message.edit(content=message)
    #         await asyncio.sleep(2)

    if backend_data:
        filename = "report_preview.png"
        create_image_with_data(backend_data, filename)

        frontend_url = f"https://raid-highlights.netlify.app/?report_code={code}"
        response = f"Preview of the Highlights for the report {code} has been created.\n[View Full Report]({frontend_url})"
        await interaction.followup.send(response, file=File(filename))
    else:
        await interaction.followup.send(f"Failed to send Report Code {code} to the backend.")

client.tree.add_command(highlight)


# STEP 2: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running !')

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    await client.tree.sync()



# Function to create the image with the extracted data
def create_image_with_data(data: Dict[str, Any], filename: str) -> None:
    width, height = 1200, 600  # Previous ideal size for Discord
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)
    font_path = "arial.ttf"  # You can replace with a path to your preferred font

    # Create a blank image with white background
    image = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(image)

    # Load a font
    try:
        font = ImageFont.truetype(font_path, 20)
    except IOError:
        font = ImageFont.load_default()

    # Load the individual images
    images_info = {
        "Maxupgrade": "../static/assets/img/dwarf-looting.png",
        "Max_healthstones_used": "../static/assets/img/elf-drinking.jpg",
        "Deaths": "../static/assets/img/Gnomish-grave-digger.jpg"
    }

    x_offsets = [0, 300, 900]
    widths = [300, 600, 300]
    card_height = 600
    border_size = 40
    border_color = (0, 0, 0)  # Black border

    for i, (key, img_path) in enumerate(images_info.items()):
        # Open the image
        card_image = Image.open(img_path)
        card_image = card_image.resize((widths[i], card_height), Image.LANCZOS)  # Resize to fit

        # Apply blur to the cards on the ends
        if i != 1:
            card_image = card_image.filter(ImageFilter.BLUR)

        # Add border to the image
        bordered_image = Image.new('RGB', (widths[i] + 2 * border_size, card_height + 2 * border_size), border_color)
        bordered_image.paste(card_image, (border_size, border_size))

        # Paste the image onto the main canvas
        image.paste(card_image, (x_offsets[i], 0))

        # Add the data text onto the image
        y_text = 10
        if key in data:
            draw.text((x_offsets[i] + 10, y_text), f"{key}:", fill=text_color, font=font)
            y_text += 30
            for player_id, player_info in data[key].items():
                for k, v in player_info.items():
                    text = f"{k.capitalize()}: {v}"
                    draw.text((x_offsets[i] + 20, y_text), text, fill=text_color, font=font)
                    y_text += 20
            y_text += 10

    # Save the combined image
    image.save(filename)


# STEP 3: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    print(f'Debug: Message object - {message}')

    username: str = str(message.author)
    channel: str = str(message.channel)
    user_message: str = message.content

    print(f'Debug: Username - {username}')
    print(f'Debug: User Message - {user_message}')
    print(f'Debug: Channel - {channel}')

    command_prefix = "!sendcode "
    if user_message.startswith(command_prefix):
        report_code = user_message[len(command_prefix):]
        print(f"Report Code to send: {report_code}")
        backend_data = send_to_backend(report_code)

        if backend_data:
            filename = "report_preview.png"
            create_image_with_data(backend_data, filename)
            response = f"Preview of the Higlights for the report {report_code} has been created."
            await send_message(message, response, filename)
        else:
            response = f"Failed to send Report Code {report_code} to the backend."
            await send_message(message, response, "")

        return

    embed_data = []

    if len(message.embeds) > 0:
        for embed in message.embeds:
            embed_info = {'username': username, 'is_private': False}
            if embed.title:
                embed_info['title'] = embed.title
            if embed.description:
                embed_info['description'] = embed.description
            if embed.fields:
                embed_info['fields'] = {field.name: field.value for field in embed.fields}
            if embed.footer:
                embed_info['footer'] = embed.footer.text
            if embed.author:
                embed_info['author'] = embed.author.name

            embed_data.append(embed_info)

    print(f'Embed Data: {embed_data}')

    print(f'[{channel}] {username} - {embed_data}')
    await send_message(message, str(embed_data), "")


# STEP 4: MESSAGE FUNCTIONALITY
async def send_message(message: Message, response: str, filename: str) -> None:
    print("=== Send message function ===")
    try:
        await message.channel.send(response, file=File(filename))
    except Exception as e:
        print(e)


def send_to_backend(report_code: str, discord_pseudo: str) -> Dict[str, Any]:
    # backend_url = "http://localhost:8000/api/"
    backend_url = "https://highlightmebackend-production.up.railway.app/api/"
    payload = {
        'wl_report_code': report_code,
        'discord_pseudo': discord_pseudo
    }

    try:
        response = requests.post(backend_url, json=payload)
        response.raise_for_status()
        print(f"Successfully sent report code to backend: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send report code to backend: {e}")
        return {}

def check_existing_highlights(report_code: str) -> Dict[str, Any]:
    backend_url = f"http://localhost:8000/report/check_highlights_existence/{report_code}"

    try:
        response = requests.get(backend_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to check existing highlights for report code {report_code}: {e}")
        return {}



# STEP 5: MAIN ENTRY POINT
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
