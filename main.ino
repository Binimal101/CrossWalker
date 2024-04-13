//GLOBAL ACCESS VARIABLES
int previousSequenceNumber = -1; //Will be overwritten on first command read

void Setup() {
  Serial.begin(9600);
}

String getInstruction() {
  char c;

  String instruction = "";
  String constructedSequenceNumber = "";

  if (Serial.available() <= 0) { //command buffer empty
    return "DO NOTHING"; //device should wait
  }

  while (c = Serial.read() != "\n") { //dumps newline delim
    if(isdigit(c)) { //construction of packet #
      constructedSequenceNumber += c;
    } else { //construction of instruction
      instruction += c;
    }
  }

  int sequenceNumber = constructedSequenceNumber.toInt();
  if sequenceNumber > previousSequenceNumber {
    return instruction;
  } else {
    return "DO NOTHING";
  }
}

void forward();
void backward();
void stop();
void turn(float degrees);

void loop() {
  instruction = getInstruction();

  switch (instruction) {
    case "DO NOTHING": //leftovers from command buffer || waiting for command
      break;
    case "FORWARD":
      forward();
      break;
    case "BACKWARD":
      backward();
      break;
    case "STOP":
      stop();
      break;
    default:
      //downtime in command execution is irrelavent with sequential ordering
      if(instruction.substring(0,4) == "TURN") {
        //POSITIVE it clockwise, NEGATIVE is ccw
        //command is TURN (number), " " + 1 begins the number
        float degrees = (instruction.substring(instruction.find(" ")+1, instruction.length())).toFloat();
        turn(degrees);
      } else {
        //something bad happened
      }
  }

  delay(100);
}

