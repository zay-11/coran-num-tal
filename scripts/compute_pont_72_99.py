#!/usr/bin/env python3
"""
PONT DES 72+99 — Calcul des resonances phi entre les noms divins
Shem HaMephorash (72 noms hebreux) et Asma ul-Husna (99 noms arabes).
"""

from __future__ import annotations
import json, math, sys
from pathlib import Path

PHI = (1 + math.sqrt(5)) / 2
INV_PHI = 1 / PHI

ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))

# --- 72 Noms hebreux (Shem HaMephorash) ---
# Derives d'Exode 14:19-21. Chaque nom = 3 lettres hebraiques.
# Format: (hebrew, transliteration, meaning, gematria manual if known)
HEBREW_72 = [
    ("והו", "VaHeVa", "Amour inconditionnel", 22),
    ("ילי", "YodLamedYod", "Sagesse divine", 50),
    ("סיט", "SamekhYodTet", "Protection contre l'envie", 79),
    ("עלמ", "AyinLamedMem", "Guerison du corps", 150),
    ("מהש", "MemHeShin", "Guerison de l'ame", 345),
    ("ללה", "LamedLamedHe", "Revelation des secrets", 65),
    ("אכא", "AlephKhafAleph", "Abondance financiere", 22),
    ("כהת", "KhafHeTav", "Fertilite et prosperite", 425),
    ("הזי", "HeZayinYod", "Pardon et compassion", 22),
    ("אלד", "AlephLamedDalet", "Protection des enfants", 35),
    ("לאו", "LamedAlephVav", "Victoire sur les ennemis", 37),
    ("ההע", "HeHeAyin", "Liberation des peurs", 80),
    ("יזל", "YodZayinLamed", "Abondance et richesse", 47),
    ("מבה", "MemBetHe", "Harmonie conjugale", 47),
    ("הרי", "HeReshYod", "Clarte mentale", 215),
    ("הקם", "HeQofMem", "Elevation spirituelle", 145),
    ("לאו", "LamedAlephVav", "Revelation prophetique", 37),
    ("כלי", "KhafLamedYod", "Abondance universelle", 60),
    ("לוו", "LamedVavVav", "Liberation de la culpabilite", 42),
    ("פהל", "PeHeLamed", "Transformation interieure", 115),
    ("נלכ", "NunLamedKhaf", "Liberation des addictions", 110),
    ("ייי", "YodYodYod", "Connexion divine directe", 30),
    ("מלה", "MemLamedHe", "Protection en voyage", 75),
    ("חהו", "ChetHeVav", "Guerison emotionnelle", 25),
    ("נתה", "NunTavHe", "Paix interieure", 455),
    ("האא", "HeAlephAleph", "Pardon de soi", 7),
    ("ירת", "YodReshTav", "Prosperite financiere", 610),
    ("שאה", "ShinAlephHe", "Abondance de sante", 306),
    ("ריא", "ReshYodAyin", "Guerison spirituelle", 281),
    ("אומ", "AlephVavMem", "Protection divine supreme", 47),
    ("לכב", "LamedKhafBet", "Equilibre emotionnel", 52),
    ("ושר", "VavShinResh", "Clarte des priorites", 506),
    ("יחו", "YodChetVav", "Liberation du karma", 34),
    ("להח", "LamedHeChet", "Annulation des mauvais decrets", 73),
    ("כוק", "KhafVavQof", "Fertilite et enfantement", 126),
    ("מנד", "MemNunDalet", "Guerison des maladies graves", 94),
    ("אני", "AlephNunYod", "Abondance de sagesse", 61),
    ("חעמ", "ChetAyinMem", "Protection du foyer", 118),
    ("רהע", "ReshHeAyin", "Pardon divin", 275),
    ("ייז", "YodYodZayin", "Annulation du mauvais oeil", 27),
    ("ההה", "HeHeHe", "Purification de l'ame", 15),
    ("מיכ", "MemYodKhaf", "Guerison de la depressions", 80),
    ("ווו", "VavVavVav", "Annulation des malefices", 18),
    ("ילה", "YodLamedHe", "Succes et reconnaissance", 45),
    ("סאל", "SamekhAlephLamed", "Abondance financiere soudaine", 91),
    ("ערי", "AyinReshYod", "Protection des biens", 280),
    ("עשל", "AyinShinLamed", "Elevation professionnelle", 400),
    ("מיה", "MemYodHe", "Liberte et independance", 55),
    ("והו", "VavHeVav", "Joie et bonheur", 17),
    ("דני", "DaletNunYod", "Justice divine", 64),
    ("החש", "HeChetShin", "Guerison genetique", 313),
    ("עמם", "AyinMemMem", "Protection des proches", 140),
    ("ננא", "NunNunAleph", "Abondance d'amour", 101),
    ("נית", "NunYodTav", "Immortalite de l'ame", 460),
    ("מבה", "MemBetHe", "Communication divine", 47),
    ("פוי", "PeVavYod", "Transformation financiere", 96),
    ("נממ", "NunMemMem", "Purification energetique", 130),
    ("ייל", "YodYodLamed", "Protection nocturne", 50),
    ("הרח", "HeReshChet", "Liberation des blocages", 213),
    ("מצר", "MemTzadiResh", "Annulation des dettes", 330),
    ("ומב", "VavMemBet", "Fidelite et loyaute", 48),
    ("יהה", "YodHeHe", "Lumiere interieure", 21),
    ("ענו", "AyinNunVav", "Abondance de paix", 126),
    ("מחי", "MemChetYod", "Protection spirituelle avancee", 58),
    ("דמב", "DaletMemBet", "Guerison de l'inconscient", 46),
    ("מנק", "MemNunQof", "Liberation des peurs profondes", 190),
    ("איע", "AlephYodAyin", "Sagesse universelle", 81),
    ("חבו", "ChetBetVav", "Abondance de bonheur", 20),
    ("ראה", "ReshAlephHe", "Vision spirituelle", 206),
    ("יבמ", "YodBetMem", "Protection angélique", 52),
    ("היי", "HeYodYod", "Guerison miraculeuse", 25),
]

