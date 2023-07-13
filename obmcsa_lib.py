#!/usr/bin/env python3
#MIT License

#Copyright (c) 2023 hramacha

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

import os 
from pathlib import Path

OBMC_SRC_DIR = ""
obmcYactoAnalyzerData = None

def AnalyzeOpenBMCSourceMain():
    global OBMC_SRC_DIR
    global obmcYactoAnalyzerData

    # Set the OpenBMC Source Directory 
    OBMC_SRC_DIR = input("Provide the OpenBMC Source Directory Path : ")
    # Check if the directory is valid
    if os.path.exists(OBMC_SRC_DIR):
        obmcYactoAnalyzerData = ObmcYactoAnalyzerClass(OBMC_SRC_DIR)
        obmcYactoAnalyzerData.AnalyzeOpenBMCSource()
        return obmcYactoAnalyzerData
    else:
        exit()   

# DataType Classes
class DataTypeElementClass:
    def __init__(self, f, attrib):
        self.file = f
        self.Attribute = attrib
        self.InitializedString = None
        self.AssignedString = []

class ExtractFileLinesClass:
    def __init__(self, f):
        self.file = f
        self.Filelines = []
        self.fileReader = open(self.file, "r")
        self.Filelines = self.fileReader.readlines()
        self.fileReader.close()

class PackageConfigDataClass:
    def __init__(self):
        self.ConfigParam = ""
        self.OptionList = []

class PackageGroupDataElementClass:
    def __init__(self):
        self.PackageName = ""
        self.Description = ""
        self.DependList = []
    
    def PrintElements(self):
        print("\tPackage Name = ", self.PackageName, "Description = ", self.Description, "Depends = ", self.DependList)

class ParameterDataClass:
    def __init__(self, type, atype, param, value):
        self.Type = type
        self.AssignmentType = atype
        self.index = -1
        self.Parameter = param 
        self.Value = value
        self.MultiValue = []
    
    def PrintParamData(self):
        if self.Value != None:
            print("\t",self.Parameter, " = ", self.Value)
        else:
            print("\t",self.Parameter, " = ", self.MultiValue)
            
class ParameterRecordClass:
    def __init__(self, param):
        self.Parameter = param 
        self.DefaultValueList = []
        self.WeakValueList = []
        self.ParamDataList = []

# Functional Classes 

