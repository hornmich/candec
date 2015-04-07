# candec
CAN message decoder
## Description
This script has been designed to decode values received from CAN bus, but can be as well used for decoding any hexadecimal values.

##Installation
This is a python script, so it does not need any installation.

##Requirements
Python 2.7.6

##Usage
        Usage: candec.py [options] msgVal descriptor
        Options:
        -h, --help            show this help message and exit
          -s NAME, --signal=NAME
                        Print only signal with the specified NAME
                        
          -b STARTBIT, --start-bit=STARTBIT
                        Determines the start index of bits. 0 by default.
                        
          -B STARTBYTE, --start-byte=STARTBYTE
                        Determines the start index for bytes. 1 by default
                        

The msgVal argument is a 32b hexadecimal message value tha will be decoded.
The descriptor is a path to the file, containing description of the signals, encoded in the msgVal. See Signals description for details.

The options -b and -B should not be needed if you follow the rules in Signals description sections. But if you decide not to index bytes from 1, but form zero, use the -B option to tell the script.

##Signals description
###Introduction
Signals encoded in the message value are described in description files by a simple structured language, containing those key words:
* %sig
* %val
* %endsig

The message can encode several signals. Each signal definition begins with %sig, contains several %val for every defined signal value and is closed by %endsig.

###%sig
Syntax: %sig signal_name start_bit byte length

Where:
* signal_name is used for filtering and referencing signals.
* start_bit determines the start bit of the signal in the selected byte in the value
* byte selects the byte of the value, where the signal is encoded
* length determines the length of the signal data in bits

Notes:
* Bits should be byte alligned - no bytes overlapping is allowed.
* Bytes are indexed from one, bits are indexed from yero. To change this default behavioral see options -b and -B.
* Parameters of the %sig are separated by any white character, so no spaces are allowed in the signal_name
* Signal_name may not be unique, but in this case only the last appearance in the decoding process will be remembered for the filtering 9with the -s option). All of them will be visible in raw output (without the -s option).

###%val
Syntax: %val value value_description

Where:
* value is a defined value for the signal, which has asigned some description
* value_description is a description for the value encoded in the signal

Notes:
* One signal can have several defined values, up to length^2.
* Values which are not defined are assigned 'unknown' automatically.
* Darameters of the %val are separated by tabulators, so spaces are allowed in the value_description.
* If one signal value has more than one description, only the last one is accepted.

###%endsig
Syntax: %endsig
Must be used to finish every signal definition.

###example
This example shows how to use the keywords to define a description file for the decoder. This file describes three signals.
* Signal_1 in the first byte of the message, with three values (0, 1, 2) defined.
* Signal_2 in the first half of the second byte with another three values (0, 1, 2) defined.
* Signal_3 in the second half of the second byte with another three values (0, 1, 2) defined.
* The rest data are marked named as void with no values defied. Those data are not of our interrest.

        %sig	Signal_1	1	0	8
        %val	0	Sig 1 Val 0
        %val	1	Sig 1 Val 1
        %val	2	Sig 1 Val 2
        %endsig
        
        %sig	Signal_2	2	0	4
        %val	0	Sig 2 Val 0
        %val	1	Sig 2 Val 1
        %val	2	Sig 2 Val 2
        %endsig
        
        %sig	Signal_3	2	4	4
        %val	0	Sig 3 Val 0
        %val	1	Sig 3 Val 1
        %val	2	Sig 3 Val 2
        %endsig
        
        %sig	void	3	0	8
        %endsig
        
        %sig	void	4	0	8
        %endsig
        
        %sig	void	5	0	8
        %endsig
        
        %sig	void	6	0	8
        %endsig
        
        %sig	void	7	0	8
        %endsig
        
        %sig	void	8	0	8
        %endsig
