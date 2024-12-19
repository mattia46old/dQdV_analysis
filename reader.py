'''
it needs shebang #!/home/mattia/mypyvenv/bin/python3 if I plan not to use jupyter notebook to import this class
the jupyter kernel environment is the same as /home/mattia/mypyvenv/bin/python3 
'''

from galvani import BioLogic
import pandas as pd, os


class MultipleFiles:
    def __init__(self, files):
        self.f = files # we hold the hole file list


    
    def readFile(self):
        '''
        it loads the BioLogic file by using galvani library
        '''
        self.dic = {}
        for n,i in enumerate(self.f):
            self.read = BioLogic.MPRfile(i).data
            self.df = pd.DataFrame(self.read)
            self.dic[f"{self.f}"] = self.df
        return self.dic
            

            

class SingleFile:
    def __init__(self, file):
        self.f = file # we hold the path in the class construnctor


    def readFile(self):
        '''
        it loads the BioLogic file by using galvani library
        '''
        self.read = BioLogic.MPRfile(self.f).data
        self.dataFrame = pd.DataFrame(self.read)
        return self.dataFrame
     
    def extractCycles(self, dataframe, cycle_ch, cycle_disch): #in dataframe we can call readFile()
        '''
        this method extracts each cycle indipendently putting it in an csv file.

        According to log in LN&B_FC+LTC_CA5.mpr, Ns= 1 corresponds to first charge cycles, whereas 4 to first discharge. 
        Same for Ns=7 and Ns= 10. The program loops on 7 and 10 where we find most of the cycles. 
        So no need to extract Ns=1 and 4.
        from LN1B_LTC_ESRF_continue_C03.mpr on Ns = 1, Ns = 4 discharge
        '''

        self.r = dataframe
        self.label = self.f.split("/")[-1].split(".")[0]
        self.max_cycle = max(self.r["half cycle"])
        # check if output folder exists, otherwise create it!
        if os.path.exists("output/") == True:
            print("folder output exists\nextraction started...")
        else :
            os.makedirs("output/")
            print("folder didn't exit, created!\nextraction started...")
        
        self.counter = 0 #needed for labels during the extraction
        for i in range(0, self.max_cycle, 1):
            self.filterdf = self.r.loc[(self.r["Ns"] == cycle_ch) & (self.r["half cycle"] == i)]
            if self.filterdf.empty == False:
                self.filterdf.to_csv(f"output/{self.label}_{self.counter}_charge.csv", index=False)
                self.counter += 1


        self.counter = 0 #needed for the labels during extraction
        for i in range(0, self.max_cycle, 1):
            self.filterdf = self.r.loc[(self.r["Ns"] == cycle_disch) & (self.r["half cycle"] == i)]
            if self.filterdf.empty == False:
                self.filterdf.to_csv(f"output/{self.label}_{self.counter}_discharge.csv", index=False)
                self.counter += 1