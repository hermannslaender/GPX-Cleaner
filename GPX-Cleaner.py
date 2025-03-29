import sys
import io

if len(sys.argv) == 1:
    print('Es muss ein Dateiname als einziger Parameter übergeben werden')
    print('z.B.: GPX-Cleaner.exe d:\\test.gpx')
    print()
    input('ENTER zum beenden')
    sys.exit()

print('Lösche Logs und Wegpunkte')
print('Datei: ' + sys.argv[1])

SourceFile = io.open(sys.argv[1], mode="r", encoding="utf-8")
TargetFile = io.open(sys.argv[1].replace('.gpx', '_clean.gpx'), mode="w", encoding="utf-8")

String = SourceFile.read(10)

while String.find('</gpx>') == -1:
    # "<wpt" suchen
    while String.find('<wpt') == -1 and String.find('</gpx>') == -1:
        String += SourceFile.read(1)

    if String.find('</gpx>') != -1:
        break

    print(String[:len(String)-4].strip())
    TargetFile.write(String[:len(String)-4].strip())

    # "</wpt>" suchen
    String = "<wpt"
    while String.find('</wpt>') == -1:
        String += SourceFile.read(1)

    if String.find('<type>Waypoint') != -1:
        print('Gelöscht:\n'+String.strip()+'\n\n')
        String=''
    else:   
        print('Start: '+str(String.find('<groundspeak:logs>')))
        print('End:   '+str(String.find('</groundspeak:logs>')))
        String = String[:String.find('<groundspeak:logs>')+18] + String[String.find('</groundspeak:logs>'):]
        print(String)
        TargetFile.write(String)
    String = ''

print(String)
TargetFile.write(String)
TargetFile.close()

print('##################### Ende ##########################')