# --- 99 Noms arabes (Asma ul-Husna) ---
# Format: (arabic, transliteration, meaning, abjad if precomputed)
ARABIC_99 = [
    ("الله", "Allah", "Le Nom Supreme", 66),
    ("الرحمن", "Ar-Rahman", "Le Tout Misericordieux", 329),
    ("الرحيم", "Ar-Rahim", "Le Tres Misericordieux", 289),
    ("الملك", "Al-Malik", "Le Roi", 90),
    ("القدوس", "Al-Quddus", "Le Saint", 170),
    ("السلام", "As-Salam", "La Paix", 131),
    ("المؤمن", "Al-Mu'min", "Le Securisant", 167),
    ("المهيمن", "Al-Muhaymin", "Le Preservateur", 145),
    ("العزيز", "Al-Aziz", "Le Puissant", 94),
    ("الجبار", "Al-Jabbar", "Le Contraignant", 206),
    ("المتكبر", "Al-Mutakabbir", "Le Superbe", 662),
    ("الخالق", "Al-Khaliq", "Le Createur", 731),
    ("البارئ", "Al-Bari'", "Le Producteur", 213),
    ("المصور", "Al-Musawwir", "Le Formateur", 336),
    ("الغفار", "Al-Ghaffar", "Le Grand Pardonneur", 1281),
    ("القهار", "Al-Qahhar", "Le Dominateur Supreme", 306),
    ("الوهاب", "Al-Wahhab", "Le Donateur", 14),
    ("الرزاق", "Ar-Razzaq", "Le Pourvoyeur", 308),
    ("الفتاح", "Al-Fattah", "L'Ouvreur", 489),
    ("العليم", "Al-Alim", "L'Omniscient", 150),
    ("القابض", "Al-Qabid", "Celui qui retient", 903),
    ("الباسط", "Al-Basit", "Celui qui etend", 72),
    ("الخافض", "Al-Khafid", "Celui qui abaisse", 1481),
    ("الرافع", "Ar-Rafi'", "Celui qui eleve", 351),
    ("المعز", "Al-Mu'izz", "Celui qui honore", 117),
    ("المذل", "Al-Mudhill", "Celui qui humilie", 770),
    ("السميع", "As-Sami'", "L'Audient", 180),
    ("البصير", "Al-Basir", "Le Clairvoyant", 302),
    ("الحكم", "Al-Hakam", "Le Juge", 68),
    ("العدل", "Al-Adl", "Le Juste", 104),
    ("اللطيف", "Al-Latif", "Le Subtil", 129),
    ("الخبير", "Al-Khabir", "Le Bien Informe", 812),
    ("الحليم", "Al-Halim", "L'Indulgent", 88),
    ("العظيم", "Al-Azim", "L'Immense", 1020),
    ("الغفور", "Al-Ghafur", "Le Pardonneur", 1286),
    ("الشكور", "Ash-Shakur", "Le Reconnaissant", 526),
    ("العلي", "Al-Ali", "L'Eleve", 110),
    ("الكبير", "Al-Kabir", "Le Grand", 232),
    ("الحفيظ", "Al-Hafiz", "Le Gardien", 998),
    ("المقيت", "Al-Muqit", "Le Nourricier", 550),
    ("الحسيب", "Al-Hasib", "Le Suffisant", 80),
    ("الجليل", "Al-Jalil", "Le Majestueux", 73),
    ("الكريم", "Al-Karim", "Le Genereux", 270),
    ("الرقيب", "Ar-Raqib", "L'Observateur", 312),
    ("المجيب", "Al-Mujib", "Celui qui repond", 55),
    ("الواسع", "Al-Wasi'", "L'Immense", 137),
    ("الحكيم", "Al-Hakim", "Le Sage", 78),
    ("الودود", "Al-Wadud", "L'Aimant", 20),
    ("المجيد", "Al-Majid", "Le Glorieux", 57),
    ("الباعث", "Al-Ba'ith", "Celui qui ressuscite", 573),
    ("الشهيد", "Ash-Shahid", "Le Temoin", 319),
    ("الحق", "Al-Haqq", "La Verite", 108),
    ("الوكيل", "Al-Wakil", "Le Garant", 66),
    ("القوي", "Al-Qawi", "Le Fort", 116),
    ("المتين", "Al-Matin", "Le Ferme", 500),
    ("الولي", "Al-Wali", "Le Protecteur", 46),
    ("الحميد", "Al-Hamid", "Le Digne de Louange", 62),
    ("المحصي", "Al-Muhsi", "Le Computeur", 148),
    ("المبدئ", "Al-Mubdi'", "L'Initiateur", 86),
    ("المعيد", "Al-Mu'id", "Le Restaurateur", 124),
    ("المحيي", "Al-Muhyi", "Celui qui fait vivre", 68),
    ("المميت", "Al-Mumit", "Celui qui fait mourir", 490),
    ("الحي", "Al-Hayy", "Le Vivant", 18),
    ("القيوم", "Al-Qayyum", "L'Eternel", 156),
    ("الواجد", "Al-Wajid", "Celui qui trouve", 47),
    ("الماجد", "Al-Majid", "Le Noble", 48),
    ("الواحد", "Al-Wahid", "L'Unique", 19),
    ("الاحد", "Al-Ahad", "Le Seul", 13),
    ("الصمد", "As-Samad", "L'Impenetrable", 134),
    ("القادر", "Al-Qadir", "Le Capable", 305),
    ("المقتدر", "Al-Muqtadir", "Le Tout-Puissant", 744),
    ("المقدم", "Al-Muqaddim", "Celui qui avance", 184),
    ("المؤخر", "Al-Mu'akhkhir", "Celui qui retarde", 846),
    ("الأول", "Al-Awwal", "Le Premier", 37),
    ("الآخر", "Al-Akhir", "Le Dernier", 801),
    ("الظاهر", "Az-Zahir", "L'Apparent", 1106),
    ("الباطن", "Al-Batin", "Le Cache", 62),
    ("الوالي", "Al-Wali", "Le Maitre", 47),
    ("المتعالي", "Al-Muta'ali", "Le Transcendant", 551),
    ("البر", "Al-Barr", "Le Bienfaisant", 202),
    ("التواب", "At-Tawwab", "L'Accepteur du repentir", 409),
    ("المنتقم", "Al-Muntaqim", "Le Vengeur", 630),
    ("العفو", "Al-Afuww", "L'Indulgent", 156),
    ("الرؤوف", "Ar-Ra'uf", "Le Bienveillant", 287),
    ("مالك الملك", "Malik al-Mulk", "Le Roi du Royaume", 211),
    ("ذو الجلال والإكرام", "Dhu al-Jalal wa al-Ikram", "Le Detenteur de Majeste", 1099),
    ("المقسط", "Al-Muqsit", "L'Equitable", 239),
    ("الجامع", "Al-Jami'", "Le Rassembleur", 114),
    ("الغني", "Al-Ghani", "Le Riche", 1060),
    ("المغني", "Al-Mughni", "L'Enrichisseur", 1100),
    ("المانع", "Al-Mani'", "Celui qui empeche", 161),
    ("الضار", "Ad-Darr", "Celui qui nuit", 1001),
    ("النافع", "An-Nafi'", "L'Utile", 201),
    ("النور", "An-Nur", "La Lumiere", 256),
    ("الهادي", "Al-Hadi", "Le Guide", 20),
    ("البديع", "Al-Badi'", "L'Inventeur", 86),
    ("الباقي", "Al-Baqi", "Le Permanent", 113),
    ("الوارث", "Al-Warith", "L'Heritier", 707),
    ("الرشيد", "Ar-Rashid", "Le Bien-Dirige", 514),
    ("الصبور", "As-Sabur", "Le Patient", 298),
]


