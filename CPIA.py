#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CPIA / JOHNSON / IAQ — SISTEMA COGNITIVO UNIFICADO
Versión robusta sin dependencias externas
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import List


# =====================================================
# CONFIG
# =====================================================

MAX_DERIVADAS = 3
DOMAIN_SNAPSHOT = "cpia_snapshot_v1"
DOMAIN_SEAL = "johnson_seal_v1"


# =====================================================
# MERKLE TREE
# =====================================================

class MerkleTree:

    def __init__(self):
        self.leaves = []

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def add(self, data: str):
        self.leaves.append(self._hash(data))

    def root(self):

        if not self.leaves:
            return None

        level = self.leaves[:]

        while len(level) > 1:

            nxt = []

            for i in range(0, len(level), 2):

                left = level[i]
                right = level[i+1] if i+1 < len(level) else left

                nxt.append(self._hash(left + right))

            level = nxt

        return level[0]


# =====================================================
# DICCIONARIO EPISTEMOLÓGICO
# =====================================================

VERIFICACION = [
"se comprobó","se confirmó","se verificó","se observó",
"se midió","se registró","se documentó","se publicó",
"se ejecutó correctamente","se logró","está funcionando"
]

INFERENCIA = [
"según los datos","los datos muestran","el análisis demuestra",
"parece","todo indica","todo apunta a","sugiere",
"podría indicar","se deduce","se infiere"
]

ESPECULACION = [
"se plantea","se propone","se sugiere","se teoriza",
"podría","quizá","tal vez","posiblemente",
"probablemente","se cree","se supone",
"se rumorea","a lo mejor","quién sabe",
"en el futuro","en desarrollo","en pruebas"
]


# =====================================================
# CLASIFICADOR
# =====================================================

def clasificar(texto:str)->str:

    t=texto.lower()

    score_v=0
    score_i=0
    score_e=0

    for m in VERIFICACION:
        if m in t:
            score_v+=2

    for m in INFERENCIA:
        if m in t:
            score_i+=2

    for m in ESPECULACION:
        if m in t:
            score_e+=2

    scores={
    "VERIFICADA":score_v,
    "INFERENCIA":score_i,
    "ESPECULATIVA":score_e
    }

    return max(scores,key=scores.get)


# =====================================================
# BURBUJA
# =====================================================

class Bubble:

    def __init__(self,content,kind):

        self.content=content
        self.kind=kind
        self.timestamp=datetime.now(timezone.utc).isoformat()

    def to_dict(self):

        return{
        "contenido":self.content,
        "tipo":self.kind,
        "timestamp":self.timestamp
        }


# =====================================================
# THEORY ENGINE
# =====================================================

class TheoryEngine:

    def generar(self,text):

        preguntas=[
        f"¿Qué implica realmente: {text}?",
        f"¿Qué pasaría si {text} no fuera cierto?",
        f"¿Qué otros sistemas se ven afectados por {text}?"
        ]

        return preguntas[:MAX_DERIVADAS]


# =====================================================
# LEDGER JOHNSON
# =====================================================

class JohnsonLedger:

    def __init__(self):

        self.chain=[]

    def _hash(self,data):

        canon=json.dumps(data,sort_keys=True,ensure_ascii=False)

        return hashlib.sha256(canon.encode("utf-8")).hexdigest()

    def registrar(self,tipo,data):

        prev=self.chain[-1]["hash"] if self.chain else None

        evento={
        "index":len(self.chain),
        "timestamp":datetime.now(timezone.utc).isoformat(),
        "tipo":tipo,
        "data":data,
        "hash_prev":prev
        }

        evento["hash"]=self._hash(evento)

        self.chain.append(evento)

        return evento


# =====================================================
# SNAPSHOT
# =====================================================

class Snapshot:

    def __init__(self,bubbles,merkle_root):

        self.timestamp=datetime.now(timezone.utc).isoformat()
        self.bubbles=bubbles
        self.merkle_root=merkle_root

    def generar(self):

        resumen={
        "verificadas":sum(1 for b in self.bubbles if b.kind=="VERIFICADA"),
        "inferencias":sum(1 for b in self.bubbles if b.kind=="INFERENCIA"),
        "especulativas":sum(1 for b in self.bubbles if b.kind=="ESPECULATIVA"),
        "derivadas":sum(1 for b in self.bubbles if b.kind=="DERIVADA")
        }

        esencia={
        "estado":"EN_CURSO",
        "resumen":resumen,
        "merkle_root":self.merkle_root
        }

        canon=json.dumps(esencia,sort_keys=True)

        base=f"{DOMAIN_SNAPSHOT}|{self.timestamp}|{canon}"

        h=hashlib.sha256(base.encode()).hexdigest()

        return{
        "timestamp":self.timestamp,
        "hash":h,
        "esencia":esencia
        }


# =====================================================
# SELLO CONTEXTUAL
# =====================================================

class JohnsonSeal:

    def __init__(self,snapshot,responsable,proposito,entorno):

        self.snapshot=snapshot
        self.responsable=responsable
        self.proposito=proposito
        self.entorno=entorno
        self.timestamp=datetime.now(timezone.utc).isoformat()

    def generar(self):

        payload={
        "timestamp":self.timestamp,
        "snapshot_hash":self.snapshot["hash"],
        "responsable":self.responsable,
        "proposito":self.proposito,
        "entorno":self.entorno
        }

        canon=json.dumps(payload,sort_keys=True)

        base=f"{DOMAIN_SEAL}|{canon}"

        h=hashlib.sha256(base.encode()).hexdigest()

        payload["sello_hash"]=h

        return payload


# =====================================================
# MAIN
# =====================================================

def main():

    print("\n=== CPIA / JOHNSON — SISTEMA UNIFICADO ===")
    print("Salir escribiendo: soy el 3\n")

    engine=TheoryEngine()
    ledger=JohnsonLedger()
    merkle=MerkleTree()

    bubbles=[]

    while True:

        texto=input("Contenido: ").strip()

        if texto.lower()=="soy el 3":
            break

        if not texto:
            continue

        bloques=[b.strip() for b in texto.split("\n\n") if b.strip()]

        for bloque in bloques:

            tipo=clasificar(bloque)

            bubble=Bubble(bloque,tipo)

            bubbles.append(bubble)

            merkle.add(bloque)

            ledger.registrar("BURBUJA",bubble.to_dict())

            print("✔",tipo,"\n")

            if tipo!="VERIFICADA":

                preguntas=engine.generar(bloque)

                for p in preguntas:

                    b=Bubble(p,"DERIVADA")

                    bubbles.append(b)

                    ledger.registrar("DERIVADA",b.to_dict())


    root=merkle.root()

    snapshot=Snapshot(bubbles,root).generar()

    ledger.registrar("SNAPSHOT",snapshot)

    sello=JohnsonSeal(
    snapshot,
    responsable="operador",
    proposito="análisis epistemológico",
    entorno="Termux"
    ).generar()

    ledger.registrar("SELLO",sello)

    print("\n=== SNAPSHOT ===")
    print(json.dumps(snapshot,indent=2,ensure_ascii=False))

    print("\n=== SELLO CONTEXTUAL ===")
    print(json.dumps(sello,indent=2,ensure_ascii=False))

    print("\n=== MERKLE ROOT ===")
    print(root)

    print("\n[Fin]")


if __name__=="__main__":
    main()
