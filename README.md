# ftn-oi-travelling-salesman
[Operaciona Istraživanja]\
Predmetni Zadatak + Implementacija Simplex Algoritma

## Pokretanje

Program se pokreće iz `travellingSalesman.py` koristeći Python 3.\
Jedina neophodna biblioteka za pokretanje je `numpy`.

Na vrhu fajla se nalaze podešavanja za rad algoritama :
- `ALGO` - Biranje algoritma za rešavanje TSP-a, `0` je Brute Force, `1` je Nearest Neighbour, `2` je Hungarian Algorithm i `3` je Genetic Algorithm.
- `SHOW_TABLE` - Opcija koja prikazuje tabelu sa rutama i cenama u Brute Force algoritmu.
- `POPULATION_SIZE` - Broj jedinki u populaciji za genetski algoritam, uneti broj će se povećati do sledećeg množioca četvorke.
- `ITERATIONS` - Broj iteracija koje će genetski algoritam izvršiti.
- `MUTATION_RATE` - Verovatnoća da ce se dete mutirati u genetskom algoritmu.

## Travelling Salesman Problem

**Problem Trgovačkog Putnika** predstavlja optimizacioni problem usko povezan sa kombinatorikom, gde trgovac želi da obiđe `n` destinacija kako bi prodao svoj proizvod, tako da obiđe svaku destinaciju tačno jednom i vrati se odakle je pošao.
Ovaj problem možemo reprezentovati grafom, gde će čvorovi biti destinacije, a grane između čvorova putevi, odnosno prelazi između destinacija, sa određenom cenom ili težinom. 
Možemo gledati na tu cenu puta i kao, na primer, distancu, ili možda vreme potrebno za put.
Smatramo da je Problem Trgovačkog Putnika rešen ako smo našli putanju koja zadovoljava navedene uslove, sa najmanjom mogućom cenom.

Moguće je definisati 2 tipa Problema Trgovačkog Putnika:
- Kada postoji putanja iz svakog čvora do svakog čvora,
- Kada ne postoji putanja iz svakog čvora do svakog čvora.

Mi se fokusiramo na prvu varijantu.

Kao cenu putanje možemo uzimati potrebno vreme, novčanu cenu, neku njihovu kombinaciju ili drugo.

### Primer Travelling Salesman Problema

Neka nam je nekoliko drugova došlo u posetu.
Na kraju večeri moramo sve njih odvesti kući kolima, i vratiti se svojoj, ali nam je nakon spremanja večere ostalo malo novca, pa ne možemo kupiti puno goriva.
Problem moramo rešiti tako što formiramo optimalnu putanju, odnosno, onu koja je najkraća.
U ovom slučaju radimo sa optimizacionim problemom gde nam je cilj da minimizujemo ukupnu distancu pređenu između čvorova.

## Algoritmi i Njihova Implementacija

Za predmetni projekat smo izabrali četiri algoritama za implementaciju rešenja Problema Trgovačkog Putnika - Brute Force, Nearest Neighbour, Mađarski i Genetski Algoritam.

Svim algoritmima je dodeljena početna matrica cena prelaza iz svakog čvora u određeni čvor - `priceMatrix`. Iz svakog čvora se može doći u svaki drugi, odnosno, ne može se ići u isti čvor (kao što je po pravilu algoritma). Zbog toga je glavna dijagonala u matrici napunjena dosta većim vrednostima - da algoritmi nikad ne izaberu tu opciju.
Matricu cena prelaza možemo da čitamo kao da su redovi, redom, čvorovi iz kojih moramo krenuti, a kolone čvorovi u koje završavamo.
Odatle je cena prelaza iz čvora `A` u čvor `C` element na poziciji `(0,2)`.

### Brute Force Algorithm

Brute Force je jedini algoritam u ovoj listi koji će svaki put dati **tačno rešenje**. Drugim rečima, svi ostali algoritmi su zapravo heuristike za nalaženje dobrog rešenja.

