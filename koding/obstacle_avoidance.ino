/*
 * UAS Intelligent Systems and Robotics (ISR)
 * Kode Program Pengendali Robot Obstacle Avoidance
 * 
 * Kelompok: [Nama Kelompok Anda]
 * Anggota:
 * 1. Nama Anggota 1 (1234567890)
 * 2. Nama Anggota 2 (1234567891)
 * 3. Nama Anggota 3 (1234567892)
 * 4. Nama Anggota 4 (1234567893)
 */

// Definisi pin sensor ultrasonik HC-SR04
const int trigPin = 9;
const int echoPin = 10;

// Definisi pin motor DC (L298N driver)
const int motorL1 = 5;
const int motorL2 = 6;
const int motorR1 = 7;
const int motorR2 = 8;

// Threshold jarak aman untuk menghindari tabrakan (dalam cm)
const int thresholdDistance = 20;

void setup() {
  // Inisialisasi pin sensor
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  
  // Inisialisasi pin motor
  pinMode(motorL1, OUTPUT);
  pinMode(motorL2, OUTPUT);
  pinMode(motorR1, OUTPUT);
  pinMode(motorR2, OUTPUT);
  
  // Inisialisasi komunikasi serial untuk monitoring data
  Serial.begin(9600);
  Serial.println("Robot Obstacle Avoidance Siap!");
}

void loop() {
  long duration;
  int distance;
  
  // Memicu sensor ultrasonik memancarkan gelombang
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  // Membaca durasi pantulan gelombang
  duration = pulseIn(echoPin, HIGH);
  
  // Menghitung jarak berdasarkan kecepatan suara (340 m/s)
  distance = duration * 0.034 / 2;
  
  // Menampilkan data ke Serial Monitor
  Serial.print("Jarak terdeteksi: ");
  Serial.print(distance);
  Serial.println(" cm");
  
  // Logika pengambilan keputusan (Intelligent Decision)
  if (distance > 0 && distance < thresholdDistance) {
    // Halangan terdeteksi, lakukan manuver menghindar
    Serial.println("Ada halangan! Robot belok kanan.");
    belokKanan();
    delay(500); // Waktu manuver belok
  } else {
    // Jalur aman, robot berjalan maju
    Serial.println("Jalur aman. Robot maju lurus.");
    majuLurus();
  }
  
  delay(100); // Interval pembacaan
}

// Fungsi kendali motor untuk gerak maju lurus
void majuLurus() {
  digitalWrite(motorL1, HIGH);
  digitalWrite(motorL2, LOW);
  digitalWrite(motorR1, HIGH);
  digitalWrite(motorR2, LOW);
}

// Fungsi kendali motor untuk belok kanan di tempat (pivot turn)
void belokKanan() {
  digitalWrite(motorL1, HIGH);
  digitalWrite(motorL2, LOW);
  digitalWrite(motorR1, LOW);
  digitalWrite(motorR2, HIGH);
}

// Fungsi kendali motor untuk berhenti
void berhenti() {
  digitalWrite(motorL1, LOW);
  digitalWrite(motorL2, LOW);
  digitalWrite(motorR1, LOW);
  digitalWrite(motorR2, LOW);
}
