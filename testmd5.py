import hashlib, os, sys, traceback

FILE_NAME = 'hongs_final.zip'
MD5_FILE_NAME = 'hongs_md5sum_final.txt'

def testmd5():

    try:

               chkSumValue = hashlib.md5(open(FILE_NAME, 'rb').read()).hexdigest()
    
               md5ChkSumFile = open(MD5_FILE_NAME)

               for line in md5ChkSumFile:
                    
                    data = line.split(" ")
                    
                    if data[0] != chkSumValue:
                    
                        print ( " **** md 5 values DO NOT MATCH **** ")

		    else:

                        print (" !!!!! md5 values match !!!!!!!! ")

    except:

        traceback.print_exc(file=sys.stdout)

    return

testmd5()

