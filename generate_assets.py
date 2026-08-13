import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import io

# Download profile picture
url = "https://github.com/Kaustav-Mukherjee.png"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    img_data = response.read()
    
img = Image.open(io.BytesIO(img_data)).convert('L') # Convert to grayscale

# Enhance contrast
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.5)

# Convert to ASCII
# Standard dense ASCII characters for better shading
chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
# We might need to invert it depending on whether background is dark or light.
# For dark background, darker pixels -> space, brighter pixels -> @

def image_to_ascii(image, width=70):
    aspect_ratio = image.height / image.width
    # Multiply by 0.5 because characters are roughly twice as tall as they are wide
    new_height = int(aspect_ratio * width * 0.5)
    resized = image.resize((width, new_height))
    
    pixels = list(resized.getdata())
    
    ascii_str = ""
    for i, pixel in enumerate(pixels):
        # Map 0-255 to chars
        idx = int((pixel / 255.0) * (len(chars) - 1))
        ascii_str += chars[idx]
        if (i + 1) % width == 0:
            ascii_str += "\n"
    return ascii_str

base_ascii = image_to_ascii(img, width=70)

frames = []
lines = base_ascii.split('\n')
try:
    font = ImageFont.truetype("arial.ttf", 12)
except IOError:
    font = ImageFont.load_default()

width = 70 * 7
height = len(lines) * 12

bg_color = (13, 17, 23) # 0D1117 (GitHub Page BG) or (22, 27, 34) # 161B22 (GitHub Code Block BG)
# Let's use 0D1117 to blend with the GitHub dark theme page background entirely.
# This way, no border is needed, it just floats beautifully.

for i in range(1, len(lines) + 1):
    frame_img = Image.new('RGB', (width, height), color=(13, 17, 23))
    draw = ImageDraw.Draw(frame_img)
    
    # Draw partial ASCII art
    partial_ascii = "\n".join(lines[:i])
    # White/Light Gray text for the profile picture
    draw.text((10, 10), partial_ascii, fill=(200, 200, 200), font=font)
    frames.append(frame_img)

# Hold the last frame for a while
for _ in range(20):
    frames.append(frames[-1])

frames[0].save('ascii_profile.gif', save_all=True, append_images=frames[1:], duration=80, loop=0)

# Create an iOS/macOS window header SVG
# We will use 0D1117 as background so it blends with the page, giving a clean look
svg_content = """<svg xmlns="http://www.w3.org/2000/svg" width="900" height="30" viewBox="0 0 900 30">
  <rect width="900" height="30" fill="#0D1117" />
  <circle cx="20" cy="15" r="6" fill="#ff5f56" />
  <circle cx="40" cy="15" r="6" fill="#ffbd2e" />
  <circle cx="60" cy="15" r="6" fill="#27c93f" />
</svg>"""
with open('window_header.svg', 'w') as f:
    f.write(svg_content)
    
print("Assets generated successfully!")
