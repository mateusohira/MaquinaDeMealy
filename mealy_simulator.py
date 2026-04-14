#!/usr/bin/env python3
"""
ECM253 – Linguagens Formais, Autômatos e Compiladores
Simulador de Máquina de Mealy
"""

import json
import sys
import os


def carregar_maquina(caminho_arquivo: str) -> dict:
    """Lê a descrição da Máquina de Mealy a partir de um arquivo JSON ou Python."""
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError(f"Arquivo '{caminho_arquivo}' não encontrado.")

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    ext = os.path.splitext(caminho_arquivo)[1].lower()

    if ext == '.json':
        maquina = json.loads(conteudo)
    else:
        # Tenta como dict Python via eval()
        maquina = eval(conteudo)

    # Normaliza conjuntos (JSON carrega listas)
    maquina['S'] = set(maquina['S'])
    maquina['I'] = set(maquina['I'])
    maquina['O'] = set(maquina['O'])

    # Normaliza função de transição f
    # Aceita tanto formato aninhado {"s0": {"0": "s1"}} quanto tuplas {("s0","0"): "s1"}
    f_raw = maquina['f']
    if f_raw and isinstance(next(iter(f_raw)), str):
        # formato aninhado
        f_norm = {}
        for estado, transicoes in f_raw.items():
            for simbolo, prox in transicoes.items():
                f_norm[(estado, simbolo)] = prox
        maquina['f'] = f_norm

    # Normaliza função de saída g
    g_raw = maquina['g']
    if g_raw and isinstance(next(iter(g_raw)), str):
        g_norm = {}
        for estado, saidas in g_raw.items():
            for simbolo, out in saidas.items():
                g_norm[(estado, simbolo)] = out
        maquina['g'] = g_norm

    return maquina


def validar_maquina(maquina: dict):
    """Verifica se a estrutura da máquina possui todos os campos obrigatórios."""
    obrigatorios = ['S', 'I', 'O', 'f', 'g', 's_ini']
    for campo in obrigatorios:
        if campo not in maquina:
            raise ValueError(f"Campo obrigatório ausente na descrição da máquina: '{campo}'")

    if maquina['s_ini'] not in maquina['S']:
        raise ValueError(
            f"Estado inicial '{maquina['s_ini']}' não pertence ao conjunto de estados S."
        )


def simular_mealy(maquina: dict, entrada: str):
    """
    Simula a Máquina de Mealy para a cadeia de entrada fornecida.
    Exibe cada transição no formato (si, ci) -> (sj, oj).
    """
    S     = maquina['S']
    I     = maquina['I']
    f     = maquina['f']
    g     = maquina['g']
    s_ini = maquina['s_ini']

    estado = s_ini
    fita   = list(entrada)          # lista de símbolos da cadeia

    print()
    if not fita:
        print("  [Cadeia vazia – nenhuma transição realizada.]")
        return

    for c in fita:
        # Valida estado atual
        if estado not in S:
            print(f"  ERRO: O estado '{estado}' não pertence ao conjunto de estados da máquina!")
            return

        # Valida símbolo de entrada
        if c not in I:
            print(f"  ERRO: O símbolo '{c}' não pertence ao alfabeto de entrada {sorted(I)}!")
            return

        # Obtém próximo estado
        if (estado, c) not in f:
            print(
                f"  ERRO: Não há transição definida para o estado '{estado}' "
                f"com entrada '{c}'!"
            )
            return

        proximo_estado = f[(estado, c)]
        saida          = g.get((estado, c), '?')

        print(f"  ({estado}, {c}) -> ({proximo_estado}, {saida})")

        estado = proximo_estado

    print(f"\n  Estado final: {estado}")


def exibir_maquina(maquina: dict):
    """Exibe um resumo da máquina carregada."""
    print("\n" + "=" * 50)
    print("  Máquina de Mealy carregada com sucesso!")
    print("=" * 50)
    print(f"  Estados (S)        : {sorted(maquina['S'])}")
    print(f"  Alfabeto entrada(I): {sorted(maquina['I'])}")
    print(f"  Alfabeto saída  (O): {sorted(maquina['O'])}")
    print(f"  Estado inicial     : {maquina['s_ini']}")
    print("\n  Função de transição f e saída g:")
    estados_ordenados = sorted(maquina['S'])
    simbolos_ordenados = sorted(maquina['I'])
    for s in estados_ordenados:
        for c in simbolos_ordenados:
            prox = maquina['f'].get((s, c), '-')
            out  = maquina['g'].get((s, c), '-')
            print(f"    f({s}, {c}) = {prox:<6}  g({s}, {c}) = {out}")
    print("=" * 50)


def obter_arquivo() -> str:
    """Obtém o caminho do arquivo da máquina via argumento ou input()."""
    if len(sys.argv) > 1:
        return sys.argv[1]
    return input("Informe o caminho do arquivo da Máquina de Mealy: ").strip()


print("╔══════════════════════════════════════════════╗")
print("║   Simulador de Máquina de Mealy – ECM253    ║")
print("╚══════════════════════════════════════════════╝")

    # --- Carregar arquivo ---
caminho = obter_arquivo()
try:
    maquina = carregar_maquina(caminho)
    validar_maquina(maquina)
except FileNotFoundError as e:
    print(f"\n  ERRO: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n  ERRO ao carregar a máquina: {e}")
    sys.exit(1)

exibir_maquina(maquina)

    # --- Loop de simulação ---
print("\n  Digite uma cadeia para simular (ou 'sair' para encerrar).")
while True:
    try:
        cadeia = input("\nEntrada: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Programa encerrado.")
        break

    if cadeia.lower() in ('sair', 'exit', 'quit', 'q'):
        print("  Programa encerrado.")
        break

    simular_mealy(maquina, cadeia)


