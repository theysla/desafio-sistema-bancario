saldo = 0.0
limite_saque = 500.0
extrato = ""
numero_saques = 0
LIMITE_SAQUES_DIARIOS = 3
usuarios = []
contas = []
contador_contas = 1

def criar_usuario():
    cpf = input("Informe o CPF (apenas números): ").strip()
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("CPF já cadastrado! Não é possível criar outro usuário com o mesmo CPF.")
        return
    
    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (DD/MM/AAAA): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    novo_usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!")

def encontrar_usuario_por_cpf(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_conta():
    global contador_contas

    cpf = input("Informe o CPF do usuário: ").strip()
    usuario = encontrar_usuario_por_cpf(cpf)

    if usuario:
        nova_conta = {
            "agencia": "0001",
            "numero_conta": contador_contas,
            "usuario": usuario
        }
        contas.append(nova_conta)
        contador_contas += 1
        print(f"Conta criada com sucesso! Agência: 0001 | Número da conta: {nova_conta['numero_conta']}")
    else:
        print("Usuário não encontrado. Crie o usuário antes de abrir a conta.")

# ======================== MENU PRINCIPAL ===========================

while True:
    print("\n=== MENU ===")
    print("[1] Depositar")
    print("[2] Sacar")
    print("[3] Extrato")
    print("[4] Criar Usuário")
    print("[5] Criar Conta Corrente")
    print("[0] Sair")
    
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        valor = float(input("Informe o valor do depósito: R$ "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito realizado com sucesso.")
        else:
            print("Valor inválido. O depósito deve ser positivo.")

    elif opcao == "2":
        valor = float(input("Informe o valor do saque: R$ "))
        if numero_saques >= LIMITE_SAQUES_DIARIOS:
            print("Limite diário de saques atingido.")
        elif valor > limite_saque:
            print("Limite máximo por saque é de R$ 500.00.")
        elif valor > saldo:
            print("Saldo insuficiente.")
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque:    R$ {valor:.2f}\n"
            numero_saques += 1
            print("Saque realizado com sucesso.")
        else:
            print("Valor inválido para saque.")

    elif opcao == "3":
        print("\n=== EXTRATO ===")
        if extrato == "":
            print("Não foram realizadas movimentações.")
        else:
            print(extrato)
        print(f"Saldo atual: R$ {saldo:.2f}")

    elif opcao == "4":
        criar_usuario()

    elif opcao == "5":
        criar_conta()

    elif opcao == "0":
        print("Encerrando o sistema. Até logo!")
        break

    else:
        print("Opção inválida. Tente novamente.")
