import reflex as rx
from app.pages.base_page import base_auth_page
from app.components.auth import sign_in_card, sign_up_card

def sign_in():
    return base_auth_page(
        sign_in_card(),
    )

def sign_up():
    return base_auth_page(
        sign_up_card(),
    )
