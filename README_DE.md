# BlibBlop

Cross-platfrom tool um die eigenen Reaktionszeiten auf visuelle oder akkustische Stimuli zu messen.

## Abhängigkeiten
 BlipBlop ist in python geschrieben und die graphische Oberfläche (GUI) benutzt
 
- PyQt5

## Installation/Ausführen von BlipBlop

Einfach das für die Zielplatform gepackte Zip-Archiv herunterladen (BlipBlop_win.exe für Windows, BlipBlop_linux für Linux and BlipBlop_mac.app für macOS) und entpacken. Z.B. durch Rechtsklick und auswählen von *extrahieren*. Das Archiv enthält nur eine einzige Datei.

### Linux (Ubuntu)

Unter Linux (getestet unter Ubuntu 20.04) muss die entpackte Datei ausführbar gemacht werden. Nehmen wir an, dass das Archiv im *Downloads* Ordner entpackt wurde. Öffne ein Terminal und führe die folgenden Befehle aus:

``` shell
> cd Downloads/BlipBlop-linux/
> chmod a+x BlipBlop
> ./BlipBlop
```

### macOS

Das *macOS* Paket wurde unter macOS 11 (BigSur) bebaut und sowohl auf einem Intel und M1 basierten System getestet. Um die App auszuführen muss das heruntergeladene Archiv entpackt werden und die darin enthaltene Datei kann dann durch doppelklick ausgeführt werden.

Es kann sein, dass macOS die Anwendung blockiert, da sie nicht signiert wurde. In dem Fall informiert ein sich öffnendes Fenster darüber. Um die Anwendung dennoch auszuführen, schliesst man dieses Fenster und öffnet die *Systemeinstellungen>Sicherheit>Allgemein*. Unten sollte eine Notiz erscheinen, die noch einmal sagt, dass die Anwenung geblockt wurde und anbietet sie dennoch (auf eigene Gefahr) auszuführen.

### Windows10

Unter Windows 10 muss das heruntergeladene Archiv entpackt werden und die *exe* Datei kann dann durch Doppelklick gestartet werden. Auch unter Windows kann es sein, dass die Anwendung durch das System geblockt wird. 

![win_block1](docs/images/win_blocking_1.png)

Durch klicken auf den link "Weitere Informationen" ändert sich das Fenster und bietet nun die Möglichkeit die Anwendung dennoch zu starten.

![win_block2](docs/images/win_blocking_2.png)


## Starten der Anwendung aus dem Quellcode heraus

Um diesen Weg zu gehen muss eine Python3 Entwicklungsumgebung installiert sein. Zudem benötigt BlipBlop das Paket pyqt5. Dies kann am einfachsten mittels *pip* installiert werden.

``` bash
> pip3 install pyqt5
``` 

Als nächstes muss das Repository von GitHub repository geklont werden.

``` shell
> git clone --depth 1 https://github.com/jgrewe/blipblop.git
```
Obiges Kommando erzeugt einen *shallow* Klon des Repositories welcher nur den aktuellen Stand enthält.

Zum Ausführen reicht es in den Projektordner zu wechseln und das *main* Skript mit python3 ausführen zu lassen.

``` shell
> cd blipblop
> python3 blipblop_main.py
```
