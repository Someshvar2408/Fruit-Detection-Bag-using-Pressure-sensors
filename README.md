
# 🍎 Real-Time Fruit Classification using Arduino Sensor Data

This project implements a real-time fruit classification system using an Arduino-based sensor array and a machine learning model. The system collects contact and weight sensor data from fruits, processes it through a trained ML model, and visualizes the prediction with emojis and probabilities using a Processing GUI.

---

## 📁 Repository Structure

```

├──SerialDataCollector.py           # Collects real-time data from Arduino and saves it as CSV
├── preprocessing.py             # Cleans, labels, and merges fruit CSVs into a training dataset
├── Updated-Server.py                    # TCP server to predict fruit type from incoming sensor data
├── fruit_model(1).pkl              # Trained machine learning model
├── scaler(1).pkl                   # Scaler used to normalize input features
├── label_encoder(1).pkl            # Label encoder mapping numeric classes to fruit labels
├── specialproject.pde      # Processing GUI to visualize prediction with emoji and bars
├── fruit_csvs/                  # Directory containing individual fruit CSVs (e.g., apple2.csv)
├── merged_with_other.csv              # Final preprocessed dataset ready for training or testing
├── Fruit_detection(1).ipynb         # Machine learning model

````

---

## 🛠 Requirements

### Python
- Python 3.7+
- `pandas`
- `numpy`
- `scikit-learn`
- `joblib`
- `pyserial`
- `scipy`

Install dependencies using:
```bash
pip install -r requirements.txt
````

### Processing

* [Processing IDE](https://processing.org/download/)
* Processing `net` library (pre-installed)

---

## 🔌 Hardware Setup

* Arduino board (e.g., MKR WiFi 1010)
* 6 analog contact sensors
* 1 weight pressure sensor
* 50 ohm, 100ohm Resistors
* Breadboard and jumper wires
* USB connection to PC

---

## 🚀 Getting Started

### 1. Collect Sensor Data

Edit the `SERIAL_PORT` value in `SerialDataCollector.py` to match your Arduino port.

Run:

```bash
python SerialDataCollector.py
```

This will log incoming sensor data to a CSV file (e.g., `apple.csv`) inside the `fruit_csvs/` directory.

---

### 2. Preprocess Dataset

To clean and merge CSVs into a single training dataset:

```bash
python preprocessing.py
```

It will output `merged_with_other.csv` labeled with fruit names, ready for model training.

---

### 3. Train Your Model (Optional)

Use the `Fruit-detection(1).ipynb`. You can also train your own classifier using `merged_with_other.csv`:

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import pandas as pd

# Load and preprocess data
df = pd.read_csv("merged_with_other.csv")
X = df.drop(columns=["Timestamp", "Label"])
y = df["Label"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Train model
model = RandomForestClassifier()
model.fit(X_scaled, y_encoded)

# Save artifacts
joblib.dump(model, "fruit_model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(le, "label_encoder.pkl")
```

---

### 4. Start the Prediction Server

```bash
python Updated-Server.py
```

This script:

* Receives sensor data via TCP
* Scales and feeds it to the ML model
* Predicts fruit type and top-2 probabilities
* Broadcasts the result to the Processing visualization

---

### 5. Visualize Predictions (Processing)

Open `specialproject.pde` in the Processing IDE and run it.

This GUI:

* Connects to the server
* Shows the predicted fruit as an emoji
* Displays top-2 prediction probabilities in a graphical bar chart

---

## 📊 Example Output

**Raw Input:**

```
Contacts:3,Sensors:110,120,130,140,115,125,WeightSensor:210.3,Weight:165.0
```

**Console Output:**

```
🍎 Predicted Fruit: apple
🔢 Top-2 Predictions:
   - apple: 92.31%
   - orange: 5.62%
```

**Processing UI:**

* Displays 🍎 Apple emoji
* Two bars for top-2 class probabilities

---

## 📈 Machine Learning Model

* **Type:** Random Forest (or compatible classifier)
* **Input:** 9 features

  * Contact Count
  * Sensor1–Sensor6 values
  * WeightSensorAvg
  * Weight
* **Output:** Fruit label
* **Bonus:** Probability-based top-2 prediction

---

## 🧪 Testing and Evaluation

You can use `merged_test.csv` to cross-validate and evaluate model accuracy using metrics like:

* Accuracy
* Confusion Matrix
* Top-1 and Top-2 prediction accuracy

---

```
📡 Real-time Fruit Prediction
🍎
Predicted: Apple
Apple: 92.3%
Orange: 5.6%
```


---

## 📬 Contact

For questions or contributions, feel free to open an issue or pull request.

```