Algoritam radi na sledeći način:
- Izgenerisati sve moguće permutacije redosleda čvorova, koje će predstavljati sve moguće rute u sistemu.
- Za svaku rutu naći ukupnu cenu.
- Selektovati kao optimalnu putanju bilo koju rutu sa najmanjom cenom. 
	- U slučaju da je bitno iz kog čvora krećemo, selektovati adekvatnu rutu, ponovo sa najmanjom cenom.

Implementacija počinje u funkciji `bruteForce()`, u njoj se pravi lista svih permutacija pozivom (third party) funkcije `generatePermutations()`. Svakom elementu te liste, odnosno svakoj ruti, se na kraj stavlja ukupna cena te rute dobijena iz funkcije `calcCost(route)`, koja koristi `priceMatrix` za dobijanje cena.

Brute Force je ubedljivo najsporiji algoritam, jer prolazi kroz svaku moguću rutu, kojih za `n` čvorova ima `n!`. To se, naravno, ne primećuje toliko na primerima sa manjim brojem čvorova, pa je u tim slučajevima ovaj algoritam najbolji. U drugim slučajevima, doduše, ovaj algoritam nema smisla koristiti, jer za već sistem sa 10 čvorova, treba praviti listu od 3.6 miliona ruta i sve njih porediti, što nikako nije efikasno.

### Nearest Neighbour Algorithm

Nearest Neighbour algoritam nam daje rute formirane po najmanjim cenama po prelasku u susede, za svaki čvor kao početak, posebno.
Dakle, za `n` čvorova ćemo imati listu od `n` izgenerisanih ruta.

Algoritam radi na sledeći način:
- Iz svakog čvora grafa se pravi tačno jedna ruta. 
- U redu matrice cene prelaza se nalazi najmanja cena prelaza. 
- Bira se kolona tog najmanjeg elementa za novi red po kojem će se dalje tražiti. Odnosno, prelazimo u "najbliži sused".
- Postupak se ponavlja dok ne iskoristimo sve kolone, odnosno dok ne posetimo svakog suseda.
- Kada posetimo svakog suseda forsiramo vraćanje u početni čvor, odnosno kolonu.

Za implementaciju ovog algoritma je korišćena maska `mask` koja se puni jedinicama po kolonama pri prelasku iz čvora u čvor.
Kada se proverava minimalni element iz reda, mora se paziti da li smo već posetili taj čvor, odnosno da li je ta kolona u masci postavljena na `1`. Ako jeste, prelazimo na sledeći najmanji element u redu.

Nearest Neighbour je ubedljivo najbrži algoritam, ali i najjednostavniji. Postoje situacije u kojima je ovako nizak nivo optimizacije dovoljan, međutim, ako vreme nije problem, trebali bi da koristimo neke druge metode, jer ova ne garantuje optimalnu rutu, iz kojeg god čvora krenuli.

### Hungarian Algorithm

Hungarian Algorithm, odnosno Mađarski metod, je optimizacioni problem namenjen za rešavanje problema dodele poslova.
Primer ovakvog problema je da imamo `n` ljudi koji rade na određenom poslu koji ima `m` potproblema koje oni zajedno trebaju rešiti. Svako od njih može da rešava bilo koji od `m` potproblema, ali svako od njih za različitu cenu (ili vreme).
Mađarski metod ovaj problem rešava tako što će pronaći prave ljude za pravi problem, minimizujući ukupnu potrebnu cenu (ili vreme).
Problem Balansirane Dodele je slučaj kada imamo jednak broj ljudi i problema, odnosno `n = m` - u suprotnom imamo Problem Nebalansirane Dodele.

U određenim slučajevima Mađarski algoritam možemo koristiti i za rešavanje Problema Trgovačkog Putnika.

Algoritam radi na sledeći način:
- Početna matrica cena prelaza se redukuje :
	- Redukcija po redu se odvija tako što najmanji element u selektovanom redu oduzimamo od svih elemenata tog reda, i tako za svaki red matrice. Elementi na glavnoj dijagonali ostaju nepromenjeni.
	- Redukcija po koloni se odvija na sličan način.
