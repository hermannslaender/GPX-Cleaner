import sys
import re


def main():
    if len(sys.argv) != 2:
        raise Exception('Nur 1 Filename als Parameter')
    
    source = sys.argv[1]

    filename, ext = source.rsplit('.', 1)
    targetname = f'{filename}_cleaned.{ext}'
    content = get_file_content(source)
    cleaned_content = clean_gpx(content)
    save_file(targetname, cleaned_content)
    
    
def get_file_content(filename):
    if not filename.split('.')[-1] == 'gpx'.lower():
        raise Exception('Keine GPX Datei.')
    
    try:
        with open(filename, mode='r') as f:
            content = f.read()
    except FileNotFoundError:
        raise Exception("Datei nicht gefunden.")
                    
    return content

    
def save_file(filename, cleaned_content):
    try:
        with open(filename, mode='w') as f:
            f.write(cleaned_content)
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")


def clean_gpx(content):
        # first remove all logs
        sanitized = re.sub(r"<groundspeak:logs>.*?</groundspeak:logs>",
               "", content, flags=re.DOTALL)
        
        # remove all additional waypoints
        sanitized = re.sub(r"<wpt.*?</wpt>",  # Finde jeden <wpt>...</wpt>-Block
            lambda match: "" if not re.search(r"<type>Geocache",
            match.group(0)) else match.group(0),
            sanitized, flags=re.DOTALL)
        return sanitized


if __name__ == '__main__':
    main()