def gematria_hebrew(text: str) -> int:
    values = {
        "א": 1, "ב": 2, "ג": 3, "ד": 4, "ה": 5, "ו": 6, "ז": 7, "ח": 8, "ט": 9,
        "י": 10, "כ": 20, "ך": 20, "ל": 30, "מ": 40, "ם": 40, "נ": 50, "ן": 50,
        "ס": 60, "ע": 70, "פ": 80, "ף": 80, "צ": 90, "ץ": 90, "ק": 100, "ר": 200,
        "ש": 300, "ת": 400,
    }
    return sum(values.get(c, 0) for c in text)


def abjad_arabic(text: str) -> int:
    values = {
        "ا": 1, "أ": 1, "إ": 1, "آ": 1, "ٱ": 1, "ء": 1, "ؤ": 6, "ئ": 10,
        "ب": 2, "ج": 3, "د": 4, "ه": 5, "ة": 5, "و": 6, "ز": 7, "ح": 8, "ط": 9,
        "ي": 10, "ى": 10, "ك": 20, "ل": 30, "م": 40, "ن": 50, "س": 60, "ع": 70,
        "ف": 80, "ص": 90, "ق": 100, "ر": 200, "ش": 300, "ت": 400, "ث": 500,
        "خ": 600, "ذ": 700, "ض": 800, "ظ": 900, "غ": 1000,
    }
    return sum(values.get(c, 0) for c in text)


