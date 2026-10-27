#!/usr/bin/env python3
"""Roda um comando toda vez que um arquivo muda. Sem instalar nada.

    python main.py "pytest -q"
    python main.py "python app.py" --pasta src --ext .py .html

Existe biblioteca para isso (watchdog), e ela é melhor em pasta gigante. Esta
versão cabe num arquivo e usa só a biblioteca padrão: compara o mtime de cada
arquivo a cada intervalo.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path


def instantaneo(pasta, extensoes):
    """{caminho: mtime} de tudo que interessa, agora."""
    return {f: f.stat().st_mtime for f in pasta.rglob("*")
            if f.is_file() and (not extensoes or f.suffix in extensoes)
            and ".git" not in f.parts and "__pycache__" not in f.parts}


def main():
    ap = argparse.ArgumentParser(description="roda um comando quando algo muda")
    ap.add_argument("comando")
    ap.add_argument("--pasta", type=Path, default=Path("."))
    ap.add_argument("--ext", nargs="*", default=[".py"])
    ap.add_argument("--intervalo", type=float, default=0.5)
    ap.add_argument("--uma-vez", action="store_true", help="sai após o primeiro ciclo")
    a = ap.parse_args()

    extensoes = set(a.ext)
    antes = instantaneo(a.pasta, extensoes)
    print(f"vigiando {len(antes)} arquivo(s) em {a.pasta.resolve()} — ctrl+c para sair")

    if a.uma_vez:
        return 0

    while True:
        time.sleep(a.intervalo)
        agora = instantaneo(a.pasta, extensoes)
        mudou = [f for f in agora if antes.get(f) != agora[f]]
        # Salvar um arquivo costuma gerar DOIS eventos (o editor escreve e
        # depois ajusta o mtime). Comparar o instantâneo inteiro de uma vez,
        # em vez de reagir a evento, já resolve isso sem debounce.
        if mudou:
            print(f"\n>>> mudou: {', '.join(f.name for f in mudou[:3])}")
            subprocess.run(a.comando, shell=True)
        antes = agora


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nsaindo")
