import asyncio
from typing import Tuple, cast
import flet as ft
from data_loader import data_loader, Job
from translate import run_translate, run_translate_job
from job_matcher import find_suitable_jobs, merge_job_list
from roadmap_generator import generate_learning_roadmap, format_roadmap_for_display, Roadmap

def toggle_theme(e: ft.Event[ft.IconButton]) -> None:
    if(e.page.theme_mode == ft.ThemeMode.LIGHT):
        e.page.theme_mode = ft.ThemeMode.DARK
        e.control.icon = ft.Icons.DARK_MODE_ROUNDED
    else:
        e.page.theme_mode = ft.ThemeMode.LIGHT
        e.control.icon = ft.Icons.LIGHT_MODE_ROUNDED
    e.page.update()

class JobDetailTab:
    def __init__(self, job: Job, user_knowledge: list[str]):
        self.job = job
        self.user_knowledge = user_knowledge
        self.roadmap: Roadmap = generate_learning_roadmap(self.job, self.user_knowledge)
        self.widget = ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            controls=[
                ft.Text(self.job.name, size=32),
                ft.Text(self.job.description, size=20),
                ft.Container(height=10),
                ft.Text("Your Learning Roadmap:", size=24),
                ft.Text(format_roadmap_for_display(self.roadmap), size=16),
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )

class JobSeekTab:
    def __init__(self):
        self.chip_list: list[ft.Chip] = []
        self.chip_string: list[str] = []
        self.job_list: list[Tuple[float, Job]] = []
        self.left_textfield = ft.CupertinoTextField(
            placeholder_text="Enter skill or knowledge",
            autofocus=True,
            on_submit=self.add_chip_textfield
        )
        self.right_textfield = ft.CupertinoTextField(
            placeholder_text="Enter job description",
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

        self.left_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Skills and knowledges", size=20),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8.0,
                        controls=[
                            self.left_textfield,
                            ft.CupertinoTintedButton(
                                icon=ft.Icons.ADD,
                                content=ft.Text("Add"),
                                on_click=self.add_chip_button,
                            ),
                        ],
                        expand=1
                    )
                ]
            ),
            expand=1,
            padding=4,
        )

        self.right_container = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Job description", size=20),
                    ft.CupertinoTextField(
                        placeholder_text="Enter job description",
                        min_lines=5,
                        expand=True,
                    ),
                ]
            ),
            expand=1,
            padding=4,
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
                        self.left_container,
                        self.right_container
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
    
    async def push_navigation(self, e: ft.Event[ft.CupertinoListTile], job: Job, user_knowledge: list[str]) -> None:
        print(f"Navigating to job detail: {job.name}")
        job_detail_view = JobDetailTab(job, user_knowledge)

        e.page.views.append(
            ft.View(
                route="/job-detail",
                controls=[
                    ft.CupertinoAppBar(
                        title=ft.Text("careersearch"),
                        trailing=ft.IconButton(
                            icon=ft.Icons.LIGHT_MODE_ROUNDED,
                            on_click=lambda e: toggle_theme(e),
                        ),
                    ),
                    job_detail_view.widget
                ],
            )
        )
        e.page.update()

    def draw_job_list(self) -> ft.ListView:
        print(f"Drawing job list...{self.job_list}")
        job_list_views: list[ft.CupertinoListTile] = []
        for score, job in self.job_list:
            job_list_views.append(
                ft.CupertinoListTile(
                    title=ft.Text(job.name),
                    subtitle=ft.Text(f"Matched {score}%", size=16),
                    trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
                    on_click=lambda e, current_job=job: asyncio.create_task(self.push_navigation(e, current_job, self.chip_string))
                ),
            )

        return ft.ListView(
            controls=cast(list[ft.Control], job_list_views)
        )
    
    def run_func(self, e: ft.Event[ft.CupertinoButton]) -> None:
        print(f"chip_string: {self.chip_string}")
        self.output_container.content = ft.CupertinoActivityIndicator(radius=16)
        self.output_container.update()
        e.control.disabled = True
        e.control.update()

        async def process():
            """
            temp = await run_translate(self.chip_string)
            temp2 = await run_translate_job(self.right_textfield.value)
            if(temp is None or temp2 is None):
                self.output_container.content = ft.Text("Error in translation")
            else:
                [user_skill, user_knowledge] = temp
                joblist1 = await find_suitable_jobs(user_skill, user_knowledge)
                joblist2 = temp2
                self.job_list = merge_job_list(joblist1, joblist2)
                self.output_container.content = self.draw_job_list()
            """
            ## debug
            self.job_list = [
                [95.0, data_loader.job_map.get("cloud DevOps engineer")],
                [90.0, data_loader.job_map.get("cloud architect")],
                [90.0, data_loader.job_map.get("cloud software developer")],
            ]
            self.output_container.content = self.draw_job_list()

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
        input_string = self.left_textfield.value.strip()
        self.left_textfield.value = ""
        if input_string and input_string not in self.chip_string:
            self.add_chip(input_string)
        self.left_textfield.update()
        await self.left_textfield.focus()

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

    appbar = ft.CupertinoAppBar(
        title=ft.Text("careersearch"),
        trailing=ft.IconButton(
            icon=ft.Icons.LIGHT_MODE_ROUNDED,
            on_click=lambda e: toggle_theme(e),
        ),
    )
    page.appbar = appbar

    jobseek_tab = JobSeekTab()

    content_container = ft.Container(
        content=jobseek_tab.widget,
        expand=True,
    )

    def route_change():
        page.views.clear()
        page.views.append(
            ft.View(
                route="/",
                controls=[
                    appbar,
                    content_container
                ],
            )
        )
        page.update()
    
    async def view_pop(e):
        if e.view is not None:
            # print("View pop:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()


if __name__ == "__main__":
    ft.run(main)
    # ft.app(target=main, view=ft.AppView.FLET_APP_WEB, host="0.0.0.0")
    # app = ft.app(main, export_asgi_app=True)