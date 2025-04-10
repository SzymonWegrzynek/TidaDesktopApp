# Zadanie: Aplikacja desktopowa do słuchania muzyki

## Opis

Pierwszym zadaniem w tym semestrze będzie napisanie aplikacji desktopowej do słuchania muzyki.  
Aplikacja powinna mieć układ podobny do tego, który jest w załączniku.  
Nie musi być odwzorowana jeden do jeden, natomiast ważne jest użycie właściwych układów do pozycjonowania przycisków czy informacji o piosence.

## Wymagania funkcjonalne

Aplikacja powinna:

- Wyświetlać:
  - Aktualny czas utworu
  - Tytuł piosenki
  - Parametry bitrate i mixrate
  - Suwak z poziomem głośności
- Posiadać przyciski:
  - Następnej piosenki
  - Poprzedniej piosenki
  - Uruchomienia piosenki
  - Zapauzowania piosenki
  - Rozpoczęcia tej samej piosenki od początku
  - **Shuffle** – losowanie następnego utworu z listy
  - **Loop** – odtwarzanie utworu w pętli
- Domyślnie po skończeniu utworu przechodzić do następnego na playliście.

## Uwagi

- Nie trzeba implementować switcha mono/stereo.
- Odtwarzane utwory są plikami MP3, które znajdują się w folderze z projektem.
- Nie wysyłam żadnych plików MP3.

## Technologie

Praca domowa nie musi być napisana w Pythonie. Natomiast musi być użyta jedna z poniższych technologii:

- **C++/C#** – Windows Forms, WPF, MAUI, Xcode lub Qt
- **Python** – PyQt
- **Java** – Swing lub Qt
