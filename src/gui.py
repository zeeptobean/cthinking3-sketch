from typing import cast
import flet as ft
from translate import run_translate

def toggle_theme(e: ft.Event[ft.IconButton]) -> None:
    if(e.page.theme_mode == ft.ThemeMode.LIGHT):
        e.page.theme_mode = ft.ThemeMode.DARK
        e.control.icon = ft.Icons.DARK_MODE_ROUNDED
    else:
        e.page.theme_mode = ft.ThemeMode.LIGHT
        e.control.icon = ft.Icons.LIGHT_MODE_ROUNDED
    e.page.update()

class JobSeekTab:
    def __init__(self):
        self.chip_list: list[ft.Chip] = []
        self.chip_string: list[str] = []
        self.text_field = ft.CupertinoTextField(
            placeholder_text="Enter skill or knowledge",
            autofocus=True,
            on_submit=self.add_chip_textfield
        )
        self.scroll_container = ft.Container(
            content=ft.ListView(
                controls=[
                    ft.Row(
                        controls=cast(list[ft.Control], self.chip_list),
                        spacing=8.0,
                        run_spacing=8.0,
                        wrap=True,
                    )
                ],
                # scroll=ft.ScrollMode.AUTO,
            ),
            padding=4,
            border_radius=8,
            width=700,
            height=400,
            expand=1,
        )

        self.output_container = ft.Container(
            content=ft.Container(),
            padding=4,
            expand=4
        )

        self.widget = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Find your jobs",
                    size=32,
                    expand=1
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=8.0,
                    controls=[
                        self.text_field,
                        ft.CupertinoTintedButton(
                            icon=ft.Icons.ADD,
                            content=ft.Text("Add"),
                            on_click=self.add_chip_button,
                        ),
                    ],
                    expand=1
                ),
                ft.Container(height=10),
                ft.CupertinoFilledButton(
                    # bgcolor=ft.Colors.PRIMARY,
                    # color=ft.Colors.ON_PRIMARY,
                    content=ft.Text("Run"),
                    on_click=self.run_func,
                    expand=1
                ),
                self.scroll_container,
                self.output_container
            ]
        )
    def run_func(self, e: ft.Event[ft.CupertinoButton]) -> None:
        print(f"chip_string: {self.chip_string}")
        self.output_container.content = ft.CupertinoActivityIndicator(radius=16)
        self.output_container.update()
        e.control.disabled = True
        e.control.update()

        async def process():
            result = await run_translate(self.chip_string)
            self.output_container.content = ft.Text(f"Result: {result}")
            self.output_container.update()
            e.control.disabled = False
            e.control.update()

        e.page.run_task(process)

    def remove_chip(self, e: ft.Event[ft.Chip]) -> None:
        label_text: str = e.control.label.value
        self.chip_string.remove(label_text)
        self.chip_list.remove(e.control)
        self.scroll_container.content.controls[0].controls = self.chip_list
        self.scroll_container.update()

    async def add_chip_textfield(self, e: ft.Event[ft.TextField]) -> None:
        input_string = e.control.value.strip()
        e.control.value = ""
        if input_string and input_string not in self.chip_string:
            self.add_chip(input_string)
        e.control.update()
        await e.control.focus()

    async def add_chip_button(self, e: ft.Event[ft.CupertinoButton]) -> None:
        input_string = self.text_field.value.strip()
        self.text_field.value = ""
        if input_string and input_string not in self.chip_string:
            self.add_chip(input_string)
        self.text_field.update()
        await self.text_field.focus()

    def add_chip(self, input_string: str) -> None:
        self.chip_string.append(input_string)
        self.chip_list.append(
            ft.Chip(
                label=ft.Text(input_string),
                on_delete=self.remove_chip,
            )
        )
        self.scroll_container.content.controls[0].controls = self.chip_list
        self.scroll_container.update()

def abc_content() -> ft.Container:
    return ft.Container(
        content=ft.Text("ABC content"),
    )

def main(page: ft.Page) -> None:
    page.title = "careersearch"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT
    page.appbar = ft.CupertinoAppBar(
        title=ft.Text("careersearch"),
        trailing=ft.IconButton(
            icon=ft.Icons.LIGHT_MODE_ROUNDED,
            on_click=lambda e: toggle_theme(e),
        ),
    )

    page.navigation_bar = ft.CupertinoNavigationBar(
        on_change=lambda e: change_tab(e),
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.CASES_OUTLINED,
                selected_icon=ft.Icons.CASES_ROUNDED,
                label="Job seek",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COMMUTE_OUTLINED,
                selected_icon=ft.Icons.COMMUTE_ROUNDED,
                label="ABC",
            ),
        ],
    )

    jokseek_tab = JobSeekTab()

    content_container = ft.Container(
        content=jokseek_tab.widget,
        expand=True,
    )

    def change_tab(e: ft.Event[ft.CupertinoNavigationBar]) -> None:
        print("Selected tab:", e.control.selected_index)
        match e.control.selected_index:
            case 0:
                content_container.content = jokseek_tab.widget
            case 1:
                content_container.content = abc_content()
        page.update()
        

    page.add(
        ft.SafeArea(
            content=content_container
        )
    )


ft.run(main)