README: Image Watermarking Tool
Overview
This project allows you to apply a text-based watermark to an image. The user can select an image from their local file system, add a text watermark, and save the watermarked image to a selected directory. The tool is built using Python with the Pillow and Tkinter libraries.

```
pip install pillow
```

When you run the script, it will first prompt you to choose an image file from your local machine.

After selecting the image, it will ask you for a folder where the watermarked image will be saved.

Next, you will be prompted to enter the watermark text (e.g., "My Watermark").

The script will apply the watermark to the image and save it to the folder you selected.

The output image will be saved as watermarked_text.jpg in the chosen directory.

### Example Input:

```
Image: image.jpg

Watermark Text: "My Watermark"

Output Folder: "/path/to/output/folder"

Output: The watermarked image will be saved as watermarked_text.jpg in the selected folder.
```

JSON Format for Upload (Optional)
If you want to upload an image with a watermark directly via an API (e.g., using Postman), you can use a JSON payload like this:

```
{
  "image": "/path/to/your/image.jpg",
  "watermark_text": "My Custom Watermark",
  "output_folder": "/path/to/output/folder"
}
```

Important: You can modify the script to support JSON-based input via an API for automation.

README: Image Metadata Extraction Tool
Overview
This project allows you to extract metadata from an image file, such as EXIF data, and display basic information about the image (e.g., format, size, and mode). The metadata extraction tool uses the Pillow library.

Step-by-step Usage:

When you run the script, it will ask you to provide the path to the image file you want to extract metadata from.

The script will open the image, extract EXIF data (if available), and print the information in the terminal.

It will also display basic information such as format, size, and color mode.

### Example Input:

```
Image Path: /path/to/your/image.jpg

Output Example: The script will output:
```

```
yaml
Copy
Edit
Metadane EXIF:
Make: Canon
Model: Canon EOS 5D Mark IV
DateTime: 2021:08:15 14:30:22
ExposureTime: 0.01
FNumber: 2.8
...

Podstawowe informacje o obrazie:
Format: JPEG
Rozmiar: (4000, 3000)
Tryb: RGB
Color Palette: None
EXIF Data
EXIF metadata may include the following types of information (if available):

Make: Camera manufacturer

Model: Camera model

DateTime: Date and time the photo was taken

ExposureTime: Exposure time

FNumber: Aperture value

GPS info: Location data (if the image has GPS info)
```

### Code Explanation

EXIF Metadata Extraction: The script uses the Pillow library to open the image and extract EXIF data using the \_getexif() method.

Basic Image Info: The script also displays basic information about the image, such as its format, size (in pixels), and color mode (RGB, RGBA, etc.).

### Additional Notes

#### Image Formats Supported:

```
JPEG

PNG

TIFF

GIF

BMP
```

#### No EXIF Data: Some images may not have EXIF metadata (e.g., images edited in certain programs or screenshots). The script will inform you if EXIF data is not available.
