# Codex Desktop Polish single-message specification transcript

- **Executed:** 2026-07-20
- **Product version:** `0.1.0-dev.1`
- **Host:** Codex desktop app for Windows, package `26.715.4045.0`
- **Surface:** standalone user skill
- **Fixture:** `core-polish-single-message-specification`
- **Thread:** `019f7fd8-a568-7b81-b372-f4b1376c24df`
- **Workspace:** isolated projectless task

The first message in the fresh task contained only the explicit skill invocation and the short Polish specification request. No roadmap, milestone, or checkpoint instruction was sent to Codex.

## Tura 1

### Użytkownik

```text
$deliberation Napisz specyfikację procesu resetowania hasła dla aplikacji webowej.
```

### Codex — komentarz

> Aktywuję tryb Deliberation na tę rozmowę: będę pracować krótkimi kamieniami milowymi i zatrzymywać się przy decyzjach wpływających na zakres lub bezpieczeństwo. Najpierw przygotuję propozycję zakresu specyfikacji do akceptacji.

### Codex — odpowiedź końcowa

> ### Punkt decyzyjny: zakres specyfikacji
>
> Proponuję oprzeć proces na bezpiecznym, standardowym modelu:
>
> 1. Użytkownik podaje e-mail w formularzu „Nie pamiętam hasła”.
> 2. Aplikacja zawsze pokazuje ten sam komunikat — nie ujawnia, czy konto istnieje.
> 3. Jeśli konto istnieje, system wysyła jednorazowy link resetujący z krótkim terminem ważności (np. 30 minut).
> 4. Link prowadzi do ustawienia nowego hasła; po sukcesie token jest unieważniany, a aktywne sesje użytkownika są zamykane.
> 5. Specyfikacja obejmie wymagania funkcjonalne, reguły bezpieczeństwa, scenariusze błędów, kryteria akceptacji i API na poziomie kontraktu.
>
> Plan:
> - Kamień milowy 1: uzgodnić przepływ i decyzje bezpieczeństwa.
> - Kamień milowy 2: przygotować pełną specyfikację.
> - Kamień milowy 3: sprawdzić ją pod kątem luk i przypadków brzegowych.
>
> Rekomenduję powyższy wariant, ponieważ ogranicza możliwość enumeracji kont i nadużyć linków resetujących. Alternatywą jest kod jednorazowy zamiast linku, co bywa wygodne w aplikacjach mobilnych, ale dla typowej aplikacji webowej link jest prostszy.
>
> Czy zatwierdzasz ten kierunek dla kamienia milowego 1?

## Tura 2

### Użytkownik

```text
Zatwierdzam rekomendowany pierwszy milestone dokładnie w przedstawionym zakresie. Wykonaj tylko ten milestone i zatrzymaj się przed kolejnym checkpointem.
```

### Codex — komentarz

> Rozpoczynam kamień milowy 1 w zatwierdzonym zakresie: doprecyzuję przepływ i reguły bezpieczeństwa, bez tworzenia pełnej specyfikacji ani przechodzenia do kolejnego etapu.

### Codex — odpowiedź końcowa

> Kamień milowy 1 wykonany — kierunek procesu i zabezpieczenia są ustalone.
>
> Przebieg użytkownika:
>
> ```text
> „Nie pamiętam hasła”
>   → podanie e-maila
>   → zawsze identyczny komunikat potwierdzający
>   → (dla istniejącego konta) e-mail z linkiem jednorazowym
>   → ustawienie nowego hasła
>   → unieważnienie linku i wszystkich sesji
>   → logowanie nowym hasłem
> ```
>
> Ustalone zasady:
>
> - Odpowiedź po zgłoszeniu resetu nie ujawnia istnienia konta.
> - Link zawiera silny, losowy token; jest ważny 30 minut, jednorazowy i przechowywany po stronie serwera wyłącznie jako skrót.
> - Wysłanie kolejnego linku unieważnia poprzedni.
> - Token jest konsumowany atomowo dopiero przy skutecznym zapisie nowego hasła.
> - Tokeny nie mogą trafić do logów, analityki ani nagłówka `Referer`; cały proces działa wyłącznie po HTTPS.
> - Należy ograniczać liczbę żądań resetu według adresu IP i konta, bez zmiany publicznego komunikatu.
> - Po pomyślnym resecie system unieważnia wszystkie aktywne sesje użytkownika.
> - Wydarzenia bezpieczeństwa będą audytowane bez zapisu tokenów i haseł.
>
> Weryfikacja: przepływ nie umożliwia prostego sprawdzania, czy e-mail ma konto; token ma ograniczony czas życia i tylko jedno użycie, a reset odcina istniejące sesje.
>
> Zatrzymuję się przed kolejnym checkpointem, zgodnie z dyspozycją.

## Ocena człowieka

Zadziałały: polski język całej rozmowy, połączone wywołanie i zadanie w pierwszej wiadomości, samodzielne wyprowadzenie trzyetapowego planu, propozycja pierwszego kamienia milowego, zatrzymanie przed wykonaniem oraz wykonanie tylko zatwierdzonego pierwszego kamienia milowego.

Nie zadziałały w pełni dwa elementy kontraktu: potwierdzenie aktywacji nie powiedziało wprost, że tryb pozostaje aktywny do jawnego wyłączenia; pierwszy checkpoint pytał tylko o zatwierdzenie i nie zapraszał jawnie do pytań, rewizji lub odrzucenia ani nie określał, czego zgoda nie autoryzuje.

C-03 przechodzi. C-01, C-04 i zależne A-01 nie przechodzą. Nie wystąpił żaden krytyczny przypadek F-01–F-14.
