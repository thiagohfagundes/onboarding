import reflex as rx
from typing import List
from app.pages.base_page import base_blank_page
from app.models.processo import Etapa, Processo, Tarefa
from sqlmodel import select
from app.components.componentes_gerais import heading_pagina, card_headings, card_description, forms_label
from functools import partial

class OnboardingDetailsState(rx.State):
    processo: Processo = None
    etapas: List[Etapa] = []
    loading_tarefa: bool = False
    id_tarefa_selecionada: int
    loading_dados: bool = True

    @rx.var(cache=True)
    def onboarding_id(self) -> str:
        return self.router.page.params.get("id", "")
    
    def captura_detalhes_onboarding(self): # GET onboarding
        with rx.session() as session:
            dados = session.exec(
                Processo.select().where(
                    Processo.id == self.onboarding_id
                )
            ).first()

            self.processo = dados
            self.etapas = dados.etapas

            etapas_list = list(dados.etapas or [])
            for e in etapas_list:
                try:
                    e.tarefas = list(e.tarefas or [])
                except Exception:
                    e.tarefas = []

            self.etapas = etapas_list
            self.loading_dados = False
            print("Etapas carregadas:", [(e.id, e.nome, len(e.tarefas)) for e in self.etapas])

    def cria_etapa(self, form_data: dict): # POST etapa
        with rx.session() as session:
            nova_etapa = Etapa(
                nome=form_data.get("nome"),
                processo_id=self.onboarding_id
            )
            session.add(nova_etapa)
            session.commit()
            session.refresh(nova_etapa)
            print(f"Etapa criada: {nova_etapa}")

    def cria_tarefa(self, form_data: dict):  # POST tarefa
        self.loading_tarefa = True # Não está funcionando
        etapa_id = form_data.get("etapa_id")
        nome = form_data.get("nome")

        try:
            # garante tipo correto
            try:
                etapa_id = int(etapa_id)
            except Exception:
                etapa_id = None

            with rx.session() as session:
                # pega o processo/etapa do DB
                processo = session.get(Processo, int(self.onboarding_id))
                etapa_obj = session.get(Etapa, etapa_id) if etapa_id else None

                nova_tarefa = Tarefa(
                    nome=nome,
                    etapa_id=etapa_id,
                    processo_id=int(self.onboarding_id),
                    etapa=etapa_obj,
                    processo=processo,
                )

                session.add(nova_tarefa)
                session.commit()
                session.refresh(nova_tarefa)
                print(f"Tarefa criada: {nova_tarefa}")

            # Recarrega dados do DB para sincronizar o state (faz a query pesada aqui)
            # (mantenha isso dentro do try para garantir que loading só pare depois)
            try:
                self.captura_detalhes_onboarding()
            except Exception as e:
                print("Erro ao recarregar detalhes após criar tarefa:", e)

        except Exception as e:
            print("Erro ao criar tarefa:", e)
        finally:
            # garante que o spinner pare apenas quando tudo terminar (commit + recarga)
            self.loading_tarefa = False

    @rx.event
    def excluir_tarefa(self, id: int):
        print(f"Tarefa {id} excluída")

    @rx.event
    def detalhes_tarefa(self, id: int):
        print(f"Detalhes da tarefa {id}")

    @rx.event
    def finalizar_tarefa(self, id:int):
        print(f"Tarefa {id} finalizada")

        

def breadcrumbs(caminho: list = []) -> rx.Component:
    return rx.hstack(
        rx.foreach(
            caminho,
            lambda item: rx.fragment(
                rx.link(item, href="#", color_scheme="blue"),
                rx.cond(item != caminho[-1],
                    rx.text(" / "),
                    rx.text("")
                )
            )
        ),
        margin_bottom="1em",
    )

def card_detalhes_onboarding(titulo: str, descricao: str, data_inicio: str, data_fim: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            card_headings(titulo),
            card_description(descricao),
            rx.divider(),
            rx.hstack(
                rx.icon("calendar", size=15, color=rx.color("accent")),
                rx.text(f"Início: {data_inicio}", size='2'),
                align='center',
                width='100%'
            ),
            rx.hstack(
                rx.icon("calendar-check", size=15, color=rx.color("accent")),
                rx.text(f"Término: {data_fim}", size='2'),
                align='center',
                width='100%'
            ),
            width="100%"
        ),
        width="100%",
        class_name="shadow-md"
    )

