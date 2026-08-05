import streamlit as st
from openai import OpenAI
import json


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="QAS-99 izboljševalnik vprašanj",
    page_icon="📋",
    layout="centered"
)


# =====================================================
# CSS
# =====================================================

st.markdown(
"""
<style>

.main {
    padding-top:2rem;
}


h1 {
    color:#1f4e79;
    text-align:center;
}


.stButton button {

    background-color:#1f4e79;
    color:white;
    font-weight:600;
    border-radius:8px;

}


.result-box {

background:#eef5fb;
border-left:6px solid #1f4e79;
padding:20px;
border-radius:8px;

}


.success-box {

background:#f1fff4;
border-left:6px solid #198754;
padding:20px;
border-radius:8px;

}


.warning-box {

background:#fff7ef;
border-left:6px solid #fd7e14;
padding:20px;
border-radius:8px;

}

</style>
""",
unsafe_allow_html=True
)



# =====================================================
# GROQ CLIENT
# =====================================================

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)



# =====================================================
# QAS-99 PROMPT
# =====================================================

SYSTEM_PROMPT = """

Ste strokovnjak za metodologijo anketiranja in oblikovanje vprašalnikov. Vaša naloga je evalvacija osnutkov anketnih vprašanj in njihovih kategorij odgovorov z uporabo sistema presoje vprašanj RTI (Question Appraisal System – QAS-99) (glej Willis, G. in Lesser, J. T. (1999). Question Appraisal System: QAS-99. Rockville: Research Triangle Institute).

QAS je metoda za sistematično presojo anketnih vprašanj, ki omogoča prepoznavanje težav v formulaciji ali strukturi vprašanj ter kategorijah odgovorov, ki lahko povzročijo težave pri izvedbi ankete ali predstavljajo izzive za respondente pri izvajanju kognitivnih procesov, potrebnih za odgovarjanje na vprašanja.

Pet glavnih faz kognitivne obdelave pri odgovarjanju na anketna vprašanja je:

razumevanje vprašanja in priklic informacij iz spomina, potrebnih za odgovor;
razumevanje vprašanja in naloge odgovarjanja;
priklic potrebnih informacij iz spomina;
oblikovanje presoje na podlagi priklicanih informacij;
odločanje o načinu poročanja odgovora in izbira ustrezne kategorije odgovora.

Vaša naloga je pregledati osnutke anketnih vprašanj in jih ovrednotiti z uporabo sistema QAS. Pri tem upoštevajte posamezne značilnosti vprašanja in kategorij odgovorov po posameznih korakih.

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

Na podlagi analize odločite:


Če vprašanje nima nobenih metodoloških težav na podlagi zgornjega sistematičnega pregleda:

improvement_needed = "NE"

in predlog naj bo enak originalnemu vprašanju.


Če obstajajo težave:

improvement_needed = "DA"

Predlagajte tri popravljene verzije vprašanja z odpravljenimi težavami.  

Če so problematične odgovorne kategorije,
predlagajte tudi izboljšane kategorije.


Odgovorite IZKLJUČNO v JSON formatu:


{
"improved_question": [
"Izboljšano vprašanje 1",
"Izboljšano vprašanje 2",
"Izboljšano vprašanje 3"
]

"improved_categories":[
"odgovor 1",
"odgovor 2"
]

}


"""



# =====================================================
# TITLE
# =====================================================

st.markdown(
"""
<h1>
📋 QAS-99 izboljševalnik vprašanj
</h1>
""",
unsafe_allow_html=True
)


st.markdown(
"""
<div class="result-box">

Orodje pregleda anketno vprašanje po metodologiji
<b>QAS-99</b> in predlaga izboljšano formulacijo,
če zazna potencialne metodološke težave.

</div>
""",
unsafe_allow_html=True
)



st.divider()



# =====================================================
# INPUT
# =====================================================


question = st.text_area(
    "Vnesite vprašanje",
    height=120,
    placeholder=
    "Primer: Kako pogosto uporabljate splet?"
)



categories = st.text_area(
    "Vnesite kategorije odgovorov",
    height=120,
    placeholder=
"""
Vsak dan
Večkrat tedensko
Redko
Nikoli
"""
)



# =====================================================
# BUTTON
# =====================================================


if st.button(
    "🔍 Izboljšaj vprašanje",
    use_container_width=True
):


    if not question.strip():

        st.warning(
            "Vnesite vprašanje."
        )

        st.stop()



    prompt=f"""

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


    with st.spinner(
        "Analiziram vprašanje po QAS-99..."
    ):


        try:


            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                temperature=0.1,

                messages=[

                    {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                    },

                    {
                    "role":"user",
                    "content":prompt
                    }

                ]

            )



            result_text=response.choices[0].message.content



            result_text=result_text.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()



            result=json.loads(
                result_text
            )



            st.divider()



            st.subheader(
                "Predlagano vprašanje"
            )


            st.info(
                result["improved_question"]
            )



            if result["improved_categories"]:


                st.subheader(
                    "Predlagane kategorije odgovorov"
                )


                for cat in result["improved_categories"]:

                    st.write(
                        "- " + cat
                    )



        except Exception as e:


            st.error(
                f"Napaka pri analizi: {e}"
            )
