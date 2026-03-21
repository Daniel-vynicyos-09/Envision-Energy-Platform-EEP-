#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "tcc";
const char* password = "tcc12345";

void setup() {
  Serial.begin(115200);
  delay(100);

  // Inicia a conexão WiFi e espera indefinidamente até conectar
  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado! IP: ");
  Serial.println(WiFi.localIP());

  // Inicializa gerador de números aleatórios
  randomSeed(analogRead(0));
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    WiFiClient client;

    const char* url = "http://192.168.1.2:8000/dados";

    http.begin(client, url);
    http.addHeader("Content-Type", "application/json");

    float valor = random(1000, 2000) / 10.0; // exemplo: 100.0 a 199.9

    String json = "{\"valor\":" + String(valor) + "}";

    int httpCode = http.POST(json);
    if (httpCode > 0) {
      Serial.print("POST enviado, código HTTP: ");
      Serial.println(httpCode);
      String payload = http.getString();
      Serial.print("Resposta: ");
      Serial.println(payload);
    } else {
      Serial.print("Erro ao enviar POST: ");
      Serial.println(httpCode);
    }

    http.end();
  } else {
    // Caso desconecte depois de conectado, tenta reconectar
    Serial.println("WiFi não conectado. Tentando reconectar...");
    WiFi.reconnect();
  }

  delay(5000);
}