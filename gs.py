# Laura Barreto - RM561965
# Matheus Freitas Vieira - RM566198
# Natália Camargo - RM565769

import random
import time

ALTURA_TOTAL_RESERVATORIO_CM = 400.0
LIMIAR_ATENCAO_PERCENT = 0.50 # Acima de 50% atenção
LIMIAR_CRITICO_PERCENT = 0.70 # Acima de 70% Risco Crítico

DADOS_SENSOR_SIMULADOS = [
    50.0, 100.0, 150.0, 190.0, # Seguro
    220.0, 250.0, 270.0, # Atenção
    285.0, 300.0, 350.0, 395.0, # Risco Crítico
    405.0, # Erro ou rio acima do limite máximo
    -5.0, # Erro
    10.0 # Reset
]
indice_leitura_sensor = 0

def validar_entrada_texto_obrigatorio(prompt_usuario, tamanho_max=150):
    while True:
        entrada = input(prompt_usuario).strip()
        if not entrada:
            exibir_mensagem_console("Esta informação é obrigatória. Por favor, tente novamente.", "ERRO")
        elif len(entrada) > tamanho_max:
            exibir_mensagem_console(f"O texto não pode exceder {tamanho_max} caracteres. Por favor, tente novamente.", "ERRO")
        else:
            return entrada

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

def ler_dados_sensor_simulado(sensor_id="principal"):

    global indice_leitura_sensor
    if not DADOS_SENSOR_SIMULADOS:
        return round(random.uniform(5.0, 25.0), 1)

    nivel_simulado = DADOS_SENSOR_SIMULADOS[indice_leitura_sensor]
    indice_leitura_sensor = (indice_leitura_sensor + 1) % len(DADOS_SENSOR_SIMULADOS)

    time.sleep(0.5)
    return nivel_simulado

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

def exibir_mensagem_console(mensagem, tipo="INFO"):
    if tipo == "ALERTA":
        print(f"[ALERTA 🔴] {mensagem}")
    elif tipo == "ERRO":
        print(f"[ERRO ❌] {mensagem}")
    elif tipo == "DESTAQUE":
        print(f"\n--- {mensagem} ---\n")
    else: # INFO
        print(f"[INFO ℹ️] {mensagem}")

def main_loop_simulador():

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

if __name__ == "__main__":
    main_loop_simulador()