# NSM FRP Shear Resistance Prediction App

This repository contains a Streamlit application for predicting the design value of shear resistance ($V_{Rd}$) for RC beams strengthened with Near-Surface Mounted (NSM) FRP reinforcement.

The application implements the semi-empirical model and reliability-based design framework proposed in the associated manuscript.

## Features

- **Premium Light Design**: Clean, high-end UI with glassmorphism and responsive layout.
- **Interactive Inputs**: Sliders for geometric, material, and reinforcement parameters.
- **Multiple Methods**: Calculates resistance using both WLSM and Lind reliability methods.
- **Visualizations**: Interactive charts for resistance comparison and component contribution.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/amirxdbx/Design_Model_for_Shear_Strength_NSM.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application using Streamlit:

```bash
streamlit run app.py
```

## Structure

- `app.py`: Main application code.
- `verify_logic.py`: Script to verify calculation logic against manuscript examples.
