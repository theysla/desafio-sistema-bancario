saldo = 0.0
limite_saque = 500.0
extrato = ""
numero_saques = 0
LIMITE_SAQUES_DIARIOS = 3

while True:
    print("\n=== MENU ===")
    print("[1] Depositar")
    print("[2] Sacar")
    print("[3] Extrato")
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

    elif opcao == "0":
        print("Encerrando o sistema. Até logo!")
        break

    else:
        print("Opção inválida. Tente novamente.")