def detalhes_tarefa() -> rx.Component:
    return rx.dialog.content(
        rx.dialog.title("Detalhes da tarefa"),
        rx.divider(margin_bottom="1em"),
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon("check", size=15, color="white"),
                        width="30px",
                        height="30px",
                        border_radius="15px",
                        bg=rx.color("green", 7),
                        class_name="flex items-center justify-center"
                    ),
                    rx.text("Concluída?", weight="medium"),
                    align="center"
                ),
                rx.switch(color_scheme="teal"),
                justify="between",
                width='100%',
                padding='1em',
                align="center",
                class_name="rounded-xl border border-gray-200"
            ),
            forms_label("Nome da tarefa"),
            rx.input(width='100%', size="3"),
            rx.hstack(
                rx.vstack(
                    forms_label("Responsável"),
                    rx.select(items=["Pessoa"],width='100%', size="3"),
                    width='100%'
                ),
                rx.vstack(
                    forms_label("Prazo"),
                    rx.input(width='100%', type="date", size="3"),
                    width='100%'
                ),
                width='100%'
            ),
            rx.hstack(
                rx.switch(),
                forms_label("Tarefa externa (permitir visualização do cliente)"),
                width='100%',
                align="center"
            ),
            rx.vstack(
                rx.data_list.root(
                    rx.data_list.item(
                        rx.data_list.label("Data de criação"),
                        rx.data_list.value("21-10-2025"),
                        align="center",
                        width="100%"
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Data da última modif."),
                        rx.data_list.value("21-10-2025"),
                        align="center",
                        width="100%"
                    ),
                    rx.data_list.item(
                        rx.data_list.label("Data de conclusão"),
                        rx.data_list.value("-"),
                        align="center",
                        width="100%"
                    ),
                ),
                width="100%",
                padding="1em",
                class_name="rounded-xl border border-gray-200"
            ),
            rx.hstack(
                rx.text("Excluir"),
                rx.hstack(
                    rx.button("Cancelar", size="3"),
                    rx.button("Salvar alterações", size="3")
                ),
                justify='between',
                align="center",
                width='100%'
            )

        )
    )

def item_tarefa(tarefa: Tarefa) -> rx.Component:
    nome = tarefa.nome
    responsavel = rx.cond(
        tarefa.responsavel != None,
        tarefa.responsavel,
        "Sem responsável atribuído"
    )
    id = tarefa['id']
    status = tarefa.concluido
    status_prazo = "Em dia"

    return rx.hstack(
        rx.dialog.root(
            rx.dialog.trigger(
                rx.hstack(
                    rx.checkbox(checked=status, size='3'),
                    rx.text(nome, size='3', weight="medium", class_name=rx.cond(status, "line-through text-gray-500", "")),
                    rx.hstack(
                        rx.icon("circle-user", size=15, color=rx.color("gray", 7)),
                        rx.text(responsavel, size='3'),
                        align="center"
                    ),
                    rx.cond(status_prazo == "Em dia", 
                        rx.badge("Em dia", color_scheme='green', size='3'),
                        rx.badge("Atrasado", color_scheme='red', size='3')
                    ),
                    spacing ="4",
                    align="center",
                    width="100%",
                    class_name="hover:bg-gray-100 cursor-pointer p-2 rounded-lg",
                    on_click=lambda *_: OnboardingDetailsState.detalhes_tarefa(id)
                ),
                width="100%"
            ),
            detalhes_tarefa()
        ),
        rx.box(
            rx.icon("trash-2", size=15),
            class_name="p-2 rounded-full bg-red-100 text-red-600 hover:bg-red-200 hover:text-red-700 transition-all duration-200 cursor-pointer",
            on_click=lambda *_: OnboardingDetailsState.excluir_tarefa(id) # passando sempre o mesmo id
        ),
        width="100%"
    )

def icone_etapa(icone: str = "check-circle") -> rx.Component:
    return rx.box(
        rx.icon(icone, size=20, color="white"),
        width="40px",
        height="40px",
        border_radius="25px",
        bg=rx.color("blue", 7),
        class_name="flex items-center justify-center"
    )

def adicionar_tarefa(etapa_id) -> rx.Component:
    return rx.hstack(
        rx.form(
            rx.hstack(
                rx.input(placeholder="Nova tarefa", name="nome", size="3", width="100%"),
                rx.input(name="etapa_id", value=etapa_id, class_name='hidden'),
                rx.button(
                    rx.icon("plus", size=15, color="white"),
                    rx.text("Adicionar", size="3"),
                    loading=OnboardingDetailsState.loading_tarefa,
                    color_scheme="blue",
                    variant="solid",
                    size="3",
                    radius="large",
                    class_name="cursor-pointer hover:brightness-90",
                ),
                width="100%"
            ),
            width="100%",
            on_submit=OnboardingDetailsState.cria_tarefa  
        ),
        spacing="2",
        width="100%",
        margin_top="1em"
    )

