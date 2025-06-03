# Laura Barreto - RM561965
# Matheus Freitas Vieira - RM566198
# Natália Camargo - RM565769

import random
import time

ALTURA_TOTAL_RESERVATORIO_CM = 400.0
LIMIAR_ATENCAO_PERCENT = 0.50
LIMIAR_CRITICO_PERCENT = 0.70

# Determinar a altura total do reservatorio/rio que está sendo analizado pelo sensor simulado, além de dizer qual é o nível de atenção e o crítico em %.

DADOS_SENSOR_SIMULADOS = [
    50.0, 100.0, 150.0, 190.0, # Seguro
    220.0, 250.0, 270.0, # Atenção
    285.0, 300.0, 350.0, 395.0, # Risco Crítico
    405.0, # Erro ou rio acima do limite máximo
    -5.0, # Erro
    10.0 # Reset
]

# Lista que apresenta os valores que podem ser lidos pelo sensor simulado.

def validar_entrada_texto_obrigatorio(prompt_usuario, tamanho_max=150):
    while True:
        entrada = input(prompt_usuario).strip()
        if not entrada:
            exibir_mensagem_console("Esta informação é obrigatória. Por favor, tente novamente.", "ERRO")
        elif len(entrada) > tamanho_max:
            exibir_mensagem_console(f"O texto não pode exceder {tamanho_max} caracteres. Por favor, tente novamente.", "ERRO")
        else:
            return entrada

# Essa função verifica se o usuário inseriu o texto solicitado e se o texto está dentro do tamanho correto, se o texto estiver dentro dos parâmetros
# a função retorna o texto, caso o usuário não digite o texto exibe uma mensagem de erro e o while retorna para o inicio para o usuario digitar o texto,
# caso o usuário digite um texto maior do que o permitido é exibido uma mensagem de erro e solicita para ele digitar novamente.

def validar_opcao_lista(prompt_usuario, opcoes_validas):
    print(prompt_usuario)
    for chave, descricao in opcoes_validas.items():
        print(f"  {chave}) {descricao}")

    while True:
        escolha = input("Digite sua opção: ").lower()
        if escolha in opcoes_validas:
            return escolha
        else:
            exibir_mensagem_console(f"Opção inválida. Por favor, escolha entre: {', '.join(opcoes_validas.keys())}.", "ERRO")

# Essa função exibe um menu com opções válidas para o usuário escolher, caso o usuário selecione uma opção existente, a função retorna a escolha,
# se a opção for inválida, exibe uma mensagem de erro e solicita novamente a escolha até que uma opção válida seja digitada.

def ler_dados_sensor_simulado(sensor_id="principal"):
    global indice_leitura_sensor

    if indice_leitura_sensor is None:
        indice_leitura_sensor = random.randint(0, 3)

    if not DADOS_SENSOR_SIMULADOS:
        return round(random.uniform(50, 400), 1)

    nivel_simulado = DADOS_SENSOR_SIMULADOS[indice_leitura_sensor]
    indice_leitura_sensor = (indice_leitura_sensor + 1) % len(DADOS_SENSOR_SIMULADOS)

    time.sleep(0.5)
    return nivel_simulado


# Essa função simula a leitura do sensor de nível de água, na primeira execução, começa por um índice aleatório entre os quatro primeiros da lista,
# depois segue pelos dados simulados se a lista estiver vazia, gera um valor aleatório entre 50 e 400 cm.

def calcular_status_alerta_sensor(nivel_agua_cm, altura_total_cm, limiar_atencao_p, limiar_critico_p):

    if nivel_agua_cm < 0 or nivel_agua_cm > (altura_total_cm + altura_total_cm * 0.1) :
        return "Falha Sensor"

    nivel_atencao_abs = altura_total_cm * limiar_atencao_p
    nivel_critico_abs = altura_total_cm * limiar_critico_p

    if nivel_agua_cm >= nivel_critico_abs:
        return "Crítico"
    elif nivel_agua_cm >= nivel_atencao_abs:
        return "Atenção"
    else:
        return "Seguro"

