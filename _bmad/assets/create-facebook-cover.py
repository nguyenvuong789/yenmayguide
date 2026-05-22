from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT = Path("/Users/vincent/Sites/Yen May Vintage")
SRC = ROOT / "Yên Mây Store" / "1.jpg"
OUT_DIR = ROOT / "_bmad" / "assets"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1640, 624
paper = (245, 239, 230)
cream = (255, 250, 241)
kraft = (216, 195, 165)
taupe = (184, 169, 154)
ink = (42, 33, 26)
muted = (110, 96, 82)
clay = (139, 87, 56)

def font(path, size):
    return ImageFont.truetype(path, size)

display = "/System/Library/Fonts/NewYork.ttf"
serif = "/System/Library/Fonts/Supplemental/Georgia.ttf"
sans = "/System/Library/Fonts/HelveticaNeue.ttc"

img = Image.open(SRC).convert("RGB")

# Source slide 1 contains a useful real-shop photo band between the deck header and title block.
photo_band = img.crop((0, 122, 1920, 700))
photo_band = ImageEnhance.Color(photo_band).enhance(0.90)
photo_band = ImageEnhance.Contrast(photo_band).enhance(0.96)
photo_band = ImageEnhance.Brightness(photo_band).enhance(1.02)

cover = Image.new("RGB", (W, H), paper)
draw = ImageDraw.Draw(cover)

# Subtle paper texture.
for x in range(0, W, 8):
    draw.line((x, 0, x, H), fill=(235, 226, 212), width=1)

# Right photo field.
photo_w = 1000
photo_h = H
scale = max(photo_w / photo_band.width, photo_h / photo_band.height)
resized = photo_band.resize((int(photo_band.width * scale), int(photo_band.height * scale)), Image.Resampling.LANCZOS)
left = (resized.width - photo_w) // 2
top = (resized.height - photo_h) // 2
photo = resized.crop((left, top, left + photo_w, top + photo_h))

# Warm wash so it fits the brand palette.
wash = Image.new("RGB", (photo_w, photo_h), kraft)
photo = Image.blend(photo, wash, 0.16)
cover.paste(photo, (W - photo_w, 0))

# Soft gradient over photo for calmer Facebook cover readability.
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)
for i in range(photo_w):
    alpha = int(172 * (1 - i / photo_w))
    od.line((W - photo_w + i, 0, W - photo_w + i, H), fill=(245, 239, 230, alpha), width=1)
cover = Image.alpha_composite(cover.convert("RGBA"), overlay).convert("RGB")
draw = ImageDraw.Draw(cover)

# Left editorial panel.
panel_x, panel_y = 240, 78
panel_w, panel_h = 635, 430
draw.rounded_rectangle((panel_x, panel_y, panel_x + panel_w, panel_y + panel_h), radius=8, fill=(255, 250, 241), outline=(205, 189, 169), width=2)
draw.rectangle((panel_x, panel_y, panel_x + 9, panel_y + panel_h), fill=(79, 95, 72))

draw.text((panel_x + 42, panel_y + 42), "Yên Mây", font=font(display, 92), fill=ink)
draw.text((panel_x + 47, panel_y + 138), "VINTAGE", font=font(serif, 34), fill=clay)

line_y = panel_y + 206
draw.line((panel_x + 46, line_y, panel_x + 486, line_y), fill=taupe, width=2)

draw.text((panel_x + 46, panel_y + 238), "Curated Y2K & vintage in Da Nang", font=font(sans, 31), fill=ink)
draw.text((panel_x + 46, panel_y + 286), "Đồ được chọn kỹ cho người có gu riêng.", font=font(sans, 27), fill=muted)

pill_y = panel_y + 354
draw.rounded_rectangle((panel_x + 46, pill_y, panel_x + 348, pill_y + 50), radius=25, fill=(42, 33, 26), outline=(42, 33, 26), width=1)
draw.text((panel_x + 74, pill_y + 12), "Open daily 10:00-21:00", font=font(sans, 23), fill=cream)

draw.text((panel_x + 376, pill_y + 12), "Get Directions", font=font(sans, 23), fill=clay)

# Small footer line, kept away from likely profile-photo overlap.
draw.text((240, 560), "45/3 An Hai Dong 1, Da Nang  |  0906 452 023", font=font(sans, 24), fill=muted)

png = OUT_DIR / "yen-may-facebook-cover.png"
jpg = OUT_DIR / "yen-may-facebook-cover.jpg"
cover.save(png)
cover.save(jpg, quality=92, optimize=True)

print(png)
print(jpg)
