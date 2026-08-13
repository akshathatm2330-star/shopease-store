import os

folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "images"
)

print("IMAGE FOLDER:")
print(folder)

if not os.path.exists(folder):
    print("❌ images folder NOT FOUND")
else:
    print("✅ images folder found")

    supported = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
        ".avif"
    )

    count = 0

    for file in os.listdir(folder):
        if file.lower().endswith(supported):
            print("✅", file)
            count += 1

    print("Total supported images:", count)