- Prolazi se kroz redove i kolone redukovane matrice i posmatramo da li imamo samo jednu nulu u redu ili koloni.
	- Ako imamo, u masci `mask` označavamo precrtane kolone ili redove. 
	- Takođe, u novoj masci `routeMask`, označavamo poziciju selektovane nule, kao selektovani prelaz iz jednog čvora u drugi u matrici cena prelaza.
- Nakon punjenja maski, ako nije bilo problema, možemo proveriti da li u `routeMask` imamo po jednu označenu poziciju u svakom redu i u svakoj koloni - ako je to slučaj, možemo formirati rutu i završiti algoritam.
- Ako `routeMask` nije dobro napunjena, algoritam nastavljamo gledajući sve elemente ostavljene kao `0` u `mask`, od njih biramo minimalni element, oduzimamo ga od svih tih elemenata, i dodajemo ga na elemente u preseku precrtanih redova i kolona. 

Mađarski algoritam garantuje jednu optimalnu rutu, iako može više njih da postoji.

Pri rešavanju Problema Trgovačkog Putnika ovim algoritmom možemo naići na problem gde nakon svog precrtavanja redova i kolona u masci imamo slučaj da u svakom redu i koloni imamo ili nula ili više od jedne nule.\
To označava da postoji više optimalnih ruta u sistemu.\
U ovoj implementaciji smo se odlučili da takve slučajeve ne pokrivamo, jer bi rešavanje onda uvelo i neke od metoda backtracking-a ili grananja.\
U [ovom ](https://youtu.be/BUGIhEecipE?t=1915) snimku se prelazi navedeni slučaj.
U implementaciji prvi primer (sa `5x5` tabelom) neće izbaciti optimalno rešenje baš zbog ovog problema.

### Genetic Algorithm

Genetski Algoritam rešava optimizacione probleme po uzoru na proces prirodne selekcije. 

Algoritam radi na sledeći način:
- Inicijalizuje se početna populacija. Svaki element populacije, odnosno jedinka, će predstavljati jednu rutu u sistemu. Populacija se inicijalizuje stohastično.
- Nakon inicijalizacije se svakoj jedinki računa prilagođenost (fitness) ka rešenju, odnosno, u ovom slučaju, ukupna cena rute, koju želimo da minimizujemo.
- Nakon dodavanja cena u listu jedinki, prelazi se na fazu selekcije roditelja. Selekcija se vrši na osnovu fitness-a, odnosno, uzima se polovina populacije koja ima najmanje cene.
- Od selektovanih roditelja, u fazi ukrštanja, kreiramo decu, koja će zajedno sa roditeljima ući u sledeću populaciju za novu iteraciju. Ukrštanje se vrši tako što se prva polovina čvorova iz prvog roditelja kopira, pa se iz drugog roditelja redom uzimaju čvorovi koji su ostali. Isto se radi i za drugu polovinu prvog roditelja, za kreiranje drugog deteta. Ovime se održava validnost rute.
- Nakon kreiranja dece vršimo mutaciju dece po određenoj verovatnoći mutacije `MUTATION_RATE`. Mutacija se vrši tako što se zamene nasumični čvorovi u ruti, tako da se održi validnost rute.
- Kada imamo validne jednike ponovo računamo fitness, pravimo novu populaciju na gore navedeni način, i ponavljamo iteraciju dok ne dostignemo `ITERATIONS` iteraciju.
- Za najbolju rutu biramo onu koja u poslednjoj populaciji ima najmanju cenu. Ako su podešavanja algoritma dobra, poslednja populacija će konvergirati u jednu, minimalnu vrednost za optimalnu cenu rute.

Ova implementacija Genetskog Algoritma ne pamti najbolju trenutnu rutu, odnosno jedinku, već gleda koja je najbolja ruta, odnosno jedinka, u poslednjoj populaciji.\
Da smo pamtili najbolju rutu, algoritam bi dosta ličio na neku implementaciju algoritma roja, gde se svim jedinkama saopštava trenutno najbolje rešenje ka kojem one trebaju da teže. 