# CODIGO (TF 11) - APOS PASSO 7 (LEI DE DEMETER E DIGA, NAO PERGUNTE)


class Cpf:
    """Encapsula e valida o CPF."""

    def __init__(self, valor: str):
        if len(valor) != 11:
            raise ValueError("cpf invalido")
        self._valor = valor

    def __str__(self) -> str:
        return self._valor


class Email:
    """Encapsula e valida o e-mail."""

    def __init__(self, endereco: str):
        if not endereco:
            raise ValueError("email vazio")
        if "@" not in endereco:
            raise ValueError("email invalido")
        self._endereco = endereco

    def __str__(self) -> str:
        return self._endereco


class Cep:
    """Encapsula e valida o CEP."""

    def __init__(self, codigo: str):
        if len(codigo) != 8:
            raise ValueError("cep invalido")
        self._codigo = codigo

    def __str__(self) -> str:
        return self._codigo


class Dinheiro:
    """Guarda valores em centavos inteiros e realiza operacoes exatas."""

    def __init__(self, centavos: int):
        self._centavos = centavos

    @classmethod
    def de_centavos(cls, centavos: int) -> "Dinheiro":
        return cls(centavos)

    def somar(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self._centavos + outro._centavos)

    def subtrair(self, outro: "Dinheiro") -> "Dinheiro":
        return Dinheiro(self._centavos - outro._centavos)

    def multiplicar_por_quantidade(self, quantidade: int) -> "Dinheiro":
        return Dinheiro(self._centavos * quantidade)

    def calcular_percentual(self, percentual: int) -> "Dinheiro":
        return Dinheiro(round(self._centavos * percentual / 100))

    def __str__(self) -> str:
        reais = self._centavos / 100
        return f"R$ {reais:.2f}"


class Status:
    """Controla o estado de ciclo de vida do pedido."""

    _DESCRICOES = {
        "A": "aberto",
        "P": "pago",
        "C": "cancelado",
    }

    def __init__(self, codigo: str = "A"):
        self._codigo = codigo

    def esta_aberto(self) -> bool:
        return self._codigo == "A"

    def esta_pago(self) -> bool:
        return self._codigo == "P"

    def definir_pago(self) -> None:
        self._codigo = "P"

    def definir_cancelado(self) -> None:
        self._codigo = "C"

    def __str__(self) -> str:
        return self._DESCRICOES.get(self._codigo, "")


class Pessoa:
    """Guarda a identidade civil e formata o nome."""

    def __init__(self, nome: str, cpf: Cpf, email: Email):
        self._nome = nome
        self._cpf = cpf
        self._email = email

    def formatar_identificacao(self) -> str:
        return self._nome


class Endereco:
    """Guarda a localizacao e formata a cidade."""

    def __init__(self, rua: str, cidade: str, cep: Cep):
        self._rua = rua
        self._cidade = cidade
        self._cep = cep

    def formatar_cidade(self) -> str:
        return self._cidade


class Cliente:
    """Associa pessoa, endereco e tipo, respondendo por seus dados sem vazar dependencias."""

    def __init__(self, pessoa: Pessoa, endereco: Endereco, tipo: str):
        self._pessoa = pessoa
        self._endereco = endereco
        self._tipo = tipo

    def formatar_cabecalho(self) -> str:
        nome = self._pessoa.formatar_identificacao()
        cidade = self._endereco.formatar_cidade()
        return f"{nome} - {cidade}"

    def calcular_desconto_sobre(self, valor: Dinheiro) -> Dinheiro:
        if self._tipo == "V":
            return valor.calcular_percentual(10)
        elif self._tipo == "F":
            return valor.calcular_percentual(20)
        else:
            return Dinheiro.de_centavos(0)


class Produto:
    """Define o produto comercializado."""

    def __init__(self, nome: str, preco: Dinheiro):
        self._nome = nome
        self._preco = preco

    def calcular_total_do_item(self, quantidade: int) -> Dinheiro:
        return self._preco.multiplicar_por_quantidade(quantidade)

    def descrever_linha(self, quantidade: int, subtotal: Dinheiro) -> str:
        return f"   {quantidade} x {self._nome} = {subtotal}"


class ItemDoPedido:
    """Associa produto e quantidade demandada."""

    def __init__(self, produto: Produto, quantidade: int):
        self._produto = produto
        self._quantidade = quantidade

    def subtotal(self) -> Dinheiro:
        return self._produto.calcular_total_do_item(self._quantidade)

    def imprimir_linha(self) -> None:
        linha = self._produto.descrever_linha(self._quantidade, self.subtotal())
        print(linha)


class ItensDoPedido:
    """Colecao de primeira classe para os itens do pedido."""

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
    """Aplica o principio 'diga, nao pergunte' nas transicoes de status e impressao."""

    def __init__(self, cliente: Cliente, itens: ItensDoPedido):
        self._cliente = cliente
        self._itens = itens
        self._status = Status("A")

    def adicionar_item(self, item: ItemDoPedido) -> None:
        self._itens.adicionar(item)

    def pagar(self) -> bool:
        if self._status.esta_aberto():
            if not self._itens.esta_vazia():
                self._status.definir_pago()
                return True
            else:
                return False
        else:
            return False

    def cancelar(self) -> bool:
        if self._status.esta_aberto():
            self._status.definir_cancelado()
            return True
        else:
            return False

    def esta_aberto(self) -> bool:
        return self._status.esta_aberto()

    def valor_a_pagar(self) -> Dinheiro:
        total = self._itens.calcular_total()
        desconto = self._cliente.calcular_desconto_sobre(total)
        return total.subtrair(desconto)

    def somar_se_pago(self, acumulador: Dinheiro) -> Dinheiro:
        if self._status.esta_pago():
            return acumulador.somar(self.valor_a_pagar())
        return acumulador

    def imprimir_detalhes(self, numero: int) -> None:
        cabecalho = self._cliente.formatar_cabecalho()
        print(f"Pedido {numero} - {cabecalho}")
        print(f"  status: {self._status}")
        self._itens.imprimir_itens()
        if not self._itens.esta_vazia():
            total = self._itens.calcular_total()
            desconto = self._cliente.calcular_desconto_sobre(total)
            a_pagar = total.subtrair(desconto)
            print(f"  total: {total} | desconto: {desconto} | a pagar: {a_pagar}")


class Pedidos:
    """Colecao de primeira classe para armazenamento e consultas de pedidos."""

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
            total = pedido.somar_se_pago(total)
        return total

    def contar_pedidos_abertos(self) -> int:
        contador = 0
        for pedido in self._pedidos.values():
            if pedido.esta_aberto():
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