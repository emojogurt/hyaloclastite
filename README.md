# hyaloclastite

## Opis - aspiracje
Skrypty do obsługi terminalowej (curses) notatek w formacie kompatybilnym z obsidianem.

## Opis
Hyaloclastite is a volcanoclastic accumulation or breccia consisting of glass.
TODO

## Projekt highlevelowy
Dostępne mają być trzy tryby:
* Przeglądarka plików w vaulcie: pozwala na poruszanie się po drzewku folderów i plików w vaulcie, nawigacja odbywa się za pomocą strzałek, plik otwiera się enterem. Ponadto odpowiednia komenda pozwala na wyjście z programu. Opcjonalnie tryb ten pozwala również na wyszukiwanie plików, wyszukiwanie w tekście i inne operacje do rozważenia.
* Czytnik: pozwala na pretty-print tekstu w mdpodobnym formacie obsidiana, przeskakiwanie pomiędzy plikami za pomocą linków oraz na śledzenie otwartych plików. Nawigacja odbywa się za pomocą strzałek, nawigacja po linkach za pomocą Tab, Shift + Tab i Enter, nawigacja po historii otwartych plików za pomocą \< i \>. Zdefiniowany klawisz pozwala na wyjście do Przeglądarki plików. Inny zdefiniowany klawisz pozwala przejść do trybu edycji.
* Edycja: uruchomienie trybu edycji wywołuje zdefiniowany w zmiennych środowiskowych edytor i pozwala mu przejąć kontrolę nad IO, po jego zamknięciu program powraca do poprzednio uruchomionego trybu.

Przełączanie pomiędzy trybami odbywa się za pomocą komend.

## Planowane etapy
* POC: rudymentarna przeglądarka plików (byle zadziałała) + czytnik robiący z grubsza less nieprzetworzonego pliku i obsługujący wywoływanie edytora oraz wyjście do przeglądarki
* Wstępny 1: Nawigacja w czytniku plików po linkach
* Wstępny 2: Mały pretty print (zastępowanie linków odpowiednimi nazwami, wypisywanie list, wytłuszczanie tytułów)
* Wstępny 3: obsługa pomocy 
* Wstępny 4: interfejs przeglądarki niepowodujący nadmiernego wkurwu u użytkownika i wyglądający w miarę ok
* Działający 1: Obsługa historii plików i nawigacji po niej
* Działający 2: Poprawiony pretty print (obsługa kursywy, wytłuszczenia, podkreślenia w tekście, obsługa kolorów do tytułów i dodawanie odpowiednich znaków żeby wyróżnić poziomy tytułów)
* Ulepszony - j.w. + obsługa wyszukiwania i innych ulepszeń, które wyklarują się po drodze.
