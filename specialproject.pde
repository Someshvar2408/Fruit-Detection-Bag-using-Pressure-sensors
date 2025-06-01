/*import processing.net.*;

Client client;
String fruitName = "Waiting...";
float prob1 = 0;
String label1 = "";
float prob2 = 0;
String label2 = "";

void setup() {
  size(500, 300);
  client = new Client(this, "192.168.255.87", 23456);  // Connect to Python server
  textAlign(CENTER, CENTER);
  textSize(20);
}

void draw() {
  background(240);

  fill(0);
  text("🍓 Predicted Fruit: " + fruitName, width/2, 40);

  // Bar chart
  fill(100, 180, 100);
  rect(width/4, 100, prob1 * 200, 30);
  fill(0);
  text(nf(prob1 * 100, 0, 1) + "% - " + label1, width/2, 115);

  fill(100, 100, 200);
  rect(width/4, 160, prob2 * 200, 30);
  fill(0);
  text(nf(prob2 * 100, 0, 1) + "% - " + label2, width/2, 175);
}

void clientEvent(Client c) {
  String msg = c.readStringUntil('\n');
  if (msg != null) {
    msg = trim(msg);
    println("Received: " + msg);

    String[] parts = split(msg, ",");
    if (parts.length == 5) {
      fruitName = parts[0];
      prob1 = float(parts[1]);
      label1 = parts[2];
      prob2 = float(parts[3]);
      label2 = parts[4];
    }
  }
}*/

import processing.net.*;
import java.util.HashMap;

Client client;
String fruitName = "Waiting...";
float prob1 = 0;
String label1 = "";
float prob2 = 0;
String label2 = "";

// Emoji map
HashMap<String, String> emojiMap;

void setup() {
  size(600, 400);
  client = new Client(this, "127.0.0.1", 23456);
  textAlign(CENTER, CENTER);
  textFont(createFont("Arial", 20));
  smooth();

  // Set emoji map
  // Set emoji map
  emojiMap = new HashMap<String, String>();
  emojiMap.put("apple", "🍎");
  emojiMap.put("banana", "🍌");
  emojiMap.put("mango", "🥭");
  emojiMap.put("lime", "🍋");
  emojiMap.put("orange", "🍊");
  emojiMap.put("pear", "🍐");
  emojiMap.put("melon", "🍈");
  emojiMap.put("strawberry", "🍓");
  emojiMap.put("greenapple", "🍏");
  emojiMap.put("lemon", "🍋");
  emojiMap.put("unknown", "❓");

}

void draw() {
  background(255);

  fill(0);
  textSize(26);
  text("📡 Real-time Fruit Prediction", width/2, 30);

  // Show emoji
  String emoji = emojiMap.containsKey(fruitName.toLowerCase()) ? emojiMap.get(fruitName.toLowerCase()) : emojiMap.get("unknown");
  textSize(80);
  text(emoji, width/2, 110);

  // Predicted name
  textSize(24);
  fill(20, 100, 160);
  text("Predicted: " + fruitName, width/2, 200);

  // Top-2 probabilities
  drawProbBar(label1, prob1, 250, color(100, 200, 100));
  drawProbBar(label2, prob2, 300, color(100, 150, 220));
}

void drawProbBar(String label, float prob, float y, color c) {
  fill(0);
  textAlign(LEFT);
  text(label + ": " + nf(prob * 100, 0, 1) + "%", 60, y);

  fill(c);
  noStroke();
  rect(200, y - 10, prob * 300, 20, 10);  // rounded bar
}

void clientEvent(Client c) {
  String msg = c.readStringUntil('\n');
  if (msg != null) {
    msg = trim(msg);
    println("Received: " + msg);

    String[] parts = split(msg, ",");
    if (parts.length == 5) {
      fruitName = parts[0];
      prob1 = float(parts[1]);
      label1 = parts[2];
      prob2 = float(parts[3]);
      label2 = parts[4];
    }
  }
}
