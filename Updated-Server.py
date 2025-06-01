import socket
import joblib
import numpy as np
import sys
import threading
# Add this to the top of your Python script
processing_clients = []

def broadcast_to_processing_clients(msg):
    for pc in processing_clients:
        try:
            pc.sendall((msg + "\n").encode("utf-8"))
        except:
            processing_clients.remove(pc)

# Load model, scaler, and label encoder
try:
    #model = joblib.load("fruit_model.pkl")
    model = joblib.load("fruit_model (1).pkl")
    #scaler = joblib.load("scaler.pkl")
    scaler = joblib.load("scaler (1).pkl")
    #label_encoder = joblib.load("label_encoder.pkl")
    label_encoder = joblib.load("label_encoder (1).pkl")
except (FileNotFoundError, EOFError) as e:
    print(f"❌ Error loading model/scaler/label encoder: {e}")
    sys.exit(1)

HOST = "0.0.0.0"
PORT = 12345
def processing_server_thread():
    ps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ps.bind(("0.0.0.0", 23456))  # Port for Processing to connect
    ps.listen()
    print("🟢 Processing client server running on port 23456")
    while True:
        client, addr = ps.accept()
        print(f"🧩 Processing client connected from {addr}")
        processing_clients.append(client)

threading.Thread(target=processing_server_thread, daemon=True).start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"📡 Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"🔌 Connected by {addr}")
            try:
                data = conn.recv(1024)
                if not data:
                    continue

                decoded = data.decode("utf-8").strip()
                print(f"📥 Received: {decoded}")
                values = list(map(float, decoded.split(",")))

                if len(values) == 9:
                    input_array = np.array(values).reshape(1, -1)
                    input_scaled = scaler.transform(input_array)

                    # Predict
                    prediction = model.predict(input_scaled)[0]
                    predicted_label = label_encoder.inverse_transform([prediction])[0]
                    print(f"🍎 Predicted Fruit: {predicted_label}")
                    


                    # Show top-2 predictions with probabilities
                    if hasattr(model, "predict_proba"):
                        probs = model.predict_proba(input_scaled)[0]
                        top2 = probs.argsort()[-2:][::-1]
                        print(f"🔢 Top-2 Predictions:")
                        for i in top2:
                            label = label_encoder.inverse_transform([i])[0]
                            print(f"   - {label}: {probs[i]*100:.2f}%")
                            msg = f"{predicted_label},{probs[top2[0]]:.2f},{label_encoder.inverse_transform([top2[0]])[0]},{probs[top2[1]]:.2f},{label_encoder.inverse_transform([top2[1]])[0]}"
                            broadcast_to_processing_clients(msg)

                else:
                    print(f"⚠️ Invalid input length: Expected 9 values, got {len(values)}")

            except Exception as e:
                print(f"❗ Error during prediction: {e}")
