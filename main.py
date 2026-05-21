import flet as ft
from MANAGER_GYM_DIARY import (
    load_routine,
    save_routine,
    IDIOMAS,
    date_update
)

def main(page: ft.Page):
    page.title = "GYM DIARY"
    page.window.maximized = True
    page.scroll = "auto"

    page.theme_mode = ft.ThemeMode.DARK

    page.fonts = {
        "TechFont": "https://fonts.gstatic.com/s/sharetechmono/v15/J7aRng14dB386O07F7ZRE6qfvA.ttf",
        "ModernFont": "https://fonts.gstatic.com/s/poppins/v20/pxiByp8kv8JHgFVrLEj6Z1xlFQ.ttf"
    }

    # Estado do idioma atual (padrão: inglês 'en')
    current_lang = "en"

    routine_now = load_routine()
    dropdowns_week = {}
    ss_exe = {}
    columns_dict = {}
    day_titles_components = {} # Guarda os componentes de texto dos dias para atualizar o idioma
    
    grade_excel = ft.Row(spacing=15, vertical_alignment=ft.CrossAxisAlignment.START)

    def toggle_theme(e):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            theme_button.icon = ft.Icons.DARK_MODE
            theme_button.tooltip = "Mudar para Modo Escuro"
        else:
            page.theme_mode = ft.ThemeMode.DARK
            theme_button.icon = ft.Icons.LIGHT_MODE
            theme_button.tooltip = "Mudar para Modo Claro"
        page.update()

    theme_button = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Mudar para Modo Claro",
        on_click=toggle_theme
    )

    # Função responsável por alternar o idioma dos títulos
    def toggle_language(e):
        nonlocal current_lang
        if current_lang == "en":
            current_lang = "pt"
            language_button.icon = ft.Icons.LANGUAGE
            language_button.tooltip = "Change to English / Mudar para Inglês"
        else:
            current_lang = "en"
            language_button.icon = ft.Icons.TRANSLATE
            language_button.tooltip = "Mudar para Português / Switch to Portuguese"

        # Atualiza o texto visual de cada dia na tela usando nosso mapeamento de IDIOMAS
        for day_en, text_component in day_titles_components.items():
            text_component.value = IDIOMAS[current_lang][day_en]
        
        page.update()

    # Utilizando o IconButton clássico (Imune a bugs de argumentos de texto ou inicializadores inválidos)
    language_button = ft.IconButton(
        icon=ft.Icons.TRANSLATE,
        tooltip="Mudar para Português / Switch to Portuguese",
        on_click=toggle_language
    )

    def add_exercise_field(e):
        day_key = e.control.data
        create_and_append_field(day_key, value="")
        page.update()

    def create_and_append_field(day_key, value="", date_str=""):
        new_cel = ft.TextField(
            value=value,
            text_size=15,
            content_padding=10,
            text_align=ft.TextAlign.CENTER
        )
        
        date_text = ft.Text(
            value=date_str if date_str else "",
            size=13,
            color=ft.Colors.WHITE,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER
        )
        
        exercise_block = ft.Column(
            controls=[new_cel, date_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2
        )
        
        ss_exe[day_key].append(new_cel)
        columns_dict[day_key].controls.append(exercise_block)

    def remove_exercise_field(e):
        day_key = e.control.data
        if len(ss_exe[day_key]) > 0:
            ss_exe[day_key].pop() 
            columns_dict[day_key].controls.pop() 
            page.update()
    
    # Construção da Interface baseada nas chaves padrão em inglês
    for day_en in IDIOMAS["en"].keys():
        ss_exe[day_en] = []

        # Começa exibindo o valor padrão definido em current_lang ('en')
        day_text = ft.Text(
            value=IDIOMAS[current_lang][day_en],
            size=18,
            font_family="ModernFont",
            weight=ft.FontWeight.W_800,
            color=ft.Colors.BLUE_500,
            text_align=ft.TextAlign.CENTER
        )
        
        # Guardamos a referência do componente de texto linkado com a chave dele
        day_titles_components[day_en] = day_text

        container_topo = ft.Container(
            content=day_text,
            alignment=ft.Alignment(0, 0),
            padding=ft.Padding(left=0, right=0, top=5, bottom=5)
        )

        day_data = routine_now.get(day_en, {"block": "", "exercises": []})
        if isinstance(day_data, str):
            day_data = {"block": day_data, "exercises": []}

        input_macro = ft.TextField(
            value=day_data.get("block", ""),
            capitalization=ft.TextCapitalization.CHARACTERS,
            text_align=ft.TextAlign.CENTER,
            content_padding=12,
            text_style=ft.TextStyle(
                font_family="TechFont",
                size=15,
                weight=ft.FontWeight.BOLD
            )
        )

        dropdowns_week[day_en] = input_macro

        btn_add = ft.IconButton(
            icon=ft.Icons.ADD_BOX_ROUNDED,
            icon_color=ft.Colors.GREEN_400,
            icon_size=20,
            tooltip="Adicionar Exercício",
            data=day_en,
            on_click=add_exercise_field
        )

        btn_remove = ft.IconButton(
            icon=ft.Icons.INDETERMINATE_CHECK_BOX_ROUNDED,
            icon_color=ft.Colors.RED_400,
            icon_size=20,
            tooltip="Remover Último Exercício",
            data=day_en,
            on_click=remove_exercise_field
        )

        row_botoes = ft.Row(
            controls=[btn_add, btn_remove],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=0
        )

        column_day = ft.Column(
            controls=[container_topo, input_macro, row_botoes, ft.Divider(height=5)],
            spacing=5,
            expand=True
        )
        
        columns_dict[day_en] = column_day

        saved_exercises = day_data.get("exercises", [])
        if saved_exercises:
            for exe_info in saved_exercises:
                if isinstance(exe_info, dict):
                    create_and_append_field(
                        day_en, 
                        value=exe_info.get("name", ""), 
                        date_str=exe_info.get("saved_at", "")
                    )
                else:
                    create_and_append_field(day_en, value=exe_info, date_str="")
        else:
            create_and_append_field(day_en, value="", date_str="")

        grade_excel.controls.append(column_day)

    def save_routine_click(e):
        new_routine_screen = {}
        actual_date = date_update()
        
        for day_key in IDIOMAS["en"].keys():
            list_exe_type = []
            
            exercicios_visuais = [
                ctrl for ctrl in columns_dict[day_key].controls 
                if isinstance(ctrl, ft.Column)
            ]
            
            for i, field in enumerate(ss_exe[day_key]):
                if field.value.strip() != "":
                    list_exe_type.append({
                        "name": field.value,
                        "saved_at": actual_date
                    })

                    if i < len(exercicios_visuais):
                        exe_block = exercicios_visuais[i]
                        if len(exe_block.controls) > 1:
                            date_text = exe_block.controls[1]
                            date_text.value = actual_date
                            
            new_routine_screen[day_key] = {
                "block": dropdowns_week[day_key].value,
                "exercises": list_exe_type
            }
            
        save_routine(new_routine_screen)

        msg_success = "Rotina atualizada!" if current_lang == "en" else "Rotina atualizada com sucesso!"
        page.snack_bar = ft.SnackBar(ft.Text(msg_success))
        page.snack_bar.open = True
        page.update()

    page.floating_action_button = ft.FloatingActionButton(
        content=ft.Text("SAVE", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        on_click=save_routine_click,
        bgcolor=ft.Colors.GREEN_700,
        shape=ft.RoundedRectangleBorder(radius=8)
    )

    header_buttons = ft.Row(
        controls=[language_button, theme_button],
        spacing=10,
        vertical_alignment=ft.CrossAxisAlignment.CENTER
    )

    header = ft.Row(
        controls=[
            ft.Text("GYM DIARY — Weekly Training Plan", size=22, weight=ft.FontWeight.BOLD),
            header_buttons
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    page.add(
        header,
        ft.Container(height=10),
        ft.Container(
            content=grade_excel,
            padding=ft.Padding(left=20, right=20, top=10, bottom=10),
            expand=True
        )
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)