class ObmcYactoAnalyzerClass:
    def __init__(self, openbmcbase):
        self.BmcDirList = ["meta-aspeed", "meta-nuvoton"]
        self.ProcDirList = ["meta-amd", "meta-arm", "meta-intel"]
        self.GlobalPackageElementList = []
        self.GlobalDataCollectionList = []
        self.GlobalBBDataCollectionList = []
        self.GlobalINCDataCollectionList = []
        self.GlobalBBClassDataCollectionList = []
        self.GlobalConfDataCollectionList = []
        self.GlobalOpenBMCMachineList = []
        self.GlobalOpenBMCNonSupportedMachineList = []
        self.YoctoVariableTypesDict = None
        self.BMCMetaList = []
        self.ProcMetaList = []
        self.PlatformMetaList = []
        self.OpenBMCPhosphorMeta = None
        self.OpenBMCSecurityMeta = None
        self.OpenBMCOeMeta = None
        self.OpenBMCPokyMeta = None
        self.OpenBMCBaseFile = openbmcbase
    
    def PrintGlobalData(self):
        print(" OpenBMC Source Analysis :")
        print(" Total Packages Found                       = ", len(self.GlobalPackageElementList))
        print(" Total Data Collected                       = ", len(self.GlobalDataCollectionList))
        print(" Total Bitbake Recipes Found                = ", len(self.GlobalBBDataCollectionList))
        print(" Total Bitbake Includes Found               = ", len(self.GlobalINCDataCollectionList))
        print(" Total Bitbake Classes Found                = ", len(self.GlobalBBClassDataCollectionList))
        print(" Total Bitbake Conf Found                   = ", len(self.GlobalConfDataCollectionList))


    def CheckForProc(self, entry):
        for p in self.ProcDirList:
            if p in entry.name:
                return True
        
        return False

    def AnalyzeOpenBMCSource(self):
        self.YoctoVariableTypesDict = YoctoVariableTypesClass(self.OpenBMCBaseFile)
        if os.path.exists(self.OpenBMCBaseFile) == False:
            print("OpenBMC base does not exist \n")
            return

        obj = os.scandir(self.OpenBMCBaseFile)
        for entry in obj:
            if entry.is_dir():
                #if "poky" in entry.name:
                #   self.OpenBMCPokyMeta = MetaDataElementClass(entry, "poky")           
                if "meta-phosphor" in  entry.name:
                    self.OpenBMCPhosphorMeta = MetaDataElementClass(self, entry, "phosphor")                
                elif "meta-openembedded" in  entry.name: 
                    self.OpenBMCOeMeta = MetaDataElementClass(self, entry, "openembedded");                
                elif entry.name in self.BmcDirList:
                    mdata = MetaDataElementClass(self, entry, "bmc-"+entry.name.replace("meta-",""))
                    self.BMCMetaList.append(mdata)
                elif self.CheckForProc(entry):
                    mdata = MetaDataElementClass(self, entry, "proc-"+entry.name.replace("meta-",""))
                    self.ProcMetaList.append(mdata)
                elif "meta-security" in entry.name:
                    self.OpenBMCSecurityMeta = MetaDataElementClass(self, entry, entry.name.replace("meta-",""))
                elif  entry.name.startswith("meta-"):
                    mdata = MetaDataElementClass(self, entry, "platform-"+entry.name.replace("meta-",""))
                    self.PlatformMetaList.append(mdata)

        #print("\r\nFile,Name,Type,FileName,RC,PC,RL,RRL,INCL,INCRL,INHL,INHRL,INHCL,INHCRL")
        #fanalysis = FilePatternAnalysisClass()
        #for i in range(0, len(fanalysis.DelimiterPrintTypeList)):
        #    print(fanalysis.DelimiterPrintTypeList[i], end=",")
        #print("")
        #self.OpenBMCPokyMeta.CollectDataFiles();
        self.OpenBMCPhosphorMeta.CollectDataFiles()
        self.OpenBMCOeMeta.CollectDataFiles();        
        self.OpenBMCSecurityMeta.CollectDataFiles();        

        for mde in self.BMCMetaList:
            mde.CollectDataFiles()

        for mde in self.ProcMetaList:
            mde.CollectDataFiles()

        for mde in self.PlatformMetaList:
            mde.CollectDataFiles()
        
        # Linking files 
        self.LinkMetaFiles()
    
    def PrintMetaInfo(self, metainfo, option, fmt):
        if metainfo == "Base":
            self.OpenBMCPhosphorMeta.PrintMetaData(option, fmt)
        elif metainfo == "Security":
            self.OpenBMCSecurityMeta.PrintMetaData(option, fmt)
        elif metainfo.startswith("bmc-"):
            for mde in self.BMCMetaList:
                if mde.Type == metainfo:
                    mde.PrintMetaData(option, fmt)
        elif metainfo.startswith("proc-"):
            for mde in self.ProcMetaList:
                if mde.Type == metainfo:
                    mde.PrintMetaData(option, fmt)
        elif metainfo.startswith("platform-"):
            for mde in self.PlatformMetaList:
                if mde.Type == metainfo:
                    mde.PrintMetaData(option, fmt)

    def GetMetaInfo(self, metainfo):
        if metainfo == "Base":
            return self.OpenBMCPhosphorMeta
        elif metainfo == "Security":
            return self.OpenBMCSecurityMeta
        elif metainfo.startswith("bmc-"):
            for mde in self.BMCMetaList:
                if mde.Type == metainfo:
                    return mde
        elif metainfo.startswith("proc-"):
            for mde in self.ProcMetaList:
                if mde.Type == metainfo:
                    return mde
        elif metainfo.startswith("platform-"):
            for mde in self.PlatformMetaList:
                if mde.Type == metainfo:
                    return mde
        return None
    

    def PrintLegends(self):
        print("List of Acronyms and short representations used in the Stats and Info")
        print("PKGLst     = Package Group List")
        print("MCDLst     = Machine Data List")
        print("BBDLst     = BB Data List")
        print("INCDLst    = Include Data List")
        print("BBClDLst   = BBClass Data List")
        print("CnfDLst    = Conf Data List")
        print("BBFLst     = BB File List")
        print("INCFLst    = Include File List")
        print("BBClFLst   = BBClass File List")
        print("CnfFLst    = Conf File List")
        print("MCCnfFLst  = Machine Conf File List")
        print("CnfNtsFLst = Conf Notes File List")
        print("SvcsFLst   = Services File List")

              
    def PrintStats(self):

        print("{: <64} {: ^6} {: ^6} {: ^6} {: ^7} {: ^8} {: ^7} {: ^6} {: ^7} {: ^8} {: ^7} {: ^9} {: ^10} {: ^8}" .format(\
            "Meta Name",\
            "PKGLst",\
            "MCDLst",\
            "BBDLst",\
            "INCDLst",\
            "BBClDLst",\
            "CnfDLst",\
            "BBFLst",\
            "INCFLst",\
            "BBClFLst",\
            "CnfFLst",\
            "MCCnfFLst",\
            "CnfNtsFLst",\
            "SvcsFLst"))

        print("{: <64} {: ^6} {: ^6} {: ^6} {: ^7} {: ^8} {: ^7} {: ^6} {: ^7} {: ^8} {: ^7} {: ^9} {: ^10} {: ^8}" .format(\
            "Base", \
            len(self.OpenBMCPhosphorMeta.PackageGroupList),\
            len(self.OpenBMCPhosphorMeta.MachineDataList),\
            len(self.OpenBMCPhosphorMeta.BBDataList),\
            len(self.OpenBMCPhosphorMeta.INCDataList),\
            len(self.OpenBMCPhosphorMeta.BBClassDataList),\
            len(self.OpenBMCPhosphorMeta.ConfDataList),\
            len(self.OpenBMCPhosphorMeta.BBFileList),\
            len(self.OpenBMCPhosphorMeta.INCFileList),\
            len(self.OpenBMCPhosphorMeta.BBClassFileList),\
            len(self.OpenBMCPhosphorMeta.ConfFileList),\
            len(self.OpenBMCPhosphorMeta.MachineConfFileList),\
            len(self.OpenBMCPhosphorMeta.ConfNotesFileList),\
            len(self.OpenBMCPhosphorMeta.ServicesFileList)))

        print("{: <64} {: ^6} {: ^6} {: ^6} {: ^7} {: ^8} {: ^7} {: ^6} {: ^7} {: ^8} {: ^7} {: ^9} {: ^10} {: ^8}" .format(\
            "Security", \
            len(self.OpenBMCSecurityMeta.PackageGroupList),\
            len(self.OpenBMCSecurityMeta.MachineDataList),\
            len(self.OpenBMCSecurityMeta.BBDataList),\
            len(self.OpenBMCSecurityMeta.INCDataList),\
            len(self.OpenBMCSecurityMeta.BBClassDataList),\
            len(self.OpenBMCSecurityMeta.ConfDataList),\
            len(self.OpenBMCSecurityMeta.BBFileList),\
            len(self.OpenBMCSecurityMeta.INCFileList),\
            len(self.OpenBMCSecurityMeta.BBClassFileList),\
            len(self.OpenBMCSecurityMeta.ConfFileList),\
            len(self.OpenBMCSecurityMeta.MachineConfFileList),\
            len(self.OpenBMCSecurityMeta.ConfNotesFileList),\
            len(self.OpenBMCSecurityMeta.ServicesFileList)))

        print("")
        for mde in self.BMCMetaList:
            print("{: <64} {: ^6} {: ^6} {: ^6} {: ^7} {: ^8} {: ^7} {: ^6} {: ^7} {: ^8} {: ^7} {: ^9} {: ^10} {: ^8}" .format(\
                mde.Type, \
                len(mde.PackageGroupList),\
                len(mde.MachineDataList),\
                len(mde.BBDataList),\
                len(mde.INCDataList),\
                len(mde.BBClassDataList),\
                len(mde.ConfDataList),\
                len(mde.BBFileList),\
                len(mde.INCFileList),\
                len(mde.BBClassFileList),\
                len(mde.ConfFileList),\
                len(mde.MachineConfFileList),\
                len(mde.ConfNotesFileList),\
                len(mde.ServicesFileList)))
        print("")
        for mde in self.ProcMetaList:
            print("{: <64} {: ^6} {: ^6} {: ^6} {: ^7} {: ^8} {: ^7} {: ^6} {: ^7} {: ^8} {: ^7} {: ^9} {: ^10} {: ^8}" .format(\
                mde.Type, \
                len(mde.PackageGroupList),\
                len(mde.MachineDataList),\
                len(mde.BBDataList),\
                len(mde.INCDataList),\
                len(mde.BBClassDataList),\
                len(mde.ConfDataList),\
                len(mde.BBFileList),\
                len(mde.INCFileList),\
                len(mde.BBClassFileList),\
                len(mde.ConfFileList),\
                len(mde.MachineConfFileList),\
                len(mde.ConfNotesFileList),\
                len(mde.ServicesFileList)))
        print("")
        for mde in self.PlatformMetaList:
            print("{: <64} {: ^6} {: ^6} {: ^6} {: ^7} {: ^8} {: ^7} {: ^6} {: ^7} {: ^8} {: ^7} {: ^9} {: ^10} {: ^8}" .format(\
                mde.Type, \
                len(mde.PackageGroupList),\
                len(mde.MachineDataList),\
                len(mde.BBDataList),\
                len(mde.INCDataList),\
                len(mde.BBClassDataList),\
                len(mde.ConfDataList),\
                len(mde.BBFileList),\
                len(mde.INCFileList),\
                len(mde.BBClassFileList),\
                len(mde.ConfFileList),\
                len(mde.MachineConfFileList),\
                len(mde.ConfNotesFileList),\
                len(mde.ServicesFileList)))
    
    def LinkMetaFiles(self):

        for obmcdc in self.GlobalDataCollectionList:
            if len(obmcdc.RequireList) > 0:
                for require in obmcdc.RequireList:
                    obmc_dc = None
                    if "/" in require.Value:
                        obmc_dc = self.GetDataCollection(require.Value.split("/")[len(require.Value.split("/")) -1])
                    else:
                         obmc_dc = self.GetDataCollection(require.Value)

                    if obmc_dc != None:
                        obmcdc.RequireReferenceList.append(obmc_dc)

            if len(obmcdc.IncludeList) > 0:
                for include in obmcdc.IncludeList:
                    obmc_dc = None
                    if "/" in include.Value:
                        obmc_dc = self.GetDataCollection(include.Value.split("/")[len(include.Value.split("/")) -1])
                    else:
                         obmc_dc = self.GetDataCollection(include.Value)

                    if obmc_dc != None:
                        obmcdc.IncludeReferenceList.append(obmc_dc)
    
    def GetDataCollection(self, filename):
        for obmcdc in self.GlobalDataCollectionList:
            if obmcdc.file.name.endswith(filename): 
                return obmcdc

        return None

