import os
import glob
import subprocess
import re

# 1. Update App Name to WED+CAL in strings.xml
strings_path = "android/app/src/main/res/values/strings.xml"
if os.path.exists(strings_path):
    with open(strings_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = re.sub(r'<string name="app_name">.*?</string>', '<string name="app_name">WED+CAL</string>', content)
    content = re.sub(r'<string name="title_activity_main">.*?</string>', '<string name="title_activity_main">WED+CAL</string>', content)
    with open(strings_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✓ App name changed to WED+CAL in strings.xml")

# 2. Find logo file in repo
images = glob.glob("./*.png") + glob.glob("./*.jpg") + glob.glob("./*/*.png") + glob.glob("./*/*.jpg")
valid_images = [img for img in images if not img.startswith("./android") and not img.startswith("./.git")]

if not valid_images:
    print("⚠️ Warning: No image found, skipping icon generation.")
    exit(0)

logo_src = valid_images[0]
print(f"Applying Logo from: {logo_src}")

res_dir = "android/app/src/main/res"

# 3. Generate PNGs for all standard densities
sizes = {
    "mipmap-mdpi": (48, 108),
    "mipmap-hdpi": (72, 162),
    "mipmap-xhdpi": (96, 216),
    "mipmap-xxhdpi": (144, 324),
    "mipmap-xxxhdpi": (192, 432)
}

for folder, (size, fg_size) in sizes.items():
    target_dir = os.path.join(res_dir, folder)
    os.makedirs(target_dir, exist_ok=True)
    subprocess.run(["convert", logo_src, "-resize", f"{size}x{size}!", os.path.join(target_dir, "ic_launcher.png")])
    subprocess.run(["convert", logo_src, "-resize", f"{size}x{size}!", os.path.join(target_dir, "ic_launcher_round.png")])
    subprocess.run(["convert", logo_src, "-resize", f"{fg_size}x{fg_size}!", os.path.join(target_dir, "ic_launcher_foreground.png")])

# 4. Adaptive XML files
anydpi_dir = os.path.join(res_dir, "mipmap-anydpi-v26")
os.makedirs(anydpi_dir, exist_ok=True)

xml_adaptive = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
"""

with open(os.path.join(anydpi_dir, "ic_launcher.xml"), "w", encoding="utf-8") as f:
    f.write(xml_adaptive)
with open(os.path.join(anydpi_dir, "ic_launcher_round.xml"), "w", encoding="utf-8") as f:
    f.write(xml_adaptive)

# 5. Background Color
values_dir = os.path.join(res_dir, "values")
os.makedirs(values_dir, exist_ok=True)
with open(os.path.join(values_dir, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#11080a</color>
</resources>
""")

print("✓ Android Logo & App Name successfully applied!")
