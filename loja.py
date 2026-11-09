# CODIGO (TF 11) - APOS PASSO 4 (CLASSES DE VALOR / PRIMITIVOS EMBRULHADOS)

pedidos = []  # lista global de pedidos


class Cpf:
    def __init__(self, valor: str):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self.valor = valor

    def __str__(self) -> str:
        return self.valor


class Email:
    def __init__(self, endereco: str):
        if not endereco:
            raise ValueError("email vazio")
        if "@" not in endereco:
            raise ValueError("email invalido")
        self.endereco = endereco

    def __str__(self) -> str:
        return self.endereco


class Cep:
    def __init__(self, codigo: str):
        if len(codigo) != 8:
            raise ValueError("cep invalido")
        self.codigo = codigo

    def __str__(self) -> str:
        return self.codigo


class Dinheiro:
    def __init__(self, centavos: int):
        self.centavos = centavos

    @classmethod
    def de_centavos(cls, centavos: int) -> "Dinheiro":
        return cls(centavos)

    def somar(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self.centavos + outro.centavos)

    def subtrair(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self.centavos - outro.centavos)

    def multiplicar_por_quantidade(self, quantidade: int) -> "Dinheiro":
        return Dinheiro(self.centavos * quantidade)

    def calcular_percentual(self, percentual: int) -> "Dinheiro":
        return Dinheiro(round(self.centavos * percentual / 100))

    def __str__(self) -> str:
        reais = self.centavos / 100
        return f"R$ {reais:.2f}"


class Status:
    _DESCRICOES = {
        "A": "aberto",
        "P": "pago",
        "C": "cancelado",
    }

    def __init__(self, codigo: str = "A"):
        self.codigo = codigo

    def esta_aberto(self) -> bool:
        return self.codigo == "A"

    def definir_pago(self) -> None:
        self.codigo = "P"

    def definir_cancelado(self) -> None:
        self.codigo = "C"

    def __str__(self) -> str:
        return self._DESCRICOES.get(self.codigo, "desconhecido")


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
    def __init__(self, nome: str, preco: Dinheiro):
        self.nome = nome
        self.preco = preco


class ItemDoPedido:
    def __init__(self, produto: Produto, quantidade: int):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self) -> Dinheiro:
        return self.produto.preco.multiplicar_por_quantidade(self.quantidade)


class Pedido:
    def __init__(self, numero: int, cliente: Cliente):
        self.numero = numero
        self.cliente = cliente
        self.itens = []
        self.status = Status("A")


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.append(ItemDoPedido(produto, quantidade))


def calcular_desconto(tipo, valor: Dinheiro) -> Dinheiro:
    if tipo == "V":
        return valor.calcular_percentual(10)
    elif tipo == "F":
        return valor.calcular_percentual(20)
    else:
        return Dinheiro.de_centavos(0)


def pagar(pedido):
    if pedido.status.esta_aberto():
        if len(pedido.itens) > 0:
            pedido.status.definir_pago()
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.status.esta_aberto():
        pedido.status.definir_cancelado()
        return True
    else:
        return False


def calcular_valor_a_pagar(pedido) -> Dinheiro:
    total = Dinheiro.de_centavos(0)
    for item in pedido.itens:
        total = total.somar(item.subtotal())
    desconto = calcular_desconto(pedido.cliente.tipo, total)
    return total.subtrair(desconto)


def relatorio():
    for pedido in pedidos:
        print(f"Pedido {pedido.numero} - {pedido.cliente.nome} - {pedido.cliente.cidade}")
        print(f"  status: {pedido.status}")
        total = Dinheiro.de_centavos(0)
        for item in pedido.itens:
            subtotal = item.subtotal()
            print(f"   {item.quantidade} x {item.produto.nome} = {subtotal}")
            total = total.somar(subtotal)
        if len(pedido.itens) > 0:
            desconto = calcular_desconto(pedido.cliente.tipo, total)
            a_pagar = total.subtrair(desconto)
            print(f"  total: {total} | desconto: {desconto} | a pagar: {a_pagar}")


