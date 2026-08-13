import os

folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "images"
)

print("IMAGE FOLDER:")
print(folder)

if not os.path.exists(folder):
    print("images folder NOT FOUND")
else:
    files = os.listdir(folder)

    for f in files:
        print(f)