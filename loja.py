# CODIGO FEIO DE PROPOSITO (TF 11) - APOS PASSO 2 (SEM ABREVIACOES)

pedidos = []  # todos os pedidos da loja: lista solta, global


class Pedido:
    def __init__(
        self,
        numero,
        nome_do_cliente,
        cpf_do_cliente,
        email_do_cliente,
        rua,
        cidade,
        cep,
        tipo,
    ):
        self.numero = numero
        self.nome_do_cliente = nome_do_cliente
        self.cpf_do_cliente = cpf_do_cliente
        self.email_do_cliente = email_do_cliente
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo
        self.itens = []
        self.status = "A"


def novo_pedido(
    numero,
    nome_do_cliente,
    cpf_do_cliente,
    email_do_cliente,
    rua,
    cidade,
    cep,
    tipo,
):
    # Hadouken de validacao (sera eliminado nos proximos passos)
    if len(cpf_do_cliente) != 11:
        print(f"pedido {numero} recusado: cpf invalido")
        return None
    if not email_do_cliente or "@" not in email_do_cliente:
        if not email_do_cliente:
            print(f"pedido {numero} recusado: email vazio")
        else:
            print(f"pedido {numero} recusado: email invalido")
        return None
    if len(cep) != 8:
        print(f"pedido {numero} recusado: cep invalido")
        return None

    pedido = Pedido(
        numero,
        nome_do_cliente,
        cpf_do_cliente,
        email_do_cliente,
        rua,
        cidade,
        cep,
        tipo,
    )
    pedidos.append(pedido)
    return pedido


def adicionar_item(pedido, produto, quantidade, preco):
    pedido.itens.append([produto, quantidade, preco])


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
    total = sum(item[1] * item[2] for item in pedido.itens)
    desconto = calcular_desconto(pedido.tipo, total)
    return total - desconto


def relatorio():
    for pedido in pedidos:
        print(f"Pedido {pedido.numero} - {pedido.nome_do_cliente} - {pedido.cidade}")
        print(f"  status: {descrever_status(pedido.status)}")
        total = 0
        for item in pedido.itens:
            subtotal = item[1] * item[2]
            print(f"   {item[1]} x {item[0]} = R$ {subtotal:.2f}")
            total += subtotal
        if len(pedido.itens) > 0:
            desconto = calcular_desconto(pedido.tipo, total)
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


# ROTEIRO DA LOJA (com nomes descritivos)
pedido_da_ana = novo_pedido(
    1, "Ana Souza", "11122233344", "ana@email.com", "Rua A, 10", "Sorocaba", "18010000", "V"
)
adicionar_item(pedido_da_ana, "Caderno", 2, 15.50)
adicionar_item(pedido_da_ana, "Caneta", 5, 2.50)

pedido_do_beto = novo_pedido(
    2, "Beto Lima", "123", "beto@email.com", "Rua B, 20", "Itu", "13300000", "N"
)

pedido_da_ana_dois = novo_pedido(
    3, "Ana Souza", "11122233344", "ana@email.com", "Rua A, 10", "Sorocaba", "18010000", "V"
)
adicionar_item(pedido_da_ana_dois, "Livro", 1, 89.50)

pedido_do_caio = novo_pedido(
    4, "Caio Cruz", "22233344455", "caiosemarroba", "Rua C, 30", "Salto", "13320000", "N"
)

pedido_do_diego = novo_pedido(
    5, "Diego Rocha", "33344455566", "diego@email.com", "Rua D, 40", "Itu", "13301000", "N"
)

pedido_da_eva = novo_pedido(
    6, "Eva Nunes", "44455566677", "eva@email.com", "Rua E, 50", "Itu", "13302000", "F"
)
adicionar_item(pedido_da_eva, "Fone", 1, 60.00)

pedido_da_fay = novo_pedido(
    7, "Fay Dias", "55566677788", "fay@email.com", "Rua F, 60", "Salto", "0", "N"
)

pedido_do_gil = novo_pedido(
    8, "Gil Alves", "66677788899", "gil@email.com", "Rua G, 70", "Sorocaba", "18020000", "N"
)
adicionar_item(pedido_do_gil, "Fone", 2, 60.00)

print(f"pagar 1: {pagar(pedido_da_ana)}")
print(f"pagar 3: {pagar(pedido_da_ana_dois)}")
print(f"pagar 5: {pagar(pedido_do_diego)}")
print(f"pagar 6: {pagar(pedido_da_eva)}")
print(f"cancelar 5: {cancelar(pedido_do_diego)}")
print(f"cancelar 1: {cancelar(pedido_da_ana)}")

relatorio()
print(f"arrecadado: R$ {total_arrecadado():.2f}")
print(f"abertos: {total_pedidos_abertos()}") 