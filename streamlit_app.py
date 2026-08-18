import streamlit as st
from openai import OpenAI
import json

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="QAS-99 – Izboljšava anketnih vprašanj",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SURS OBLIKOVANJE
# ============================================================

st.markdown(
    """
    <style>

    .main .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .surs-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 18px;
        margin-bottom: 35px;
        border-bottom: 2px solid #0078A8;
    }

    .app-title {
        font-size: 32px;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 6px;
    }

    .app-subtitle {
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 32px;
    }

    textarea {
        border-radius: 8px !important;
    }

    .stButton > button {
        border-radius: 7px;
        font-weight: 600;
        min-height: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SURS GLAVA
# ============================================================

col_logo, col_empty = st.columns([3, 1])

with col_logo:

    st.image(
        "surs_logo.png",
        width=230
    )

    st.markdown(
        """
        <div style="
            margin-top: -12px;
            margin-left: 2px;
            color: #6B7280;
            font-size: 18px;
            font-weight: 500;
            letter-spacing: 0.2px;
        ">
            Oddelek za sprejemanje podatkov
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    "<div class='surs-header'></div>",
    unsafe_allow_html=True
)


# ============================================================
# NASLOV APLIKACIJE
# ============================================================


# ============================================================
# OPENROUTER CLIENT
# ============================================================

