import os
import sys
import logging
import traceback
import re



if __name__ == "__main__" :
    logging.basicConfig( format="[%(asctime)s][%(levelname)s][%(process)04X:%(thread)04X][%(filename)s][%(funcName)s_%(lineno)d]: %(message)s" , level=logging.DEBUG )

    if len( sys.argv ) <= 1 :
        print( "Usage: {} <path of userdb.txt>".format( os.path.basename( sys.argv[0] ) ) )
        exit( 0 )

    strFilePath = sys.argv[1]
    strFileDir , strFileFullName = os.path.split( strFilePath )
    strFileName , strFileExt = os.path.splitext( strFileFullName )
    strNewUserDbPath = "{}\\{}-new{}".format( strFileDir , strFileName , strFileExt )

    reHex = re.compile( "^([0-9a-fA-F?]{2} )+[0-9a-fA-F?]{2}$" )
    uTotalSigCnt = 0
    uInvalidSigCnt = 0
    uDuplicateCnt = 0
    uSameSigWithDiffNameCnt = 0

    with open( strFilePath , "rt" , encoding="utf8" ) as fileUserDb :
        with open( strNewUserDbPath , "wt" , encoding="utf8" ) as fileNewUserDb :
            strLine = None
            strCurrentSection = ""
            pairKeyVal = None
            bValidSection = True
            mapSigSections = dict()        #<key , value> = <signature , list of section names>

            strSecBuffer = ""
            try :
                for strLine in fileUserDb :
                    if None == strLine :
                        break
                    strLine = strLine.strip()
                    if ( 0 < len(strLine) and False == strLine.startswith( ";" ) ) :
                        if ( strLine.startswith("[") and strLine.endswith("]") ) :
                            #Flush previous section
                            if ( bValidSection != False ) :
                                fileNewUserDb.writelines( strSecBuffer )

                            #Start new section
                            uTotalSigCnt = uTotalSigCnt + 1
                            strCurrentSection = strLine[1:-1].strip()
                            strSecBuffer = ""
                            bValidSection = True
                        elif ( bValidSection == False ) :
                                continue
                        else :
                            pairKeyVal = strLine.split( '=' , 2 )
                            pairKeyVal[0] = pairKeyVal[0].strip()
                            pairKeyVal[1] = pairKeyVal[1].strip()

                            if ( pairKeyVal[0] == "signature" ) :
                                if ( reHex.match(pairKeyVal[1]) == None ) :
                                    #Check whether signature contains invalid hex value
                                    uInvalidSigCnt = uInvalidSigCnt + 1
                                    bValidSection = False
                                    strSecBuffer = ""
                                    print( "Invalid signature:\n[{}]\n{}\n".format(strCurrentSection,pairKeyVal[1]) )
                                elif ( pairKeyVal[1] in mapSigSections ) :
                                    #Check whether it's duplicate
                                    for strSecName in mapSigSections[pairKeyVal[1]] :
                                        if ( strSecName == strCurrentSection ) :
                                            uDuplicateCnt = uDuplicateCnt + 1
                                            bValidSection = False
                                            strSecBuffer = ""
                                            print( "Duplicate entry:\n[{}]\n{}\n".format(strCurrentSection,pairKeyVal[1]) )
                                            break
                                    else :
                                        uSameSigWithDiffNameCnt = uSameSigWithDiffNameCnt + 1
                                        mapSigSections[pairKeyVal[1]].append( strCurrentSection )
                                        print( "Same signature with different name:\n[{}]\n{}\n".format(pairKeyVal[1] , ",".join(mapSigSections[pairKeyVal[1]])) )
                                else :
                                    mapSigSections[pairKeyVal[1]] = list()
                                    mapSigSections[pairKeyVal[1]].append( strCurrentSection )
                                

                    if ( bValidSection != False ) :
                        strSecBuffer += strLine + "\n"

                #Flush last section
                if ( bValidSection != False ) :
                    fileNewUserDb.writelines( strSecBuffer )
                    strSecBuffer = ""
            except Exception as ex :
                print( traceback.format_exc() )
                logging.exception( ex )

    print( "Total signatures count: {}".format( uTotalSigCnt ) )
    print( "Invalid signatures removed: {}".format( uInvalidSigCnt ) )
    print( "Duplicate entries removed: {}".format( uDuplicateCnt ) )
    print( "Same signature with different name: {}".format( uSameSigWithDiffNameCnt ) )
    print( "Press any key to leave" )
    input()
 