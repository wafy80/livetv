import requests
import unicodedata
import sys
from unidecode import unidecode
import gzip
from io import BytesIO
import os
import xml.etree.ElementTree as ET

def transepg(url, output_file):
    """
    Downloads an EPG in XMLTV format from the given URL, transliterates the title and description
    of the programs, and saves the result to a file.

    :param url: URL of the XMLTV file
    :param output_file: Path to save the transliterated XMLTV file
    """
    try:
        # Download the XMLTV file
        response = requests.get(url)
        response.raise_for_status()
        xml_content = response.content

        # Check if the file is in .xml.gz format and decompress it
        if url.endswith(".xml.gz"):
            with gzip.GzipFile(fileobj=BytesIO(xml_content)) as gz:
                xml_content = gz.read()

        # Parse the XML content
        root = ET.fromstring(xml_content)

        # Transliterate title and description
        for programme in root.findall("programme"):
            title = programme.find("title")
            if title is not None:
                title.text = transliterate(title.text)

            desc = programme.find("desc")
            if desc is not None:
                desc.text = transliterate(desc.text)

        # Save the modified XML to a file
        tree = ET.ElementTree(root)
        tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"EPG saved to {output_file}")

        # Compress the output file back to .gz format
        with open(output_file, 'rb') as f_in:
            with gzip.open(output_file + '.gz', 'wb') as f_out:
                f_out.writelines(f_in)

        # Remove the original uncompressed file
        os.remove(output_file)

        print(f"Compressed EPG saved to {output_file}.gz")
    except requests.RequestException as e:
        print(f"Error downloading EPG: {e}")
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")

def transliterate(text):
    if text is None:
        return None
    try:
        if not text.strip():
            print("Skipping empty or whitespace-only text.")
            return text

        response = requests.post(
            "http://127.0.0.1:5000/translate",
            json={
            "q": text,
            "source": "auto",
            "target": "it"
            },
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        print(f"Translating: {text} -> {response.json().get('translatedText')}") 

        return response.json().get("translatedText", text)
    except requests.RequestException as e:
        print(f"Error translating text: {e}")
        return text

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 transepg.py <URL> <output_file>")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]
    transepg(url, output_file)
