#Mateus Ohira 24.00752-8
#Kauã Ortega 24.00031-0
#David Daniel 24.00029-9
"""
ECM253 – Linguagens Formais, Autômatos e Compiladores
Simulador de Máquina de Mealy
"""

import json
import sys
import os


def carregar_maquina(caminho_arquivo):
    if not os.path.exists(caminho_arquivo):
        raise FileNotFoundError("Arquivo '" + caminho_arquivo + "' nao encontrado.")

    arquivo = open(caminho_arquivo, 'r', encoding='utf-8')
    conteudo = arquivo.read()
    arquivo.close()

    ext = os.path.splitext(caminho_arquivo)[1].lower()

    if ext == '.json':
        maquina = json.loads(conteudo)
    else:
        maquina = eval(conteudo)

    # Converte listas em conjuntos (quando vem do JSON)
    conjunto_S = set()
    for estado in maquina['S']:
        conjunto_S.add(estado)
    maquina['S'] = conjunto_S

    conjunto_I = set()
    for simbolo in maquina['I']:
        conjunto_I.add(simbolo)
    maquina['I'] = conjunto_I

    conjunto_O = set()
    for simbolo in maquina['O']:
        conjunto_O.add(simbolo)
    maquina['O'] = conjunto_O

    # Normaliza funcao de transicao f para formato de tuplas
    f_raw = maquina['f']
    primeira_chave = None
    for chave in f_raw:
        primeira_chave = chave
        break

    if primeira_chave is not None and isinstance(primeira_chave, str):
        f_norm = {}
        for estado in f_raw:
            transicoes = f_raw[estado]
            for simbolo in transicoes:
                f_norm[(estado, simbolo)] = transicoes[simbolo]
        maquina['f'] = f_norm

    # Normaliza funcao de saida g para formato de tuplas
    g_raw = maquina['g']
    primeira_chave = None
    for chave in g_raw:
        primeira_chave = chave
        break

    if primeira_chave is not None and isinstance(primeira_chave, str):
        g_norm = {}
        for estado in g_raw:
            saidas = g_raw[estado]
            for simbolo in saidas:
                g_norm[(estado, simbolo)] = saidas[simbolo]
        maquina['g'] = g_norm

    return maquina


def validar_maquina(maquina):
    campos_obrigatorios = ['S', 'I', 'O', 'f', 'g', 's_ini']

    for campo in campos_obrigatorios:
        if campo not in maquina:
            raise ValueError("Campo obrigatorio ausente na descricao da maquina: '" + campo + "'")

    if maquina['s_ini'] not in maquina['S']:
        raise ValueError(
            "Estado inicial '" + maquina['s_ini'] +
            "' nao pertence ao conjunto de estados S."
        )


def simular_mealy(maquina, entrada):
    S     = maquina['S']
    I     = maquina['I']
    f     = maquina['f']
    g     = maquina['g']
    s_ini = maquina['s_ini']

    estado = s_ini

    print()

    if len(entrada) == 0:
        print("  [Cadeia vazia - nenhuma transicao realizada.]")
        return

    i = 0
    while i < len(entrada):
        c = entrada[i]

        # Valida estado atual
        if estado not in S:
            print("  ERRO: O estado '" + estado + "' nao pertence ao conjunto de estados!")
            return

        # Valida simbolo de entrada
        if c not in I:
            alfabeto_str = "{"
            primeiro = True
            for s in sorted(I):
                if not primeiro:
                    alfabeto_str += ", "
                alfabeto_str += s
                primeiro = False
            alfabeto_str += "}"
            print("  ERRO: O simbolo '" + c + "' nao pertence ao alfabeto de entrada " + alfabeto_str + "!")
            return

        # Verifica se existe transicao
        if (estado, c) not in f:
            print(
                "  ERRO: Nao ha transicao definida para o estado '" +
                estado + "' com entrada '" + c + "'!"
            )
            return

        proximo_estado = f[(estado, c)]

        if (estado, c) in g:
            saida = g[(estado, c)]
        else:
            saida = '?'

        print("  (" + estado + ", " + c + ") -> (" + proximo_estado + ", " + saida + ")")

        estado = proximo_estado
        i += 1

    print("\n  Estado final: " + estado)


def exibir_maquina(maquina):
    print("  Maquina de Mealy carregada com sucesso!")

    estados_str = "["
    primeiro = True
    for e in sorted(maquina['S']):
        if not primeiro:
            estados_str += ", "
        estados_str += e
        primeiro = False
    estados_str += "]"

    entrada_str = "["
    primeiro = True
    for s in sorted(maquina['I']):
        if not primeiro:
            entrada_str += ", "
        entrada_str += s
        primeiro = False
    entrada_str += "]"

    saida_str = "["
    primeiro = True
    for s in sorted(maquina['O']):
        if not primeiro:
            saida_str += ", "
        saida_str += s
        primeiro = False
    saida_str += "]"

    print("  Estados (S)         : " + estados_str)
    print("  Alfabeto entrada (I): " + entrada_str)
    print("  Alfabeto saida   (O): " + saida_str)
    print("  Estado inicial      : " + maquina['s_ini'])
    print("\n  Funcao de transicao f e saida g:")

    for s in sorted(maquina['S']):
        for c in sorted(maquina['I']):
            if (s, c) in maquina['f']:
                prox = maquina['f'][(s, c)]
            else:
                prox = '-'

            if (s, c) in maquina['g']:
                out = maquina['g'][(s, c)]
            else:
                out = '-'

            print("    f(" + s + ", " + c + ") = " + prox + "    g(" + s + ", " + c + ") = " + out)

    print("=" * 50)


def obter_arquivo():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return input("Informe o caminho do arquivo da Maquina de Mealy: ").strip()



caminho = obter_arquivo()

try:
    maquina = carregar_maquina(caminho)
    validar_maquina(maquina)
except FileNotFoundError as e:
    print("\n  ERRO: " + str(e))
    sys.exit(1)
except Exception as e:
    print("\n  ERRO ao carregar a maquina: " + str(e))
    sys.exit(1)

exibir_maquina(maquina)

print("\n  Digite uma cadeia para simular (ou 'sair' para encerrar).")

while True:
    try:
        cadeia = input("\nEntrada: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n  Programa encerrado.")
        break

    if cadeia == 'sair':
        print("  Programa encerrado.")
        break

    simular_mealy(maquina, cadeia)
