import reflex as rx

class StateUsuario(rx.State):
    usuario_nome: str = "Thiago Fagundes"
    usuario_email: str = "thiago.fagundes@superlogica.com"
    usuario_iniciais: str = "TF"
    usuario_empresa: str = "Superlógica"

from app.supabase.supabase_client import supabase


class AuthState(rx.State):
    """Gerencia autenticação de usuários com Supabase."""
    
    # Guarda sessão e email logado
    session: dict | None = None
    user_email: str | None = None

    @rx.var
    def in_session(self) -> bool:
        """Verifica se há uma sessão válida."""
        return self.session is not None

    # --- SIGN UP ---
    @rx.event
    def sign_up(self, form_data: dict):
        """Cria um novo usuário no Supabase Auth."""
        email = form_data.get("email")
        password = form_data.get("password")

        try:
            response = supabase.auth.sign_up({"email": email, "password": password})
            if response.user:
                yield rx.toast("Conta criada! Verifique seu e-mail.", duration=4000)
                return rx.redirect("/sign-in")
            else:
                yield rx.toast("Erro ao criar conta. Tente novamente.", duration=4000)
        except Exception as e:
            yield rx.toast(f"Erro: {str(e)}", duration=4000)

    # --- SIGN IN ---
    @rx.event
    def sign_in(self, form_data: dict):
        """Autentica o usuário e armazena a sessão."""
        email = form_data.get("email")
        password = form_data.get("password")

        try:
            response = supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if response.session:
                self.session = response.session.model_dump()
                self.user_email = email
                yield rx.toast("Login realizado com sucesso!", duration=3000)
                return rx.redirect("/")
            else:
                yield rx.toast("Credenciais inválidas.", duration=3000)
        except Exception as e:
            yield rx.toast(f"Erro: {str(e)}", duration=4000)

    # --- SIGN OUT ---
    @rx.event
    def sign_out(self):
        """Sai do Supabase e limpa o estado local."""
        try:
            supabase.auth.sign_out()
        except Exception:
            pass
        self.session = None
        self.user_email = None
        return rx.redirect("/sign-in")

    # --- CHECK SESSION ---
    @rx.event
    def check_session(self):
        """Valida a sessão atual (pode ser chamada em páginas protegidas)."""
        if not self.session:
            return rx.redirect("/sign-in")
        
    @rx.var
    def user_id(self) -> str | None:
        if self.session and "user" in self.session:
            return self.session["user"]["id"]
        return None