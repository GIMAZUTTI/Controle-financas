from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import Rectangle, Color

# Definindo a cor de fundo da janela
Window.clearcolor = (0.95, 0.95, 0.95, 1)  # Um cinza claro

class Transacao:
    def __init__(self, valor):
        self.valor = valor

class Receita(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

class Despesa(Transacao):
    def __init__(self, valor):
        super().__init__(valor)

class ControleFinancas:
    def __init__(self):
        self.transacoes = []

    def adicionar_receita(self, valor):
        receita = Receita(valor)
        self.transacoes.append(receita)

    def adicionar_despesa(self, valor):
        despesa = Despesa(-valor)  # Despesas são negativas para o saldo
        self.transacoes.append(despesa)

    def calcular_saldo(self):
        saldo = sum(transacao.valor for transacao in self.transacoes)
        return saldo

class FinancasApp(App):
    def build(self):
        self.controle_financas = ControleFinancas()

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Adicionando cifrões no fundo da tela
        with layout.canvas.before:
            Color(0.8, 0.8, 0.8, 1)  # Cor de fundo cinza claro
            self.rect = Rectangle(size=Window.size, pos=(0, 0))

        # Cifrões no fundo (agora centralizados)
        for i in range(0, Window.height, 120):
            for j in range(0, Window.width, 120):
                layout.add_widget(Label(text='$', font_size=40, color=(0, 0.5, 0, 0.2), size_hint=(None, None), size=(50, 50), pos=(j, i)))

        # Título da aplicação (cor verde)
        title_label = Label(text='Controle de Finanças Pessoais', font_size='24sp', bold=True, color=(0, 0.8, 0, 1), size_hint_y=None, height=40)
        layout.add_widget(title_label)

        self.valor_input = TextInput(hint_text='Valor', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.valor_input)

        # Botão de Adicionar Receita
        btn_receita = Button(text='Adicionar Receita', background_color=(0.2, 0.7, 0.2, 1), size_hint_y=None, height=50, font_name='Roboto')
        btn_receita.bind(on_press=self.adicionar_receita)
        layout.add_widget(btn_receita)

        # Botão de Adicionar Despesa
        btn_despesa = Button(text='Adicionar Despesa', background_color=(0.7, 0.2, 0.2, 1), size_hint_y=None, height=50, font_name='Roboto')
        btn_despesa.bind(on_press=self.adicionar_despesa)
        layout.add_widget(btn_despesa)

        self.saldo_label = Label(text='Saldo: R$ 0.00', font_size='20sp', color=(0, 0, 0, 1), size_hint_y=None, height=40)
        layout.add_widget(self.saldo_label)

        # Botão de Fechar Aplicação
        btn_fechar = Button(text='Fechar Aplicação', background_color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=50, font_name='Roboto')
        btn_fechar.bind(on_press=self.confirmar_fechar)
        layout.add_widget(btn_fechar)

        return layout

    def adicionar_receita(self, instance):
        try:
            valor = float(self.valor_input.text)
            self.controle_financas.adicionar_receita(valor)
            self.atualizar_saldo()
        except ValueError:
            self.exibir_popup("Erro", "Por favor, insira um valor válido.")

    def adicionar_despesa(self, instance):
        try:
            valor = float(self.valor_input.text)
            self.controle_financas.adicionar_despesa(valor)
            self.atualizar_saldo()
        except ValueError:
            self.exibir_popup("Erro", "Por favor, insira um valor válido.")

    def atualizar_saldo(self):
        saldo = self.controle_financas.calcular_saldo()
        self.saldo_label.text = f'Saldo: R$ {saldo:.2f}'
        self.valor_input.text = ''

    def confirmar_fechar(self, instance):
        # Criar um layout para o popup de confirmação de fechamento
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text='Você realmente deseja fechar a aplicação?', size_hint_y=None, height=40)
        popup_layout.add_widget(popup_label)

        # Criar botão "Sim"
        btn_sim = Button(text='Sim', background_color=(0.2, 0.7, 0.2, 1), size_hint_y=None, height=50)
        btn_sim.bind(on_press=self.fechar_aplicacao)
        popup_layout.add_widget(btn_sim)

        # Criar botão "Não"
        btn_nao = Button(text='Não', background_color=(0.7, 0.2, 0.2, 1), size_hint_y=None, height=50)
        btn_nao.bind(on_press=self.fechar_popup)
        popup_layout.add_widget(btn_nao)

        # Exibir popup
        self.popup = Popup(title='Confirmar Fechamento', content=popup_layout, size_hint=(None, None), size=(400, 200))
        self.popup.open()

    def fechar_aplicacao(self, instance):
        # Fechar a aplicação
        App.get_running_app().stop()

    def fechar_popup(self, instance):
        # Fechar o popup e evitar o fechamento da aplicação
        self.popup.dismiss()

    def exibir_popup(self, titulo, mensagem):
        # Exibe o popup de erro
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=mensagem, size_hint_y=None, height=40)
        popup_layout.add_widget(popup_label)

        # Alterado para fechar apenas o popup de erro
        btn_fechar = Button(text='Fechar', background_color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=50)
        btn_fechar.bind(on_press=self.fechar_popup_erro)
        popup_layout.add_widget(btn_fechar)

        self.popup_erro = Popup(title=titulo, content=popup_layout, size_hint=(None, None), size=(400, 200))
        self.popup_erro.open()

    def fechar_popup_erro(self, instance):
        # Fechar apenas o popup de erro
        self.popup_erro.dismiss()

if __name__ == '__main__':
    FinancasApp().run()
