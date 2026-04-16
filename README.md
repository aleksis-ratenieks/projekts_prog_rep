# projekts_prog_rep
Programmēšana II eksāmena piekļuves darba projekts
# 💻 Datoru noslogojuma sistēma

**Izstrādātājs:** Aleksis Ratenieks  
**Darba vadītājs:** Kristaps Upenieks  
**Skola:** V. Plūdoņa Kuldīgas vidusskola  
**Priekšmets:** Programmēšana II piekļuves darbs

---

## 📄 Projekta apraksts
Tīmekļa lietotne, kas ļauj reāllaikā pārskatīt, kuri Chromebook datori ir **pieejami**, **aizņemti**, un kuri skolotāji tos izmanto.  
Projekts izveidots, ievērojot KISS un DRY principus un balstoties uz labākās prakses ieteikumiem.

---

## 🚀 Funkcionalitāte
- Datoru saraksta un statusa pārvaldība
- Skolotāju reģistrācija
- Datoru paņemšana un atgriešana
- Lietošanas vēstures uzskaite
- API integrācija (Open-Meteo – reālā laika temperatūra)
- Vienību testi
- Objektorientēta struktūra ar SQLAlchemy ORM

---

## 🧰 Tehnoloģijas
- **Python 3 / Flask**
- **SQLite datubāze**
- **HTML / CSS**
- **Requests** (API pieprasījumiem)
- **Unittest** testēšanai

---

## ⚙️ Projekta palaišana

```bash
# 1. Instalē atkarības
pip install -r requirements.txt

# 2. Palaiž lietotni
python app.py

# 3. Atver pārlūkā
[127.0.0.1](http://127.0.0.1:5000)
