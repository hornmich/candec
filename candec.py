'''
  Copyright 2015 Michal Horn

  Authors: Michal horn <michal@apartman.cz>

  This file is part of CANDec.

  CANDec is free software: you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 2 of the License, or
  (at your option) any later version.

  CANDec is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with CANDec.   If not, see <http://www.gnu.org/licenses/>.
'''

from optparse import OptionParser

parser = OptionParser()

(options, args) = parser.parse_args()

if len(args) != 2:
	exit(1)

canMsgVal = int(args[0], 16)
descFileName = args[1]

file = open(descFileName, 'r')

state = 'start'
lineNum = 0

for line in file:
	if '%sig' in line:
		if state != 'start' :
			print 'Unexpected token %sig found at line ' + str(lineNum) + 'in state ' + state
			continue
		params = line.rsplit()
		if len(params) != 5:
			continue
		sigName = params[1]
		startByte = int(params[2])
		startBit = int(params[3])
		segLen = int(params[4]);
		valDescriptor = {}
		state = 'sig'
		
	elif '%val' in line:
		if state != 'sig' :
			print 'Unexpected token %val found at line ' + str(lineNum) + 'in state ' + state
			continue
		params = line.rsplit('\t')
		if len(params) != 3:
			continue
		descriptor = params[2]
		value = int(params[1])
		#print 'Descriptor: ' + descriptor[2]
		valDescriptor[value] = descriptor
	elif '%endsig' in line:
		if state != 'sig' :
			print 'Unexpected token %endsig found at line ' + str(lineNum) + 'in state ' + state
			continue
		state = 'start'
		
		byte = (canMsgVal >> (startByte-1)*8) & 0xFF
		#print 'Byte: ' + str(byte)
		bitCodeMask = 0x0
		for i in range(segLen) :
			bitCodeMask = bitCodeMask | 1 << i;
		#print 'bitCodeMask: ' + str(bitCodeMask)
		bitCode = (byte >> startBit) & bitCodeMask;
		#print 'bitCode: ' + str(bitCode)
		if len(valDescriptor) > 0 and bitCode >= len(valDescriptor):
			print sigName + '[' + str(startByte) + ', ' + str(startBit) + ', ' + str(segLen) + '] = ' + ' (' + str(bitCode) + ') undefined\n' 
		elif len(valDescriptor) == 0:
			print sigName + '[' + str(startByte) + ', ' + str(startBit) + ', ' + str(segLen) + '] = ' + str(bitCode) + '\n' 
		else:
			print sigName + '[' + str(startByte) + ', ' + str(startBit) + ', ' + str(segLen) + '] = ' + ' (' + str(bitCode) + ')' + valDescriptor[bitCode] 
print 'done'