def adicionar_etapa() -> rx.Component:
    return rx.vstack(
        rx.heading("Adicionar nova etapa", size="4", weight="bold", color_scheme="gray"),
        rx.form(
            rx.hstack(
                rx.input(placeholder="Nova etapa", size="3", width="100%", name="nome"),
                rx.button(
                    rx.icon("plus", size=15, color="white"),
                    rx.text("Adicionar Etapa", size="3"),
                    color_scheme="blue",
                    variant="solid",
                    size="3",
                    radius="large",
                    class_name="cursor-pointer hover:brightness-90",
                ),
                width="100%",
            ),
            spacing="2",
            width="100%",
            on_submit=OnboardingDetailsState.cria_etapa,
        ),
        spacing="2",
        width="100%",
        padding = "1em",
        bg = rx.color("gray", 3),
        border_radius = "10px",
        border=f"2px dashed {rx.color('gray',6)}"
    )

def tarefa_item_provisorio(tarefa: Tarefa) -> rx.Component:
    return rx.cond(
        tarefa.nome != None,
        rx.text(tarefa.nome, size="3"),
        rx.text("Tarefa sem nome", size="3", color_scheme="gray")
    )

def card_etapa(etapa: Etapa) -> rx.Component:
    return rx.card(
        rx.hstack(
            icone_etapa(),
            card_headings(etapa.nome),
            align="center",
        ),
        rx.vstack(
            rx.text("Tarefas", size="4", weight="bold"),
            rx.cond(
                etapa.tarefas.length() == 0,
                rx.text("Nenhuma tarefa vinculada à etapa ainda. Crie a primeira"),
                rx.foreach(
                    etapa.tarefas,
                    lambda tarefa: item_tarefa(tarefa)
                )
            ),

            adicionar_tarefa(etapa.id),
            width="100%",
            spacing="2",
            padding="1em",
        ),
        width="100%",
        class_name="shadow-md"
    )

def bloco_etapas_onboarding(lista_etapas: List['Etapa'] = []) -> rx.Component:
    return rx.vstack(
            rx.hstack(
                rx.text("Etapas do Onboarding", size="5", weight="bold"),
                justify="between",
                width="100%"
            ),
            rx.vstack(
                rx.cond(
                    OnboardingDetailsState.loading_dados,
                    rx.hstack(
                        rx.spinner(),
                        width="100%",
                        padding='1em',
                        align="center"
                    ),
                    rx.cond(
                        OnboardingDetailsState.etapas.length() > 0,
                        rx.foreach(
                            OnboardingDetailsState.etapas,
                            card_etapa
                        ),
                        rx.text("Nenhuma etapa criada. Crie sua primeira etapa")
                    ),
                ),
                rx.divider(),
                adicionar_etapa(),
                width="100%",
                spacing="6",
                margin_bottom="2em"
            ),
            width="100%"
        )

def card_progresso_onboarding() -> rx.Component:
    return rx.card(
        rx.vstack(
            card_headings("Progresso do Onboarding"),
            rx.vstack(
                rx.progress(value=70, size="3", width="100%"),
                rx.hstack(
                    rx.text("70 % concluído", size='2'),
                    rx.text("7 de 10 tarefas concluídas", size='2'),
                    justify="between",
                    width="100%"
                ),
                align="center",
                width="100%"
            ),
            width="100%"
        ),
        width="100%",
        class_name="shadow-md"
    )

def participantes_item(nome: str, email: str, iniciais: str, empresa: str, cargo: str, papel: str) -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.avatar(fallback=iniciais),
            rx.vstack(
                rx.text(nome, size='3', weight='bold'),
                rx.text(email, size='2', color_scheme='gray'),
                spacing='1'
            ),
            spacing='3',
            align='center',
        ),
        rx.badge(
            papel,
            color_scheme='cyan',
            size='3'
        ),
        rx.icon("pencil", size=20, color=rx.color("gray", 7)),
        width='100%',
        align='center',
        justify='between',
        spacing='5',
        padding_x='1em',
    )

def card_participantes_onboarding() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                card_headings("Participantes"),
                rx.button(
                    rx.icon("plus"),
                    rx.text("Adicionar"),
                    color_scheme="blue",
                    variant="solid",
                    size="2",
                    radius="large",
                    class_name="cursor-pointer hover:brightness-90"
                ),
                justify="between",
                width="100%"
            ),
            rx.vstack(
                participantes_item("Thiago Silva", "thiago.silva@example.com", "TS", "Gerente", "Empresa X", "Ponto focal"),
                width="100%",
            ),
            width="100%"
        ),
        width="100%",
        class_name="shadow-md"
    )

def icone_proxima_tarefa() -> rx.Component:
    return rx.box(
        rx.icon("flag", size=20, color="white"),
        width="40px",
        height="40px",
        border_radius="25px",
        bg=rx.color("blue", 7),
        class_name="flex items-center justify-center"
    )

