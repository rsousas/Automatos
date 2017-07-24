# -*- coding: UTF-8 -*-
import sys

def AFN_para_AFD(estados_AFN, alfabeto, estado_Inicial, estados_Finais, trancicoes_AFN):

    transicao_afn = trancicoes_AFN
    estados       = estados_AFN
    transicao_afd = {}  # Preenchida com as novas transiçoes encontrdas
    tabela_estados = [] # Representa a coluna de estados novos encontrados no AFD, da tabela quando realizado o processo a mão

    tabela_estados.append((estado_Inicial,))        
    # Monta a tabela de transições de AFN para AFD
	# Ao fim do laço se terá todas as transições em um formato desordenado
	# Ex.: {((0,), 'b'): [2], ((0, 1, 2), a): [3]}
    for estado_afd in tabela_estados:
        # Analogo a tabela, Verifica pra cada estado contando com os novos o que ocorre pra cada simbolo lido
        for simbolo in alfabeto:
		    # Vê se é um estado simples (os definidos no AFN "0,1...") e existir transição do estado e simbolo lido nas transições do AFN
            if len(estado_afd) == 1 and (estado_afd[0], simbolo) in transicao_afn:
			    # Adiciona a transição do AFN na tabela AFD
                transicao_afd[(estado_afd, simbolo)] = transicao_afn[(estado_afd[0], simbolo)]
                
				# Verifica se a tupla adicionada existe na coluna dos estados AFD, caso não, adiciona
                if tuple(transicao_afd[(estado_afd, simbolo)]) not in tabela_estados:
                    tabela_estados.append(tuple(transicao_afd[(estado_afd, simbolo)]))
        
			# Caso seja um estado composto <1,2>, ou não exista transição definida para o simbolo lido
            else:
                destinos = []
                destino_final = []
				# Para cada estado do estado composto 
                for estado_afn in estado_afd:
				    # Verifica se existe transição no AFN para o estado e simbolo lido
                    if (estado_afn, simbolo) in transicao_afn and transicao_afn[(estado_afn, simbolo)] not in destinos:
                        destinos.append(transicao_afn[(estado_afn, simbolo)])
        
                # Se há movimentos definidos
                if destinos:
                    # Verifica todos os destinos e adiciona a uma variável formando algo como: [[2][2,3]] - > (2,3)
                    for destino in destinos:
                        for valor in destino:
                            if valor not in destino_final:
                                destino_final.append(valor)         
        
				    # Adiciona o destino resultante para a transição pesquisada
                    transicao_afd[(estado_afd, simbolo)] = destino_final
                 
                    # Verifica se a tupla adicionada existe na coluna dos estados AFD, caso não, adiciona				 
                    if tuple(destino_final) not in tabela_estados:
                        tabela_estados.append(tuple(destino_final))

    # Converte estados formados para o AFD em um formato como (0, 'b', 5)
    transicoes = []
    finais = []
    for chave in transicao_afd:
        transicoes.append((tabela_estados.index(tuple(chave[0])), chave[1], tabela_estados.index(tuple(transicao_afd[chave]))))
        for final in chave[0]:
            if final in estados_Finais:
                if tabela_estados.index(tuple(chave[0])) not in finais:
                    finais.append(tabela_estados.index(tuple(chave[0])))  # Verifica quais são os novos estados Finais
					
    for estado in transicoes:
        if not str(estado[0]) in estados:
            estados.append(str(estado[0]))  # Busca todos os novos estados   			

	# Guarda os dados para impressão
    saida = {}
    saida['estados']    = list(map(str, estados))
    saida['terminais']  = alfabeto
    saida['inicial']    = estado_Inicial
    saida['finais']     = list(map(str, finais))
    saida['transicoes'] = transicoes
    return saida   

	
def salva_saida(saida_Final):
    # Salva arquivo de saida
    arqSaida.write('AFD' + '\n')
    arqSaida.write(str(len(saida_Final['estados'])) + ' ' + ' '.join(saida_Final['estados']) + '\n')
    arqSaida.write(str(len(saida_Final['terminais'])) + ' ' + ' '.join(saida_Final['terminais']) + '\n')
    arqSaida.write(str(saida_Final['inicial']) + '\n')
    arqSaida.write(str(len(saida_Final['finais'])) + ' ' + ' '.join(sorted(saida_Final['finais'])) + '\n')
    
    for transicao in sorted(saida_Final['transicoes']):
        transicao = map(str, transicao)
        arqSaida.write(' '.join(transicao) + '\n')	


		
try:
    descricao = sys.argv[1]
except IndexError:
    descricao = 'descricao.txt' 
try:
    saida = sys.argv[2]
except IndexError:
    saida = 'saida.txt'
		
# Abrindo arquivo de descrição
arqDescricao = open(descricao, "r")	  
# Abrindo arquivo de saida
arqSaida     = open(saida,"w")

linhas = arqDescricao.readlines()

# 1: Define o Formalismo
linha      = linhas[0]
formalismo = linha[0:linha.index('#')]		

# 2: Define os estados
estados = []
linha   = linhas[1]
linha   = linha[1:linha.index('#')]
linha   = linha.split()
for coluna in linha:
    if coluna:
        estados.append(coluna)
		
# 3: Define o alfabeto
alfabeto = []
linha    = linhas[2]
linha    = linha[1:linha.index('#')]
linha    = linha.split()
for coluna in linha:
    if coluna:
        alfabeto.append(coluna)		
		
# 4: Define o estado inicial	
linha         = linhas[3]
estado_Inicial = linha[0]

# 5: Define estados finais
estados_Finais = []
linha         = linhas[4]
linha         = linha[1:linha.index('#')]
linha         = linha.split()
for coluna in linha:
    if coluna:
        estados_Finais.append(coluna)		

# 6+: Funcoes de transicao
trancicoes_AFN = {}
for i in range(5, len(linhas)):
    linha          = linhas[i]
    linha          = linha[0:linha.index('#')]
    linha          = linha.split()
    estado_partida = linha[0]
    simbolo        = linha[1]
    for l in linha[2:len(linha)]:
        if l:
            estado_destino = l
            if (estado_partida, simbolo) in trancicoes_AFN:
                trancicoes_AFN[(estado_partida, simbolo)].append(estado_destino)
            else:
                trancicoes_AFN[(estado_partida, simbolo)] = [estado_destino]
# Passa os dados para serem processados em AFN_para_AFD
saida_Final = AFN_para_AFD(estados, alfabeto, estado_Inicial, estados_Finais, trancicoes_AFN)
salva_saida(saida_Final)

# Fecha os arquivos abertos    
arqDescricao.close()
arqSaida.close()