client = OpenAI(
    api_key=st.secrets["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1"
)

# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
Si strokovnjak za metodologijo anketiranja in oblikovanje vprašalnikov. Tvoja naloga je evalvacija osnutkov anketnih vprašanj in njihovih kategorij odgovorov z uporabo sistema presoje vprašanj RTI (Question Appraisal System – QAS-99) (glej Willis, G. in Lesser, J. T. (1999). Question Appraisal System: QAS-99. Rockville: Research Triangle Institute).

QAS je metoda za sistematično presojo anketnih vprašanj, ki omogoča prepoznavanje težav v formulaciji ali strukturi vprašanj ter kategorijah odgovorov, ki lahko povzročijo težave pri izvedbi ankete ali predstavljajo izzive za respondente pri izvajanju kognitivnih procesov, potrebnih za odgovarjanje na vprašanja.

Pet glavnih faz kognitivne obdelave pri odgovarjanju na anketna vprašanja je:

razumevanje vprašanja in priklic informacij iz spomina, potrebnih za odgovor;
razumevanje vprašanja in naloge odgovarjanja;
priklic potrebnih informacij iz spomina;
oblikovanje presoje na podlagi priklicanih informacij;
odločanje o načinu poročanja odgovora in izbira ustrezne kategorije odgovora.

Vaša naloga je pregledati anketna vprašanja in jih ovrednotiti z uporabo sistema QAS. Pri tem upoštevajte posamezne značilnosti vprašanja in kategorij odgovorov po posameznih korakih.

Pri vsakem koraku presodite, ali vprašanje vsebuje značilnosti, ki bi lahko povzročile težave.

Za izvedbo evalvacije morate upoštevati:

formulacijo vprašanja;
kategorije odgovorov;

ter za vsak korak določiti, ali je prisotna težava (DA ali NE), in v primeru odgovora DA potem v končnem predlogu vprašanja to napako odpraviti. 
1. KORAK: BRANJE (READING)

Presodite, ali imajo anketarji težave pri enotni predstavitvi vprašanja vsem respondentom ali ali imajo respondenti težave pri samostojnem branju vprašanja.

Q1a:

Anketar ima lahko težave pri določanju, katere dele vprašanja mora prebrati, ali respondent težko presodi, katere dele vprašanja mora upoštevati kot pomembne.

Primeri:

besedilo v oklepajih,
drugačna pisava,
poševno tiskano besedilo.
Q1b:

Informacije, ki jih anketar potrebuje za izvedbo vprašanja ali ki jih respondent potrebuje za razumevanje vprašanja, niso vključene.

Q1c:

Vprašanje ni v celoti pripravljeno za branje s strani anketarja, zato ga je težko pravilno prebrati, ali pa zahteva od respondentov visoko raven bralne sposobnosti oziroma izobrazbe za razumevanje.

2. KORAK: NAVODILA (INSTRUCTIONS)

Poiščite težave z uvodi, navodili ali pojasnili z vidika respondenta.

Q2a:

Nasprotujoča ali netočna navodila, uvodi ali pojasnila.

Q2b:

Zapletena navodila, uvodi ali pojasnila.

3. KORAK: JASNOST (CLARITY)

Prepoznajte težave, povezane s sporočanjem namena oziroma pomena vprašanja respondentom.

Q3a: Formulacija vprašanja

Vprašanje je:

predolgo,
nerodno oblikovano,
slovnično nepravilno,
vsebuje zapleteno skladnjo.
Q3b: Strokovni oziroma tehnični izrazi

Tehnični izrazi so:

nedefinirani,
nejasni,
zapleteni.
Q3c: Nejasnost (vagueness)

Obstaja več možnih načinov interpretacije vprašanja ali odločanja, kaj vključiti oziroma izključiti.

Q3d: Referenčno obdobje

Referenčno obdobje (npr. »v zadnjem mesecu«):

manjka,
ni ustrezno določeno,
je v nasprotju z drugimi deli vprašanja.
4. KORAK: PREDPOSTAVKE (ASSUMPTIONS)

Presodite, ali vprašanje vsebuje problematične predpostavke ali neustrezno logiko.

Q4a:

Prisotne so neustrezne predpostavke o respondentu ali njegovem življenjskem položaju.

Q4b:

Vprašanje predpostavlja nespremenljivo vedenje ali izkušnje pri situacijah, ki se lahko razlikujejo.

Q4c:

Dvojno vprašanje: vprašanje vsebuje več kot eno implicitno vprašanje.

5. KORAK: ZNANJE/SPOMIN (KNOWLEDGE/MEMORY)

Preverite, ali respondenti verjetno nimajo potrebnega znanja ali imajo težave s priklicem informacij.

Q5a: Znanje morda ne obstaja

Respondent verjetno ne pozna odgovora na dejstveno vprašanje.

Q5b: Stališče morda ne obstaja

Respondent verjetno nima oblikovanega stališča o temi, na katero se vprašanje nanaša.

Q5c: Težava s priklicem

Respondent se morda ne more spomniti zahtevane informacije.

Q5d: Težava z računanjem

Vprašanje zahteva zahtevno miselno računanje.

6. KORAK: OBČUTLJIVOST/PRISTRANSKOST (SENSITIVITY/BIAS)

Presodite vprašanja glede občutljive vsebine, formulacije in možnosti pristranskosti.

Q6a: Splošna občutljiva vsebina

Vprašanje se nanaša na temo, ki je:

neprijetna,
zelo zasebna,
povezana z nezakonitim vedenjem.
Q6b: Občutljiva formulacija

Ker je tema občutljiva, bi bilo treba formulacijo izboljšati, da bi zmanjšali občutljivost vprašanja.

Q6c:

Vprašanje nakazuje družbeno zaželen odgovor.

7. KORAK: KATEGORIJE ODGOVOROV (RESPONSE CATEGORIES)

Presodite ustreznost razpona možnih odgovorov.

Q7a:

Odprto vprašanje je neustrezno ali težavno za odgovor.

Q7b:

Neujemanje med vprašanjem in kategorijami odgovorov.

Q7c:

Tehnični izrazi v kategorijah odgovorov so nedefinirani, nejasni ali zapleteni.

Q7d:

Nejasne kategorije odgovorov omogočajo več različnih interpretacij.

Q7e:

Kategorije odgovorov se prekrivajo.

Q7f:

Manjkajo možni odgovori, ki bi jih respondent lahko izbral.

Q7g:

Nelogičen vrstni red kategorij odgovorov.

8. KORAK: DRUGO (OTHER)

Poiščite težave, ki niso bile prepoznane v korakih 1–7.

Q8a:

Druge težave, ki niso bile predhodno identificirane.

Vaša naloga je oceniti osnutke vprašanj tako, da sistematično pregledate vseh 8 korakov in pripadajoče podkategorije.

Dodatna priporočila

a. Predpostavite, da bodo vprašanja uporabljena v samostojno izpolnjevanem papirnem vprašalniku, vendar upoštevajte tudi, ali bi bila primerna za izvedbo osebnega ali telefonskega anketiranja.

b. Vprašanja se razlikujejo glede na število in vrsto težav, ki jih lahko povzročajo. Ni treba, da vsako vprašanje vsebuje vse vrste težav, vendar bodite pri presoji čim bolj temeljiti.

c. Pri kodiranju si predstavljajte različne tipe respondentov in različne življenjske okoliščine. Upoštevajte dejavnike, kot so starost ali izobrazba respondenta, ki lahko vplivajo na njegovo sposobnost odgovarjanja.

d. Pri presoji bodite previdni – če obstaja kakršnakoli možnost, da bi vprašanje pri nekaterih respondentih povzročilo zmedo ali napačno interpretacijo, ga označite z DA.Navodila za evalvacijo

Na podlagi analize odloči:


Če vprašanje nima nobenih metodoloških težav na podlagi zgornjega sistematičnega pregleda:

improvement_needed = "NE"

in predlog naj bo enak originalnemu vprašanju.


Če obstajajo težave:

improvement_needed = "DA"

Predlagaj tri popravljene verzije vprašanja z odpravljenimi težavami.  

Če so tudi kategorije odgovorov neustrezne, odpravi težave in predlagaj izboljšane kategorije.



============================================================
FORMAT KONČNEGA ODGOVORA
============================================================

Po opravljeni analizi po QAS-99 moraš na koncu vrniti rezultate
v obliki veljavnega JSON-a.

Pomembno:

- Ne odstranjuj ali izpuščaj nobenega dela zgornjih navodil.
- Analizo po QAS-99 izvedi na podlagi vseh zgornjih navodil.
- Uporabniku ne prikazuj razlage analize.
- Končni odgovor mora biti IZKLJUČNO veljaven JSON.
- Pred JSON-om ne dodajaj nobenega besedila.
- Za JSON-om ne dodajaj nobenega besedila.
- Ne uporabljaj Markdown oznak.
- Ne uporabljaj ```json ali ``` oznak.
- Ne dodajaj uvoda, zaključka ali komentarjev.

Vrni 2 do 3 različne smiselne predloge izboljšanega vprašanja.

Uporabi natanko naslednjo strukturo:

{
  "results": [
    {
      "improved_question": "izboljšano vprašanje 1",
      "improved_categories": [
        "kategorija odgovora 1",
        "kategorija odgovora 2"
      ]
    },
    {
      "improved_question": "izboljšano vprašanje 2",
      "improved_categories": [
        "kategorija odgovora 1",
        "kategorija odgovora 2"
      ]
    },
    {
      "improved_question": "izboljšano vprašanje 3",
      "improved_categories": [
        "kategorija odgovora 1",
        "kategorija odgovora 2"
      ]
    }
  ]
}

Vsak element v "results" mora vsebovati:

1. "improved_question"
   - izboljšano oziroma popravljeno vprašanje;

2. "improved_categories"
   - ustrezne kategorije odgovorov za to vprašanje.

Če vprašanje ne potrebuje bistvenega izboljšanja, ga lahko ohraniš
oziroma minimalno spremeniš.

Kategorije odgovorov morajo biti smiselne glede na vprašanje,
medsebojno čim bolj izključujoče in skupaj pokrivati relevantne
možne odgovore.

Če gre za odprto vprašanje, uporabi:

"improved_categories": []

Ne vračaj nobenega dodatnega besedila izven JSON strukture.

Vedno vrni veljaven JSON.
"""


# ============================================================
# NASLOV APLIKACIJE
# ============================================================

st.title("Izboljšava anketnih vprašanj")

st.write(
    "Vnesite anketno vprašanje in po potrebi kategorije odgovorov. "
    "Vprašanje bo analizirano po metodologiji QAS-99 (Willis in Lesser, 1999)."
)


# ============================================================
# VNOS VPRAŠANJA
# ============================================================

question = st.text_area(
    "Anketno vprašanje",
    placeholder="Vnesite vprašanje ...",
    height=120
)


# ============================================================
# VNOS KATEGORIJ
# ============================================================

categories = st.text_area(
    "Kategorije odgovorov",
    placeholder=(
        "Vnesite kategorije odgovorov, vsako v svojo vrstico "
        "(če gre za odprto vprašanje, pustite prazno)."
    ),
    height=150
)


# ============================================================
# GUMB
# ============================================================

if st.button(
    "Izboljšaj vprašanje",
    use_container_width=True
):

    # --------------------------------------------------------
    # PREVERJANJE VPRAŠANJA
    # --------------------------------------------------------

    if not question.strip():

        st.warning(
            "Vnesite vprašanje."
        )

        st.stop()


    # --------------------------------------------------------
    # PRIPRAVA PROMPTA
    # --------------------------------------------------------

    prompt = f"""
VPRAŠANJE:

{question}

KATEGORIJE ODGOVOROV:

{
categories
if categories.strip()
else
"Odprto vprašanje"
}
"""


    # --------------------------------------------------------
    # KLIC MODELA
    # --------------------------------------------------------

    with st.spinner(
        "Analiziram vprašanje po QAS-99..."
    ):

        try:

            response = client.chat.completions.create(

                model= "gpt-oss-20b",

                temperature=0.1,

                messages=[

                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ]

            )


            # ------------------------------------------------
            # PREBERI ODGOVOR MODELA
            # ------------------------------------------------

            result_text = response.choices[0].message.content


            # ------------------------------------------------
            # PREVERI PRAZEN ODGOVOR
            # ------------------------------------------------

            if not result_text:

                raise ValueError(
                    "Model je vrnil prazen odgovor."
                )


            # ------------------------------------------------
            # ODSTRANI MOREBITNE MARKDOWN OZNAKE
            # ------------------------------------------------

            result_text = (
                result_text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )


            # ------------------------------------------------
            # PRETVORBA JSON
            # ------------------------------------------------

            try:

                result = json.loads(
                    result_text
                )

            except json.JSONDecodeError as e:

                st.error(
                    "Model ni vrnil veljavnega JSON-a."
                )

                st.code(
                    result_text,
                    language="text"
                )

                st.stop()


            # ------------------------------------------------
            # PREVERJANJE STRUKTURE JSON-A
            # ------------------------------------------------

            if "results" not in result:

                st.error(
                    "Odgovor modela nima pričakovane strukture "
                    "'results'."
                )

                st.code(
                    json.dumps(
                        result,
                        ensure_ascii=False,
                        indent=2
                    ),
                    language="json"
                )

                st.stop()


            if not isinstance(
                result["results"],
                list
            ):

                st.error(
                    "Polje 'results' mora biti seznam."
                )

                st.stop()


            if len(result["results"]) == 0:

                st.error(
                    "Model ni vrnil nobenega predloga."
                )

                st.stop()


            # ------------------------------------------------
            # PRIKAZ REZULTATOV
            # ------------------------------------------------

            st.divider()

            st.subheader(
                "Predlagane izboljšave"
            )


            # ------------------------------------------------
            # POSAMEZNI PREDLOGI
            # ------------------------------------------------

            for i, suggestion in enumerate(
                result["results"],
                start=1
            ):

                st.markdown(
                    f"### Predlog {i}"
                )


                # --------------------------------------------
                # PREVERI VPRAŠANJE
                # --------------------------------------------

                improved_question = suggestion.get(
                    "improved_question",
                    ""
                )


                if improved_question:

                    st.info(
                        improved_question
                    )

                else:

                    st.warning(
                        "Predlog nima navedenega vprašanja."
                    )


                # --------------------------------------------
                # KATEGORIJE ODGOVOROV
                # --------------------------------------------

                improved_categories = suggestion.get(
                    "improved_categories",
                    []
                )


                if improved_categories:

                    st.markdown(
                        "**Predlagane kategorije odgovorov:**"
                    )


                    for cat in improved_categories:

                        st.write(
                            f"- {cat}"
                        )

                else:

                    st.caption(
                        "Odprto vprašanje – kategorije odgovorov "
                        "niso predlagane."
                    )


                # --------------------------------------------
                # LOČNICA
                # --------------------------------------------

                if i < len(result["results"]):

                    st.divider()


        # ====================================================
        # NAPAKA
        # ====================================================

        except Exception as e:

            st.error(
                f"Napaka pri analizi: {e}"
            )
