
from abc import ABC, abstractmethod
from datetime import date

class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: Transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, cliente, numero: int, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente, numero: int):
        return cls(cliente, numero)

    def sacar(self, valor: float):
        if valor > 0 and valor <= self.saldo:
            self.saldo -= valor
            return True
        return False

    def depositar(self, valor: float):
        if valor > 0:
            self.saldo += valor
            return True
        return False

class ContaCorrente(Conta):
    def __init__(self, cliente, numero: int, limite: float, limite_saques: int, agencia="0001"):
        super().__init__(cliente, numero, agencia)
        self.limite = limite
        self.limite_saques = limite_saques

class Cliente:
    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        if conta in self.contas:
            return transacao.registrar(conta)
        return False

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf: str, nome: str, data_nascimento: date, endereco: str):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
