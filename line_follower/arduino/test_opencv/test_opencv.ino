#include <Wire.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

int velocity_robot = 140;

int motor_ctrl_data = 0; 
int offset_left  = 0;
int offset_right = 0;
//------------------------------------------------------
// Variables
//motor A
int IN1 = 4;
int IN2 = 2;
int velocidadeA = 3;//llanta derecha

 
//motor B
int IN3 = 7;
int IN4 = 5;
int velocidadeB = 6;//llanta izquierda

//----------------------------------------------------------------------
//
// 
//
//----------------------------------------------------------------------
void motor_cfg_forward(){
  
//Sentido Horario
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
//Sentido Horario
  digitalWrite(IN4,HIGH);
  digitalWrite(IN3,LOW);
}
//----------------------------------------------------------------------
//
// 
//
//----------------------------------------------------------------------
void motor_cfg_back(){
  
//Sentido AntiHorario
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
//Sentido AntiHorario
  digitalWrite(IN4,LOW);
  digitalWrite(IN3,HIGH);
}
//----------------------------------------------------------------------
//
// 
//
//----------------------------------------------------------------------
void motor_cfg_left(){
//Sentido AntiHorario
  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
//Sentido Horario
  digitalWrite(IN4,HIGH);
  digitalWrite(IN3,LOW);

}
//----------------------------------------------------------------------
//
// 
//
//----------------------------------------------------------------------
void motor_cfg_right(){

//Sentido Horario
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
//Sentido AntiHorario
  digitalWrite(IN4,LOW);
  digitalWrite(IN3,HIGH);
}

//----------------------------------------------------------------------
//
// 
//
//----------------------------------------------------------------------
void motor_cfg_stop(){

//Sentido Horario
  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,HIGH);
//Sentido AntiHorario
  digitalWrite(IN4,HIGH);
  digitalWrite(IN3,HIGH);
}

//-------------------------------------------------------
void setup_motor(){

  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(velocidadeA,OUTPUT);
  pinMode(velocidadeB,OUTPUT);

  Serial.begin(9600);
  
}
//-------------------------------------------------------


void setup() {
  
setup_motor();

pinMode(13, OUTPUT);
Serial.begin(9600); // start serial for output
// initialize i2c as slave
Wire.begin(SLAVE_ADDRESS);

// define callbacks for i2c communication
Wire.onReceive(receiveData);
Wire.onRequest(sendData);

Serial.println("Ready!");


}
//-------------------------------------------------------
void loop() {

  delay(100);

}
//-------------------------------------------------------

// callback for received data
void receiveData(int byteCount){

while(Wire.available()) {
motor_ctrl_data = Wire.read();
Serial.print("data received:");
Serial.println(motor_ctrl_data);

offset_right = 0;
offset_left  = 0;

//always go front
motor_cfg_back();
 
if (motor_ctrl_data > 100){
offset_left = motor_ctrl_data - 100;
digitalWrite(velocidadeB, HIGH);
delay(900 + offset_left);
digitalWrite(velocidadeB, LOW);
}

if (motor_ctrl_data < 100){
offset_right = 100 - motor_ctrl_data;
digitalWrite(velocidadeA, HIGH);
delay(900 + offset_right);
digitalWrite(velocidadeA, LOW);
}

if (motor_ctrl_data < 105 & motor_ctrl_data > 95)
{
digitalWrite(13, HIGH); // set the LED on

digitalWrite(velocidadeA, HIGH);
digitalWrite(velocidadeB, HIGH);
delay(900 );
digitalWrite(velocidadeA, LOW);
digitalWrite(velocidadeB, LOW);
}
else
//
{
digitalWrite(13, LOW); // set the LED off
}
  // analogWrite(velocidadeA,velocity_robot + offset_right);
  // analogWrite(velocidadeB,velocity_robot + offset_left); //llanta izquierda
    
  //Serial.print("motor left:");
  //Serial.println(velocity_robot + offset_left);
  //Serial.print("motor right:");
  //Serial.println(velocity_robot + offset_right);

}// wire available
}// receive data

// callback for sending data
void sendData(){
Wire.write(motor_ctrl_data);
Serial.print("data sent:");
Serial.println(motor_ctrl_data);
//:)
}
