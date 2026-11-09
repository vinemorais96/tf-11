# CODIGO (TF 11) - APOS PASSO 6 (ENTIDADES PEQUENAS: PESSOA E ENDERECO)


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


class Pessoa:
    """Entidade pequena com dados de identidade civil (max 3 atributos)."""

    def __init__(self, nome: str, cpf: Cpf, email: Email):
        self.nome = nome
        self.cpf = cpf
        self.email = email


class Endereco:
    """Entidade pequena com dados de localizacao (max 3 atributos)."""

    def __init__(self, rua: str, cidade: str, cep: Cep):
        self.rua = rua
        self.cidade = cidade
        self.cep = cep


class Cliente:
    """Entidade pequena que associa pessoa, endereco e modalidade (max 3 atributos)."""

    def __init__(self, pessoa: Pessoa, endereco: Endereco, tipo: str):
        self.pessoa = pessoa
        self.endereco = endereco
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

    def imprimir_linha(self) -> None:
        print(f"   {self.quantidade} x {self.produto.nome} = {self.subtotal()}")


class ItensDoPedido:
    def __init__(self):
        self._itens = []

    def adicionar(self, item: ItemDoPedido) -> None:
        self._itens.append(item)

    def esta_vazia(self) -> bool:
        return len(self._itens) == 0

    def calcular_total(self) -> Dinheiro:
        total = Dinheiro.de_centavos(0)
        for item in self._itens:
            total = total.somar(item.subtotal())
        return total

    def imprimir_itens(self) -> None:
        for item in self._itens:
            item.imprimir_linha()


class Pedido:
    def __init__(self, cliente: Cliente, itens: ItensDoPedido):
        self.cliente = cliente
        self.itens = itens
        self.status = Status("A")

    def adicionar_item(self, item: ItemDoPedido) -> None:
        self.itens.adicionar(item)

    def pagar(self) -> bool:
        if self.status.esta_aberto():
            if not self.itens.esta_vazia():
                self.status.definir_pago()
                return True
            else:
                return False
        else:
            return False

    def cancelar(self) -> bool:
        if self.status.esta_aberto():
            self.status.definir_cancelado()
            return True
        else:
            return False

    def calcular_desconto(self, total: Dinheiro) -> Dinheiro:
        if self.cliente.tipo == "V":
            return total.calcular_percentual(10)
        elif self.cliente.tipo == "F":
            return total.calcular_percentual(20)
        else:
            return Dinheiro.de_centavos(0)

    def valor_a_pagar(self) -> Dinheiro:
        total = self.itens.calcular_total()
        desconto = self.calcular_desconto(total)
        return total.subtrair(desconto)

    def imprimir_detalhes(self, numero: int) -> None:
        print(f"Pedido {numero} - {self.cliente.pessoa.nome} - {self.cliente.endereco.cidade}")
        print(f"  status: {self.status}")
        self.itens.imprimir_itens()
        if not self.itens.esta_vazia():
            total = self.itens.calcular_total()
            desconto = self.calcular_desconto(total)
            a_pagar = total.subtrair(desconto)
            print(f"  total: {total} | desconto: {desconto} | a pagar: {a_pagar}")


class Pedidos:
    def __init__(self):
        self._pedidos = {}

    def registrar(self, numero: int, pedido: Pedido) -> None:
        self._pedidos[numero] = pedido

    def obter_pedido(self, numero: int) -> Pedido:
        return self._pedidos.get(numero)

    def pagar_pedido(self, numero: int) -> bool:
        pedido = self.obter_pedido(numero)
        if pedido:
            return pedido.pagar()
        return False

    def cancelar_pedido(self, numero: int) -> bool:
        pedido = self.obter_pedido(numero)
        if pedido:
            return pedido.cancelar()
        return False

    def imprimir_relatorio(self) -> None:
        for numero, pedido in self._pedidos.items():
            pedido.imprimir_detalhes(numero)

    def calcular_total_arrecadado(self) -> Dinheiro:
        total = Dinheiro.de_centavos(0)
        for pedido in self._pedidos.values():
            if str(pedido.status) == "pago":
                total = total.somar(pedido.valor_a_pagar())
        return total

    def contar_pedidos_abertos(self) -> int:
        contador = 0
        for pedido in self._pedidos.values():
            if pedido.status.esta_aberto():
                contador += 1
        return contador


