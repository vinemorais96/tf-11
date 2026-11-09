# CODIGO (TF 11) - APOS PASSO 3 (NORMALIZACAO)

pedidos = []  # lista global de pedidos


class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo


class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self):
        return self.quantidade * self.produto.preco


class Pedido:
    def __init__(self, numero, cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = "A"


def novo_pedido(numero, cliente):
    # Validacao provisoria (no Passo 4 vai para dentro das classes de valor)
    if len(cliente.cpf) != 11:
        print(f"pedido {numero} recusado: cpf invalido")
        return None
    if not cliente.email or "@" not in cliente.email:
        if not cliente.email:
            print(f"pedido {numero} recusado: email vazio")
        else:
            print(f"pedido {numero} recusado: email invalido")
        return None
    if len(cliente.cep) != 8:
        print(f"pedido {numero} recusado: cep invalido")
        return None

    pedido = Pedido(numero, cliente)
    pedidos.append(pedido)
    return pedido


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_desconto(tipo, valor):
    if tipo == "V":
        return valor * 0.10
    elif tipo == "F":
        return valor * 0.20
    else:
        return 0.0


def pagar(pedido):
    if pedido.status == "A":
        if len(pedido.itens) > 0:
            pedido.status = "P"
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.status == "A":
        pedido.status = "C"
        return True
    else:
        return False


def descrever_status(status):
    if status == "A":
        return "aberto"
    elif status == "P":
        return "pago"
    elif status == "C":
        return "cancelado"
    else:
        return "desconhecido"


def calcular_valor_a_pagar(pedido):
    total = sum(item.subtotal() for item in pedido.itens)
    desconto = calcular_desconto(pedido.cliente.tipo, total)
    return total - desconto


def relatorio():
    for pedido in pedidos:
        print(f"Pedido {pedido.numero} - {pedido.cliente.nome} - {pedido.cliente.cidade}")
        print(f"  status: {descrever_status(pedido.status)}")
        total = 0
        for item in pedido.itens:
            subtotal = item.subtotal()
            print(f"   {item.quantidade} x {item.produto.nome} = R$ {subtotal:.2f}")
            total += subtotal
        if len(pedido.itens) > 0:
            desconto = calcular_desconto(pedido.cliente.tipo, total)
            a_pagar = total - desconto
            print(f"  total: R$ {total:.2f} | desconto: R$ {desconto:.2f} | a pagar: R$ {a_pagar:.2f}")


def total_arrecadado():
    total = 0
    for pedido in pedidos:
        if pedido.status == "P":
            total += calcular_valor_a_pagar(pedido)
    return total


def total_pedidos_abertos():
    contador = 0
    for pedido in pedidos:
        if pedido.status == "A":
            contador += 1
    return contador


# PRODUTOS NORMALIZADOS (criados uma vez so)
caderno = Produto("Caderno", 15.50)
caneta = Produto("Caneta", 2.50)
livro = Produto("Livro", 89.50)
fone = Produto("Fone", 60.00)

# CLIENTES NORMALIZADOS (Ana criada uma unica vez)
cliente_ana = Cliente("Ana Souza", "11122233344", "ana@email.com", "Rua A, 10", "Sorocaba", "18010000", "V")
cliente_beto = Cliente("Beto Lima", "123", "beto@email.com", "Rua B, 20", "Itu", "13300000", "N")
cliente_caio = Cliente("Caio Cruz", "22233344455", "caiosemarroba", "Rua C, 30", "Salto", "13320000", "N")
cliente_diego = Cliente("Diego Rocha", "33344455566", "diego@email.com", "Rua D, 40", "Itu", "13301000", "N")
cliente_eva = Cliente("Eva Nunes", "44455566677", "eva@email.com", "Rua E, 50", "Itu", "13302000", "F")
cliente_fay = Cliente("Fay Dias", "55566677788", "fay@email.com", "Rua F, 60", "Salto", "0", "N")
cliente_gil = Cliente("Gil Alves", "66677788899", "gil@email.com", "Rua G, 70", "Sorocaba", "18020000", "N")

# ROTEIRO
pedido_da_ana = novo_pedido(1, cliente_ana)
adicionar_item(pedido_da_ana, caderno, 2)
adicionar_item(pedido_da_ana, caneta, 5)

pedido_do_beto = novo_pedido(2, cliente_beto)

# Pedido 3 aponta para o MESMO objeto cliente_ana
pedido_da_ana_dois = novo_pedido(3, cliente_ana)
adicionar_item(pedido_da_ana_dois, livro, 1)

pedido_do_caio = novo_pedido(4, cliente_caio)

pedido_do_diego = novo_pedido(5, cliente_diego)

pedido_da_eva = novo_pedido(6, cliente_eva)
adicionar_item(pedido_da_eva, fone, 1)

pedido_da_fay = novo_pedido(7, cliente_fay)

pedido_do_gil = novo_pedido(8, cliente_gil)
adicionar_item(pedido_do_gil, fone, 2)

print(f"pagar 1: {pagar(pedido_da_ana)}")
print(f"pagar 3: {pagar(pedido_da_ana_dois)}")
print(f"pagar 5: {pagar(pedido_do_diego)}")
print(f"pagar 6: {pagar(pedido_da_eva)}")
print(f"cancelar 5: {cancelar(pedido_do_diego)}")
print(f"cancelar 1: {cancelar(pedido_da_ana)}")

relatorio()
print(f"arrecadado: R$ {total_arrecadado():.2f}")
print(f"abertos: {total_pedidos_abertos()}") 