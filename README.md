# Gulf Corridor Index (GCI)

A free tool that scores 6 Gulf shipping routes against current Hormuz
crisis conditions and recommends the best route based on cost, time,
or safety priority.

## How to run this on your laptop (Week 1)

You need Python installed (3.9 or newer). If you're not sure, open a
terminal and type `python3 --version`. If that fails, install Python
from python.org first.

### Step 1: Open a terminal in this folder

If you downloaded this as a zip, unzip it, then open a terminal and
navigate into the folder:

    cd path/to/gulf_corridor_index

### Step 2: Install the one dependency

    pip install -r requirements.txt

(If that fails on a Mac with an error about "externally managed
environment," use: `pip install -r requirements.txt --break-system-packages`)

### Step 3: Run the app

    streamlit run app.py

This will open automatically in your browser at http://localhost:8501

### Step 4: Click around

- Try switching the priority radio button (cost / time / safety) and
  watch the recommendation and the ranking table change.
- Expand "How is this calculated?" to see the GCI methodology note.
- Expand each route's details to see the sourcing notes.

## What to look for / give feedback on

- Does the recommended route for each priority make sense to you,
  given what you know about current conditions?
- Is anything confusing about the layout?
- Are there numbers that feel wrong or outdated? (Check route_data.py,
  every number has a source listed.)
- Notice the green "Confirmed" vs yellow "Estimated" labels next to each
  route. Confirmed means a specific named source backs that route's exact
  numbers. Estimated means it's built from general industry patterns.
  Be honest about this distinction if a logistics professional asks,
  it builds trust rather than undermining it.

## File structure

- `app.py` — the screen you see, all UI code
- `scoring_engine.py` — the math that ranks routes (cost/time/risk
  normalization and weighting)
- `route_data.py` — every editable number lives here. This is the
  file you'll update weekly as crisis conditions change.

## Next steps (Week 2 onward)

Once you've run this and given feedback, we'll:
1. Walk through updating route_data.py yourself with fresh numbers
2. Polish the visual design with your branding
3. Deploy it to a free public URL (Streamlit Community Cloud)
4. Use it in outreach emails to logistics companies
