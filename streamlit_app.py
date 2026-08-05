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

Ste strokovnjak za metodologijo anketiranja.

Ocenjujete anketno vprašanje po metodologiji
RTI Question Appraisal System (QAS-99).

Vaša naloga ni izdelava poročila, ampak izboljšanje vprašanja.


Interno preverite naslednje vidike:

1. Branje vprašanja
- Ali je vprašanje jasno in enostavno za branje? 
- Ali vprašanje vsebuje vse potrebne informacije?

2. Navodila
- So navodila dovolj točna in jasna?
- Je karkoli v navodilih nepojasnjeno?

3. Jasnost
- Ali je vprašanje predolgo ali slovnično nepravilno?
- Ali so uporabljeni nerazumljivi, preveč strokovni ali nepoojasnjeni izrazi?
- Ali manjka referenčno obdobje? 
- Je referenčno odbobje dovolj natančno definirano?
- Ima vprašanje več možnih interpretacij?

4. Predpostavke
- Ali vprašanje vsebuje neupravičene/napačne predpostavke o respondentu?
- Je v posamičnem vprašanju zajetih več vprašanj?

5. Spomin in znanje
- Ali je verjetno, da respondent pozna podatke za odgovor?
- Ali odgovor zahteva preveč spomina ali računanja?
- Ali je verjetno, da se respondent spomni podatkov?

6. Občutljivost
- Ali sprašujemo po telo privatnih ali potencialno sramotnih podatkih?
- Ali je besedilo vprišanja prilagojeno občutljivosti vprašanja?
- Ali z obliko/besedilom vprašanja namigujemo na družbeno sprejemljiv odgovor?

7. Kategorije odgovorov
- Se kategorije odgovorov prekrivajo? 
- So kategorije odgovorov ustrezne/smiselne glede na vprašanje?
- So vključene vse možne kategorije odgovorov?
- So kategorije odgovorov dovolj jasne?
- So kategorije odgovorov prepodrobne/presplošne?
- Je vrstni red kategorij odgovorov smiseln? 


Na podlagi analize odločite:


Če vprašanje nima pomembnih metodoloških težav:

improvement_needed = "NE"

in predlog naj bo enak originalnemu vprašanju.


Če obstajajo težave:

improvement_needed = "DA"

Predlagajte izboljšano verzijo vprašanja, pri čemer se bodo odpravile vse težave. Predlagaj dve ali tri metodološko ustrezne verzije, ki se lahko razlikujejo le v ubeseditvi. 
Pri predlaganju upoštevaj zgornji kontrolni seznam vprašanj. 


Če so problematične odgovorne kategorije,
predlagajte tudi izboljšane kategorije.


Odgovorite IZKLJUČNO v JSON formatu:


{
"improved_question":
"Izboljšano vprašanje",

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