class MetaDataElementClass:    
    def __init__(self,analyzer,  f, type):
        self.ObmcYactoAnalyzer = analyzer
        self.MetaFile = f
        self.Type = type
        self.PackageGroupList = []
        self.MachineDataList = []
        self.BBDataList = []
        self.INCDataList = []
        self.MCINCDataList = []
        self.BBClassDataList = []
        self.ConfDataList = []
        self.BBFileList = []
        self.INCFileList = []
        self.BBClassFileList = []
        self.ConfFileList = []
        self.MachineConfFileList = []
        self.ConfNotesFileList = []
        self.ServicesFileList = []

    def PrintDataCollectionInfo(self, type, idx, dtype):
        if type == "bb":
            meta = self.BBDataList[idx]
            meta.PrintDataCollection(dtype)                        
        if type == "inc":
            meta = self.INCDataList[idx]
            meta.PrintDataCollection(dtype)                        
        if type == "bbclass":
            meta = self.BBClassDataList[idx]
            meta.PrintDataCollection(dtype)                        
        if type == "conf":
            meta = self.ConfDataList[idx]
            meta.PrintDataCollection(dtype)                        

    def PrintMetaData(self, option, fmt):
        pkgdatatype = False
        bbdatatype = False
        incdatatype = False
        bbclassdatatype = False
        confdatatype = False

        print("\n")
        if option == "": 
            pkgdatatype = True
            bbdatatype = True
            incdatatype = True
            bbclassdatatype = True
            confdatatype = True
        elif option == "pkg":
            pkgdatatype = True
        elif option == "bb":
            bbdatatype = True
        elif option == "inc":
            incdatatype = True
        elif option == "bbclass":
            bbclassdatatype = True
        elif option == "conf":
            confdatatype = True

        if pkgdatatype == True:
            if len(self.PackageGroupList) > 0:
                print("Package Group Information: ")
                for pkg in self.PackageGroupList:
                    pkg.PrintPackageGroupData()
            else:
                print("Package Group Information: None ")

        if bbdatatype == True:
            if len(self.BBDataList) > 0:
                print("BB Information: ")
                print("{: ^8} {: <64} {: ^7} {: ^8} {: ^6} {: ^9} {: ^6} {: ^9} {: ^10} {: ^13} {: ^11} {: ^9} {: ^11}" .format(\
                    "Index", "File Name", "YoctoVL",\
                    "ParamLst",\
                    "ReqLst",\
                    "ReqRefLst",\
                    "IncLst",\
                    "IncRefLst",\
                    "InheritLst",\
                    "InheritRefLst",\
                    "PrefProvLst",\
                    "VirtRTLst",\
                    "ParamRecLst"))

                for meta in self.BBDataList:
                    if fmt == True:
                        metafilename = os.path.abspath(meta.file).replace(os.path.abspath(self.MetaFile), "")
                        print(metafilename+":")
                    print("{: ^8} {: <64} {: ^7} {: ^8} {: ^6} {: ^9} {: ^6} {: ^9} {: ^10} {: ^13} {: ^11} {: ^9} {: ^11}" .format(\
                        self.BBDataList.index(meta),\
                        meta.file.name,\
                        len(meta.YoctoList),\
                        len(meta.ParamList),\
                        len(meta.RequireList),\
                        len(meta.RequireReferenceList),\
                        len(meta.IncludeList),\
                        len(meta.IncludeReferenceList),\
                        len(meta.InheritList),\
                        len(meta.InheritReferenceList),\
                        len(meta.PreferredProviderList),\
                        len(meta.VirtualRuntimeList),\
                        len(meta.ParameterRecordList)))
            else:
                print("BB Information : None")

        if incdatatype == True:
            if len(self.INCDataList) > 0:
                print("\nIncluding Files  Information: ")

                print("{: ^8} {: <64} {: ^7} {: ^8} {: ^6} {: ^9} {: ^6} {: ^9} {: ^10} {: ^13} {: ^11} {: ^9} {: ^11}" .format(\
                    "Index", "File Name", "YoctoVL",\
                    "ParamLst",\
                    "ReqLst",\
                    "ReqRefLst",\
                    "IncLst",\
                    "IncRefLst",\
                    "InheritLst",\
                    "InheritRefLst",\
                    "PrefProvLst",\
                    "VirtRTLst",\
                    "ParamRecLst"))

                for meta in self.INCDataList:
                    if fmt == True:
                        metafilename = os.path.abspath(meta.file).replace(os.path.abspath(self.MetaFile), "")
                        print(metafilename+":")
                    print("{: ^8} {: <64} {: ^7} {: ^8} {: ^6} {: ^9} {: ^6} {: ^9} {: ^10} {: ^13} {: ^11} {: ^9} {: ^11}" .format(\
                        self.INCDataList.index(meta),\
                        meta.file.name,\
                        len(meta.YoctoList),\
                        len(meta.ParamList),\
                        len(meta.RequireList),\
                        len(meta.RequireReferenceList),\
                        len(meta.IncludeList),\
                        len(meta.IncludeReferenceList),\
                        len(meta.InheritList),\
                        len(meta.InheritReferenceList),\
                        len(meta.PreferredProviderList),\
                        len(meta.VirtualRuntimeList),\
                        len(meta.ParameterRecordList)))
            else:
                print("Including Files : None")

        if bbclassdatatype == True:
            if len(self.BBClassDataList) > 0:
                print("BB Class Files Information: ")

                print("{: ^8} {: <64} {: ^7} {: ^8} {: ^6} {: ^9} {: ^6} {: ^9} {: ^10} {: ^13} {: ^11} {: ^9} {: ^11}" .format(\
                    "Index", "File Name", "YoctoVL",\
                    "ParamLst",\
                    "ReqLst",\
                    "ReqRefLst",\
                    "IncLst",\
                    "IncRefLst",\
                    "InheritLst",\
                    "InheritRefLst",\
                    "PrefProvLst",\
                    "VirtRTLst",\
                    "ParamRecLst"))

                for meta in self.BBClassDataList:   
                    if fmt == True:
                        metafilename = os.path.abspath(meta.file).replace(os.path.abspath(self.MetaFile), "")
                        print(metafilename+":")
                    print("{: ^8} {: <64} {: ^7} {: ^8} {: ^6} {: ^9} {: ^6} {: ^9} {: ^10} {: ^13} {: ^11} {: ^9} {: ^11}" .format(\
                        self.BBClassDataList.index(meta),\
                        meta.file.name,\
                        len(meta.YoctoList),\
                        len(meta.ParamList),\
                        len(meta.RequireList),\
                        len(meta.RequireReferenceList),\
                        len(meta.IncludeList),\
                        len(meta.IncludeReferenceList),\
                        len(meta.InheritList),\
                        len(meta.InheritReferenceList),\
                        len(meta.PreferredProviderList),\
                        len(meta.VirtualRuntimeList),\
                        len(meta.ParameterRecordList)))
            else:
                print("BB Class Files : None")

        if confdatatype == True:
            if len(self.ConfDataList) > 0:

                print("Conf Data Files Information: ")

                print("{: ^8} {: <64} {: ^7} {: ^8} {: ^6} {: ^9} {: ^6} {: ^9} {: ^10} {: ^13} {: ^11} {: ^9} {: ^11}" .format(\
                    "Index", "File Name", "YoctoVL",\
                    "ParamLst",\
                    "ReqLst",\
                    "ReqRefLst",\
                    "IncLst",\
                    "IncRefLst",\
                    "InheritLst",\
                    "InheritRefLst",\
                    "PrefProvLst",\
                    "VirtRTLst",\
                    "ParamRecLst"))

                for meta in self.ConfDataList:         
                    if fmt == True:
                        metafilename = os.path.abspath(meta.file).replace(os.path.abspath(self.MetaFile), "")
                        print(metafilename+":")
                    print("{: ^8} {: <64} {: ^7} {: ^8} {: ^6} {: ^9} {: ^6} {: ^9} {: ^10} {: ^13} {: ^11} {: ^9} {: ^11}" .format(\
                        self.ConfDataList.index(meta),\
                        meta.file.name,\
                        len(meta.YoctoList),\
                        len(meta.ParamList),\
                        len(meta.RequireList),\
                        len(meta.RequireReferenceList),\
                        len(meta.IncludeList),\
                        len(meta.IncludeReferenceList),\
                        len(meta.InheritList),\
                        len(meta.InheritReferenceList),\
                        len(meta.PreferredProviderList),\
                        len(meta.VirtualRuntimeList),\
                        len(meta.ParameterRecordList)))
            else:
                print("Conf Data Files : None")

    def CollectDataFiles(self):
        self.CollectData(self.MetaFile)
    
    def CollectData(self, dirFile):
        obj = os.scandir(dirFile)
        for entry in obj:
            if entry.is_dir():
                self.CollectData(entry)
                continue
            else:
                if entry.name.endswith('.bb'):
                    self.BBFileList.append(entry)
                    mdata = OpenBMCDataCollectionClass(self, "BB", entry)
                    mdata.ProcessMachineData()
                    self.BBDataList.append(mdata)
                    self.ObmcYactoAnalyzer.GlobalDataCollectionList.append(mdata)
                    self.ObmcYactoAnalyzer.GlobalBBDataCollectionList.append(mdata)
                    if "packagegroups" in str(Path(entry).absolute()):
                        pgdata = PackageGroupDataClass(self.ObmcYactoAnalyzer,entry)
                        self.PackageGroupList.append(pgdata)
                        pgdata.ProcessPackageData()
                if entry.name.endswith('.inc'):
                    self.INCFileList.append(entry)
                    mdata = OpenBMCDataCollectionClass(self, "INC", entry)
                    mdata.ProcessMachineData()
                    self.INCDataList.append(mdata)
                    self.ObmcYactoAnalyzer.GlobalDataCollectionList.append(mdata)
                    self.ObmcYactoAnalyzer.GlobalINCDataCollectionList.append(mdata)
                    if "machine" in str(Path(entry).absolute()) and "include" in str(Path(entry).absolute()):
                        self.MCINCDataList.append(mdata)                        
                if entry.name.endswith('.bbclass'):
                    self.BBClassFileList.append(entry)
                    mdata = OpenBMCDataCollectionClass(self, "BBCLASS", entry)
                    mdata.ProcessMachineData()
                    self.BBClassDataList.append(mdata)
                    self.ObmcYactoAnalyzer.GlobalDataCollectionList.append(mdata)
                    self.ObmcYactoAnalyzer.GlobalBBClassDataCollectionList.append(mdata)
                if entry.name.endswith('.conf'):
                    self.ConfFileList.append(entry)
                    mdata = OpenBMCDataCollectionClass(self, "CONF", entry)
                    mdata.ProcessMachineData()
                    self.ConfDataList.append(mdata)
                    self.ObmcYactoAnalyzer.GlobalDataCollectionList.append(mdata)
                    self.ObmcYactoAnalyzer.GlobalConfDataCollectionList.append(mdata)
                    if "machine" in str(Path(entry).absolute()):
                        self.MachineDataList.append(mdata)
                if entry.name.startswith('conf-notes'):
                    self.ConfNotesFileList.append(entry)
                if entry.name.endswith('.service'):
                    self.ServicesFileList.append(entry)



