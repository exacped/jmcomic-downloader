import os
from PIL import Image

downloads_dir = os.path.join(os.path.dirname(__file__), 'downloads')
output_dir = os.path.join(os.path.dirname(__file__), 'pdf')
exts = {'.webp', '.jpg', '.jpeg', '.png', '.gif', '.bmp'}

os.makedirs(output_dir, exist_ok=True)

for folder in sorted(os.listdir(downloads_dir)):
    folder_path = os.path.join(downloads_dir, folder)
    if not os.path.isdir(folder_path):
        continue

    files = sorted([f for f in os.listdir(folder_path) if os.path.splitext(f)[1].lower() in exts])
    if not files:
        continue

    print(f'Processing: {folder} ({len(files)} pages)')

    images = []
    for f in files:
        img = Image.open(os.path.join(folder_path, f)).convert('RGB')
        images.append(img)

    pdf_name = folder.replace('/', '_').replace('\\', '_').replace(':', '_') + '.pdf'
    pdf_path = os.path.join(output_dir, pdf_name)

    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f'  -> Saved: {pdf_name}')

    for f in files:
        os.remove(os.path.join(folder_path, f))
    print(f'  -> Deleted {len(files)} original images')

    try:
        os.rmdir(folder_path)
    except OSError:
        pass

try:
    os.rmdir(downloads_dir)
    print(f'Deleted: {downloads_dir}')
except OSError:
    pass

print('Done!')