def caixa_proxima_tarefa() -> rx.Component:
    return rx.card(
        rx.hstack(
            icone_proxima_tarefa(),
            rx.vstack(
                card_headings("Próxima Tarefa"),
                rx.vstack(
                    rx.text("Configurar conta do cliente", size='3', weight='medium'),
                    rx.text("Data de vencimento: 25/11/2025", size='2', color_scheme='gray'),
                    rx.text("Responsável: Ana Pereira", size='2', color_scheme='gray'),
                    spacing='2',
                    width="100%"
                ),
                width="100%"
            ),
        ),
        width="100%",
        bg=rx.color("blue", 9),
        class_name="shadow-md"
    )

def card_gamificacao() -> rx.Component:
    return rx.card(
        rx.vstack(
            card_headings("Gamificação"),
            card_description("Conclua tarefas e ganhe pontos para desbloquear recompensas exclusivas!"),
            rx.hstack(
                rx.text("Sua pontuação atual:", size='2', weight='medium'),
                rx.text("1200 Pontos", size='2', weight='bold'),
            ),
            rx.hstack(
                rx.link("Ver recompensas disponíveis", href="#", size='2'),
                justify="end",
                width="100%"
            ),
            width="100%",
            spacing="3",
        ),
        width="100%",
        class_name="shadow-md"
    )


def card_consultor() -> rx.Component:
    pass

def reuniao_item(descricao: str, titulo:str, data:str, hora:str) -> rx.Component:
    return rx.vstack(
        rx.text(descricao, size='2', weight='medium', color_scheme='gray'),
        rx.text(titulo, size='2', weight='bold'),
        rx.text(f"{data} às {hora}", size='2', color_scheme='gray'),
        spacing='1',
        width="100%",
        bg=rx.color("gray", 3),
        padding="1em",
        border_radius="10px"
    )

def card_reunioes() -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.hstack(
                card_headings("Reuniões"),
                rx.button(
                    rx.icon("plus"),
                    rx.text("Agendar"),
                    color_scheme="blue",
                    variant="solid",
                    size="2",
                    radius="large",
                    class_name="cursor-pointer hover:brightness-90"
                ),
                justify="between",
                width="100%"
            ),
            rx.vstack(
                reuniao_item("Última reunião", "Alinhamento inicial do projeto", "22/10/2025", "10:00"),
                reuniao_item("Próxima reunião", "Verificação do progresso", "29/10/2025", "14:00"),
                spacing="2",
                width="100%",
            ),
            rx.hstack(
                rx.link("Ver todas as reuniões", href="#", size="2", color_scheme='blue'),
                justify="end",
                width="100%"
            ),
            spacing="3",
            width="100%",
            ),  
        width="100%",
        class_name="shadow-md"
    )

def header_onboarding_details() -> rx.Component:
    return rx.box(
        rx.text("Detalhes do Onboarding", size="6", weight="bold", align="center"),
        align="center",
        justify="center",
        width="100%",
        padding="1em",
        margin_top="1em",
        border_radius="10px",
        bg=rx.color("blue"),
        margin_y="2em",
        class_name="shadow-md"
    )

def bloco_esquedo() -> rx.Component:
    return rx.vstack(
            card_detalhes_onboarding(
                "Onboarding de Cliente X",
                "Este é o onboarding do Cliente X, que inclui todas as etapas necessárias para garantir uma integração bem-sucedida.",
                "22/10/2025",
                "22/12/2025"
            ),
            card_participantes_onboarding(),
            card_reunioes(),
            card_gamificacao(),
            spacing="6",
            width="100%"
        )

def bloco_direito() -> rx.Component:
    return rx.vstack(
            rx.vstack(
                breadcrumbs(["Home", "Onboardings", "Detalhes do Onboarding"]),
                rx.heading("Plano de onboarding", size="6", weight="bold"),
                rx.text("Seja bem-vindo ao seu plano de onboarding! Aqui você encontrará todas as etapas necessárias para garantir uma integração suave e bem-sucedida.", size='2', color_scheme='gray'),
                width="100%",
                spacing="1",
                margin_top="1em"
            ),
            caixa_proxima_tarefa(),
            card_progresso_onboarding(),
            bloco_etapas_onboarding(OnboardingDetailsState.etapas),
            spacing="6",
            width="100%",
            padding_left="1em"
        )

def onboarding_screen() -> rx.Component:
    return rx.vstack(
        header_onboarding_details(),
        rx.grid(
            bloco_esquedo(),
            bloco_direito(),
            width="100%",
            columns="1fr 3fr",
            spacing="4",
        ),
        margin_x='1em',
        width="80%",
        align="center",
    )


def detalhes_onboarding():
    return base_blank_page(
        onboarding_screen()
    )