import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Integracao:
  def __init__(self):
    self.token: str = os.environ.get("HUBSPOT_ACCESS_TOKEN")
    self.headers = {
        "Authorization": f"Bearer {self.token}",
        "Content-Type": "application/json"
    }
    self.status_conectado: bool = False
    self.propriedades_empresas: list = []
    self.tipo_pipeline: str = "tickets"
    self.pipelines: list = []
    self.proprietarios: list = []
    self.membros_equipe: list = []

    # COLOCAR UMA REGRA PARA NÃO FAZER SEMPRE ESSA REQUISIÇÃO -> armazenar esses dados no BD?
    self.captura_proprietarios()
    self.captura_pipelines()

  def definir_propriedades_empresa(self, propriedades: list):
    self.propriedades_empresas = propriedades

  def definir_propriedades_empresa(self, membros: list):
    self.membros_equipe = membros

  # --------- HELPERS -----------------
  def parse_dates(self, d):
    return {
        k: (
            datetime.fromisoformat(v.replace("Z", "+00:00")).date()
            if isinstance(v, str) and "T" in v and v.endswith("Z")
            else v
        )
        for k, v in d.items()
    }
  
  def traduzir_owner(self, objeto):
    # Cria um dicionário de mapeamento id → nome completo
    mapa_owners = {
        str(p["id"]): f"{p.get('firstName', '')} {p.get('lastName', '')}".strip()
        for p in self.proprietarios
    }

    # Cria uma cópia do objeto para não sobrescrever o original
    resultado = objeto.copy()
    owner_id = str(objeto.get("hubspot_owner_id"))

    # Substitui pelo nome se encontrar
    resultado["hubspot_owner_nome"] = mapa_owners.get(owner_id, "Desconhecido")
    return resultado

  # ------------ FUNÇÕES BASE ----------------
  def captura_proprietarios(self):
    URL = "https://api.hubspot.com/crm/v3/owners"
    all_owners = []
    after = None

    while True:
        params = {}
        if after:
            params['after'] = after

        response = requests.get(URL, headers=self.headers, params=params)

        if response.status_code != 200:
            print(f"Erro na requisição: {response.status_code}, {response.text}")
            break

        data = response.json()
        all_owners.extend(data.get("results", []))

        paging = data.get('paging', {})
        after = paging.get('next', {}).get('after')

        if not after:
            break

    self.proprietarios = all_owners

  def captura_pipelines(self):
    url = f"https://api.hubapi.com/crm/v3/pipelines/{self.tipo_pipeline}"

    response = requests.get(url, headers=self.headers)

    if response.status_code == 200:
        registros = response.json().get("results", [])
        self.pipelines = [{"id": r.get("id", ""), "nome": r.get("label", "")} for r in registros]
    else:
        print(f"Erro ao buscar os pipelines: {response.status_code} - {response.text}")
        return []
    

  def captura_detalhes_pipeline(self, pipeline_id):
    url = f'https://api.hubapi.com/crm/v3/pipelines/tickets/{pipeline_id}'
    response = requests.get(url, headers=self.headers)

    if response.status_code == 200:
        return [{"id": r.get("id", ""), "etapa": r.get("label", ""), "fechado": r.get("metadata").get("isClosed")} for r in response.json().get("stages")]
    else:
        print("Erro ao buscar estágios do pipeline:", response.text)
        return []

  def capturar_objetos_associados(self, ticket_id: str, objeto_associado: str, propriedades: list = []):
    url = f"https://api.hubapi.com/crm/v3/objects/{self.tipo_pipeline}/{ticket_id}/associations/{objeto_associado}"
    response = requests.get(url, headers=self.headers)

    if response.status_code == 200:
      results = response.json().get("results", [])
      object_ids = [item["id"] for item in results]

      objetos_associados = []

      for id in object_ids:
        url = f"https://api.hubapi.com/crm/v3/objects/{objeto_associado}/{id}"
        propriedades_objeto = propriedades
        if propriedades != []:
          params = {
              "properties": propriedades_objeto
          }
        else:
          params = {}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
          objetos_associados.append(response.json()['properties'])

      return objetos_associados

    else:
        print(f"[ERRO] Falha ao buscar objetos associados: {response.status_code}, {response.text}")
        return []

  # ------------- FUNÇÕES DE DETALHES DO ONBOARDING ---------------------
  def capturar_detalhes_ticket(self, 
    ticket_id: str, 
    propriedades: list = [
      "subject",
      'content',
      'hs_object_id',
      'hs_pipeline',
      'hs_pipeline_stage',
      "createdate",
      "closed_date",
      "hubspot_owner_id",
    ]):

    url = f"https://api.hubapi.com/crm/v3/objects/{self.tipo_pipeline}/{ticket_id}"
      
    params = {
        "properties": propriedades
    }

    response = requests.get(url, headers=self.headers, params=params)     

    if response.status_code == 200:
      return self.traduzir_owner(self.parse_dates(response.json()['properties']))
    else:
      print(f"Erro na requisição de captura de detalhes do ticket: {response.status_code}, {response.text}")
      return None

  def capturar_contatos_associados(self, ticket_id):
    propriedades_contatos = [
      "firstname",                    # Primeiro nome do contato
      "lastname",                     # Sobrenome do contato
      "email",                        # E-mail principal
      "phone",                        # Telefone principal
      "company",                      # Nome da empresa (campo de texto livre)
      "jobtitle",                     # Cargo do contato
      "hs_lastmodifieddate"           # Data da última modificação no contato
    ]
    return [self.parse_dates(r) for r in self.capturar_objetos_associados(ticket_id, "contacts", propriedades_contatos)]

  def capturar_reunioes(self, ticket_id):
    propriedades_reunioes = [
      "hs_meeting_title",             # Título da reunião
      "hs_meeting_body",              # Descrição ou pauta da reunião
      "hubspot_owner_id",             # ID do responsável pela reunião (usuário HubSpot)
      "hs_internal_meeting_notes",    # Notas internas (visíveis apenas internamente)
      "hs_meeting_external_url",      # Link externo da reunião (ex: Zoom, Meet)
      "hs_meeting_location",          # Local da reunião (físico ou virtual)
      "hs_meeting_start_time",        # Data e hora de início da reunião
      "hs_meeting_end_time",          # Data e hora de término da reunião
      "hs_meeting_outcome",           # Resultado da reunião (ex: "Completed", "Scheduled", etc.)
      "hs_activity_type",             # Tipo de atividade (deve ser "MEETING")
      "hs_attachment_ids"             # IDs de arquivos anexados à reunião
    ]
    registros = [self.parse_dates(r) for r in self.capturar_objetos_associados(ticket_id, "meetings", propriedades_reunioes)]
    return [self.traduzir_owner(r) for r in registros]

  def capturar_emails(self, ticket_id):
    propriedades_emails = [
      "hs_timestamp",               # Data/hora do e-mail (define a posição na timeline do CRM)
      "hubspot_owner_id",          # ID do proprietário do HubSpot (usuário associado ao e-mail)
      "hs_email_direction",        # Direção do e-mail (INCOMING_EMAIL, FORWARDED_EMAIL, etc.)
      "hs_email_html",             # Corpo do e-mail em HTML (se enviado do CRM)
      "hs_email_status",           # Status do envio (BOUNCED, FAILED, SCHEDULED, SENDING, SENT)
      "hs_email_subject",          # Assunto do e-mail
      "hs_email_text",             # Corpo do e-mail em texto simples
      "hs_attachment_ids",         # IDs dos anexos do e-mail (separados por ponto e vírgula)
      "hs_email_headers",          # Headers do e-mail (campos técnicos do e-mail)
      "hs_email_from_email",       # E-mail do remetente
      "hs_email_from_firstname",   # Primeiro nome do remetente
      "hs_email_from_lastname",    # Sobrenome do remetente
      "hs_email_to_email",         # E-mail(s) do(s) destinatário(s)
      "hs_email_to_firstname",     # Primeiro nome do(s) destinatário(s)
      "hs_email_to_lastname"       # Sobrenome do(s) destinatário(s)
    ]
    registros = [self.parse_dates(r) for r in self.capturar_objetos_associados(ticket_id, "emails", propriedades_emails)]
    return [self.traduzir_owner(r) for r in registros]
  
  def capturar_anotacoes(self, ticket_id):
    propriedades_notes = [
      "hs_timestamp",         # Data/hora da criação da nota (posiciona na timeline do CRM)
      "hs_note_body",         # Conteúdo textual da nota (até 65.536 caracteres)
      "hubspot_owner_id",     # ID do proprietário (usuário que criou a nota no HubSpot)
      "hs_attachment_ids"     # IDs de anexos da nota (separados por ponto e vírgula)
    ]
    registros = [self.parse_dates(r) for r in self.capturar_objetos_associados(ticket_id, "notes", propriedades_notes)]
    return [self.traduzir_owner(r) for r in registros]

  def capturar_tarefas(self, ticket_id):
    propriedades_tarefas = [
      "hs_task_body",                # Corpo/texto da tarefa
      "hs_timestamp",                # Data e hora programada da tarefa
      "hs_task_priority",            # Prioridade: HIGH, MEDIUM, LOW
      "hs_task_status",              # Status: NOT_STARTED, COMPLETED, etc.
      "hs_task_subject",            # Título/assunto da tarefa
      "hubspot_owner_id",           # ID do responsável pela tarefa
      "hs_note_body",               # Também armazena o corpo para atividades em geral
      "hs_createdate",              # Data de criação
      "hs_lastmodifieddate",        # Data da última modificação
      "hs_activity_type",           # Deve ser 'TASK' para esse tipo de objeto
      "hs_task_type",               # Tipo da tarefa (customizável, ex: FOLLOW_UP)
      "hs_task_reminders",          # Lembretes definidos
      "hs_task_completion_date",    # Data de conclusão
      "hs_task_due_date",           # Data de vencimento (se existir)
      "hs_task_associated_contacts",# Contatos relacionados
      "hs_task_associated_companies", # Empresas relacionadas
      "hs_task_associated_deals",   # Negócios relacionados
      "hs_task_associated_tickets", # Tickets relacionados
      "hs_object_id"                # ID da tarefa
    ]
    
    registros = [self.parse_dates(r) for r in self.capturar_objetos_associados(ticket_id, "tasks", propriedades_tarefas)]
    return [self.traduzir_owner(r) for r in registros]

  def capturar_empresa_associada(self, ticket_id):
    if self.propriedades_empresas == []:
      propriedades_empresas = [
        "hs_object_id",                 
        "name",                    
        "createdate",
        "domain",                                                               
        "hs_lastmodifieddate"          
      ]
    else:
      propriedades_empresas = self.propriedades_empresas

    return [self.parse_dates(r) for r in self.capturar_objetos_associados(ticket_id, "companies", propriedades_empresas)]