# Nënshkrimi digjital me RSA-PSS

**Case study 36 · Introduction to Information Security**
Viona Macastena, Bjondina Hasani dhe Blenda Avdyli

## Nisja hap pas hapi

Duhet Python 3.9.2 ose më i ri. Testimi i paketës është bërë me Python 3.12.14. Hap terminalin brenda dosjes së projektit.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python demo.py
```

**Windows PowerShell**

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe demo.py
```

Rezultati i pritur është `4/4 teste kaluan`. Programi rigjeneron materialin e përkohshëm në çdo ekzekutim. Çelësat privatë përdoren në memorien e procesit. Te tri provat negative, verifikimi duhet të kthejë `False` dhe testi duhet të shënohet `PASS`.

## Rigjenerimi i evidencës

Me ambientin aktiv, përdor komandën e mëposhtme. Në Windows mund të përdorësh po atë rrugë të Python-it si më sipër. Për çdo provë përdor emër të ri për dosjen.

```bash
python demo.py --artifacts prova-01 > log-01.txt
```

`prova-01` përmban dokumentin origjinal, kopjen e ndryshuar, nënshkrimin dhe dy çelësat publikë. Mbaji dokumentin, nënshkrimin dhe çelësin publik të të njëjtit ekzekutim së bashku.

## Verifikimi me OpenSSL

Opsional. Me OpenSSL 3.x, nga dosja e projektit, mund të verifikosh evidencën e paketuar.

```bash
openssl dgst -sha256 -verify evidenca/material-publik/publik.pem -signature evidenca/material-publik/nenshkrimi.sig -sigopt rsa_padding_mode:pss -sigopt rsa_pss_saltlen:32 -sigopt rsa_mgf1_md:sha256 evidenca/material-publik/origjinali.txt
```

Pritet `Verified OK`. Provo të zëvendësosh argumentin e fundit me `evidenca/material-publik/ndryshuar.txt`. Pritet refuzim. Për rastin me çelës të gabuar përdor dokumentin origjinal dhe zëvendëso `publik.pem` me `publik_tjeter.pem`.

## Përgatitja për mbrojtje

- Hap shënimet e folësit në PowerPoint. Ato përmbajnë rrjedhën e prezantimit 8-minutësh dhe kohën e demonstrimit.
- Secili anëtar të provojë `python demo.py` nga fillimi dhe të gjejë në kod ku krijohen çelësat, ku nënshkruhet dokumenti dhe ku trajtohet `InvalidSignature`.
- Për mini-sfidën, ndrysho vetëm `b"950 EUR"` te `document.replace(...)` në `b"700 EUR"` dhe ekzekuto përsëri. Hash-i i kopjes së ndryshuar del ndryshe dhe T2 duhet përsëri të refuzohet.
- Për pyetjen mbi besimin, shpjego çfarë ndodh nëse marrësi pranon një çelës të dërguar nga sulmuesi bashkë me dokumentin dhe nënshkrimin e tij.
- Ndarje e propozuar për provën e prezantimit: Viona Macastena mbulon analizën e sigurisë, Bjondina Hasani demonstron kodin dhe Blenda Avdyli shpjegon evidencën dhe auditimin. Konfirmojeni ndarjen dhe deklaratën e AI në raport. Materiali i kursit përmend një Assessment Brief të veçantë me fazat I–III. Kjo paketë mbulon rastin 36 nga përshkrimi i dhënë.

## Skedarët

| Skedari | Përmbajtja |
| --- | --- |
| Raporti.pdf / Raporti.docx | Raporti pesëfaqësh dhe kopja për redaktim |
| Prezantimi.pptx | Shtatë slajde me shënime për tetë minuta |
| demo.py | Gjenerimi i çelësave, nënshkrimi dhe testet |
| vendimi_fiktiv.txt | Dokumenti hyrës |
| requirements.txt | Versioni i bibliotekës së testuar |
| evidenca/ | Logët dhe materiali publik i testimit |
