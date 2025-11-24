#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
This program is the main program to execute data flow confusion, 
its input is a .sol source code file and the corresponding compiled 
json.ast file, its output is a .sol source code file after data 
flow obfuscation.
'''

import os
import json
import sys
from .literal2Exp import literal2Exp
from .splitBoolVariable import splitBoolVariable

import time

colors = True # Output should be colored
machine = sys.platform # Detecting the os of current system
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False # Colors shouldn't be displayed in mac & windows
if not colors:
    end = green = bad = info = ''
    start = ' ['
    stop = ']'
    backGreenFrontWhite = ''
    white = ''
    blue = ''
    yellow = ''
else:
    end = '\033[1;m'
    green = '\033[1;32m'
    white = "\033[1;37m"
    blue = "\033[1;34m"
    yellow = "\033[1;33m"
    bad = '\033[1;31m[-]\033[1;m'
    info = '\033[1;33m[!]\033[1;m'
    start = ' \033[1;31m[\033[0m'
    stop = '\033[1;31m]\033[0m'
    backGreenFrontWhite = "\033[1;37m\033[42m"


class dataflowObfuscation:
	def __init__(self, _filepath, _jsonFile):
		self.filePath = _filepath
		self.jsonPath = _jsonFile
		self.outputFileName = self.getOutputFileName(_filepath)
		self.solContent = self.getContent(_filepath)
		self.json = self.getJsonContent(_jsonFile)
		self.middleContract = "temp.sol"
		self.middleJsonAST = "temp.sol_json.ast"
		self.configPath = os.path.join(os.path.dirname(__file__), "Configuration.json")
		self.getConfig()
		#self.finalContract = _filepath.split(".sol")[0] + "_dataflow_confuse.sol"

	def getOutputFileName(self, _filepath):
		temp = _filepath.split(".sol")
		newFileName = temp[0] + "_dataflow_confuse.sol"
		return newFileName

	def getContent(self, _filepath):
		with open(_filepath, "r", encoding = "utf-8", newline='') as f:
			return f.read()
		return str()

	def getJsonContent(self, _jsonFile):
		jsonStr = str()
		with open(_jsonFile, "r", encoding = "utf-8") as f:
			jsonStr = f.read()
		jsonDict = json.loads(jsonStr)
		return jsonDict

	def writeStrToFile(self, _filename, _str, _step):
		with open(_filename, "w", encoding = "utf-8", newline='') as f:
			f.write(_str)
		print(("%s" + _step + ".... done" + "%s") % (yellow, end))

	def recompileMiddleContract(self):
		# 使用 --ast-compact-json 以兼容 solc 0.6.x 版本
		compileResult = os.popen("solc --ast-compact-json --overwrite " + self.middleContract + " -o .")
		#print(compileResult.read())
		print(("%s" + "\rIntermediate contract is being generated." + "%s") % (white, end), end = " ")
		time.sleep(1.5)
		print(("%s" + "\rIntermediate contract is being generated....done" + "%s") % (white, end))
		self.solContent = self.getContent(self.middleContract)
		self.json = self.getJsonContent(self.middleJsonAST)

	def getConfig(self):
		config = self.getJsonContent(self.configPath)
		self.featureList = config["activateFunc"]
		#print(self.featureList)

	def isActivate(self, _name):
		for _dict in self.featureList:
			try:
				return _dict[_name][0]
			except:
				continue
		return True

	def getFeatProb(self, _name):
		for _dict in self.featureList:
			try:
				return _dict[_name][1]
			except:
				continue
		return 1

	def run(self):
		print((("%s") + "Start data flow confusion:" + ("%s")) % (backGreenFrontWhite, end))
		if self.isActivate("literal2Exp"):
			try:
				self.L2E = literal2Exp(self.solContent, self.json) #L2E is a class which is used to convert integer literal to arithmetic expressions
				nowContent = self.L2E.doGenerate(self.getFeatProb("literal2Exp"))
				self.writeStrToFile(self.middleContract, nowContent, "Convert integer literals to arithmetic expressions")
				self.recompileMiddleContract()
			except:
				self.solContent = self.getContent(self.filePath)
				self.json = self.getJsonContent(self.jsonPath)
				print(("%s" + "Convert integer literals to arithmetic expressions...Exception occurs" + "%s") % (bad, end))
		if self.isActivate("splitBoolVariable"):
			try:
				self.SBV = splitBoolVariable(self.solContent, self.json)
				nowContent = self.SBV.doSplit(self.getFeatProb("splitBoolVariable"))
				self.writeStrToFile(self.middleContract, nowContent, "Split boolean variables")
				self.recompileMiddleContract()
			except Exception as e:
				import traceback
				traceback.print_exc()
				self.solContent = self.getContent(self.filePath)
				self.json = self.getJsonContent(self.jsonPath)
				print(("%s" + "Split boolean variables...Exception occurs: " + str(e) + "%s") % (bad, end))
		print((("%s") + "Complete data flow confusion." + ("%s")) % (backGreenFrontWhite, end))
		self.writeStrToFile(self.outputFileName, self.solContent, "Save data flow confusion result")
        # self.writeStrToFile(self.outputFileName, self.solContent)


#unit test
if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("wrong parameters.")
	else:
		dfo = dataflowObfuscation(sys.argv[1], sys.argv[2])
		dfo.run()
		#print(dfo.solContent)