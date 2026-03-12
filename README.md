# PaisaPulse Explorer 💸

A powerful and visually stunning data visualization dashboard for **PhonePe Pulse** data. This project analyzes and visualizes digital payment trends in India, providing insights at the national, state, and district levels.

## 🚀 Features

- **Interactive Analytics**: Deep dive into transaction trends and user growth.
- **Geospatial Visualization**: Visualize payment distribution across India using maps.
- **Granular Insights**: Analyze data by year, quarter, state, and district.
- **Modern UI**: A sleek, premium dashboard built with Streamlit and Plotly.
- **Category DRI**: Break down transactions by type (P2P, Merchant, etc.).

## 🛠️ Tech Stack

- **Frontend/App**: [Streamlit](https://streamlit.io/)
- **Data Processing**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualization**: [Plotly](https://plotly.com/python/)
- **Data Source**: PhonePe Pulse Dataset

## 📂 Project Structure

- `app.py`: Main entry point and navigation.
- `pages/`: Individual analytics modules (Overview, State, District, etc.).
- `utils/`: Helper functions for data loading and chart generation.
- `requirements.txt`: Project dependencies.

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ShreyanshGupta205/PhonePe-Pulse-Explorer.git
   cd PhonePe-Pulse-Explorer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
