#encoding: utf-8
#-------------------------------------------------------------------------------
# Name:        scrapy
# Purpose:
# Author:      jack_mhdong
# Created:     07-09-2014
# Copyright:   (c) jack_mhdong 2014
#-------------------------------------------------------------------------------

import threading
import requests, time
from bs4 import BeautifulSoup
import os
from DayTime import DateTime

BaseDir = u'/home/jack/'

logMutex = threading.Lock()
userMutex = threading.Lock()
ThreadNum = 3

class scrapyLottery:
    def __init__(self):
        self.CODE = u'utf-8'
        self.user_agent = u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        self.headers = {u'User-Agent': self.user_agent}
        self.ProteinUrl = ''
        self.timeout= 15
        self.proxies = {}
        self.errorLogFile = BaseDir + u'Workspaces/expPPI/log/errorOfScrapyProteinGene.log'
        self.lotteryDir = BaseDir + u'local/lotteryTickets'
        
    def setLotteryUrl(self, dateTime):
        self.dateTime = dateTime
        ## http://chart.cp.360.cn/kaijiang/kaijiang?lotId=255401&spanType=2&span=2014-12-02_2014-12-02
        baseUrl = u'http://chart.cp.360.cn/kaijiang/kaijiang?lotId=255401&spanType=2&span=%s'
        self.lotteryUrl = baseUrl % (self.dateTime + "_" + self.dateTime)
        pass
    
    def getLotteryDataFromURL(self):
        ## KeyWrod: Official lotteryDate
        ## get FullProtein Name, short names/GeneName Official Name, alias name/Organism
        soup = self.getLotteryDetails()
        if soup is None:
            warnInfo = '[%s]. requests is not Existed.\n' % (self.dateTime)
            self.writeErrorMsgIntoLog(warnInfo)
            return None
        names_and_taxonomy = soup.find('div', class_='history-tab')
        ##################################################
        print names_and_taxonomy.prettify()
        # Protein Official Name
        SummaryProteinInfo = ""
        if names_and_taxonomy is not None:
            table = names_and_taxonomy.find('table')
            
            classLabels = ['tr-odd1', 'tr-odd2', 'tr-odd3']
            ####################################################################
            for classLb in classLabels:
                TrCurContents = table.find('table', class_=classLb)
                ## print table.prettify()
                divProteinNames = TrCurContents.find('tbody')
            
                if ((table is not None) and (divProteinNames is not None)):
                ##################################################
                ## recommended name
                    recommended_nameSpan = divProteinNames.findAll('tr')
                    k = 0
                    curNameSpan = recommended_nameSpan[k]
                    while (curNameSpan != None):
                        for tdContent in curNameSpan.contents:
                            recommended_name = tdContent.get_text()
                            SummaryProteinInfo += recommended_name + "\t"
                        ##################################################
                        ## changed to next 'div' Tag
                        k += 1
                        if (k >= len(recommended_nameSpan)):
                            break
                        curNameSpan = recommended_nameSpan[k]
                        SummaryProteinInfo = SummaryProteinInfo.strip() + "\n"
                    SummaryProteinInfo += "\n"
            ##################################################
        else:
            warnInfo = '[%s]. Warn Message. Non Existed.\n' % (self.dateTime)
            self.writeErrorMsgIntoLog(warnInfo)
            return None
        return SummaryProteinInfo.strip()
    
    def getLotteryDetails(self):
        openUrlCount = 1
        RequestFlag = True
        while RequestFlag:
            try:
                response = requests.get(self.lotteryUrl,
                                headers = self.headers,
                                timeout=self.timeout)
            except requests.exceptions.Timeout as e:
                # Maybe set up for a retry, or continue in a retry loop
                time.sleep(3)
                errorInfo = '[%s]. Error Message[%s]\n' % (self.lotteryUrl, e)
                if (openUrlCount <= 5):
                    print("[%d times][%s]Try again. [%s]" % (openUrlCount, self.getLotteryTime(), errorInfo))
                    openUrlCount += 1
                    continue
                self.writeErrorMsgIntoLog(errorInfo)
                # ---------------------
                # raise ConnectionError(e) ConnectionError: Write into log file
                # ---------------------
                RequestFlag = False
                pass
            except requests.exceptions.TooManyRedirects as e:
                # Tell the user their URL was bad and try a different one
                errorInfo = '[%s]. Error Message[%s]\n' % (self.lotteryUrl, e)
                if (openUrlCount <= 5):
                    print("[%d times][%s]Try again. [%s]" % (openUrlCount, self.getLotteryTime(), errorInfo))
                    openUrlCount += 1
                    continue
                self.writeErrorMsgIntoLog(errorInfo)
                # ---------------------
                # raise ConnectionError(e) ConnectionError: Write into log file
                # ---------------------
                RequestFlag = False
                pass
            except requests.exceptions.RequestException as e:
                errorInfo = '[%s]. Error Message[%s]\n' % (self.lotteryUrl, e)
                if (openUrlCount <= 5):
                    print("[%d times][%s]Try again. [%s]" % (openUrlCount, self.getLotteryTime(), errorInfo))
                    openUrlCount += 1
                    continue
                self.writeErrorMsgIntoLog(errorInfo)
                # ---------------------
                # raise ConnectionError(e) ConnectionError: Write into log file
                # ---------------------
                RequestFlag = False
                pass
            else:
                soup = BeautifulSoup(response.content)
                return soup
            pass
        return None
    
    def getLotteryInfo(self, lotteryDate, resetLotterySet):
        self.setLotteryUrl(lotteryDate)
        tryConnTimes = 1
        proteinAllInfo = self.getLotteryDataFromURL()
        while (proteinAllInfo is None and tryConnTimes <= 3):
            proteinAllInfo = self.getLotteryDataFromURL()
            tryConnTimes += 1
            pass
        # ---------------------
        ### unicode exchange
        # ---------------------
        if proteinAllInfo is not None:
            HeadLine = u"# 期号\t开奖号\t十位\t个位\t后三\n"
            proteinAllInfo = HeadLine + proteinAllInfo
            writeFilePath = self.lotteryDir + os.sep + self.dateTime
            print proteinAllInfo
            #self.writeUserMsgIntoFile(proteinAllInfo.encode('utf-8'), writeFilePath, 'w')
            return proteinAllInfo
        else:
            resetLotterySet.add(lotteryDate)
        return None
    
    def writeErrorMsgIntoLog(self, errorInfo):
        if (logMutex.acquire(2)):
            error_msg_c = open(self.errorLogFile, 'a')
            error_msg_c.write(errorInfo)
            error_msg_c.close()
            logMutex.release()
            pass
        
    def writeUserMsgIntoFile(self, userMsg, filePath, mode):
        if (userMutex.acquire(2)):
            user_msg_c = open(filePath, mode)
            user_msg_c.write(userMsg)
            user_msg_c.close()
            userMutex.release()
            pass
    
    def getLotteryTime(self):
        return self.dateTime
        
    def initAllData(self):
        if (os.path.exists(self.errorLogFile)):
            os.remove(self.errorLogFile)

