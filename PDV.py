print("Iniciando o sistema... \n")
import time
import requests

# Importando as API's
response = requests.get('https://lgminardi.com.br/ws/api/public/projetos/getCategorias')
response2 = requests.get('https://lgminardi.com.br/ws/api/public/projetos/getProdutos')

# Verificando se a solicitação foi bem-sucedida (código de status 200)
if response.status_code == 200 and response2.status_code == 200:
    listacategorias = response.json()
    listaprodutos = response2.json() 
else:
    print('Erro', response.status_code, 'reinicie o sistema.')
    exit()

# Espaço para funções
    # Limpar o terminal
def limpar():
    import os
    os.system('cls' if os.name == 'nt' else 'clear') # 'nt' == Windows / 'posix' == Mac (else)

    # Voltar ao Menu
def voltarmenu(menu):
    while True:
        confirm = input("Deseja voltar ao menu? [s] ou [n]\n").lower()
        if confirm == 's':
            return 0
        elif confirm == 'n':
            return menu
        else:
            print("Digite uma opção válida ([0] para o menu inicial)")

    # Mostrar lista de produtos
def mostrarprodutos():
    limpar()
    print(f"{'ID':<12} {'Nome do Produto':<25} {'Categoria':<32} {'Valor Unitário':<18} {'Estoque':<12}\n")
    for lista in listaprodutos: # Itera sob a lista de produtos
        for categoria in listacategorias: # Itera sob a lista de categorias, para alterar o código pelo nome
            if lista['categoria'] == categoria['codigo']:
                lista['categoria'] = categoria['nome'] # Se o código for o mesmo realiza a alteração
                break # Ao achar a categoria a busca é encerrada
        print(f"{lista['id']:<12} {lista['descricao']:<25} {lista['categoria']:<32} {lista['valorun']:<18} {lista['estoque']:<12}")
        print('-'*100)

    # Mostrar carrinho na venda
def mostrarcarrinho():
    print("\nCarrinho:")
    print(f"{'ID':<10} {'Nome do Produto':<25} {'Valor Unitário':<18} {'Quantidade':<14} {'Total da venda':<20}\n")
    for produto in carrinho:
        print(f"{produto['id']:<10} {produto['descricao']:<25} {produto['valorun']:<18} {produto['quantidade']:<14} {produto['total']:<20}")
        print('-'*90)
    print("Total: R$", totalcarrinho)

    # Mostrar vendas do dia
def mostrarvendas():
    print("\nVendas do dia:")
    print(f"{'ID':<10} {'Nome do Produto':<25} {'Valor Unitário':<18} {'Quantidade':<14} {'Total da venda':<20}\n")
    for vendas in vendasdodia:
        print(f"{vendas['id']:<10} {vendas['descricao']:<25} {vendas['valorun']:<18} {vendas['quantidade']:<14} {vendas['totalproduto']:<20}")
        print('-'*90)
    print("Lucro do dia: R$",round(totalvendas, 2))

# Variável para armazenar as vendas do dia
vendasdodia = []
totalvendas = 0