class OpenBMCDataCollectionClass:
    def __init__(self, mData, type, f):
        self.Summary = None
        self.Description = None
        self.MetaParent = mData
        self.Type = type
        self.file = f
        self.YoctoList = []
        self.ParamList = []
        self.RequireList = []
        self.RequireReferenceList = []

        self.IncludeList = []
        self.IncludeReferenceList = []
        
        self.InheritList = []
        self.InheritReferenceList = []
        self.PackageConfigList = []

        self.INHERITConfList = []
        self.InheritConfReferenceList = []
        self.PreferredProviderList = []
        self.VirtualRuntimeList = []
        self.ParameterRecordList = []
        self.PN = None
        self.PV = None
        self.FileExtractData = None
        self.DelimiterCountArray = []

        if self.file.name.endswith(".bb"):
            if len(self.file.name.split(".")) > 1:
                if len(self.file.name.split(".")[0].split("_")) > 1:
                    self.PN = self.file.name.split(".")[0].split("_")[0]
                    self.PV = self.file.name.split(".")[0].split("_")[1]

    def ProcessMachineData(self):
        
        if os.path.exists(self.file) == False:
             return
        
        FileExtractData = ExtractFileLinesClass(self.file)
        self.FileExtractData = FileExtractData
        
        if self.PN != None or self.PV != None:
            for index in range(0, len(FileExtractData.Filelines)):
                if self.PN != None:
                    if "${PN}" in FileExtractData.Filelines:
                        FileExtractData.Filelines[index] = FileExtractData.Filelines[index].replace("${PN}", self.PN)

                if self.PV != None:
                    if "${PV}" in FileExtractData.Filelines:
                        FileExtractData.Filelines[index] = FileExtractData.Filelines[index].replace("${PV}", self.PV)
             
        ArgList = []
        fanalysis = FilePatternAnalysisClass()
        self.DelimiterCountArray = [0] * len(fanalysis.DelimiterTypeList)

        if fanalysis.FindStringValue1(FileExtractData.Filelines, "SUMMARY ", "=", 1, ArgList) == True:
            self.Summary = "".join(ArgList)

        ArgList.clear()

        if fanalysis.FindStringValue1(FileExtractData.Filelines, "DESCRIPTION ", "=", 1, ArgList) == True:
            self.Description = "".join(ArgList)

        fanalysis.GetParameterList(FileExtractData.Filelines, self.ParamList, "Parameters", None, None, None, None)       
        fanalysis.GetParameterList(FileExtractData.Filelines, self.RequireList, "require", "require", None, None, " ")
        fanalysis.GetParameterList(FileExtractData.Filelines, self.IncludeList, "include", "include", None, None, " ")
        fanalysis.GetParameterList(FileExtractData.Filelines, self.InheritList, "inherit", "inherit", None, None, " ")
        fanalysis.GetParameterList(FileExtractData.Filelines, self.INHERITConfList, "INHERIT", "INHERIT", None, None, None)
        fanalysis.GetParameterList(FileExtractData.Filelines, self.PreferredProviderList, "PreferredProvider", "PREFERRED_PROVIDER", None, None, None)
        fanalysis.GetParameterList(FileExtractData.Filelines, self.VirtualRuntimeList, "VirtualRuntime", "VIRTUAL_RUNTIME", None, None, None)
                
        self.AnalyzeParamList(self.ParameterRecordList, self.ParamList)
        self.AnalyzePackageConfigList()
    
    def CheckForYoctoVariable(self, param):
        for varType in self.MetaParent.ObmcYactoAnalyzer.YoctoVariableTypesDict.YoctoVariableList:
            if varType.Variable == param:
                return True
        return False
    
    def AnalyzeParamList(self, RecordList, ParamList):
        size = 0
        for pd in ParamList:
            if len(RecordList) == 0:
                param_found = False
                for pr in RecordList:
                    if pr.Parameter == pd.Parameter:
                        self.DelimiterCountArray[pd.index] += 1
                        pr.ParamDataList.append(pd)
                        param_found = True

                if param_found == False:
                    pr = ParameterRecordClass(pd.Parameter)
                    self.DelimiterCountArray[pd.index] += 1
                    pr.ParamDataList.append(pd)
                    RecordList.append(pr)
            else:
                pr = ParameterRecordClass(pd.Parameter)
                self.DelimiterCountArray[pd.index] += 1
                pr.ParamDataList.append(pd)
                RecordList.append(pr)
           
            if self.CheckForYoctoVariable(pd.Parameter):
                self.YoctoList.append(pd)
                size = len(self.YoctoList)
    
    def AnalyzePackageConfigList(self):
        for i in range(0, len(self.FileExtractData.Filelines)):
            if self.FileExtractData.Filelines[i].startswith("PACKAGECONFIG["):
                pkgConfig = PackageConfigDataClass()
                if "\\" not in self.FileExtractData.Filelines[i]:
                    pkgConfig.ConfigParam = self.FileExtractData.Filelines[i][:self.FileExtractData.Filelines[i].index("=")].replace("PACKAGECONFIG[", "").replace("]", "").strip()
                    sp = self.FileExtractData.Filelines[i][self.FileExtractData.Filelines[i].index("=")+1:].replace("\"","").split(",")
                    for sd in sp:
                        pkgConfig.OptionList.append(sd.replace("-D", "").strip())
                else:
                    j = 0
                    pkgConfig.ConfigParam = self.FileExtractData.Filelines[i][:self.FileExtractData.Filelines[i].index("=")+1].replace("PACKAGECONFIG[", "").replace("]", "").strip()
                    multiString = []
                    s = self.FileExtractData.Filelines[i][self.FileExtractData.Filelines[i].index("=")+1:].replace("\\", "")
                    for j in range(i+1, len(self.FileExtractData.Filelines)):
                        s = s+ self.FileExtractData.Filelines[i].replace("\\", "")
                        if "\\" not in self.FileExtractData.Filelines[j]:
                            break

                    i = j
                    sp = s.split(",")
                    for sd in sp:
                        pkgConfig.OptionList.append(sd.replace("-D", "").strip())

                self.PackageConfigList.append(pkgConfig);

    def ExtractConfigValueList(self, param):
        ConfigValue = []
        if param.Value != None:
            s = param.Value.split(",")
            for sd in s:
                ConfigValue.append(sd.replace("-D", ""))

        if  len(param.MultiValue) > 0:
            for ml in param.MultiValue:
                s = ml.split(",")
                for sd in s:
                    ConfigValue.append(sd.replace("-D", ""));

        return ConfigValue
        
    def PrintDataCollection(self, dtype):
        print("Summary     : ", self.Summary)
        print("Description : ", self.Description)
        print("PN :", self.PN, "PV :", self.PV)

        if dtype == "ylist":
            print("\n\nYocto Variables List: ")
            for parm in self.YoctoList:
                parm.PrintParamData()

        if dtype == "plist":
            print("\n\nParameter List: ")
            for parm in self.ParamList:
                parm.PrintParamData()

        if len(self.RequireList) > 0:
            print("\n\nRequire List: ")
            for parm in self.RequireList:
                parm.PrintParamData()

        if len(self.IncludeList) > 0:
            print("\n\nInclude List: ")
            for parm in self.IncludeList:
                parm.PrintParamData()
        
        if len(self.InheritList) > 0:
            print("\n\nInherit List: ")
            for parm in self.InheritList:
                parm.PrintParamData()

        if len(self.PreferredProviderList) > 0:
            print("\n\nPreferredProvider List: ")
            for parm in self.PreferredProviderList:
                parm.PrintParamData()

        if len(self.VirtualRuntimeList) > 0:
            print("\n\nVirtualRuntime List: ")
            for parm in self.VirtualRuntimeList:
                parm.PrintParamData()


