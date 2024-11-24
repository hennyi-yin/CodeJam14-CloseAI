import flet as ft

mks = ft.MarkdownStyleSheet(
    p_text_style=ft.TextStyle(size=18)
)

class ChatItem(ft.Row):
    def __init__(self, speaker_type, message):
        super().__init__()
        if speaker_type == "user":
            self.controls = [
                ft.Container(
                    content=ft.Markdown(message, selectable=True, md_style_sheet=mks), 
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    alignment=ft.Alignment(x=1, y=0),
                    padding=ft.Padding(top=5, bottom=5, left=10, right=10),
                    border_radius=12,
                    expand_loose=True
                ),
                ft.CircleAvatar(
                    content=ft.Image(
                        src="hatsune-miku-dance.gif"
                    ),
                    bgcolor=ft.colors.TRANSPARENT
                )
            ]
            self.alignment = ft.MainAxisAlignment.END
            
        else:
            self.controls = [
                ft.CircleAvatar(
                    content=ft.Image(
                        src="matador.png"
                    ),
                    bgcolor=ft.colors.TRANSPARENT
                ),
                ft.Container(
                    content=ft.Markdown(message, selectable=True, md_style_sheet=mks), 
#                    bgcolor=ft.colors.SURFACE_VARIANT,
                    padding=ft.Padding(top=5, bottom=5, left=10, right=10),
                    border_radius=10,
                    expand_loose=True
                )
            ]