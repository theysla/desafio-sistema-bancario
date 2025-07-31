# Sistema Bancário em Python (POO)

Este projeto é uma simulação de um sistema bancário simples, desenvolvido com foco na prática dos principais conceitos de **Programação Orientada a Objetos (POO)** em Python. Ele permite o cadastro de clientes, criação de contas correntes, realização de depósitos, saques e visualização de extratos, com registro de todas as transações.

## Funcionalidades

- Criar clientes (Pessoa Física)
- Criar contas correntes vinculadas aos clientes
- Realizar depósitos e saques
- Limite diário de saques (3 saques por conta)
- Limite por valor de saque (R$500 por saque)
- Extrato com histórico de transações
- Validações de saldo, limites e dados de entrada

## Estrutura Orientada a Objetos

O projeto segue o diagrama UML proposto no desafio da DIO e está dividido nas seguintes classes:

- `Transacao` (classe abstrata)
  - `Deposito`
  - `Saque`
- `Historico` (registro das transações)
- `Conta`
  - `ContaCorrente` (com limites)
- `Cliente`
  - `PessoaFisica` (com nome, CPF e data de nascimento)

## Requisitos

- Python 3.10 ou superior

## Como executar

1. Clone este repositório ou copie o código para um arquivo chamado `banco_poo.py`.

2. Execute o programa via terminal ou IDE:

```bash
python banco_poo.py

