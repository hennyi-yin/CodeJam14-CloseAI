import flet as ft
import time

from src.ui.widgets import ChatItem

user_config = {
    "dark_mode": True
}

def get_bot_response(user_message):
# Chatbot responds
    time.sleep(3)
    if user_message.lower() == "hello":
        bot_reply = "**Hi** there! How can I help you?"
    elif user_message.lower() == "bye":
        bot_reply = "**Goodbye!** Have a great day!"
    else:
        bot_reply = "I'm here to **chat**. Ask me anything!"
        
    return bot_reply

def main(page: ft.Page):
    page.title = "Chatbot"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window.min_height = 600
    page.window.min_width = 400
    
    app_body = ft.Column(expand=True)
    
    toggle_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE if user_config.get("dark_mode") else ft.icons.DARK_MODE
    )
#    debug_button = ft.IconButton(
#        icon=ft.icons.WARNING
#    )
    app_bar = ft.AppBar(
        title=ft.Text("Chatbot"),
        center_title=True,
        actions=[
            toggle_button,
#            debug_button
        ],
    )
    
    chat_box = ft.ListView(expand=8)
    
    user_input = ft.TextField(
        hint_text="Type your message", 
        autofocus=True, 
        expand=True, 
        shift_enter=True
    )
    send_button = ft.IconButton(
        icon=ft.icons.ARROW_UPWARD, 
        width=40, 
        disabled=True
    )
    input_area = ft.Row(
        controls=[
            user_input,
            send_button
        ],
        alignment=ft.alignment.center,
        vertical_alignment=ft.CrossAxisAlignment.END,
        expand=1
    )
    
#    def change_debug(e):
#        page.show_semantics_debugger = not page.show_semantics_debugger
#        page.update()
#    
#    debug_button.on_click = change_debug
            
    def toggle_mode(e):
        user_config["dark_mode"] = not user_config["dark_mode"]
        if user_config["dark_mode"]:
            toggle_button.icon = ft.icons.LIGHT_MODE
            page.theme_mode = "dark"
        else:
            toggle_button.icon = ft.icons.DARK_MODE
            page.theme_mode = "light"
        page.update()
        
    toggle_button.on_click = toggle_mode
    
    def check_content(e):
        if not user_input.value:
            send_button.disabled = True
        else:
            send_button.disabled = False
            
        page.update()
        
    def on_send(e):
        user_message = user_input.value
        chat_box.controls.append(
            ChatItem("user", user_message)
        )
        user_input.value = ""
        user_input.disabled = True
        send_button.disabled = True
        page.update()
        
        bot_reply = get_bot_response(user_message)
        
        chat_box.controls.append(
            ChatItem("bot", bot_reply)
        )
        user_input.disabled = False
        page.update()
    
    user_input.on_change = check_content
    user_input.on_submit = on_send
    send_button.on_click = on_send
    
    app_body.controls += [chat_box, input_area]
    
    page.appbar = app_bar
    page.add(app_body)
#ft.Rive(
#        src="vehicles.riv",
#        placeholder=ft.ProgressBar(),
#        width=300,
#        height=200,
#    ),ft.Lottie(
#        src="test-white.json",
#        repeat=True,
#        animate=True,
#        height=300,
#        width=300
#    )
ft.app(target=main)
