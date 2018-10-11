"""
#######################################################################################################
Author: Aayush Kapadia,Suparshva Mehta
Project: DNA Cloud 3
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Website: www.guptalab.org/dnacloud
This file sorts out unsorted chunks according to their chunk ID. It also calculates chunk ID length(mu).
#######################################################################################################
"""

import io
import math
import ExtraModules
import os
import GolayDictionary

""" Number of irregular chunks dont exceed 4 in the worst case so we can sample some chunks until we get a chunklength which has occured at least 7 times. By this we will be able to calculate "mu" which is the chunkID size. """
""" Regular chunk consists: 1(Guard Trit) + 99(Payload Maximum) + TritForfileID(Depends on number of files but will be known probably written on the testtube) + muTrits(number of trits for chunkID, the only unknown before) + 1(parity) + 1(\n). """
""" If file size greater than 2000 then we can do this sampling heuristic to reduce time to find the GOD chunk, which is the largest otherwise do linear search to find the same till the end. This is the key to start decoding process further """
#Assumptions: We know the trits required for fileID as we know how many files are stored together.

fileIdTrits=2 #default to support upto 9 files
regularChunkSize = 0
mulength = 0
#
#	Chunk architecture of GOD chunk: 
#					 guard trit
#					 11 trits (1 byte) to get number of file name chunks
#					 2 trits to get maximum number of bytes which is required to store file size. (range =0 to 8, but interpretation 1 to 9) 
#					 next trits ( no of bytes for filesize * 11 * x, x is the minimum no such that god chunk size becomes greater than regular chunk size) 
#					 fileid trits
#					 parity trit
#					 guard trit




def getChunkId(string):
 global mulength
 #print 'Fwer',mulength
 beginningOfChunkIdFromEnd=1+1+1+mulength # 1(newline) + 1(guard) + 1(parity) + chunkid
 te = ExtraModules.getTrits(string[-1*beginningOfChunkIdFromEnd:-3], string[-1 * (beginningOfChunkIdFromEnd + 1)] )
 ans1 = ExtraModules.base3ToInt(te)
 #print string,ans1
 return ans1	
        
	
	
def compare_chunks(a,b):
	global regularChunkSize
	if len(a) > regularChunkSize:	#can be Godchunk, remember it has no chunk id
		return -1
	if len(b) > regularChunkSize:	#can be Godchunk, remember it has no chunk id
		return 1
	
	if a[0] == 'G' or a[0]=='C':
    		a=ExtraModules.reverseComplement(a)
    	if b[0] == 'G' or b[0]=='C':
    		b=ExtraModules.reverseComplement(b)
    	
    	a_chunkId=getChunkId(a)
    	b_chunkId=getChunkId(b)	
    	
    	return a_chunkId-b_chunkId	
    		
    		
    		
    			
def findChunkIdLength(fileToRead):
   fileSize=os.stat(fileToRead).st_size
   inputFile = io.open(fileToRead,"r")
   
   
   global mulength,fileIdTrits,regularChunkSize
   mulength=0
   GodChunk=''
   
   if fileSize >= 2000 : #Apply Heuristic only when fileSize is >= 2000 bytes
   	sizeDictionary=dict()
   	regularChunkSize1=0
   	
   	for chunk in inputFile:
   		chunklength=len(chunk)
		if sizeDictionary.get(chunklength) == None:
			sizeDictionary[chunklength]=1
   		else:
 			sizeDictionary[chunklength] = sizeDictionary[chunklength] + 1 
 		if sizeDictionary[chunklength]==7:
 			regularChunkSize1=chunklength
 			break
 	mulength=regularChunkSize1 - (1 + 99 + fileIdTrits + 1 + 1 + 1)
        regularChunkSize = regularChunkSize
     
 	
 	 		
   else : #otherwise try everyline
   	for chunk in inputFile:
		if len(chunk) > len(GodChunk):
			GodChunk=chunk
        #print GodChunk
	# calculating no of trits required for chunk ID, i.e. mu length
    	if GodChunk[0] == 'G' or GodChunk[0]=='C':
    		GodChunk=ExtraModules.reverseComplement(GodChunk)
    	
    	numberOfFileNameChunks = ExtraModules.base256ToInt(GolayDictionary.decodeSTR(ExtraModules.getTrits(GodChunk[1:12],'A' )))		
	noOfBytesForSize = ExtraModules.base3ToInt((ExtraModules.getTrits(GodChunk[12:14],GodChunk[11]))) # + 1 
        #print 'XCXC',noOfBytesForSize
	readTrits=noOfBytesForSize*11
        tempR = ExtraModules.getTrits(GodChunk[14:14+readTrits],GodChunk[13])
        #print tempR
	filelength=ExtraModules.base256ToInt(GolayDictionary.decodeSTR(tempR))
        #print 'BBBBBBBBBBBBBBB',filelength
	numberOfChunks=int( math.ceil(filelength/9.0) + numberOfFileNameChunks +1.0 ) #ceil apparently gives real number and not int	
        #print 'BBBBCCCCCCCCCC',numberOfChunks
	mulength=int( math.ceil( math.log(numberOfChunks,3) ) ) #number of trits required to address chunk indices
   inputFile.close()	
   return mulength   






def refine(filename,signalStatus):
        
	GolayDictionary.initDict()
	global regularChunkSize,mulength,fileIdTrits
	mulength=findChunkIdLength(filename)
	
	regularChunkSize=mulength + (1 + 99 + fileIdTrits + 1 + 1 + 1) #new line character included
	
	with io.open(filename,"r") as fileToRead, io.open(filename[:-5]+'.temp',"w") as OutputFile:
		
		fileToRead=io.open(filename,'r')
		chunks=fileToRead.readlines()
		chunks=sorted(chunks,cmp=compare_chunks)
		
		for chunk in chunks:
			if chunk[0] == 'G' or chunk[0]=='C':
    				chunk=ExtraModules.reverseComplement(chunk)
			OutputFile.write(chunk)
        return
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
