from PIL import Image
from PIL.ExifTags import TAGS


def get_image_metadata(image_path):
    try:
        image = Image.open(image_path)

        exif_data = image._getexif()

        if exif_data is not None:
            print("Metadane EXIF:")
            for tag, value in exif_data.items():
                tag_name = TAGS.get(tag, tag)
                print(f"{tag_name}: {value}")
        else:
            print("Brak metadanych EXIF w tym obrazie.")

        print("\nPodstawowe informacje o obrazie:")
        print(f"Format: {image.format}")
        print(f"Rozmiar: {image.size}")
        print(f"Tryb: {image.mode}")
        print(f"Color Palette: {image.getpalette()}")

    except Exception as e:
        print(f"Nie udało się otworzyć obrazu: {e}")

image_path = "C:/Users/machm/OneDrive - Politechnika Śląska/Documents/sem6/SP/TEST/Watermark/metatest.jpg"
get_image_metadata(image_path)