#        print("\r\n%-32s,%-32s,%-16s,%-64s," %(self.MetaParent.MetaFile.name, self.MetaParent.Type, self.Type, self.file.name), end=",")
#        print("%4d,%4d" %(len(self.ParameterRecordList), len(self.ParamList)), end=",")
#        print("%4d,%4d" %(len(self.RequireList), len(self.RequireReferenceList)), end=",")
#        print("%4d,%8d" %(len(self.IncludeList), len(self.IncludeReferenceList)), end=",")
#        print("%4d,%8d" %(len(self.InheritList), len(self.InheritReferenceList)), end=",")
#        print("%4d,%4d" %(len(self.INHERITConfList), len(self.InheritConfReferenceList)), end=",")
        
#        for i in range(0,len(self.DelimiterCountArray)):
#            print(",%4d" %(self.DelimiterCountArray[i]), end="")

    def PrintMachineDataCollection(self, trace_level):
        i = 0;
        print("\r\n")
        for i in range(0, trace_level+1):
            print(" ")        
        
        print(" Parameter Report")

        for pr in self.ParameterRecordList:
            print("\r\n")
            for i in range(0, trace_level+2):
                print(" ")

            print("Parameter %s [%d] ", pr.Parameter, len(pr.ParamDataList))

class FilePatternAnalysisClass:
    def __init__(self):
        self.DelimiterList = ["??=", "?=", ":=", "+=", "=+", ".=", "=.", "="]
        self.DelimiterTypeList = ["WeakDefaultValue", "DefaultValue", "ImmediateVariableExpansion", "AppendWS", "PrependWS", "AppendWOS", "PrependWOS", "Assignment"]
        self.DelimiterPrintTypeList = ["WDV", "DV", "IVE", "AWS", "PWS", "AWOS", "PWOS", "A"]

    def FindStringValue1(self, filelines, Pattern, delimiter1, offset1, rlist):
        rlist.clear()

        for i in range(0, len(filelines)):
            line = filelines[i]
            if "\\" not in line:
                if line.startswith(Pattern):
                    s = line.split(delimiter1)
                    if len(s) > offset1: 
                        rlist.append(s[offset1].strip().replace("\"", ""))
                        return True
            else:
                if line.startswith(Pattern):
                    slist = []
                    for j in range(i+1, len(filelines)):
                        if "\\" in filelines[j]:
                            slist.append(filelines[j].strip().replace("\\", "").replace("\"", ""))
                        else:
                            break
                    rlist.extend(slist)
                    return True
        
        return False
    
    def FindStringValue2(self, Filelines, Pattern, delimiter1,offset1, delimiter2, offset2, r):
        r.clear();
        
        for i in range(0, len(Filelines)):        
            if "\\" not in Filelines[i]:
                if delimiter2 == None:
                    if Filelines[i].startswith(Pattern):
                        s = Filelines[i].split(delimiter1)
                        if( len(s) > offset1 ):
                            r.append(s[offset1].strip().replace("\"",""))
                            return True                    
                else:
                    s = Filelines[i].strip().replace("\"","").split(delimiter1)[offset1].split(delimiter2)
                    r.extend(s)
                    return True
            else:
                if Filelines[i].startswith(Pattern):
                    if delimiter2 == None:
                        slist = []
                        for j in range(i+1, len(Filelines)):
                            if "\\" not in Filelines[j]:
                                break
                            slist.append(Filelines[j].strip().replace("\\", "").replace("\"",""))
                        r.extend(slist);
                        return True
                    else:
                        slist = []
                        s = Filelines[i].strip().replace("\\", "").split(delimiter1)[offset1].split(delimiter2)
                        slist.append(s[offset2].replace("\"",""))
                        for j in range(i+1, len(Filelines)):
                            if "\\" not in Filelines[j]:
                                break
                            slist.append(Filelines[j].replace("\\", "").strip().replace("\"",""))
                        r.extend(slist)
                        return True                 
        return False    

    def GetDelimiter(self, Fileline):
        for index in range(0, len(self.DelimiterList)):
            if self.DelimiterList[index] in Fileline:
                return index
        return -1;

    def GetParameterList(self, Filelines, ParamList, type, StartPattern, ContainPattern, EndPattern, delimiter):

        pattern_found = False
        
        if StartPattern == None and ContainPattern == None and EndPattern == None:
            pattern_found = True

        for i in range(0, len(Filelines)):
            if Filelines[i].strip().startswith("#"):
                 continue
            
            if StartPattern != None or ContainPattern != None or EndPattern != None:
                pattern_found = False

            if StartPattern != None:
                if Filelines[i].startswith(StartPattern):
                    pattern_found = True

            if ContainPattern != None:
                if ContainPattern in Filelines[i]:
                    pattern_found = True;                
            
            if EndPattern != None:
                if Filelines[i].endsWith(EndPattern):
                    pattern_found = True;                

            if pattern_found == True:
                delimiter_index = -1
                delimiterString = None
                delimiterType = None
                delimiter_found = False
                
                if delimiter == None:
                    # Standard Delimiter Check 
                    delimiter_index = self.GetDelimiter(Filelines[i])
                    if delimiter_index >= 0:
                        delimiterString = self.DelimiterList[delimiter_index]
                        delimiterType = self.DelimiterTypeList[delimiter_index]
                        if delimiter_index < 7:
                            Filelines[i] = Filelines[i].replace(delimiterString,self.DelimiterList[7])  
                            delimiterString = self.DelimiterList[7];

                        delimiter_found = True
                else:
                    if delimiter in Filelines[i]:
                        delimiterString = delimiter
                        delimiterType = "User"
                        delimiter_found = True

                if "\\" not in Filelines[i]:
                    # Working on Single Line Parsing 
                    if delimiter_found == True:
                        parse_string = Filelines[i].split(delimiterString)
                        param = None
                        if len(parse_string) < 2:
                            param = ParameterDataClass(type, delimiterType, parse_string[0].strip(), None)
                        else:
                            param = ParameterDataClass(type, delimiterType, parse_string[0].strip(), parse_string[1].strip())

                        param.index = delimiter_index
                        ParamList.append(param)
                else:
                    if delimiter_found == True:
                        parse_string = Filelines[i].split(delimiterString)
                        param = ParameterDataClass(type, delimiterType, parse_string[0].strip().replace("\\", "").replace("\"",""), parse_string[1].strip().replace("\\", "").replace("\"",""));
                        slist = []
                        for j in range(i+1, len(Filelines)):
                            if "\\" not in Filelines[i]:
                                i = j+1
                                break
                            param.MultiValue.append(Filelines[i].strip().replace("\\", "").replace("\"",""))
                        
                        param.index = delimiter_index
                        ParamList.append(param)
        
        return False
    
    def PrintLegent(self):
        print("\nName,");
        for i in range(0, len(self.DelimiterTypeList)):
                print("%s,", self.DelimiterTypeList[i])
        
        print("User\n")

    def PrintStat(self, ParamList):
        if len(ParamList) == 0:
             return

        stat = int[len(self.DelimiterList)]
        user_delimiter_count = 0

        for pd in ParamList:
            index = self.DelimiterTypeList.index(pd.AssignmentType)
            if( index > 0 ):
                stat[index] += 1
            else:
                user_delimiter_count += 1

        print("\n%s,", ParamList[0].Type)
        for i in range(0, len(stat)):
                print("%5d, ", stat[i])

        print("%5d", user_delimiter_count)    

