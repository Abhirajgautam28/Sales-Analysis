# Warehouse Sales Analysis — Interactive Sales Analytics

**Live demo:** [https://warehouse-sales-analysis.streamlit.app/](https://warehouse-sales-analysis.streamlit.app/)

## Project Summary

Warehouse Sales Analysis is an end-to-end analytics project that transforms raw sales, customer, product, and regional data into actionable insights. The repository includes data processing pipelines, exploratory data analysis (EDA), interactive visualizations, and a Streamlit web app for stakeholders to explore trends and product/region performance.

## Key Features

- Interactive Streamlit dashboard with filters, KPI tiles, charts, and CSV export
- Monthly revenue trend, top products, channel breakdowns, and U.S. choropleth
- Example SQL scripts and EDA notebook for reproducible data preparation

## Tech Stack

- Python: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`
- Web app: `streamlit`
- Container: `Docker`

## Repository Structure

- `app.py` — Streamlit application
- `EDA_Regional_Sales_Analysis.ipynb` — analysis notebook
- `Sales_data(EDA Exported).csv` and `Data_split/` — sample CSVs used by the app/notebook
- `SQL_codes/` — helper SQL for loading tables
- `Dockerfile`, `.github/workflows/` — containerization and CI

## Quickstart — Local (Windows PowerShell)

1. Clone the repo:

```powershell
git clone https://github.com/Abhirajgautam28/Sales-Analysis.git
cd Sales-Analysis
```

1. Create and activate a virtual environment, install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

1. Run locally:

```powershell
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Run with Docker (recommended for reproducible builds)

Build the image locally:

```powershell
docker build -t sales-analysis:local .
```

Run the container (exposes Streamlit on port 8501):

```powershell
docker run --rm -p 8501:8501 sales-analysis:local
```

Or run the published image from GitHub Container Registry:

```powershell
docker run --rm -p 8501:8501 ghcr.io/Abhirajgautam28/Sales-Analysis:latest
```

The container is configured to run Streamlit on `0.0.0.0:8501`.

## Continuous Integration / Smoke Tests

- GitHub Actions builds and publishes a Docker image to GitHub Container Registry on pushes to `main`.
- A smoke-test job pulls the pushed image, starts the container in the runner, and checks `http://localhost:8501/` to confirm the app started successfully.

## Contributing

Contributions, issues, and feature requests are welcome. Please open an issue or submit a pull request with a clear description.

## License

This project is licensed under the MIT License.
