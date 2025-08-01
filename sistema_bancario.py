from abc import ABC, abstractmethod
from datetime import datetime

# ===================== DECORADOR DE LOG =====================

def log_transacoes(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Executando {func.__name__} com args={args}, kwargs={kwargs}")
        resultado = func(*args, **kwargs)
        print(f"[LOG] Finalizou {func.__name__}")
        return resultado
    return wrapper

# ===================== TRANSACOES =====================

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.verificar_limite_diario():
            if conta.depositar(self.valor):
                conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.verificar_limite_diario():
            if conta.sacar(self.valor):
                conta.historico.adicionar_transacao(self)

# ===================== HISTORICO =====================

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })

    def contar_transacoes_do_dia(self):
        hoje = datetime.now().date()
        return sum(1 for t in self.transacoes if datetime.strptime(t["data"], "%d/%m/%Y %H:%M:%S").date() == hoje)

# ===================== CONTA E CONTA CORRENTE =====================

class Conta:
    def __init__(self, cliente, numero):
        self.agencia = "0001"
        self.numero = numero
        self.cliente = cliente
        self.saldo = 0.0
        self.historico = Historico()

    def saldo_conta(self):
        return self.saldo

    def sacar(self, valor):
        if valor <= 0:
            print("Valor inválido.")
            return False
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False
        self.saldo -= valor
        print(f"Saque de R$ {valor:.2f} realizado.")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor inválido.")
            return False
        self.saldo += valor
        print(f"Depósito de R$ {valor:.2f} realizado.")
        return True

    def verificar_limite_diario(self):
        total_hoje = self.historico.contar_transacoes_do_dia()
        if total_hoje >= 10:
            print("Limite de 10 transações diárias atingido para esta conta.")
            return False
        return True

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("Limite de saques diários atingido.")
            return False
        if valor > self.limite:
            print("Valor excede o limite por saque.")
            return False
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        return False

# ===================== CLIENTE =====================

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento

# ===================== GERADOR DE RELATÓRIO =====================

def gerar_relatorio_transacoes(conta, tipo=None):
    for transacao in conta.historico.transacoes:
        if tipo is None or transacao["tipo"].lower() == tipo.lower():
            yield transacao

# ===================== ITERADOR PERSONALIZADO =====================

class Contalterador:
    def __init__(self, contas):
        self._contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._contas):
            conta = self._contas[self._index]
            self._index += 1
            return {
                "numero": conta.numero,
                "saldo": conta.saldo,
                "cliente": conta.cliente.nome if hasattr(conta.cliente, "nome") else "Desconhecido"
            }
        else:
            raise StopIteration

# ===================== SISTEMA =====================

clientes = []
contas = []
contador_contas = 1

def buscar_cliente_por_cpf(cpf):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def criar_cliente():
    cpf = input("Informe o CPF (apenas números): ").strip()
    if buscar_cliente_por_cpf(cpf):
        print("Já existe um cliente com esse CPF.")
        return

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/UF): ").strip()

    novo_cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
    clientes.append(novo_cliente)
    print("Cliente criado com sucesso!")

def criar_conta_corrente():
    global contador_contas
    cpf = input("Informe o CPF do cliente: ").strip()
    cliente = buscar_cliente_por_cpf(cpf)

    if not cliente:
        print("Cliente não encontrado.")
        return

    nova_conta = ContaCorrente(cliente, contador_contas)
    cliente.adicionar_conta(nova_conta)
    contas.append(nova_conta)
    contador_contas += 1
    print(f"Conta criada com sucesso! Agência: {nova_conta.agencia} | Número: {nova_conta.numero}")

def listar_contas_do_cliente(cliente):
    if not cliente.contas:
        print("O cliente não possui contas.")
        return []

    for idx, conta in enumerate(cliente.contas, start=1):
        print(f"[{idx}] Conta Nº {conta.numero} | Saldo: R$ {conta.saldo:.2f}")
    return cliente.contas

@log_transacoes
def realizar_deposito():
    cpf = input("CPF do cliente: ").strip()
    cliente = buscar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    contas_cliente = listar_contas_do_cliente(cliente)
    if not contas_cliente:
        return

    opcao = int(input("Escolha a conta: ")) - 1
    conta = contas_cliente[opcao]
    valor = float(input("Valor do depósito: R$ "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

@log_transacoes
def realizar_saque():
    cpf = input("CPF do cliente: ").strip()
    cliente = buscar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    contas_cliente = listar_contas_do_cliente(cliente)
    if not contas_cliente:
        return

    opcao = int(input("Escolha a conta: ")) - 1
    conta = contas_cliente[opcao]
    valor = float(input("Valor do saque: R$ "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato():
    cpf = input("CPF do cliente: ").strip()
    cliente = buscar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    contas_cliente = listar_contas_do_cliente(cliente)
    if not contas_cliente:
        return

    opcao = int(input("Escolha a conta: ")) - 1
    conta = contas_cliente[opcao]

    print("\n=== EXTRATO ===")
    if not conta.historico.transacoes:
        print("Nenhuma transação realizada.")
    else:
        for transacao in conta.historico.transacoes:
            tipo = transacao["tipo"]
            valor = transacao["valor"]
            data = transacao["data"]
            print(f"{tipo}: R$ {valor:.2f} em {data}")
    print(f"Saldo atual: R$ {conta.saldo:.2f}")

def gerar_relatorio():
    cpf = input("CPF do cliente: ").strip()
    cliente = buscar_cliente_por_cpf(cpf)
    if not cliente:
        print("Cliente não encontrado.")
        return

    contas_cliente = listar_contas_do_cliente(cliente)
    if not contas_cliente:
        return

    opcao = int(input("Escolha a conta: ")) - 1
    conta = contas_cliente[opcao]
    tipo = input("Filtrar por tipo (Deposito/Saque ou deixe em branco): ").strip() or None

    print("\n=== RELATÓRIO DE TRANSAÇÕES ===")
    for transacao in gerar_relatorio_transacoes(conta, tipo):
        print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} em {transacao['data']}")

def listar_todas_contas():
    print("\n=== TODAS AS CONTAS DO BANCO ===")
    for info in Contalterador(contas):
        print(f"Conta Nº {info['numero']} | Cliente: {info['cliente']} | Saldo: R$ {info['saldo']:.2f}")

# ===================== MENU =========================

while True:
    print("\n=== MENU BANCO POO ===")
    print("[1] Criar Cliente")
    print("[2] Criar Conta Corrente")
    print("[3] Realizar Depósito")
    print("[4] Realizar Saque")
    print("[5] Exibir Extrato")
    print("[6] Gerar Relatório de Transações")
    print("[7] Listar Todas as Contas")
    print("[0] Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        criar_cliente()
    elif opcao == "2":
        criar_conta_corrente()
    elif opcao == "3":
        realizar_deposito()
    elif opcao == "4":
        realizar_saque()
    elif opcao == "5":
        exibir_extrato()
    elif opcao == "6":
        gerar_relatorio()
    elif opcao == "7":
        listar_todas_contas()
    elif opcao == "0":
        print("Saindo do sistema. Até logo!")
        break
    else:
        print("Opção inválida. Tente novamente.")