# Loop para a função voltar ao menu funcionar
menu = 0
while menu != 6:
    limpar()
    if menu == 0:
        menu = int(input("Menu de opções:\
                    \n[1] Abrir o caixa\
                    \n[2] Visualizar produtos\
                    \n[3] Visualizar categorias\
                    \n[4] Visualizar vendas do dia\
                    \n[5] Visualizar integrantes\
                    \n[6] Encerrar o dia\
                    \nOpção: "))

    # Menu inválido
    elif menu > 6 or menu <1:
        print("Digite uma opção válida.")
        menu = int(input("Opção: "))

    # Abrir o caixa [1]
    elif menu == 1:
        caixa = int(input("Caixa aberto, o que deseja fazer?\n[1] Realizar uma venda\n[2] Fechar o caixa\nOpção: "))
    # - Abrir uma venda
        if caixa == 1:
            carrinho = []
            totalcarrinho = 0
            loop = 0 # Loop para realizar vendas no mesmo carrinho
            while loop == 0:
                limpar()
                mostrarprodutos()
                totalproduto = 0
                loop = 1
                while loop == 1: # Loop para digitar um ID válido
                    idproduto = input("Digite o ID do produto ou [n] para voltar ao menu: ")
                    if idproduto.lower() == 'n':
                        loop = 3 # Encerra a venda
                        print("Venda encerrada!")
                        time.sleep(0.5) # Delay para mostrar a mensagem
                        break
                    elif idproduto.isdigit() and int(idproduto) in range(1,16): # Verifica se é composto por números e está entre 1 e 15
                        loop = 2 # Passa para o loop que confere a quantidade
                        for produto in listaprodutos:
                            if produto["id"] == idproduto: # Procura o dicionário que corresponde ao ID do produto
                                while loop == 2: # Loop para digitar quantidade válida
                                    quantidade = input("Digite a quantidade: ")
                                    if quantidade.isdigit() and int(quantidade) <= int(produto["estoque"]) and int(quantidade) > 0: # Verifica se é número e tem estoque suficiente
                                        valorun = produto["valorun"]
                                        totalproduto += round((float(valorun) * float(quantidade)), 2) # Multiplica valor un X quantidade
                                        totalcarrinho += round(totalproduto, 2)
                                        totalvendas += round(totalproduto, 2) # Adiciona o valor total do carrinho ao total de vendas do dia]
                                        produto["estoque"] = str(int(produto["estoque"]) - int(quantidade)) # Tira a venda do estoque

                                        # Adiciona os produtos vendidos ao carrinho e as vendas do dia [4]
                                        carrinho.append({'id':produto['id'],
                                                         'descricao':produto['descricao'], 
                                                         'valorun':produto['valorun'], 
                                                         'quantidade':quantidade, 
                                                         'total':str(totalproduto)})

                                        vendasdodia.append({'id':produto['id'], 
                                                            'descricao':produto['descricao'], 
                                                            'valorun':produto['valorun'], 
                                                            'quantidade':quantidade, 
                                                            'totalproduto':str(totalproduto)})

                                        # Carrinho
                                        mostrarcarrinho()
                                            
                                        # - Fazer outra venda
                                        refazer = input("Deseja adicionar outro produto ao carrinho? [s] ou [n]: ").lower()
                                        if refazer == 's':
                                            loop = 0 # Volta para a validação de ID
                                        elif refazer == 'n':
                                            loop = 3 # Encerra o carrinho
                                            print("Venda encerrada!")
                                            time.sleep(0.5)
                                            break
                                        else:
                                            print("Digite um valor válido")

                                    else:
                                        print(f"Digite um valor válido. (Estoque atual: {produto["estoque"]})")
                    else:
                        print("Digite um valor válido.")

    # - Fechar o caixa
        elif caixa == 2:
            menu = 0 # Pular a confirmação do voltarmenu()
    
    # Visualizar produtos[2]
    elif menu == 2:
        limpar()
        mostrarprodutos()
        # - Alterar o estoque
        idproduto = input("Deseja alterar o estoque de um produto? Digite o ID do produto ou [n] para voltar ao menu\nOpção: ")
        if idproduto.lower() == 'n':
            menu = 0
        elif idproduto.isdigit() and int(idproduto) in range(1,16): # Verifica se é composto por números e está entre 1 e 15
            estoque = input("Qual o estoque que deseja inserir?\nEstoque: ")
            if estoque.isdigit(): # Verifica se é composto por números
                for produto in listaprodutos:
                    if produto["id"] == idproduto:
                        produto["estoque"] = estoque
                        print("Estoque alterado!")
            else:
                print("Digite um valor válido.")
        else:
                print("Digite um valor válido.")

    # Visualizar categorias[3]
    elif menu == 3:
        limpar()
        print(f"{'ID':<12} {'Categoria':<30}\n") # ':' = indica formatação / '<12' = mínimo 12 caracteres
        for lista in listacategorias:
            print(f"{lista['codigo']:<12} {lista['nome']:<30}") # formatação utilizada para espaçamento
            print('-'*50)
        menu = voltarmenu(menu)
    
    # Visualizar vendas do dia[4]
    elif menu == 4:
        limpar()
        if vendasdodia == []:
            print("Ainda não houveram vendas hoje.")
            menu = voltarmenu(menu)
        else:
            mostrarvendas()
            menu = voltarmenu(menu)
    
    # Visualizar os integrantes[5]
    elif menu == 5:
        limpar()
        print("Integrantes:\n\n2002601 - Vinícius Gualtieri Moraes\n2012119 - Kauã Henrique Zefferino Santana\n")
        menu = voltarmenu(menu)

# Encerrar o dia caso o número escolhido for [6]
print("Caixa encerrado.")
exit()