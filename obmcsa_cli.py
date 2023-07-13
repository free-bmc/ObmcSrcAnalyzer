
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

from obmcsa_lib import AnalyzeOpenBMCSourceMain

obmcYactoAnalyzerData = None

def srcanalyzer_CLI(ToolVersion):
    print("OpenBMC Source Analysis: Started ...")
    obmcYactoAnalyzerData = AnalyzeOpenBMCSourceMain()
    print("OpenBMC Source Analysis: Completed ...")
    obmcYactoAnalyzerData.PrintGlobalData()
    print("CLI started ...<type help for commands> ")    
    while True:
        option = input("OBMC CLI >> ")
        #print(option)
        if option == "quit":
            exit()
        elif option == "help":
            print("Commands and Options:")
            print("\tversion                                Version Info ")
            print("\tlist                                   List all Meta Data for analysis ")
            print("\tlegends                                Print the legends in the List ")
            print("\tload          <Meta Data>              Load  Meta Data for Deeper Analysis")            
            print("\tquit                                   Quit application")            
        elif option.startswith("version"):
            print(ToolVersion)
        elif option.startswith("list"):
            obmcYactoAnalyzerData.PrintStats()
        elif option.startswith("legends"):
            obmcYactoAnalyzerData.PrintLegends()
        elif option.startswith("load"):    
            suboption = option.split(" ")
            metadata_CLI(obmcYactoAnalyzerData, suboption[1])


def metadata_CLI(obmcYactoAnalyzerData, metadata):
    print("MetaData CLI started ...<type help for commands>")    
    obmcMetaData = obmcYactoAnalyzerData.GetMetaInfo(metadata)
    while True:
        option = input("\nOBMC MetaData("+metadata+") CLI >> ")
        if option == "quit":
            return
        elif option == "help":
            print("\tinfo [options] [types]                 Meta data Info")
            print("\t                                       Supported Options  ")
            print("\t                                        -s   short format (default) ")
            print("\t                                        -l   Long format ")           
            print("\t                                       Supported Types  ")            
            print("\t                                        default:  All Meta Data Types ")
            print("\t                                        pkg       Package Groups ")                                    
            print("\t                                        bb        bitbake files ")                                    
            print("\t                                        inc       include files ")                                    
            print("\t                                        bbclass   bitbake class files ")                                    
            print("\t                                        conf      conf files ")                                    
            print("\tlist <types> index [options]           List Meta Data File Content ")
            print("\t                                        bb        bitbake type ")                                    
            print("\t                                        inc       include type ")                                    
            print("\t                                        bbclass   bitbake class type ")                                    
            print("\t                                        conf      conf type ")                                    
            print("\t                                       index = from the info ")            
            print("\t                                       Supported Options ")            
            print("\t                                        plist     Parameter List ")                                                
            print("\t                                        ylist     Yocto List ")      
            print("\tquit                                    Go back to CLI ")                                                                  
        elif option.startswith("info"):
            suboption = option.split(" ")
            mdatatypes = ""
            fmt = False
            if len(suboption) > 1:
                if len(suboption) == 2:
                    if suboption[1].startswith("-"):
                        if suboption[1].startswith("-l"):
                            fmt = True
                    else: 
                        mdatatypes = suboption[1]
                else:
                    if suboption[1].startswith("-"):
                        if suboption[1].startswith("-l"):
                            fmt = True
                    mdatatypes = suboption[2]
                
                obmcYactoAnalyzerData.PrintMetaInfo(metadata, mdatatypes, fmt)
            else:
                obmcYactoAnalyzerData.PrintMetaInfo(metadata, "", False)
        elif option.startswith("list"):
            suboption = option.split(" ")
            mdatatypes = suboption[1]
            mindex = int(suboption[2])
            if len(suboption) == 4:
                dtype = suboption[3]
            else:
                dtype = None
            obmcMetaData.PrintDataCollectionInfo(mdatatypes, mindex, dtype)
            
            