def digital_root(n: int) -> int:
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def phi_distance(a: int, b: int) -> float:
    """How close is ratio a/b or b/a to phi or 1/phi?"""
    if a == 0 or b == 0:
        return 999
    ratio = a / b
    d1 = abs(ratio - PHI)
    d2 = abs(ratio - INV_PHI)
    d3 = abs(1 / ratio - PHI) if ratio != 0 else 999
    d4 = abs(1 / ratio - INV_PHI) if ratio != 0 else 999
    return min(d1, d2, d3, d4)


def main():
    # Compute actual gematria for Hebrew names
    hebrew_data = []
    for heb, translit, meaning, _ in HEBREW_72:
        gematria = gematria_hebrew(heb)
        root_val = digital_root(gematria)
        hebrew_data.append({
            "hebrew": heb,
            "transliteration": translit,
            "meaning": meaning,
            "gematria": gematria,
            "digital_root": root_val,
        })

    # Compute actual abjad for Arabic names
    arabic_data = []
    for ar, translit, meaning, _ in ARABIC_99:
        abjad = abjad_arabic(ar)
        root_val = digital_root(abjad)
        arabic_data.append({
            "arabic": ar,
            "transliteration": translit,
            "meaning": meaning,
            "abjad": abjad,
            "digital_root": root_val,
        })

    # Find phi resonances between Hebrew and Arabic names
    phi_pairs = []
    for h in hebrew_data:
        for a in arabic_data:
            d = phi_distance(h["gematria"], a["abjad"])
            if d < 0.05:  # within 5% of phi
                ratio = h["gematria"] / a["abjad"] if a["abjad"] > 0 else 0
                phi_pairs.append({
                    "hebrew": h,
                    "arabic": a,
                    "distance": round(d, 6),
                    "ratio": round(ratio, 4),
                    "hebrew_val": h["gematria"],
                    "arabic_val": a["abjad"],
                })

    phi_pairs.sort(key=lambda x: x["distance"])

    # Stats
    total_sum = sum(h["gematria"] for h in hebrew_data) + sum(a["abjad"] for a in arabic_data)
    hebrew_sum = sum(h["gematria"] for h in hebrew_data)
    arabic_sum = sum(a["abjad"] for a in arabic_data)
    grand_total = len(hebrew_data) + len(arabic_data)

    output = {
        "meta": {
            "title": "Le Pont des 72+99 — Analyse des resonances phi",
            "hebrew_count": len(hebrew_data),
            "arabic_count": len(arabic_data),
            "total_names": grand_total,
            "total_171": 72 + 99,
            "sum_171_equation": f"72 + 99 = {grand_total} = 19 x {grand_total // 19} reste {grand_total % 19}",
            "hebrew_total_gematria": hebrew_sum,
            "arabic_total_abjad": arabic_sum,
            "combined_total": total_sum,
            "phi": PHI,
            "inverse_phi": INV_PHI,
            "phi_pairs_count": len(phi_pairs),
            "top_phi_pairs": phi_pairs[:30],
        },
        "hebrew_names": hebrew_data,
        "arabic_names": arabic_data,
        "all_phi_pairs": phi_pairs,
    }

    out_path = Path("C:/Users/eddaz/Desktop/CORAN NUM TAL/corpus/computed/pont_72_99_data.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"72 noms hebreux calcules. Total guematria: {hebrew_sum}")
    print(f"99 noms arabes calcules. Total abjad: {arabic_sum}")
    print(f"Somme combinee: {total_sum}")
    print(f"Paires en resonance phi (<5%): {len(phi_pairs)}")
    print(f"Top 10 resonances phi:")
    for p in phi_pairs[:10]:
        print(f"  {p['hebrew']['transliteration']} ({p['hebrew']['gematria']}) <-> "
              f"{p['arabic']['transliteration']} ({p['arabic']['abjad']}) "
              f"ratio={p['ratio']} dist={p['distance']}")
    print(f"\nData saved to: {out_path}")


if __name__ == "__main__":
    main()