def getAllLottery(srcFile):
    scrapyPG = scrapyLottery()
    scrapyPG.initAllData()
    
    '''2014-01-01_2014-01-01 TO 2014-11-30_2014-11-30'''
    BeginDateTime = DateTime(2012, 1, 25)
    DeadLineDateTime = DateTime(2012, 1, 26)
    
    curDateTime = BeginDateTime
    resetLotterySet = set()
    while curDateTime.getCurStrOfCurDayTime() != DeadLineDateTime.getCurStrOfCurDayTime():
        lotteryDateTime = curDateTime.getCurStrOfCurDayTime()
        scrapyPG.getLotteryInfo(lotteryDateTime, resetLotterySet)
        curDateTime.increOneDay()
        pass
    ## keep saving the release lottery.
    if (len(resetLotterySet) > 0):
        AllInvalidProteins = "# lotteryDate"
        processingFileStr = ''
        for lotteryDate in resetLotterySet:
            AllInvalidProteins += "\n" + lotteryDate
            processingFileStr += lotteryDate + ", "
            pass
        print("-"*20)
        print("But release some error lottery: %s" % processingFileStr)
        ## warnLogFile = BaseDir + u'Workspaces/expPPI/data/warningOfscrapyProteinGene.log'
        warnLogFile = BaseDir + u'Workspaces/expPPI/data/warningOfscrapyProteinGene.log'
        WriteConn = open(warnLogFile, 'w')
        WriteConn.write(AllInvalidProteins)
        WriteConn.close()
    print("Finished all lottery processing.\n")

def main():
    srcProteinFile = BaseDir + u'Workspaces/expPPI/data/UniqueProteinName_201108.intm'
    #srcProteinFile = BaseDir + u'UniqueProteinName_201108.intm'
    ##writeLogFile = BaseDir + u'Workspaces/expPPI/data/proteinGene_201108.intm'
    getAllLottery(srcProteinFile)

    #scrapyPG = scrapyLottery()
    #lotteryDate = scrapyPG.getLotteryInfo("P30085") ## P62988 P30085 P03897 Q9UKV8 O95232
    #print(lotteryDate)

if __name__ == '__main__':
    main()