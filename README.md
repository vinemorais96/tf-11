# Trabalho TF-11: Object Calisthenics

**Aluno:** Vinicius Montagner  
**RA:** 6326020  

### 1. Normalização
A normalização centraliza os dados de cada entidade numa única instância em memória, fazendo com que as restantes estruturas apenas mantenham a sua referência. No caso da cliente Ana, os pedidos 1 e 3 apontam para o mesmo objeto `Cliente`, garantindo que alterações cadastrais ou de endereço fiquem imediatamente sincronizadas sem necessidade de atualizações manuais em múltiplos pedidos.

### 2. Obsessão por Tipos Primitivos
A classe `Cpf` encapsula e valida as suas próprias regras de integridade diretamente no construtor, impedindo que sequências inválidas circulem pela lógica da aplicação. A classe `Dinheiro` guarda centavos em formato inteiro (`int`) em vez de ponto flutuante (`float`), eliminando erros de arredondamento inerentes à representação binária e assegurando cálculos financeiros exatos.

### 3. Diga, Não Pergunte (Tell, Don't Ask)
A decisão de processar a liquidação foi internalizada na própria entidade `Pedido`. Em vez de um chamador externo obter o estado e os itens através de *getters* para validar regras de negócio, a invocação limita-se a `pedido.pagar()`, cabendo ao próprio objeto verificar se se encontra aberto e apto a ser liquidado.

### 4. Fail First e Polimorfismo
A validação em cascata (*hadouken*) foi substituída por retorno antecipado (*fail first*), tratando imediatamente os casos de erro e interrompendo o fluxo. A estrutura condicional `if/elif/else` para cálculo de descontos foi refatorada através de polimorfismo com as classes `TipoClienteNormal`, `TipoClienteVip` e `TipoClienteFuncionario`, delegando a cada uma a sua taxa específica.

### 5. Modularização
- **Cpf:** Valida e mantém o formato de 11 dígitos do documento de identificação civil.
- **Email:** Valida a presença de texto e do delimitador `@`.
- **Cep:** Valida a dimensão estrita de 8 dígitos do código postal.
- **Dinheiro:** Efetua operações aritméticas e formatação representativa em centavos inteiros.
- **Status:** Controla as transições de ciclo de vida do pedido e respetiva representação textual.
- **TipoClienteNormal / TipoClienteVip / TipoClienteFuncionario:** Classes polimórficas responsáveis pelo cálculo de percentagens de desconto.
- **Pessoa:** Armazena e formata os dados de identificação pessoal.
- **Endereco:** Armazena e gere a informação postal e geográfica.
- **Cliente:** Agrega a pessoa, endereço e categoria de cliente.
- **Produto:** Define a denominação do artigo e o respetivo valor monetário unitário.
- **ItemDoPedido:** Relaciona o produto com a quantidade pretendida.
- **ItensDoPedido:** Coleção de primeira classe responsável pela gestão e soma dos artigos de um pedido.
- **Pedido:** Orquestra o ciclo de vida, cálculos e transições de pagamento.
- **Pedidos:** Coleção de primeira classe para agregação, persistência em dicionário e relatórios globais.

### 6. Dívida Técnica
A maior exigência técnica consistiu em respeitar simultaneamente o limite de 3 atributos de instância por classe, a ausência integral de *getters* e a restrição de 1 nível de indentação por método. Isso obrigou à criação de métodos utilitários em cascata respeitando a Lei de Demeter para que o relatório pudesse ser emitido sem quebrar o encapsulamento.