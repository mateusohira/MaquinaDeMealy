#Mateus Ohira 24.00752-8 
#Kauã Ortega 24.00031-0 
#David Daniel 24.00029-9

import os

# Carregar arquivo
caminho = input("Digite o nome do arquivo: ")

if not os.path.exists(caminho):
    print("Arquivo não encontrado!")
    exit()

arquivo = open(caminho, "r")
maquina = eval(arquivo.read())
arquivo.close()

# Dados da máquina
S = maquina["S"]
I = maquina["I"]
O = maquina["O"]
f = maquina["f"]
g = maquina["g"]
estado = maquina["s_ini"]

# Mostrar máquina
print("\nEstados:", S)
print("Entrada:", I)
print("Saída:", O)
print("Estado inicial:", estado)

print("\nTransições:")
for chave in f:
    print(chave, "->", f[chave], " / saída:", g.get(chave, "-"))

# Simulação
while True:
    entrada = input("\nDigite a cadeia (ou sair): ")

    if entrada == "sair":
        break

    estado_atual = estado

    for simbolo in entrada:
        if (estado_atual, simbolo) in f:
            prox = f[(estado_atual, simbolo)]
            saida = g.get((estado_atual, simbolo), "?")

            print("(", estado_atual, ",", simbolo, ") -> (", prox, ",", saida, ")")

            estado_atual = prox
        else:
            print("Transição não encontrada!")
            break

    print("Estado final:", estado_atual)