# Essa função calcula o status do alerta com base no nível de água lido pelo sensor simulado, se o nível estiver fora da faixa esperada,
# retorna "Falha Sensor", se não estiver, compara com os limiares para determinar se a situação é "Seguro", "Atenção" ou "Crítico".

def coletar_relato_cidadao():
    exibir_mensagem_console("--- Registro de Nova Ocorrência Comunitária ---", "DESTAQUE")

    tipos_ocorrencia_validos = {
        "1": "Alagamento de via",
        "2": "Bueiro entupido com acúmulo de água",
        "3": "Nível de rio/córrego subindo rapidamente",
        "4": "Risco de deslizamento devido à chuva",
        "5": "Outro tipo de ocorrência relacionada a enchentes"
    }
    tipo_escolhido_chave = validar_opcao_lista("Selecione o tipo de ocorrência:", tipos_ocorrencia_validos)
    tipo_ocorrencia_desc = tipos_ocorrencia_validos[tipo_escolhido_chave]

    local_ocorrencia = validar_entrada_texto_obrigatorio("Localização da ocorrência (ex: Rua Exemplo, perto do nº 123): ")
    descricao_adicional = validar_entrada_texto_obrigatorio("Descreva brevemente a situação: ", tamanho_max=200)

    confirmar = input("Confirmar o envio deste relato? (s/n): ").lower()
    if confirmar == 's':
        relato = {
            "tipo": tipo_ocorrencia_desc,
            "local": local_ocorrencia,
            "descricao": descricao_adicional,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return relato
    else:
        exibir_mensagem_console("Registro de ocorrência cancelado.", "INFO")
        return None

# Essa função coleta informações do cidadão sobre uma ocorrência relacionada, o usuário escolhe o tipo, informa o local e uma descrição,
# se o usuário confirmar o envio da ocorrência, a função retorna o relato, se ele não conficar, cancela o registro.

def processar_relatos_para_alerta(lista_relatos):
    if not lista_relatos:
        return None

    ultimo_relato = lista_relatos[-1]
    if "subindo rapidamente" in ultimo_relato["tipo"].lower() or \
       "alagamento de via" in ultimo_relato["tipo"].lower() or \
       "risco de deslizamento" in ultimo_relato["tipo"].lower():
        return (f"Alerta Comunitário Urgente: Recebido relato de '{ultimo_relato['tipo']}' "
                f"em '{ultimo_relato['local']}'. Descrição: '{ultimo_relato['descricao']}'. "
                f"Recomenda-se precaução na área!")
    return None

# Essa função analisa a lista de relatos enviados pela comunidade e verifica se o último relato requer um alerta urgente,
# se o tipo do relato for crítico, retorna uma mensagem de alerta ou retorna None se não for urgente.

def exibir_mensagem_console(mensagem, tipo="INFO"):
    if tipo == "ALERTA":
        print(f"[ALERTA 🔴] {mensagem}")
    elif tipo == "ERRO":
        print(f"[ERRO ❌] {mensagem}")
    elif tipo == "DESTAQUE":
        print(f"\n--- {mensagem} ---\n")
    else: # INFO
        print(f"[INFO ℹ️] {mensagem}")

# Essa função exibe mensagens no console com diferentes categorias visuais de destaque: ALERTA, ERRO, DESTAQUE ou INFO, Ajuda a organizar e
# identificar melhor o tipo da informação apresentada ao usuário para um entendimento mais facil.

def main_loop_simulador():

    global indice_leitura_sensor
    indice_leitura_sensor = None

    exibir_mensagem_console("Iniciando Simulador do Sistema de Alerta Cidadão Conectado", "DESTAQUE")

    historico_relatos_comunitarios = []
    ciclo_atual = 1

    while True:
        exibir_mensagem_console(f"Iniciando Ciclo de Monitoramento nº {ciclo_atual}", "DESTAQUE")

        nivel_agua_atual_cm = ler_dados_sensor_simulado()
        exibir_mensagem_console(f"Sensor 'Rio Principal' - Leitura Nível Água: {nivel_agua_atual_cm:.2f} cm (de {ALTURA_TOTAL_RESERVATORIO_CM:.1f} cm)")

        status_alerta_do_sensor = calcular_status_alerta_sensor(
            nivel_agua_atual_cm,
            ALTURA_TOTAL_RESERVATORIO_CM,
            LIMIAR_ATENCAO_PERCENT,
            LIMIAR_CRITICO_PERCENT
        )
        exibir_mensagem_console(f"Status do Sistema (baseado no sensor): {status_alerta_do_sensor}", "ALERTA" if status_alerta_do_sensor != "Seguro" else "INFO")

        if input("Deseja registrar uma ocorrência comunitária neste ciclo? (s/n): ").lower() == 's':
            novo_relato = coletar_relato_cidadao()
            if novo_relato:
                historico_relatos_comunitarios.append(novo_relato)
                exibir_mensagem_console("Relato comunitário adicionado com sucesso!", "INFO")

                alerta_baseado_em_relatos = processar_relatos_para_alerta(historico_relatos_comunitarios)
                if alerta_baseado_em_relatos:
                    exibir_mensagem_console(alerta_baseado_em_relatos, "ALERTA")
            else:
                exibir_mensagem_console("Nenhum relato comunitário foi adicionado neste ciclo.", "INFO")

        if input("\nContinuar para o próximo ciclo de monitoramento? (s/n): ").lower() != 's':
            break

        ciclo_atual += 1
        print("-" * 50)

    exibir_mensagem_console("Simulador encerrado pelo usuário.", "DESTAQUE")

# Essa função executa o ciclo principal do simulador, realizando leituras do sensor e permitindo o registro de ocorrências comunitárias,
# a cada ciclo, exibe as informações e solicita interações do usuário e pode ser encerrada quando o usuário desejar, no icicio da função,
# a variável global indice_leitura_sensor é inicializada como none para que a primeira leitura do sensor simulado seja aleatório.

usuarios = {}

def cadastrar_usuario():
    email = input("Digite seu e-mail (será seu login): ")
    if email in usuarios:
        print("E-mail já cadastrado!\n")
        return

    nome = input("Digite seu nome completo: ")
    telefone = input("Digite seu telefone: ")
    endereco = input("Digite seu endereço: ")
    senha = input("Crie uma senha: ")

    usuarios[email] = {
        "nome": nome,
        "telefone": telefone,
        "endereco": endereco,
        "senha": senha
    }

    print("Cadastro realizado com sucesso!\n")
    print(f"\n Login bem-sucedido! Bem-vindo(a), {usuarios[email]['nome']}!\n")

    main_loop_simulador()

# Essa função inicia pedindo o e-mail do usuário e verifica se o e-mail já foi cadastrado, dando um retorno ao usuário.
# Após verificar isso, o usuário deve preencher os outros campos para se cadastrar. Os dados são armazenados e o cadastro é realizado com sucesso.

def fazer_login():
    email = input("Digite seu e-mail: ")
    senha = input("Digite sua senha: ")

    if email in usuarios and usuarios[email]["senha"] == senha:
        print(f"\n Login bem-sucedido! Bem-vindo(a), {usuarios[email]['nome']}!\n")
        print("Seus dados:")
        print(f"E-mail: {email}")
        print(f"Telefone: {usuarios[email]['telefone']}")
        print(f"Endereço: {usuarios[email]['endereco']}\n")

        main_loop_simulador()
    else:
        print("E-mail ou senha incorretos.\n")

# Essa função inicia pedindo e-mail e senha. Caso estejam corretos, o programa exibe uma mensagem de sucesso e retorna os dados do usuário.
# Caso estejam incorretos, retorna a mensagem "E-mail ou senha incorretos."

def menu():
    while True:
        print("Menu:")
        print("1 - Cadastrar")
        print("2 - Login")
        print("3 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            fazer_login()
        elif opcao == "3":
            print("Encerrando programa.")
            break
        else:
            print("Opção inválida.\n")

# Essa função ajuda o usuário a escolher se quer se cadastrar, fazer login ou sair do programa, direcionando para as outras funções, utilizando
# um while True para o que a função seja executada até o usuário escolher uma opção válida.

menu()