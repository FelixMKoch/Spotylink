# Spotylink
---------------------------------------------------------------------------------------------------------------------------------

## Idee
Ziel ist es eine Cloud-Anwendung zu bauen, die mehrere Spotify Konten analysiert und auf Anfrage eine gemeinsame Playlist erstellt. Diese Playlist ist für jeden Benutzer unterschiedlich und wird direkt auf das Spotify Konto des Benutzers geladen!

## Use-Case

Man sitzt mit Freunden an der Isar und möchte gerne gemeinsam Musik hören. Jeder mit einem Spotify Account meldet sich über die Webapplikation an und es werden automatisch beliebte Lieder oder Genres verglichen. Die Gemeinsamkeiten in den jeweiligen Kategorien werden als Playlist angezeigt und wiedergegeben.

## MVP

- Webablikation in der sich zwei oder mehr Spotify User mit ihren Accounts anmelden können.
- Alle Accounts werden auf beliebte Genres durchsucht
- Gemeinsamkeiten werden ermittelt
- Jeder user kann eine gemeinsame Playlist herunterladen und direkt abspielen (über Spotify)
- Die App soll intuitiv verständlich für Benutzer sein, und es soll mit möglichst wenig Klicks ermöglicht werden eine Playlist zu exportieren 

Hinweis: Im Laufe des Projektes hat sich herausgestellt, dass die Spotify API keine Recommendations durch genres zurück geben kann (trotz dem, dass sie das angibt). Deswegen haben wir uns beim MVP darauf konzentriert Songs zu vergleichen und nicht Genres.

## Azure-Functions
### save_usr
1. spotylink_auth: Bekommt get Request von Spotify API und regelt den Authroisierungs Workflow mit OAtuh 2.0 (siehe unten)
2. get_user_info [userid]: Gibt Informationen über den Spotify Account des Users aus. Benötigt die Spotylink interne User-ID   

### create_session
1. get_user_in_session [sessionid]: Get Request mit Spotylink interner Session-ID gibt alle User-IDs von Benutzern in der Session zurück
2. spotylink-create-session [userid, (sessionid)]: Get Request mit User-ID und (optional) Session-ID. Falls Session-ID gegeben wird der User dieser Session joinen, ansonsten wird eine Random Session erstellt

### export_playlist
1. spotylink-export [userid]: Get Request mit User-ID. Es wird eine Playlist fürr die Session in der der User gerade ist erstellt, und auf das Spotify Konto des gegebenen Users exportiert.

## Struktur   
![Strukturbild](https://inf-git.fh-rosenheim.de/inf-ca/sose2022/spotylink/-/wikis/uploads/ef9038f803abdb75cd43a8535d8bbffe/image.png)


## Api / Resourcen

- [Dokumentation](https://developer.spotify.com/documentation/web-api/)
- Authentifizierung mit [OAuth 2.0](https://oauth.net/2/), Dokumentation befolgt nach [Spotify Auth](https://developer.spotify.com/documentation/general/guides/authorization/) workflow

## Voraussetzungen

Folgende Voraussetzungen müssen erfüllt sein, dass das Programm für den Benutzer auch funktioniert:
- Der User muss ein Spotify Konto haben (egal ob Premium oder Free)
- Der User mit Email muss in Spotify Developer API des Hosts hinzugefügt werden. Seite für Dev API findet man [hier](https://developer.spotify.com/dashboard/applications) 
- Anleitung dazu findet man im [Anleitungs Ordner](https://inf-git.fh-rosenheim.de/inf-ca/sose2022/spotylink/-/tree/main/03%20Anleitungen)
- ClientID und Secret ID in der [Auth Function](https://inf-git.fh-rosenheim.de/inf-ca/sose2022/spotylink/-/blob/Development/01Projekt/functions/save_usr/spotylink_auth/__init__.py) und in der Frontend [JS Datei](https://inf-git.fh-rosenheim.de/inf-ca/sose2022/spotylink/-/blob/main/01Projekt/frontend/spotylink_frontend/public/index.js) anpassen
- Der User stimmt mit der Anmeldung auf der Seite zu, dass Spotylink Playlists Create, Change, und Informationen abrufen kann


## Deployment

### Web-Service:  
Benötigt wird: Visual Studio Code mit installierten Azure Erweiterungen. (Azure Web Service und Azure Account)
Visual Studio Code ist mit der Erweiterung Azure Account mit dem eigenen Account angemeldet.
Bei VSC unter dem Azure-Reiter auf Ressourcengroup gehen und die gesuchte Gruppe auswählen.
Mit Rechtsklick auf Webapp den Service erst starten und dann deployen. Daraufhin mittels Rechtsklick im Browser anzeigen lassen.

### Allgemeines Deployment
Im Allgemeinen wird dieses Projekt bei Microsoft Azure gehostet. Das Deployment wir dabei von unserer CI/CD Pipeline geregelt.  
Falls jemand dieses Projekt auf einen eigenen Azure Account deployen will, müssen nur die Parameter oben in der [ci.yml](https://inf-git.fh-rosenheim.de/inf-ca/sose2022/spotylink/-/blob/main/.gitlab-ci.yml) geändert werden.  
Zum starten des Projektes müssen noch alle Dinge im unterpunkt Voraussetzungen erfüllt sein.  
Weiter Anleitungen findet man in dem dafür geschaffenen [Ordner](https://inf-git.fh-rosenheim.de/inf-ca/sose2022/spotylink/-/tree/main/03%20Anleitungen)

## Kosten Analyse
Laut dem Presirechner von Azure liegen die geschätzten Kosten bei 4,05 Dollar Monatlich. 
Die Ressourcen sind zwei Blobstorage Accounts, jeweils mit 100 GB Speicher und 10000 Änderungs und Lese Aufrufen. Der ausgewählte Tarif ist Standard. So Kostet jeder Blobstorage 2,02 Dollar Monatlich. 
Hinzu kommen drei Functions jeweils mit dem Tarif Verbrauch. Der Arbeitsspeicher liegt bei 128. Die ersten 400.000 GB/s bei der Ausführung sowie die erste 1.000.000 Ausführungen sind kostenlos. Daher werden die drei Functions in der Vorrausberechnung mit 0 Dollar angezeigt.
Alle Resourcen sind in WestEurop gehostet. 