class YoctoVariableTypesDataClass:
    def __init__(self):
        self.Variable = ""
        self.Description = ""

class YoctoVariableTypesClass:
    def __init__(self, f):
        self.ExtractedFile = None
        self.YoctoVariableList = []
        docFile = os.path.abspath(f)+"/poky/meta/conf/documentation.conf"
        if os.path.exists(docFile) == False:
            exit()

        self.ExtractedFile = ExtractFileLinesClass(docFile);
        
        variable_processing_start = False
        
        for s in self.ExtractedFile.Filelines:
            if "DESCRIPTIONS FOR VARIABLES" in s:
                variable_processing_start = True
            if variable_processing_start == True:
                if "[doc]" in s:
                    yvar = YoctoVariableTypesDataClass();
                    yvar.Variable = s.replace("[doc]", "").split("=")[0].strip()
                    yvar.Description = s.replace("[doc]", "").split("=")[1].strip()
                    self.YoctoVariableList.append(yvar);

class PackageGroupDataClass:
    def __init__(self, analyzer, f):
        self.ObmcYactoAnalyzer = analyzer
        self.file = f
        self.Summary = None
        self.PackagesList = []
        self.PackageElementList = []
        self.CurrentLineCount = 0
        self.FileExtractData = None

    def PrintPackageGroupData(self):
        if len(self.PackagesList) > 0:
            print("Package Group Data :")
            print("\tSummary = ", self.Summary, "Packages = ", self.PackagesList)
            for pgde in self.PackageElementList:
                pgde.PrintElements()              
        
    def ProcessPackageData(self):
        FileExtractData = ExtractFileLinesClass(self.file);

        ArgList = []
        ArgList1 = []
        file_pattern_analysis = FilePatternAnalysisClass()

        if file_pattern_analysis.FindStringValue1(FileExtractData.Filelines, "SUMMARY", "=", 1, ArgList) == True:
            self.Summary = ArgList[0];
        
        ArgList.clear();
        if file_pattern_analysis.FindStringValue1(FileExtractData.Filelines,"PACKAGES", "=", 1, ArgList) == False:
            self.PackagesList.append("${PN}")
        else:
            self.PackagesList.extend(ArgList)
        
        ArgList.clear();
        for p in  self.PackagesList:
            pgde = PackageGroupDataElementClass()
            pgde.PackageName = p;
            if file_pattern_analysis.FindStringValue1(FileExtractData.Filelines,"SUMMARY:"+str(p), "=", 1,ArgList) == True:
                pgde.Description = ArgList[0]
            ArgList.clear();
            if file_pattern_analysis.FindStringValue1(FileExtractData.Filelines,"RDEPENDS:"+str(p), "=", 1, ArgList) == True:
                if len(ArgList) == 1:
                    if "${" in ArgList[0]:
                        if file_pattern_analysis.FindStringValue1(FileExtractData.Filelines,ArgList[0].replace("${", "").replace("}", ""),"=", 1, ArgList1) == False:
                            pgde.DependList.extend(ArgList)
                        else:
                            pgde.DependList.extend(ArgList1)
                else:
                    pgde.DependList.extend(ArgList);
            self.PackageElementList.append(pgde);
            self.ObmcYactoAnalyzer.GlobalPackageElementList.append(pgde);

