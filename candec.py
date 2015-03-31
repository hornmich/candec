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

class CANSignal:
	def __init__(self, sigName='void', sigByte=0, sigBit=0, sigLen=0, sigVal=0, sigDecVal='n/a'):
		self.sigName = sigName
		self.sigByte = sigByte
		self.sigBit = sigBit
		self.sigLen = sigLen
		self.sigVal = sigVal
		self.sigDecVal = sigDecVal

class CANDec:
	def __init__(self):
		self.reset()

	def reset(self) :
		self.state = 'start'
		self.lineNum = 1
		self.sigNames = []
		self.signals = {}
		self.sigRawDecoded = ''
		
	def printErrTok(self, token, lineNum, state):
		print 'Unexpected token ' + token + ' found at line ' + str(lineNum) + ' in state ' + state + '\n'

	def printErrParam(self, signal, numParams, lineNum, state):
		print 'Unexpected number of parameters (' + str(numParams) + ') for signal ' + signal + ' found at line ' + str(lineNum) + ' in state ' + state + '\n'

	def decode(self, canMsgVal, descriptorFileName):
		self.reset()
		self.descFile = open(descriptorFileName, 'r')

		for line in self.descFile:
			self.lineNum = self.lineNum + 1
			if '%sig' in line:
				if self.state != 'start' :
					self.printErrTok('%sig', self.lineNum, self.state)
					continue
				sigParams = line.rsplit()
				if len(sigParams) != 5:
					self.printErrParam('%val', len(valParams), self.lineNum, self.state)
					continue
				tmpSigName = sigParams[1]		# Signal name
				tmpSigByte = int(sigParams[2])	# Signal Byte
				tmpSigBit = int(sigParams[3])	# Signal start bit
				tmpSigLen = int(sigParams[4]);	# Signal length in bits
				tmpValDescriptors = {}
				self.state = 'sig'
				
			elif '%val' in line:
				if self.state != 'sig' :
					self.printErrTok('%val', self.lineNum, self.state)
					continue
				valParams = line.rsplit('\t')
				if len(valParams) != 3:
					self.printErrParam(tmpSigName, len(valParams), self.lineNum, self.state)
					continue
				tmpSigVal = int(valParams[1])	# Signal Value
				tmpSigDesc = valParams[2]	# Signal value description
				tmpValDescriptors[tmpSigVal] = tmpSigDesc
			elif '%endsig' in line:
				if self.state != 'sig' :
					self.printErrTok('%endsig', self.lineNum, self.state)
					continue
				self.state = 'start'
				self.sigNames.append(tmpSigName)
				byte = (canMsgVal >> (tmpSigByte-1)*8) & 0xFF
				bitCodeMask = 0x0
				for i in range(tmpSigLen) :
					bitCodeMask = bitCodeMask | 1 << i;
				tmpSigDecVal = (byte >> tmpSigBit) & bitCodeMask;
				if tmpSigDecVal in tmpValDescriptors:
					self.signals[tmpSigName] = CANSignal(tmpSigName, tmpSigByte, tmpSigBit, tmpSigLen, tmpSigDecVal, tmpValDescriptors[tmpSigDecVal])
					self.sigRawDecoded = self.sigRawDecoded + (tmpSigName + '[' + str(tmpSigByte) + ', ' + str(tmpSigBit) + ', ' + str(tmpSigLen) + '] = ' + ' (' + str(tmpSigDecVal) + ')' + tmpValDescriptors[tmpSigDecVal])
				else:
					self.signals[tmpSigName] = CANSignal(tmpSigName, tmpSigByte, tmpSigBit, tmpSigLen, tmpSigDecVal, 'unknown')
					self.sigRawDecoded = self.sigRawDecoded + (tmpSigName + '[' + str(tmpSigByte) + ', ' + str(tmpSigBit) + ', ' + str(tmpSigLen) + '] = ' + ' (' + str(tmpSigDecVal) + ') unknown\n')
	
	def getSignalByte(self, sigName):
		return self.signals[sigName].sigByte
		
	def getSignalStartBit(self, sigName):
		return self.signals[sigName].sigBit
		
	def getSignalLength(self, sigName):
		return self.signals[sigName].sigLen
	
	def getSignalValue(self, sigName):
		return self.signals[sigName].sigVal

	def getSignalDecoded(self, sigName):
		return self.signals[sigName].sigDecVal

	def getSignalsNames(self):
		return self.sigNames
		
	def getSignalsRawDecoded(self):
		return self.sigRawDecoded
	
parser = OptionParser()
(options, args) = parser.parse_args()
if len(args) != 2:
	exit(1)
canMsgVal = int(args[0], 16)
descFileName = args[1]

canDecoder = CANDec()
canDecoder.decode(canMsgVal, descFileName)
print canDecoder.getSignalsRawDecoded()
