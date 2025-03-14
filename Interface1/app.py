import shiny
from shiny import ui, App, render
import datetime
import random
import pandas as pd

# Define UI
app_ui = ui.page_fluid(
    ui.head_content(
        ui.tags.style("""
            body { font-family: Arial, sans-serif; background-color: #FFFFFF; }
            h1 { color: #B22222; background-color: white; padding: 10px; }
            .warning { color: red; font-weight: bold; }
            .innovateher { position: absolute; top: 10px; right: 20px; font-size: 24px; font-weight: bold; color: #B22222; }
            .sidebar { background-color: #B22222; padding: 15px; color: white; height: 100vh; }
            .output-area { background-color: #FFE5E5; padding: 15px; border-radius: 5px; height: 100vh; width: 60%; display: inline-block; }
            .legend-area { background-color: #FFF3CD; padding: 15px; border-radius: 5px; height: 100vh; width: 35%; display: inline-block; vertical-align: top; margin-left: 10px; }
        """)
    ),
    ui.h1("SmartRoadSync"),
    ui.p("by InnovateHer", class_="innovateher"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_text("street", "Street", ""),
            ui.input_text("city", "City", ""),
            ui.input_date("start_allowed", "Earliest Start Date", value=datetime.date.today()),
            ui.input_date("deadline", "Deadline for Completion", value=datetime.date.today() + datetime.timedelta(days=30)),
            ui.input_numeric("duration", "Duration of roadworks (in days)", 10, min=1),
            ui.input_numeric("num_dates", "Number of dates to display", 20, min=1, max=100),
            ui.input_radio_buttons("sort_by", "Sort by", choices=["Date", "Color"]),
            class_="sidebar"
        ),
        ui.div(
            ui.div(ui.output_ui("suggested_dates"), class_="output-area"),
            ui.div(
                ui.h3("🔍 Meaning of the colors"),
                ui.p("🟢 Best choice! This schedule is aligned with the mobility plan and will cause the least traffic disruption."),
                ui.p("🟡 Acceptable option. It can work, but it can cause traffic jam."),
                ui.p("🔴 Avoid!This will cause traffic congestion and overlaps with other roadworks."),
                class_="legend-area"
            )
        )
    )
)

# Define server logic
def server(input, output, session):
    @output
    @render.ui
    def suggested_dates():
        try:
            start_allowed = input.start_allowed()
            deadline = input.deadline()
            num_dates = int(input.num_dates())
            sort_by = input.sort_by()

            start_allowed_date = datetime.datetime.combine(start_allowed, datetime.datetime.min.time())
            deadline_date = datetime.datetime.combine(deadline, datetime.datetime.min.time())

            # Generate all possible dates
            all_possible_dates = [start_allowed_date + datetime.timedelta(days=i) for i in range((deadline_date - start_allowed_date).days)]

            # Select the requested number of dates
            num_dates = min(num_dates, len(all_possible_dates))
            sampled_dates = random.sample(all_possible_dates, num_dates)
            sampled_dates.sort()  # Sort initially by date

            # Assign colors BEFORE sorting
            def random_score():
                return random.choices(["🟢", "🟡", "🔴"], weights=[0.4, 0.4, 0.2])[0]

            date_color_pairs = [{"Date": date.strftime("%Y-%m-%d"), "Score": random_score()} for date in sampled_dates]

            # Sort based on user choice
            if sort_by == "Date":
                date_color_pairs.sort(key=lambda x: x["Date"])
            else:
                date_color_pairs.sort(key=lambda x: x["Score"], reverse=True)

            # Display results
            rows = [ui.p(f"{entry['Date']} {entry['Score']}", style="font-size: 16px;") for entry in date_color_pairs]
            return ui.div(*rows)

        except Exception as e:
            return ui.p(f"Error: {str(e)}", class_="warning")

# Create the Shiny app
app = App(app_ui, server)
