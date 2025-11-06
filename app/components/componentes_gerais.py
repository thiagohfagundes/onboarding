import reflex as rx

def heading_pagina(titulo: str, subtitulo: str):
    return rx.vstack(
        rx.heading(titulo),
        rx.text(subtitulo, color_scheme='gray'),
        spacing='1'
    )

def card_headings(titulo: str):
    return rx.heading(titulo, size='4')

def card_description(subtitulo: str):
    return rx.text(subtitulo, size='2', color_scheme='gray')

def forms_label(texto: str):
    return rx.text(texto, class_name="text-sm font-medium leading-none")