def total_arrecadado() -> Dinheiro:
    total = Dinheiro.de_centavos(0)
    for pedido in pedidos:
        if str(pedido.status) == "pago":
            total = total.somar(calcular_valor_a_pagar(pedido))
    return total


def total_pedidos_abertos() -> int:
    contador = 0
    for pedido in pedidos:
        if pedido.status.esta_aberto():
            contador += 1
    return contador


def registrar_pedido(numero, fabricar_pedido):
    try:
        pedido = fabricar_pedido()
        pedidos.append(pedido)
        return pedido
    except ValueError as erro:
        print(f"pedido {numero} recusado: {erro}")
        return None


# PRODUTOS (precos em centavos com classe Dinheiro)
caderno = Produto("Caderno", Dinheiro.de_centavos(1550))
caneta = Produto("Caneta", Dinheiro.de_centavos(250))
livro = Produto("Livro", Dinheiro.de_centavos(8950))
fone = Produto("Fone", Dinheiro.de_centavos(6000))

# CLIENTE REUTILIZADO (Ana)
cliente_ana = Cliente("Ana Souza", Cpf("11122233344"), Email("ana@email.com"), "Rua A, 10", "Sorocaba", Cep("18010000"), "V")

# ROTEIRO
pedido_da_ana = registrar_pedido(
    1, lambda: Pedido(1, cliente_ana)
)
adicionar_item(pedido_da_ana, caderno, 2)
adicionar_item(pedido_da_ana, caneta, 5)

pedido_do_beto = registrar_pedido(
    2, lambda: Pedido(2, Cliente("Beto Lima", Cpf("123"), Email("beto@email.com"), "Rua B, 20", "Itu", Cep("13300000"), "N"))
)

pedido_da_ana_dois = registrar_pedido(
    3, lambda: Pedido(3, cliente_ana)
)
adicionar_item(pedido_da_ana_dois, livro, 1)

pedido_do_caio = registrar_pedido(
    4, lambda: Pedido(4, Cliente("Caio Cruz", Cpf("22233344455"), Email("caiosemarroba"), "Rua C, 30", "Salto", Cep("13320000"), "N"))
)

cliente_diego = Cliente("Diego Rocha", Cpf("33344455566"), Email("diego@email.com"), "Rua D, 40", "Itu", Cep("13301000"), "N")
pedido_do_diego = registrar_pedido(
    5, lambda: Pedido(5, cliente_diego)
)

cliente_eva = Cliente("Eva Nunes", Cpf("44455566677"), Email("eva@email.com"), "Rua E, 50", "Itu", Cep("13302000"), "F")
pedido_da_eva = registrar_pedido(
    6, lambda: Pedido(6, cliente_eva)
)
adicionar_item(pedido_da_eva, fone, 1)

pedido_da_fay = registrar_pedido(
    7, lambda: Pedido(7, Cliente("Fay Dias", Cpf("55566677788"), Email("fay@email.com"), "Rua F, 60", "Salto", Cep("0"), "N"))
)

cliente_gil = Cliente("Gil Alves", Cpf("66677788899"), Email("gil@email.com"), "Rua G, 70", "Sorocaba", Cep("18020000"), "N")
pedido_do_gil = registrar_pedido(
    8, lambda: Pedido(8, cliente_gil)
)
adicionar_item(pedido_do_gil, fone, 2)

print(f"pagar 1: {pagar(pedido_da_ana)}")
print(f"pagar 3: {pagar(pedido_da_ana_dois)}")
print(f"pagar 5: {pagar(pedido_do_diego)}")
print(f"pagar 6: {pagar(pedido_da_eva)}")
print(f"cancelar 5: {cancelar(pedido_do_diego)}")
print(f"cancelar 1: {cancelar(pedido_da_ana)}")

relatorio()
print(f"arrecadado: {total_arrecadado()}")
print(f"abertos: {total_pedidos_abertos()}") 