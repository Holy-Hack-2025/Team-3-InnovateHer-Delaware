import shiny
from shiny import ui, App, render, reactive
import random

# Dummy data voor wegen
roads = [
    {"id": "1", "name": "E40 (Brussels - Liège)", "type": "Highway"},
    {"id": "2", "name": "N9 (Ghent - Ostend)", "type": "Main Road"},
    {"id": "3", "name": "Dorpsstraat, Leuven", "type": "Small Road"}
]

# Schadecategorieën en juiste afbeeldingen
damage_types = {
    "Potholes": "put.jpg",
    "Road Subsidence": "verzakking.jpg",
    "Cracks": "scheur.png"
}

# UI
app_ui = ui.page_fluid(
    ui.head_content(
        ui.tags.style("""
            body { font-family: Arial, sans-serif; background-color: #FFFFFF; }
            h1 { color: #B22222; background-color: white; padding: 10px; }
            .output-area { background-color: #FFE5E5; padding: 15px; border-radius: 5px; margin-top: 20px; }
            .road-item { cursor: pointer; text-decoration: underline; color: blue; display: block; margin: 5px 0; }
        """)
    ),
    ui.h1("Road Condition Detection"),
    ui.p("Click the button to check for road damage detected by cameras."),
    ui.input_action_button("check_roads", "Check for damaged roads"),
    ui.output_ui("main_page")
)

# Server
def server(input, output, session):
    selected_road = reactive.Value(None)
    show_roads = reactive.Value(False)

    @output
    @render.ui
    def main_page():
        if selected_road.get():
            road = next((r for r in roads if r["id"] == selected_road.get()), None)
            if not road:
                return ui.p("⚠️ Road not found!")

            # Kies willekeurig een schadeprobleem en de juiste afbeelding
            problem = random.choice(list(damage_types.keys()))
            image_path = f"Interface2/www/{damage_types[problem]}" # Correcte afbeeldingsnaam

            return ui.div(
                ui.h3(f"📁 Road Condition Report: {road['name']}"),
                ui.p(f"🛣️ Type: {road['type']}"),
                ui.p(f"⚠️ Issue: {problem}"),
                ui.img(src=image_path, alt="Detected road damage",
                       style="width: 100%; max-width: 400px; border-radius: 5px;"),
                ui.br(),
                ui.input_action_button("back", "🔙 Back to road list"),
                class_="output-area"
            )

        if not show_roads.get():
            return ui.p("Press the button to scan for road damage.")

        road_reports = []
        for road in roads:
            road_reports.append(
                ui.p(
                    ui.input_action_link(f"road_{road['id']}", f"📍 {road['name']} ({road['type']})")
                )
            )

        return ui.div(
            ui.h3("🚨 Alert: Road Damage Detected!"),
            ui.p("Based on camera footage, the following roads have been detected with issues:"),
            *road_reports,
            class_="output-area"
        )

    @reactive.effect
    def handle_button():
        if input.check_roads() > 0:
            show_roads.set(True)

    @reactive.effect
    def handle_back():
        if input.back() > 0:
            selected_road.set(None)
            show_roads.set(True)

    @reactive.effect
    def handle_road_selection():
        for road in roads:
            if input[f"road_{road['id']}"]() > 0:
                selected_road.set(road["id"])
                break

# Start de Shiny-app
app = App(app_ui, server)
