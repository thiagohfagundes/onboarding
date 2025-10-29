"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

from app.pages.base_page import base_page
from app.pages.onboardings_details import container_onboarding_details
from app.pages.templates_list import templates_page, TemplateListViewState

from app.pages.new_onboarding_list import onboardings_page, OnboardingListState


def index():
    return base_page(
        ""
    )

def onboardings():
    return container_onboarding_details()

def onboardings_list():
    return base_page(
        onboardings_page()
    )

def detalhes_tarefa():
    return base_page(
        rx.text("Detalhes da tarefa")
    )

def detalhes_onboarding():
    return base_page(
        rx.text("Detalhes do onboarding")
    )

app = rx.App()
app.add_page(index)

#ListViews
app.add_page(onboardings_list, route="/onboardings", on_load=OnboardingListState.lista_processos)
app.add_page(templates_page, route="/templates", on_load=TemplateListViewState.lista_templates)

#DetailViews
app.add_page(detalhes_onboarding, route='/onboardings/[id]')
app.add_page(detalhes_tarefa, route='/tarefa/[id]')
app.add_page(detalhes_onboarding, route='/templates/[id]')
