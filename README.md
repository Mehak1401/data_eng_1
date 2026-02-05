# Data Engineering Pipeline Project

This project implements a complete data engineering pipeline including data generation, ETL processing, testing, and visualization.

## Project Structure

- `data_gen.py`: Generates synthetic dataset (16,000+ rows)
- `etl_pipeline.py`: Extracts, Transforms, and Loads data into SQLite
- `test_pipeline.py`: Unit tests for data integrity and schema validation
- `app.py`: Streamlit dashboard for data visualization
- `.github/workflows/pipeline.yml`: CI/CD configuration

## Setup & Execution

1. **Install Dependencies**
   (Pre-installed in this environment)
   ```bash
   pip install -r requirements.txt
   ```

2. **Generate Data**
   ```bash
   python data_gen.py
   ```

3. **Run ETL Pipeline**
   ```bash
   python etl_pipeline.py
   ```

4. **Run Tests**
   ```bash
   pytest -v
   ```

5. **Launch Dashboard**
   ```bash
   streamlit run app.py --server.port 5000 --server.address 0.0.0.0
   ```

## Requirements

See `requirements.txt` for the full list of Python dependencies.