pedidos = Pedidos()


def criar_cliente(nome, cpf_str, email_str, rua, cidade, cep_str, tipo):
    pessoa = Pessoa(nome, Cpf(cpf_str), Email(email_str))
    endereco = Endereco(rua, cidade, Cep(cep_str))
    return Cliente(pessoa, endereco, tipo)


def registrar_pedido(numero, fabricar_pedido):
    try:
        pedido = fabricar_pedido()
        pedidos.registrar(numero, pedido)
        return pedido
    except ValueError as erro:
        print(f"pedido {numero} recusado: {erro}")
        return None


# PRODUTOS
caderno = Produto("Caderno", Dinheiro.de_centavos(1550))
caneta = Produto("Caneta", Dinheiro.de_centavos(250))
livro = Produto("Livro", Dinheiro.de_centavos(8950))
fone = Produto("Fone", Dinheiro.de_centavos(6000))

# CLIENTES
cliente_ana = criar_cliente("Ana Souza", "11122233344", "ana@email.com", "Rua A, 10", "Sorocaba", "18010000", "V")
cliente_diego = criar_cliente("Diego Rocha", "33344455566", "diego@email.com", "Rua D, 40", "Itu", "13301000", "N")
cliente_eva = criar_cliente("Eva Nunes", "44455566677", "eva@email.com", "Rua E, 50", "Itu", "13302000", "F")
cliente_gil = criar_cliente("Gil Alves", "66677788899", "gil@email.com", "Rua G, 70", "Sorocaba", "18020000", "N")

# ROTEIRO
itens_1 = ItensDoPedido()
itens_1.adicionar(ItemDoPedido(caderno, 2))
itens_1.adicionar(ItemDoPedido(caneta, 5))
pedido_da_ana = registrar_pedido(1, lambda: Pedido(cliente_ana, itens_1))

pedido_do_beto = registrar_pedido(
    2, lambda: Pedido(criar_cliente("Beto Lima", "123", "beto@email.com", "Rua B, 20", "Itu", "13300000", "N"), ItensDoPedido())
)

itens_3 = ItensDoPedido()
itens_3.adicionar(ItemDoPedido(livro, 1))
pedido_da_ana_dois = registrar_pedido(3, lambda: Pedido(cliente_ana, itens_3))

pedido_do_caio = registrar_pedido(
    4, lambda: Pedido(criar_cliente("Caio Cruz", "22233344455", "caiosemarroba", "Rua C, 30", "Salto", "13320000", "N"), ItensDoPedido())
)

pedido_do_diego = registrar_pedido(
    5, lambda: Pedido(cliente_diego, ItensDoPedido())
)

itens_6 = ItensDoPedido()
itens_6.adicionar(ItemDoPedido(fone, 1))
pedido_da_eva = registrar_pedido(6, lambda: Pedido(cliente_eva, itens_6))

pedido_da_fay = registrar_pedido(
    7, lambda: Pedido(criar_cliente("Fay Dias", "55566677788", "fay@email.com", "Rua F, 60", "Salto", "0", "N"), ItensDoPedido())
)

itens_8 = ItensDoPedido()
itens_8.adicionar(ItemDoPedido(fone, 2))
pedido_do_gil = registrar_pedido(8, lambda: Pedido(cliente_gil, itens_8))

print(f"pagar 1: {pedidos.pagar_pedido(1)}")
print(f"pagar 3: {pedidos.pagar_pedido(3)}")
print(f"pagar 5: {pedidos.pagar_pedido(5)}")
print(f"pagar 6: {pedidos.pagar_pedido(6)}")
print(f"cancelar 5: {pedidos.cancelar_pedido(5)}")
print(f"cancelar 1: {pedidos.cancelar_pedido(1)}")

pedidos.imprimir_relatorio()
print(f"arrecadado: {pedidos.calcular_total_arrecadado()}")
print(f"abertos: {pedidos.contar_pedidos_abertos()}") 