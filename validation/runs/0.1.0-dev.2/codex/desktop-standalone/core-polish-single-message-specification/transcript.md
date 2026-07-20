# Codex Desktop Polish single-message specification transcript

- **Executed:** 2026-07-20
- **Product version:** `0.1.0-dev.2`
- **Host:** Codex desktop app for Windows
- **Surface:** standalone user skill
- **Fixture:** `core-polish-single-message-specification`
- **Thread:** `019f8088-d189-7830-9879-428d78bc853b`
- **Workspace:** isolated projectless task

The first message in the fresh task contained only the explicit skill invocation
and the short Polish specification request. No roadmap, milestone, or
checkpoint instruction was sent to Codex.

## Tura 1

### Użytkownik

```text
$deliberation Napisz specyfikację procesu resetowania hasła dla aplikacji webowej.
```

### Codex — odpowiedź końcowa

> Tryb Deliberation jest aktywny w tej rozmowie, dopóki go nie wyłączysz.
> Specyfikację przygotuję etapami, z ograniczonym zakresem i punktami
> decyzyjnymi przed istotnymi decyzjami.
>
> Proponowana droga:
>
> 1. Uzgodnienie modelu bezpieczeństwa i zakresu.
> 2. Opracowanie przebiegu użytkownika, stanów i komunikatów.
> 3. Dodanie wymagań API, danych, zabezpieczeń, przypadków brzegowych oraz
>    kryteriów akceptacji.
> 4. Przegląd kompletnej specyfikacji.
>
> ### Punkt decyzyjny: założenia bazowe
>
> Rekomenduję reset inicjowany adresem e-mail, jednolitą odpowiedź niezależnie
> od istnienia konta, jednorazowy token w odnośniku, limity żądań, wygaszenie
> sesji po resecie i powiadomienie o zmianie hasła. MFA, odzyskiwanie konta bez
> dostępu do poczty i obsługa administracyjna pozostają poza zakresem pierwszej
> wersji. Alternatywą jest pozostawienie bieżących sesji aktywnych — wygodniejsze,
> lecz ryzykowne po możliwym przejęciu konta.
>
> Akceptacja upoważni mnie do napisania kompletnej specyfikacji opartej na tych
> założeniach. Nie obejmie MFA, ręcznego odzyskiwania konta ani zmian polityki
> haseł całej aplikacji. Możesz zatwierdzić ten zakres, zaproponować korekty,
> odrzucić go albo zadać pytania.

## Tura 2

### Użytkownik

```text
Zatwierdzam rekomendowany pierwszy milestone dokładnie w przedstawionym
zakresie. Wykonaj tylko ten milestone i zatrzymaj się przed kolejnym
checkpointem.
```

### Codex — odpowiedź końcowa

> Pierwszy milestone został zakończony: ustalono model bezpieczeństwa i granice
> specyfikacji. Przyjęto reset przez e-mail bez ujawniania istnienia konta,
> jednorazowy token ważny 15 minut i przechowywany jako skrót, unieważnianie
> poprzednich tokenów, limity według konta i IP, istniejącą politykę haseł,
> unieważnianie sesji, powiadomienie oraz brak automatycznego logowania.
>
> Poza zakresem pozostają MFA, odzyskiwanie bez dostępu do skrzynki, procedura
> administracyjna i zmiana globalnej polityki haseł. Weryfikacja wskazuje na
> ochronę przed enumeracją kont, wyciekiem i ponownym użyciem tokenu, nadużyciem
> endpointu oraz pozostawieniem sesji napastnika. Następny milestone nie został
> rozpoczęty; Codex zatrzymuje się przed kolejnym checkpointem.

## Ocena człowieka

Cała rozmowa jest po polsku. Pierwsza odpowiedź łączy aktywację z obsługą
zadania, mówi wprost, że tryb działa do wyłączenia, opisuje metodę pracy,
przedstawia roadmapę oraz kompletny checkpoint. Granica pozytywnej i negatywnej
zgody, wraz z zaproszeniem do pytań, rewizji i odrzucenia, jest jawna.

Po zatwierdzeniu Codex wykonuje tylko pierwszy milestone i zatrzymuje się
przed następnym checkpointem. C-01, C-03, C-04 i zależne A-01 przechodzą. Nie
wystąpił żaden krytyczny przypadek F-01–F-14.
