import os
from tkinter import Tk, filedialog
from PIL import Image, ImageDraw, ImageFont


def choose_file():
    """Opens a file dialog and returns the selected file path."""
    root = Tk()
    root.withdraw()
    root.update()
    file_path = filedialog.askopenfilename(title="Wybierz obraz", filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")])
    return file_path if file_path else None


def choose_folder():
    """Opens a folder selection dialog and returns the selected folder path."""
    root = Tk()
    root.withdraw()
    root.update()
    folder_path = filedialog.askdirectory(title="Wybierz folder docelowy")
    return folder_path if folder_path else None


def add_text_watermark(image_path, output_folder, watermark_text="Watermark", position=(10, 10)):
    """Adds a text watermark to an image."""
    image = Image.open(image_path).convert("RGBA")
    watermark_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(watermark_layer)

    font = ImageFont.load_default()
    draw.text(position, watermark_text, font=font, fill=(255, 255, 255, 128))

    watermarked_image = Image.alpha_composite(image, watermark_layer)
    output_path = os.path.join(output_folder, "watermarked_text.jpg")
    watermarked_image.convert("RGB").save(output_path, "JPEG")
    print(f"✅ Plik zapisany jako: {output_path}")


def main():
    print("📂 Wybierz plik obrazu...")
    image_path = choose_file()
    if not image_path:
        print("❌ Nie wybrano pliku.")
        return

    print("📂 Wybierz folder docelowy...")
    output_folder = choose_folder()
    if not output_folder:
        print("❌ Nie wybrano folderu.")
        return

    text = input("Podaj tekst watermarka: ")
    add_text_watermark(image_path, output_folder, text)


if __name__ == "__main__":
    main()
