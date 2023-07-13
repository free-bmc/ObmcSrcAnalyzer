#  OpenBMC Source Analyzer Tool

This utility can be used by OpenBMC engineers, developers and explorers to get an in-depth understanding of the different aspects of the openbmc source code.   

## Rationale
1. The tool helps to understand the complete OpenBMC source instead of only looking for the specific platform 
2. This tool aspires the developers to easily review the different option chosen by other developers 

## Impact 
1. Provides more visibility instead of hopping between directory 
2. Ability to build OpenBMC solutions by aggregating other already existing solutions

## Version Information 

### 1.0 
- Supports Analysis of any OpenBMC Source Code and builds a Data Collection that can provide deeper information 
- Supports Packages, Bitbake recipes, Includes, Configurations 
- Supports Loading Meta Data Configuration and analyzing the Packages, bitbake files, include, conf and inherit files

## About the Tool

The tool utilizes standard python3 and requires a OpenBMC source tree for analysis

### Tool Setup 

Clone a OpenBMC source directory that you need for analysis b

### Tool usage 

```
$ python3 obmc_srcanalyzer.py
Welcome to OpenBMC Source Analyzer Tool
OpenBMC Source Analysis: Started ...
Provide the OpenBMC Source Directory Path : ../openbmc
OpenBMC Source Analysis: Completed ...
 OpenBMC Source Analysis :
 Total Packages Found                       =  165
 Total Data Collected                       =  3645
 Total Bitbake Recipes Found                =  2704
 Total Bitbake Includes Found               =  242
 Total Bitbake Classes Found                =  92
 Total Bitbake Conf Found                   =  607
CLI started ...<type help for commands>
OBMC CLI >> help
Commands and Options:
        version                                Version Info
        mlist                                  List of all Meta Data for analysis
        slist                                  Meta Data High level analysis
        legends                                Print the legends in the List
        load          <Meta Data>              Load  Meta Data for Deeper Analysis
        quit                                   Quit application
OBMC CLI >> mlist
Base
Security
bmc-aspeed
bmc-nuvoton
proc-amd
proc-arm
proc-intel-openbmc
...
OBMC CLI >> load proc-amd
MetaData CLI started ...<type help for commands>

OBMC MetaData(proc-amd) CLI >> help
        info [options] [types]                 Meta data Info
                                               Supported Options
                                                -s   short format (default)
                                                -l   Long format
                                               Supported Types
                                                default:  All Meta Data Types
                                                pkg       Package Groups
                                                bb        bitbake files
                                                inc       include files
                                                bbclass   bitbake class files
                                                conf      conf files
        list <types> index [options]           List Meta Data File Content
                                                bb        bitbake type
                                                inc       include type
                                                bbclass   bitbake class type
                                                conf      conf type
                                               index = from the info
                                               Supported Options
                                                plist     Parameter List
                                                ylist     Yocto List
                                                rlist     Require List
                                                ilist     Include List
                                                inlist    Inherit List
                                                pplist    Prefered Provider List
                                                vrlist    Virtual Runtime List
                                                rmap      Require Map
                                                imap      Include Map
        quit                                    Go back to CLI

OBMC MetaData(proc-amd) CLI >>

```

### Notes for Users

This tool is currently evolving with adding more analysis for entity-manager as well providing a source level analysis of the dbus map in relation to Redfish and other OpenBMC services 


