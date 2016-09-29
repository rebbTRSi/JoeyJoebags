from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter.messagebox as messagebox

import usb.core
import usb.util
#import sys
#import itertools

ROMsize=0 
RAMsize=0
ROMbuffer=""
RAMbuffer=""
USBbuffer=""
FlashBlockSize=0


for usbfill in range(64):
    USBbuffer=USBbuffer+"\x00"


Command_Get_Version =   [0x00]
Command_Get_ROM =       [0x10]
Command_Set_Bank =      [0x08]
Command_Flash_ROM =      [0x20]


class Window(Frame):
    def __init__ (self, master=None):
        Frame.__init__ (self,master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Joey Joebags by BennVenn - V3.17")
        self.pack(fill=BOTH, expand=1)

        self.lowerLeftLabel = StringVar()
        cartSelectionLabel = Label(root,  textvariable = self.lowerLeftLabel)
        cartSelectionLabel.place(x=0,y=280)
        self.lowerRightLabel = StringVar()
        hardwareStatusLabel = Label(root,  textvariable = self.lowerRightLabel)
        hardwareStatusLabel.place(x=270,y=280)

        self.ROMtitleLabel = StringVar()
        ROMtitleLabel = Label(root,  textvariable = self.ROMtitleLabel)
        ROMtitleLabel.place(x=0,y=0)
        self.ROMsizeLabel = StringVar()
        ROMsizeLabel = Label(root,  textvariable = self.ROMsizeLabel)
        ROMsizeLabel.place(x=0,y=20)
        self.RAMsizeLabel = StringVar()
        RAMsizeLabel = Label(root,  textvariable = self.RAMsizeLabel)
        RAMsizeLabel.place(x=0,y=40)
        self.MAPPERtypeLabel = StringVar()
        MAPPERtypeLabel = Label(root,  textvariable = self.MAPPERtypeLabel)
        MAPPERtypeLabel.place(x=0,y=60)

        menu=Menu(root)
        root.config(menu=menu)
        filemenu=Menu(menu)
        menu.add_cascade(label="File",menu=filemenu)
        filemenu.add_command(label="Exit",command=main_Exit)
        cartTypeMenu = Menu(menu)
        menu.add_cascade(label="Cart Type", menu=cartTypeMenu)
#MBC Generic Cart Menu
        MBCmenu = Menu(menu)
        cartTypeMenu.add_cascade(label="GB(C) Generic",menu=MBCmenu)
        MBCmenu.add_command(label='Get Save RAM',command=main_MBC_Dump_RAM)
        MBCmenu.add_command(label='Write Save RAM',command=main_MBC_Burn_RAM)
        MBCmenu.add_command(label='Dump ROM',command=main_MBC_Dump_ROM)

#MBC2 Menu
        MBC2menu = Menu(menu)
        cartTypeMenu.add_cascade(label="GB MBC2",menu=MBC2menu)
        MBC2menu.add_command(label='Get Save RAM',command=main_MBC2_Dump_RAM)
        MBC2menu.add_command(label='Write Save RAM',command=main_MBC2_Burn_RAM)
        MBC2menu.add_command(label='Dump ROM',command=main_MBC_Dump_ROM)

#GB Cam Cart Menu
        GBCammenu = Menu(menu)
        cartTypeMenu.add_cascade(label="GB Camera",menu=GBCammenu)
        GBCammenu.add_command(label='Get Save RAM',command=main_Cam_Dump_RAM)
        GBCammenu.add_command(label='Write Save RAM',command=main_Cam_Burn_RAM)
        
#Catskull 32k cart menu
        CatMenu = Menu(menu)
        cartTypeMenu.add_cascade(label="Catskull 32k",menu=CatMenu)
        CatMenu.add_command(label='Erase',command=main_Catskull_erase)
        CatMenu.add_command(label='Flash',command=main_Catskull_write)

#EMS32 Cart Menu
        EMS32menu = Menu(menu)
        cartTypeMenu.add_cascade(label="EMS32",menu=EMS32menu)
        EMS32menu.add_command(label='Get Save RAM')
        EMS32menu.add_command(label='Write Save RAM')
        EMS32menu.add_command(label='Dump ROM')
        EMS32menu.add_command(label='Flash ROM')

#EMS64 Cart Menu
        EMS64menu = Menu(menu)
        cartTypeMenu.add_cascade(label="EMS64",menu=EMS64menu)
        EMS64menu.add_command(label='Get Save RAM',command=main_MBC_Dump_256RAM)
        EMS64menu.add_command(label='Write Save RAM',command=main_MBC_Burn_RAM)
        EMS64menu.add_command(label='Dump ROM',command=main_MBC_Dump_ROM)
        EMS64menu.add_command(label='Flash ROM',command=main_EMS64_Burn_ROM)
        EMS64menu.add_command(label='Set page 2',command=main_EMS64_PageSwap)
        
#BV64 Cart Menu
        BV64menu = Menu(menu)
        BV64GSR = Menu(menu)
        BV64WSR = Menu(menu)
        cartTypeMenu.add_cascade(label="BennVenn 64M",menu=BV64menu)
        BV64menu.add_cascade(label='Get Save RAM',menu=BV64GSR)
        BV64GSR.add_command(label='128K',command=main_BV64_Dump_128K0)
        BV64GSR.add_command(label='32K (1)',command=main_BV64_Dump_32K1)
        BV64GSR.add_command(label='32K (2)',command=main_BV64_Dump_32K2)
        BV64GSR.add_command(label='32K (3)',command=main_BV64_Dump_32K3)
        BV64GSR.add_command(label='32K (4)',command=main_BV64_Dump_32K4)
        BV64menu.add_cascade(label='Write Save RAM',menu=BV64WSR)
        BV64WSR.add_command(label='128K',command=main_BV_Burn_128k0)
        BV64WSR.add_command(label='32K (1)',command=main_BV_Burn_32K0)
        BV64WSR.add_command(label='32K (2)',command=main_BV_Burn_32K1)
        BV64WSR.add_command(label='32K (3)',command=main_BV_Burn_32K2)
        BV64WSR.add_command(label='32K (4)',command=main_BV_Burn_32K3)
        BV64menu.add_command(label='Dump ROM',command=main_BV64_Dump_ROM0)
        BV64menu.add_command(label='Flash ROM',command=main_BV64_Flash_ROM0)
        
#BV256 Cart Menu
        BV256menu = Menu(menu)
        BV256B1 = Menu(menu)
        BV256B2 = Menu(menu)
        BV256B3 = Menu(menu)
        BV256B4 = Menu(menu)
        
        BV1256GSR = Menu(menu)
        BV1256WSR = Menu(menu)
        BV2256GSR = Menu(menu)
        BV2256WSR = Menu(menu)
        BV3256GSR = Menu(menu)
        BV3256WSR = Menu(menu)
        BV4256GSR = Menu(menu)
        BV4256WSR = Menu(menu)
        cartTypeMenu.add_cascade(label="BennVenn 256M",menu=BV256menu)
        BV256menu.add_cascade(label="Block1",menu=BV256B1)
        BV256menu.add_cascade(label="Block2",menu=BV256B2)
        BV256menu.add_cascade(label="Block3",menu=BV256B3)
        BV256menu.add_cascade(label="Block4",menu=BV256B4)

#Block1        
        BV256B1.add_cascade(label='Get Save RAM',menu=BV1256GSR)
        BV1256GSR.add_command(label='128K',command=main_BV64_Dump_128K0)
        BV1256GSR.add_command(label='32K (1)',command=main_BV64_Dump_32K1)
        BV1256GSR.add_command(label='32K (2)',command=main_BV64_Dump_32K1)
        BV1256GSR.add_command(label='32K (3)',command=main_BV64_Dump_32K1)
        BV1256GSR.add_command(label='32K (4)',command=main_BV64_Dump_32K1)
        BV256B1.add_cascade(label='Write Save RAM',menu=BV1256WSR)
        BV1256WSR.add_command(label='128K',command=main_BV_Burn_128k0)
        BV1256WSR.add_command(label='32K (1)',command=main_BV_Burn_32K0)
        BV1256WSR.add_command(label='32K (2)',command=main_BV_Burn_32K1)
        BV1256WSR.add_command(label='32K (3)',command=main_BV_Burn_32K2)
        BV1256WSR.add_command(label='32K (4)',command=main_BV_Burn_32K3)
        BV256B1.add_command(label='Dump ROM',command=main_BV64_Dump_ROM0)
        BV256B1.add_command(label='Flash ROM',command=main_BV64_Flash_ROM0)

#Block2        
        BV256B2.add_cascade(label='Get Save RAM',menu=BV2256GSR)
        BV2256GSR.add_command(label='128K',command=main_BV64_Dump_128K1)
        BV2256GSR.add_command(label='32K (1)',command=main_BV64_Dump_32K21)
        BV2256GSR.add_command(label='32K (2)',command=main_BV64_Dump_32K21)
        BV2256GSR.add_command(label='32K (3)',command=main_BV64_Dump_32K21)
        BV2256GSR.add_command(label='32K (4)',command=main_BV64_Dump_32K21)
        BV256B2.add_cascade(label='Write Save RAM',menu=BV2256WSR)
        BV2256WSR.add_command(label='128K',command=main_BV_Burn_128k1)
        BV2256WSR.add_command(label='32K (1)',command=main_BV_Burn_32K10)
        BV2256WSR.add_command(label='32K (2)',command=main_BV_Burn_32K11)
        BV2256WSR.add_command(label='32K (3)',command=main_BV_Burn_32K12)
        BV2256WSR.add_command(label='32K (4)',command=main_BV_Burn_32K13)
        BV256B2.add_command(label='Dump ROM',command=main_BV64_Dump_ROM1)
        BV256B2.add_command(label='Flash ROM',command=main_BV64_Flash_ROM1)

#Block3        
        BV256B3.add_cascade(label='Get Save RAM',menu=BV3256GSR)
        BV3256GSR.add_command(label='128K',command=main_BV64_Dump_128K2)
        BV3256GSR.add_command(label='32K (1)',command=main_BV64_Dump_32K31)
        BV3256GSR.add_command(label='32K (2)',command=main_BV64_Dump_32K31)
        BV3256GSR.add_command(label='32K (3)',command=main_BV64_Dump_32K31)
        BV3256GSR.add_command(label='32K (4)',command=main_BV64_Dump_32K31)
        BV256B3.add_cascade(label='Write Save RAM',menu=BV3256WSR)
        BV3256WSR.add_command(label='128K',command=main_BV_Burn_128k2)
        BV3256WSR.add_command(label='32K (1)',command=main_BV_Burn_32K20)
        BV3256WSR.add_command(label='32K (2)',command=main_BV_Burn_32K21)
        BV3256WSR.add_command(label='32K (3)',command=main_BV_Burn_32K22)
        BV3256WSR.add_command(label='32K (4)',command=main_BV_Burn_32K23)
        BV256B3.add_command(label='Dump ROM',command=main_BV64_Dump_ROM2)
        BV256B3.add_command(label='Flash ROM',command=main_BV64_Flash_ROM2)

#Block4        
        BV256B4.add_cascade(label='Get Save RAM',menu=BV4256GSR)
        BV4256GSR.add_command(label='128K',command=main_BV64_Dump_128K3)
        BV4256GSR.add_command(label='32K (1)',command=main_BV64_Dump_32K41)
        BV4256GSR.add_command(label='32K (2)',command=main_BV64_Dump_32K41)
        BV4256GSR.add_command(label='32K (3)',command=main_BV64_Dump_32K41)
        BV4256GSR.add_command(label='32K (4)',command=main_BV64_Dump_32K41)
        BV256B4.add_cascade(label='Write Save RAM',menu=BV4256WSR)
        BV4256WSR.add_command(label='128K',command=main_BV_Burn_128k3)
        BV4256WSR.add_command(label='32K (1)',command=main_BV_Burn_32K30)
        BV4256WSR.add_command(label='32K (2)',command=main_BV_Burn_32K31)
        BV4256WSR.add_command(label='32K (3)',command=main_BV_Burn_32K32)
        BV4256WSR.add_command(label='32K (4)',command=main_BV_Burn_32K33)
        BV256B4.add_command(label='Dump ROM',command=main_BV64_Dump_ROM3)
        BV256B4.add_command(label='Flash ROM',command=main_BV64_Flash_ROM3)

#Bung32 Cart Menu
        Bung32menu = Menu(menu)
        cartTypeMenu.add_cascade(label="Bung 32M",menu=Bung32menu,state=DISABLED)
        Bung32menu.add_command(label='Get Save RAM')
        Bung32menu.add_command(label='Write Save RAM')
        Bung32menu.add_command(label='Dump ROM')
        Bung32menu.add_command(label='Flash ROM')

#Bung64 Cart Menu
        Bung64menu = Menu(menu)
        cartTypeMenu.add_cascade(label="Bung 64M",menu=Bung64menu,state=DISABLED)
        Bung64menu.add_command(label='Get Save RAM')
        Bung64menu.add_command(label='Write Save RAM')
        Bung64menu.add_command(label='Dump ROM')
        Bung64menu.add_command(label='Flash ROM')



#DMG-MMSA-JPN Cart Menu
        JPNmenu = Menu(menu)
        cartTypeMenu.add_cascade(label="DMG-MMSA-JPN",menu=JPNmenu)
        JPNmenu.add_command(label='Get Save RAM',command=main_MBC_Dump_RAM)
        JPNmenu.add_command(label='Write Save RAM',command=main_MBC_Burn_RAM)
        JPNmenu.add_command(label='Dump ROM',command=main_MBC_Dump_ROM)
        JPNmenu.add_command(label='Flash ROM',command=main_JPN_Burn_ROM)
        JPNmenu.add_command(label='Unlock Sector 0',command=main_JPN_Unlock_ROM)


#Shark MX Cart Menu
        MXmenu = Menu(menu)
        cartTypeMenu.add_cascade(label="Shark MX",menu=MXmenu)
        MXmenu.add_command(label='Get Save RAM',command=main_MBC_Dump_RAM)
        MXmenu.add_command(label='Write Save RAM',command=main_MBC_Burn_RAM)
        MXmenu.add_command(label='Dump ROM',command=main_MX_Dump_ROM)
        MXmenu.add_command(label='Flash ROM',command=main_MX_Burn_ROM,)

#El Cheapo Cart Menu
        ELmenu = Menu(menu)
        cartTypeMenu.add_cascade(label="El-Cheapo",menu=ELmenu)
        ELmenu.add_command(label='Erase',command=main_ELCheapo_Erase)
        ELmenu.add_command(label='Flash ROM',command=main_ELCheapo_Write)

        cartTypeMenu.add_separator()


#El Cheapo SD Cart Menu
        ELmenuSD = Menu(menu)
        cartTypeMenu.add_cascade(label="El-Cheapo SD",menu=ELmenuSD)
        ELmenuSD.add_command(label='Erase',command=main_ELCheapoSD_Erase)
        ELmenuSD.add_command(label='Flash ROM',command=main_ELCheapoSD_Write)



        cartTypeMenu.add_separator()

#GBA stuff
        GBA_GenericMenu=Menu(menu)
        GBA_ROM_Size=Menu(menu)
        GBA_ROM_Burn=Menu(menu)
        cartTypeMenu.add_cascade(label="GBA Generic",menu=GBA_GenericMenu)
        GBA_GenericMenu.add_command(label='Read Header',command=main_GBA_ReadHeader)
        GBA_GenericMenu.add_separator()
        GBA_GenericMenu.add_command(label='Dump 4kbit EEPROM',command=main_GBA_EEPROM_4k)
        GBA_GenericMenu.add_command(label='Dump 64kbit EEPROM',command=main_GBA_EEPROM_64k)
        GBA_GenericMenu.add_command(label='Write 4kbit EEPROM',command=main_GBA_Write4kEEPROM)
        GBA_GenericMenu.add_command(label='Write 64kbit EEPROM',command=main_GBA_Write64kEEPROM)
        GBA_GenericMenu.add_separator()
        GBA_GenericMenu.add_command(label='Dump 64kbytes SRAM',command=main_GBA_Dump64kSRAM)
        GBA_GenericMenu.add_command(label='Write 64k to SRAM',command=main_GBA_Write64kSRAM)
        GBA_GenericMenu.add_separator()
        GBA_GenericMenu.add_command(label='Dump 64kbytes FLASH',command=main_GBA_Dump64kFLASH)
        GBA_GenericMenu.add_command(label='Dump 128kbytes FLASH',command=main_GBA_Dump128kFLASH)
        GBA_GenericMenu.add_command(label='Write 64k to FLASH',command=main_GBA_Write64kFLASHRAM)
        GBA_GenericMenu.add_command(label='Write 128k to FLASH',command=main_GBA_Write128kFLASHRAM)
        GBA_GenericMenu.add_separator()
        GBA_GenericMenu.add_cascade(label='Dump ROM',menu=GBA_ROM_Size)
        GBA_ROM_Size.add_command(label='8mbit',command=main_GBA_Dump_8)
        GBA_ROM_Size.add_command(label='16mbit',command=main_GBA_Dump_16)
        GBA_ROM_Size.add_command(label='32mbit',command=main_GBA_Dump_32)
        GBA_ROM_Size.add_command(label='64mbit',command=main_GBA_Dump_64)
        GBA_ROM_Size.add_command(label='128mbit',command=main_GBA_Dump_128)
        GBA_BV=Menu(menu)
        cartTypeMenu.add_cascade(label="GBA BennVenn128M",menu=GBA_BV)
        GBA_BV.add_command(label='Flash ROM',command=main_GBA_Flash_ROM)
        #GBA_BV.add_command(label='Testcode',command=main_GBA_Testcode)
        
        functionMenu = Menu(menu)
        menu.add_cascade(label="Function", menu=functionMenu)
        functionMenu.add_command(label="Read Cart Header",command=main_readCartHeader)
        functionMenu.add_separator()

        joeyMenu = Menu(menu)
        menu.add_cascade(label="Joey", menu=joeyMenu)
        joeyMenu.add_command(label="Update Firmware",command=main_updateFirmware)
        joeyMenu.add_separator()

        self.lowerRightLabel.set('Hardware Not Detected')
        self.ROMtitleLabel.set("ROM Title: Unknown")
        self.ROMsizeLabel.set("ROM Size: Unknown")
        self.RAMsizeLabel.set("RAM Size: Unknown")
        self.MAPPERtypeLabel.set("Mapper: Unknown")

def main_Header():
    global ROMsize
    global RAMsize
    Header=""
    dev.write(0x01,[0x10,0x00,0x00,0x01,0x00])#start of logo
    dat = dev.read(0x81,64)
    Header=dat
    msg = [0x10,0x00,0x00,0x01,0x40] #
    dev.write(0x01,msg)
    dat = dev.read(0x81,64)
    Header+=dat
    msg = [0x10,0x00,0x00,0x01,0x80] #
    dev.write(0x01,msg)
    dat = dev.read(0x81,64)
    Header+=dat #Header contains 0xC0 bytes of header data
    print("ROM Title: "+str(Header[0x34:0x43]))

def main_readCartHeader():
    main_BV_SetBank(0,0)
    main_ROMBankSwitch(1)
    RAMtypes = [0,2048,8192,32768,(32768*4),(32768*2)]
    global ROMsize
    global RAMsize
    Header=""
    dev.write(0x01,[0x10,0x00,0x00,0x01,0x00])#start of logo
    dat = dev.read(0x81,64)
    Header=dat
    msg = [0x10,0x00,0x00,0x01,0x40] #
    dev.write(0x01,msg)
    dat = dev.read(0x81,64)
    Header+=dat
    msg = [0x10,0x00,0x00,0x01,0x80] #
    dev.write(0x01,msg)
    dat = dev.read(0x81,64)
    Header+=dat #Header contains 0xC0 bytes of header data
    ROMsize=(32768*( 2**(Header[0x48])))
    app.ROMtitleLabel.set("ROM Title: "+str(Header[0x34:0x43],'utf-8'))
    app.ROMsizeLabel.set("ROM Size: "+str (32768*( 2**(Header[0x48]))))
    RAMsize=RAMtypes[Header[0x49]]
    app.RAMsizeLabel.set("RAM Size:"+str(RAMsize))
#    app.ROMregionLabel.set("Mapper: ?????????")
    
def main_Exit():
    exit()

def main_LoadROM():
    global ROMsize
    global ROMbuffer
    root.update()
    ROMfileName=askopenfilename(filetypes=(("GB ROM File","*.GB"),("GBC ROM File","*.GBC"),("GBA ROM File","*.GBA"),("All Files","*.*")))
    if ROMfileName:
        ROMfile=open(ROMfileName,'rb')
        ROMbuffer=ROMfile.read()
        ROMsize=len(ROMbuffer)
        ROMfile.close()
        return(1)
    return(0)

def main_SaveROM():
    global ROMsize
    global ROMbuffer
    root.update()
    ROMfileName=asksaveasfilename(defaultextension=".GB",filetypes=(("GB ROM File","*.GB"),("GBC ROM File","*.GBC"),("GBA ROM File","*.GBA"),("All Files","*.*")))
    if ROMfileName:
        ROMfile=open(ROMfileName,'wb')
        ROMfile.write(ROMbuffer)
        ROMfile.close()
        
def main_LoadRAM():
    global RAMsize
    global RAMbuffer    
    root.update()

    RAMfileName=askopenfilename(filetypes=(("GB/C/A SRAM File","*.SAV"),("All Files","*.*")))
    if RAMfileName:
        RAMfile=open(RAMfileName,'rb')
        RAMbuffer=RAMfile.read()
        RAMsize=len(RAMbuffer)
        RAMfile.close()
        return(1)
    return(0)

def main_SaveRAM():
    global RAMsize
    global RAMbuffer
    root.update()

    print (len(RAMbuffer))
    RAMfileName=asksaveasfilename(defaultextension=".SAV",filetypes=(("GB/C/A SRAM File","*.SAV"),("All Files","*.*")))
    if RAMfileName:
        RAMfile=open(RAMfileName,'wb')
        RAMfile.write(RAMbuffer)
        RAMfile.close()

def main_updateFirmware():
    root.update()
    FWfileName=askopenfilename(filetypes=(("BennVenn Firmware File","*.BEN"),("All Files","*.*")))
    if FWfileName:
        FWfile=open(FWfileName,'rb')
        FWbuffer=FWfile.read()
        FWsize=len(FWbuffer)
        if FWsize==33280:
            dev.write(0x01,[0x03])
            USBbuffer = dev.read(0x81,64)
            app.lowerRightLabel.set(("File Size Correct"))
            for FWpos in range (512,33279,64):
                dev.write(0x01,FWbuffer[FWpos:FWpos+64])
        else:
            app.lowerRightLabel.set(("File Invalid"))
        FWfile.close()
        exit()
def main_CheckVersion():
    dev.write(0x01,Command_Get_Version)
    dat = dev.read(0x81,64)
    sdat=""
    for x in range(5):
        sdat=sdat+chr(dat[x])
    app.lowerRightLabel.set(("Firmware "+sdat))



#MBC Generic Specific Code Goes here:
def main_MBC_Dump_ROM():
    global BankSize
    BankSize=16384 #bytes per bank
    main_readCartHeader()
    main_dumpROM()

def main_MX_Dump_ROM():
    global BankSize
    BankSize=16384 #bytes per bank
    main_readCartHeader()
    main_dumpMXROM()

def main_MBC_Dump_RAM():
    global BankSize
    BankSize=16384 #bytes per bank
    main_readCartHeader()
    main_dumpRAM()
    main_SaveRAM()

def main_MBC_Dump_256RAM():
    global BankSize
    global RAMsize

    BankSize=16384 #bytes per bank
    main_readCartHeader()
    RAMsize=32768*4
    main_dumpRAM()
    main_SaveRAM()
    

def main_MBC2_Dump_RAM():
    global BankSize
    global RAMsize
    RAMsize=512
    BankSize=512 #bytes per bank
    main_dumpRAM2()
    main_SaveRAM()

def main_MBC_Burn_RAM():
    global BankSize
    BankSize=16384 #bytes per bank
    main_readCartHeader()
    if main_LoadRAM() == 1:
        main_BurnRAM()

def main_MBC2_Burn_RAM():
    global BankSize
    global RAMsize
    RAMsize=512
    BankSize=512 #bytes per bank
    if main_LoadRAM() == 1:
        main_BurnRAM2()
    

#BV64 Specific Code Goes here:
def main_BV64_Dump_ROM(ROMBlk):
    global BankSize
    global ROMsize
    BankSize=16384 #bytes per bank
    ROMsize=8388608
    main_BV_SetBank(ROMBlk,0)
    main_dumpROM()

def main_BV64_Flash_ROM():
    global BankSize
    global FlashBlockSize
    FlashBlockSize=131072 #bytes per bank
    BankSize=16384 #bytes per bank
    if main_LoadROM() == 1:
        main_BV_lockBank(1)
        main_BV_FlashROM()


def main_BV64_Flash_ROM0():
    main_BV_Flash_ROM(0)
def main_BV64_Flash_ROM1():
    main_BV_Flash_ROM(1)
def main_BV64_Flash_ROM2():
    main_BV_Flash_ROM(2)
def main_BV64_Flash_ROM3():
    main_BV_Flash_ROM(3)


def main_BV64_Dump_ROM0():
    main_BV64_Dump_ROM(0)
def main_BV64_Dump_ROM1():
    main_BV64_Dump_ROM(1)
def main_BV64_Dump_ROM2():
    main_BV64_Dump_ROM(2)
def main_BV64_Dump_ROM3():
    main_BV64_Dump_ROM(3)
    
def main_BV64_Dump_32K1():
    main_BV64_Dump_32K(0,0)
def main_BV64_Dump_32K2():
    main_BV64_Dump_32K(0,1)
def main_BV64_Dump_32K3():
    main_BV64_Dump_32K(0,2)
def main_BV64_Dump_32K4():
    main_BV64_Dump_32K(0,3)

def main_BV64_Dump_32K21():
    main_BV64_Dump_32K(1,0)
def main_BV64_Dump_32K22():
    main_BV64_Dump_32K(1,1)
def main_BV64_Dump_32K23():
    main_BV64_Dump_32K(1,2)
def main_BV64_Dump_32K24():
    main_BV64_Dump_32K(1,3)

def main_BV64_Dump_32K31():
    main_BV64_Dump_32K(2,0)
def main_BV64_Dump_32K32():
    main_BV64_Dump_32K(2,1)
def main_BV64_Dump_32K33():
    main_BV64_Dump_32K(2,2)
def main_BV64_Dump_32K34():
    main_BV64_Dump_32K(2,3)

def main_BV64_Dump_32K41():
    main_BV64_Dump_32K(3,0)
def main_BV64_Dump_32K42():
    main_BV64_Dump_32K(3,1)
def main_BV64_Dump_32K43():
    main_BV64_Dump_32K(3,2)
def main_BV64_Dump_32K44():
    main_BV64_Dump_32K(3,3)

def main_BV64_Dump_128K0():
    main_BV64_Dump_128K(0)
def main_BV64_Dump_128K1():
    main_BV64_Dump_128K(1)
def main_BV64_Dump_128K2():
    main_BV64_Dump_128K(2)
def main_BV64_Dump_128K3():
    main_BV64_Dump_128K(3)

def main_Cam_Dump_RAM():
    global BankSize
    global RAMsize
    global RAMbuffer
    BankSize=16384 #bytes per bank
    RAMsize=32768*4
    main_dumpRAM()
    main_SaveRAM()

def main_Cam_Burn_RAM():
    global RAMbuffer
    global RAMsize
    if main_LoadRAM() == 1:
        RAMsize=32768*4
        main_BurnRAM()

def main_BV_Burn_32K0():
    main_BV_SetBank(0,0)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K1():
    main_BV_SetBank(0,1)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K2():
    main_BV_SetBank(0,2)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K3():
    main_BV_SetBank(0,3)
    if main_LoadRAM() == 1:
        main_BurnRAM()

def main_BV_Burn_32K10():
    main_BV_SetBank(1,0)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K11():
    main_BV_SetBank(1,1)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K12():
    main_BV_SetBank(1,2)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K13():
    main_BV_SetBank(1,3)
    if main_LoadRAM() == 1:
        main_BurnRAM()

def main_BV_Burn_32K20():
    main_BV_SetBank(2,0)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K21():
    main_BV_SetBank(2,1)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K22():
    main_BV_SetBank(2,2)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K23():
    main_BV_SetBank(2,3)
    if main_LoadRAM() == 1:
        main_BurnRAM()

def main_BV_Burn_32K30():
    main_BV_SetBank(3,0)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K31():
    main_BV_SetBank(3,1)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K32():
    main_BV_SetBank(3,2)
    if main_LoadRAM() == 1:
        main_BurnRAM()
def main_BV_Burn_32K33():
    main_BV_SetBank(3,3)
    if main_LoadRAM() == 1:
        main_BurnRAM()

def main_BV_Burn_128k0():
    main_BV_Burn_128k(0)
def main_BV_Burn_128k1():
    main_BV_Burn_128k(1)
def main_BV_Burn_128k2():
    main_BV_Burn_128k(2)
def main_BV_Burn_128k3():
    main_BV_Burn_128k(3)
    
def main_BV_Burn_128k(bnum):
    global RAMbuffer
    global RAMsize
    if main_LoadRAM() == 1:
        RAMsize=32768
        tempRAMbuffer=RAMbuffer
        RAMbuffer=tempRAMbuffer[0:32768]
        main_BV_SetBank(bnum,0)
        main_BurnRAM()
        RAMbuffer=tempRAMbuffer[32768:65536]
        main_BV_SetBank(bnum,1)
        main_BurnRAM()
        RAMbuffer=tempRAMbuffer[65536:98304]
        main_BV_SetBank(bnum,2)
        main_BurnRAM()
        RAMbuffer=tempRAMbuffer[98304:131072]
        main_BV_SetBank(bnum,3)
        main_BurnRAM()

def main_BV64_Dump_128K(blk):
    global BankSize
    global RAMsize
    global RAMbuffer
    TempRAMbuffer = b''
    BankSize=16384 #bytes per bank
    RAMsize=32768
    main_BV_SetBank(blk,0)
    main_dumpRAM()
    TempRAMbuffer=RAMbuffer        
    main_BV_SetBank(blk,1)
    main_dumpRAM()
    TempRAMbuffer=TempRAMbuffer +RAMbuffer       
    main_BV_SetBank(blk,2)
    main_dumpRAM()
    TempRAMbuffer=TempRAMbuffer +RAMbuffer       
    main_BV_SetBank(blk,3)
    main_dumpRAM()
    RAMbuffer=TempRAMbuffer +RAMbuffer       
    RAMsize=32768*4
    main_SaveRAM()
    
def main_BV64_Dump_32K(blk,sublk):
    global BankSize
    global RAMsize
    BankSize=16384 #bytes per bank
    RAMsize=32768
    main_BV_SetBank(blk,sublk)
    main_dumpRAM()
    main_SaveRAM()


def main_BV_lockBank(bnum):
#Lock cart before writing
    bnum=bnum+0x90
    print ('Flash locked to ',hex(bnum))
    dev.write(0x01,[0x0A,0x00,0x03,0x70,0x00,0x00,0x70,0x01,0x00,0x70,0x02,bnum]) #Lock flash block 
    USBbuffer = dev.read(0x81,64)

def main_BV_SetBank(blk,sublk):#1-4:1-4
#Lock cart before writing
    sublk = sublk * 64
    print (hex(blk),hex(sublk))
    dev.write(0x01,[0x0A,0x00,0x03,0x70,0x00,sublk,0x70,0x01,0xE0,0x70,0x02,blk]) #Lock flash block 
    USBbuffer = dev.read(0x81,64)

def main_BV_Flash_ROM(block):
    FFtest=""
    FFtest=b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'

    main_LoadROM()
    FlashBlockSize=131072
    messagebox.showinfo('Block Change Required','Please remove and insert Flash cart, then click OK')
    main_BV_lockBank(block)
    print ('from flashrom() ',ROMsize,FlashBlockSize)
    NumOfBlks=int(ROMsize/FlashBlockSize)
    if NumOfBlks==0:
        NumOfBlks=1
    print ('erasing ',NumOfBlks)
    print('Erasing ROM Area required for flash') 
    for blknum in range (0,NumOfBlks):
        main_BV_EraseFlashBlock(blknum)
    print('Writing ROM Data') 
    ROMpos=0
    waitcount=0
    for BankNumber in range (0,int((ROMsize/16384))):
        main_ROMBankSwitch(BankNumber) #Set the bank
        print ( BankNumber*16384, ' of ' ,ROMsize)
        for ROMAddress in range (0x4000,0x8000,32):
            if BankNumber==0:
                ROMAddress=ROMAddress-0x4000
            AddHi=ROMAddress>>8
            AddLo=ROMAddress&0xFF
            Data32Bytes=ROMbuffer[ROMpos:ROMpos+32]
            if Data32Bytes == FFtest:
                pass
            else:
                AddHi=AddHi.to_bytes(1,'little')
                AddLo=AddLo.to_bytes(1,'little')
                FlashWriteCommand=b'\x20\x00\x04\x2A\x0A\xAA\xA9\x05\x55\x56'+AddHi+AddLo+b'\x26'+AddHi+AddLo+b'\x1F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                USBoutputPacket = FlashWriteCommand+Data32Bytes
                dev.write(0x01,USBoutputPacket)
                while main_IsFlashBusy()==1:
                    pass
                    waitcount+=1
                    if waitcount==10:
                        print ('Error: ',USBoutputPacket,BankNumber,AddHi,AddLo,ROMpos)
                waitcount=0
            ROMpos+=32
    app.lowerLeftLabel.set(str(ROMsize)+' Bytes Written' )
    messagebox.showinfo('Block Unlock Required','Writing Complete. Please remove and insert Flash cart, then click OK')


def main_MX_Burn_ROM():

    #erase Flash

    print ("Erasing Flash")
    mx1()
    while main_JPN_Read(0)!=255:
        pass
    print ("Chip erase complete")
    main_LoadROM()
    addold=0
    print('Writing ROM Data') 
    for address in range (0,ROMsize,32):

        AddHi=(address>>16)&0xFF
        AddMe=(address>>8)&0xFF
        AddLo=address&0xFF
        Data32Bytes=ROMbuffer[address:address+32]
        AddHi=AddHi.to_bytes(1,'little')
        AddMe=AddMe.to_bytes(1,'little')
        AddLo=AddLo.to_bytes(1,'little')

        FlashWriteCommand=b'\x23'+AddHi+AddMe+AddLo
        Data32Bytes=ROMbuffer[address:address+32]
        USBoutputPacket = FlashWriteCommand+Data32Bytes
        dev.write(0x01,USBoutputPacket)
        USBbuffer = dev.read(0x81,64)
        print ("writing",address,ROMsize)
            
    app.lowerLeftLabel.set(str(ROMsize)+' Bytes Written' )
    messagebox.showinfo('Operation Complete','Writing Complete.')

def mx1():
    dev.write(0x01,[0x0A,0x00,0x07, 0x3f,0x00,0x41, 0x55,0x55,0xAA, 0x2A,0xAA,0x55, 0x55,0x55,0x80, 0x55,0x55,0xAA, 0x2A,0xAA,0x55, 0x55,0x55,0x10])
    print ("Erasing Flash")
    while main_JPN_Read(0)!=255:
        pass
    print ("Chip erase complete")

def mx2():    
        dev.write(0x01,[0x23,0x00,0x00,0x20,0x01,0x02,0x03,0x04,0x05,0x06,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55])
        USBbuffer = dev.read(0x81,64)

def mx3(address):
        AddHi=(address>>16)&0xFF
        AddMe=(address>>8)&0xFF
        AddLo=address&0xFF
        Data32Bytes=b'\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55\x55'
        AddHi=AddHi.to_bytes(1,'little')
        AddMe=AddMe.to_bytes(1,'little')
        AddLo=AddLo.to_bytes(1,'little')
        FlashWriteCommand=b'\x23'+AddHi+AddMe+AddLo
        USBoutputPacket = FlashWriteCommand+Data32Bytes
        dev.write(0x01,USBoutputPacket)
        USBbuffer = dev.read(0x81,64)


def main_EMS64_PageSwap():
    dev.write(0x01,[0x13])
    USBbuffer = dev.read(0x81,64)

def main_EMS64_Burn_ROM():
    main_EMS64_Flash_ROM()
    pass



def main_EMS64_Flash_ROM():
    FFtest=""
    for usbfill in range(32):
        FFtest=FFtest+"\xFF"
    main_LoadROM()
    FlashBlockSize=131072
    NumOfBlks=int(ROMsize/FlashBlockSize)
    if NumOfBlks==0:
        NumOfBlks=1
    print ('erasing ',NumOfBlks)
    print('Erasing ROM Area required for flash') 
    for blknum in range (0,NumOfBlks):
        main_EMS64_EraseFlashBlock(blknum)
    print('Writing ROM Data') 
    ROMpos=0
    waitcount=0
    for BankNumber in range (0,int((ROMsize/16384))):
        main_ROMBankSwitch(BankNumber) #Set the bank
        print ( BankNumber*16384, ' of ' ,ROMsize)
        for ROMAddress in range (0x4000,0x8000,32):
            if BankNumber==0:
                ROMAddress=ROMAddress-0x4000
            AddHi=ROMAddress>>8
            AddLo=ROMAddress&0xFF
            Data32Bytes=ROMbuffer[ROMpos:ROMpos+32]
            AddHi=AddHi.to_bytes(1,'little')
            AddLo=AddLo.to_bytes(1,'little')
            #0x21 for flash algo for EMS
            FlashWriteCommand=b'\x21\x01\x02\xD0'+AddHi+AddLo+b'\xE8'+AddHi+AddLo+b'\x1F\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            USBoutputPacket = FlashWriteCommand+Data32Bytes
            dev.write(0x01,USBoutputPacket)
            while main_IsFlashBusyEMS()==1:
                pass
                waitcount+=1
                if waitcount==10:
                    print ('Error: ',USBoutputPacket,BankNumber,AddHi,AddLo,ROMpos)
            waitcount=0
            ROMpos+=32
    app.lowerLeftLabel.set(str(ROMsize)+' Bytes Written' )
    messagebox.showinfo('Operation Complete','Writing Complete.')
    #return to read mode - datasheet says write 0xFF to any address
    main_ROMBankSwitch(0)
    dev.write(0x01,[0x0A,0x01,0x01,0x00,0x00,0xFF])
    USBbuffer = dev.read(0x81,64)
    

def main_EMS64_EraseFlashBlock(BlockNum): #1 block = 128kbytes of ROM ()
    main_ROMBankSwitch(BlockNum*8)
    print ('Erasing Block '+str(BlockNum))
    dev.write(0x01,[0x0A,0x01,0x02,0x40,0x00,0x20,0x40,0x00,0xD0])
    USBbuffer = dev.read(0x81,64)
    waitcount=0    
    while main_IsFlashBusyEMS()==1:
        waitcount+=1
        #print (waitcount)
        if waitcount==100000:
            print ('Error: ',BlockNum)
            exit()
    #return to read mode - datasheet says write 0xFF to any address
    dev.write(0x01,[0x0A,0x01,0x01,0x40,0x00,0xFF])
    USBbuffer = dev.read(0x81,64)
    print ('Done')

def main_Catskull_erase():
    print ("Erasing...")
    dev.write(0x01,[0x0A,0x01,0x06,0x55,0x55,0xAA,0x2A,0xAA,0x55,0x55,0x55,0x80,0x55,0x55,0xAA,0x2A,0xAA,0x55,0x55,0x55,0x10])
    RAMbuffer= dev.read(0x81,64)
    while main_ELCheapo_Read(0)[0]!=0xFF:
        pass
    print ("Erased")

def main_Catskull_write():
    if main_LoadROM() == 1:
        main_Catskull_erase()
        print('Writing ROM Data') 
        ROMpos=0
        for ROMAddress in range (0x0000,0x8000,1):
            AddHi=ROMAddress>>8
            AddLo=ROMAddress&0xFF
            Data1Byte=ROMbuffer[ROMpos:ROMpos+1]
            dev.write(0x01,[0x0A,0x01,0x04,0x55,0x55,0xAA,0x2A,0xAA,0x55,0x55,0x55,0xA0,AddHi,AddLo,Data1Byte[0]])
            ROMpos+=1
            messagebox.showinfo('Operation Complete','Writing Complete.')
    return
#Universal routines

def main_dumpROM():
    global ROMbuffer
    global USBbuffer
    ROMfileName=asksaveasfilename(defaultextension=".GB",filetypes=(("GB ROM File","*.GB"),("GBC ROM File","*.GBC"),("GBA ROM File","*.GBA"),("All Files","*.*")))
    if ROMfileName:
        ROMfile=open(ROMfileName,'wb')
        for bankNumber in range(0,(int(ROMsize/BankSize))):
            print ('Dumping ROM:',int(bankNumber*BankSize),' of ',ROMsize)
            if bankNumber == 0:
                ROMaddress=0 #get bank 0 from address 0, not setbank(0) and get from high bank...
            else:
                ROMaddress=BankSize
            main_ROMBankSwitch(bankNumber)    #switch to new bank.
            for packetNumber in range(0,(int(BankSize/64))):
                AddHi=ROMaddress>>8
                AddLo=ROMaddress&0xFF
                dev.write(0x01,[0x10,0x00,0x00,AddHi,AddLo])
                ROMbuffer= dev.read(0x81,64)
                ROMfile.write(ROMbuffer)
                ROMaddress += 64
        ROMfile.close()
        print ('Done!')



def main_dumpMXROM():
    global ROMbuffer
    global USBbuffer
    ROMfileName=asksaveasfilename(filetypes=(("GB ROM File","*.GB"),("GBC ROM File","*.GBC"),("GBA ROM File","*.GBA"),("All Files","*.*")))
    if ROMfileName:
        ROMfile=open(ROMfileName,'wb')
        for bankNumber in range(0,(int(ROMsize/BankSize))):
            print ('Dumping ROM:',int(bankNumber*BankSize),' of ',ROMsize)
            if bankNumber == 0:
                ROMaddress=0 #get bank 0 from address 0, not setbank(0) and get from high bank...
            else:
                ROMaddress=BankSize
            main_MXROMBankSwitch(bankNumber)    #switch to new bank.
            for packetNumber in range(0,(int(BankSize/64))):
                AddHi=ROMaddress>>8
                AddLo=ROMaddress&0xFF
                dev.write(0x01,[0x10,0x00,0x00,AddHi,AddLo])
                ROMbuffer= dev.read(0x81,64)
                ROMfile.write(ROMbuffer)
                ROMaddress += 64
        ROMfile.close()
        print ('Done!')


def main_dumpRAM():
    global RAMsize
    global RAMbuffer
    global USBbuffer
    global BankSize
    RAMbuffer=b''
    for bankNumber in range(0,(int(RAMsize/8192))):
        RAMaddress=0xA000
        main_RAMBankSwitch(bankNumber)
        for packetNumber in range(0,int(8192/64)):
            AddHi=RAMaddress>>8
            AddLo=RAMaddress&0xFF
            dev.write(0x01,[0x11,0x00,0x00,AddHi,AddLo])
            USBbuffer = dev.read(0x81,64)
            RAMaddress += 64
            RAMbuffer=b''.join([RAMbuffer,USBbuffer]) #faster way of doing it


def main_dumpRAM2():
    global RAMsize
    global RAMbuffer
    global USBbuffer
    global BankSize
    RAMbuffer=b''
    RAMaddress=0xA000
    for packetNumber in range(0,int(512/64)):
        AddHi=RAMaddress>>8
        AddLo=RAMaddress&0xFF
        dev.write(0x01,[0x11,0x00,0x00,AddHi,AddLo])
        USBbuffer = dev.read(0x81,64)
        RAMaddress += 64
        RAMbuffer=b''.join([RAMbuffer,USBbuffer]) #faster way of doing it
    print ("Done")

def main_BurnRAM():
    global RAMsize
    global RAMbuffer
    global USBbuffer
    global BankSize
    RAMaddress=0xA000
    Rpos=0

    for bankNumber in range(0,(int(RAMsize/8192))):
        RAMaddress=0xA000
        main_RAMBankSwitch(bankNumber)
        for packetNumber in range(0,int(128)):
            AddHi=RAMaddress>>8
            AddLo=RAMaddress&0xFF
            dev.write(0x01,[0x12,0x00,0x00,AddHi,AddLo])
            USBbuffer = dev.read(0x81,64)
            dev.write(0x01,RAMbuffer[Rpos:Rpos+64])
            USBbuffer = dev.read(0x81,64)
            RAMaddress += 64
            Rpos+=64
    print ("Done")

def main_BurnRAM2():#MBC2
    global RAMsize
    global RAMbuffer
    global USBbuffer
    global BankSize
    Rpos=0
    RAMaddress=0xA000
    for packetNumber in range(0,int(8)):
        AddHi=RAMaddress>>8
        AddLo=RAMaddress&0xFF
        dev.write(0x01,[0x12,0x00,0x00,AddHi,AddLo])
        USBbuffer = dev.read(0x81,64)
        dev.write(0x01,RAMbuffer[Rpos:Rpos+64])
        USBbuffer = dev.read(0x81,64)
        RAMaddress += 64
        Rpos+=64
    print ("Done")
   
def main_IsFlashBusy():
    dev.write(0x01,[0x0B,0x00]) #IsFlashBusy?
    temp = dev.read(0x81,64)
    if temp[0]==0x01:
        return(1)
    if temp[0]==0x00:
        return(0)
    
def main_IsFlashBusyEMS():
    dev.write(0x01,[0x0C,0x00]) #IsFlashBusy?
    temp = dev.read(0x81,64)
    if temp[0]==0x01:
        return(1)
    if temp[0]==0x00:
        return(0)

def main_BV_EraseFlashBlock(BlockNum): #1 block = 128kbytes of ROM (BV cart)
    main_ROMBankSwitch(BlockNum*8)
    print ('Erasing Block '+str(BlockNum))
    dev.write(0x01,[0x0A,0x00,0x06,0x0A,0xAA,0xA9,0x05,0x55,0x56,0x0A,0xAA,0x80,0x0A,0xAA,0xA9,0x05,0x55,0x56,0x40,0x00,0x30])
    USBbuffer = dev.read(0x81,64)
    waitcount=0    
    while main_IsFlashBusy()==1:
        waitcount+=1
        if waitcount==100000:
            print ('Error: ',BlockNum)
            exit()
    
    print ('Done')

def main_ROMBankSwitch(bankNumber):
    #Convert 16bit bank number to 2 x 8bit numbers
    #Write to address defined under MBC settings to swap banks. This will change depending on certain cart types...
    bhi=bankNumber>>8
    blo=bankNumber&0xFF
    if bhi > 0:
        dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,bhi])
        USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x21,0x00,blo])
    USBbuffer = dev.read(0x81,64)


def main_MXROMBankSwitch(bankNumber):
    #Convert 16bit bank number to 2 x 8bit numbers
    #Write to address defined under MBC settings to swap banks. This will change depending on certain cart types...
    blo=bankNumber&0xFF + 0x40
    dev.write(0x01,[0x0A,0x00,0x01,0x3F,0x00,blo])
    USBbuffer = dev.read(0x81,64)


def main_RAMBankSwitch(bankNumber):
    print ("Bank:"+str(bankNumber))
    #Convert 16bit bank number to 2 x 8bit numbers
    #Write to address defined under MBC settings to swap banks. This will change depending on certain cart types...
    blo=bankNumber&0xFF
    dev.write(0x01,[0x0A,0x00,0x01,0x40,0x00,blo])
    USBbuffer = dev.read(0x81,64)

def main_JPN_test():
    main_JPN_F2()
    main_JPN_F4()

    dev.write(0x01,[0x0A,0x00, 0x02  ,0x01,0x20,0x01 ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00, 0x02  ,0x01,0x20,0x02 ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)

    main_JPN_F5(0xA0) # or is it F5
    
    
    main_JPN_F5(0x60)


    main_JPN_F5(0xE0)
    
    dev.write(0x01,[0x0A,0x00, 0x02  ,0x01,0x20,0x02 ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)

    dev.write(0x01,[0x0A,0x00, 0x02  ,0x01,0x20,0x02 ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)

    for k in range (16):
        dev.write(0x01,[0x0A,0x00, 0x10  ,0x55,0x55,0x55 ,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55,0x55] )
        USBbuffer = dev.read(0x81,64)
    
    
def main_JPN_Unlock_ROM():
    main_JPN_F2()
    main_JPN_F4()
    main_JPN_F1(0x5555,0xAA)
    main_JPN_F1(0x2AAA,0x55)
    main_JPN_F1(0x5555,0x60)
    main_JPN_F1(0x5555,0xAA)
    main_JPN_F1(0x2AAA,0x55)
    main_JPN_F1(0x0000,0x40)    
    
def main_JPN_Burn_ROM():
    #Enable Flash Writing/Access
    main_JPN_F2()
    main_JPN_F4()
    main_JPN_EraseFlash()       
    #Flash Cart
    if main_LoadROM() == 1:
        addold=0
        for address in range (0,ROMsize,32):

            AddHi=(address>>16)&0xFF
            AddMe=(address>>8)&0xFF
            AddLo=address&0xFF
            Data32Bytes=ROMbuffer[address:address+32]
            AddHi=AddHi.to_bytes(1,'little')
            AddMe=AddMe.to_bytes(1,'little')
            AddLo=AddLo.to_bytes(1,'little')

            FlashWriteCommand=b'\x22'+AddHi+AddMe+AddLo
            Data32Bytes=ROMbuffer[address:address+32]
            USBoutputPacket = FlashWriteCommand+Data32Bytes
            dev.write(0x01,USBoutputPacket)
            USBbuffer = dev.read(0x81,64)
            trying=0
            while (main_JPN_Read(0)&0x80)!=128:
                trying=trying+1
                if trying==100:
                    print ("Failed writing to sector",address)
                    break
            if addold != address >> 13:
                print (address,"bytes of",ROMsize)
            addold=address >> 13
            
                
        app.lowerLeftLabel.set(str(ROMsize)+' Bytes Written' )
        messagebox.showinfo('Operation Complete','Writing Complete.')

        main_JPN_F1(0x0000,0xF0)
        #Disable Flash Access
        main_JPN_F3()
    return

def main_JPN_EraseFlash():
    #Erase Flash Cart - 64kbyte blocks, 0x00000, 0x10000, 0x20000 etc.... MBC 16kbytes/bank - 4 banks/block.
    main_JPN_F1(0x5555,0xAA)
    main_JPN_F1(0x2AAA,0x55)
    main_JPN_F1(0x5555,0x80)
    main_JPN_F1(0x5555,0xAA)
    main_JPN_F1(0x2AAA,0x55)
    main_JPN_F1(0x5555,0x10)
    while main_JPN_Read(0)!=128:
        pass
    
def main_JPN_F1(Address,Data):
    AddHi=Address>>8
    AddLo=Address&0xFF
    dev.write(0x01,[0x0A,0x00, 0x05  ,0x01,0x20,0x0F ,0x01,0x25,AddHi ,0x01,0x26,AddLo ,0x01,0x27,Data ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)
def main_JPN_F2():
    dev.write(0x01,[0x0A,0x00, 0x04  ,0x01,0x20,0x09 ,0x01,0x21,0xAA ,0x01,0x22,0x55 ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)
def main_JPN_F3():
    dev.write(0x01,[0x0A,0x00, 0x02  ,0x01,0x20,0x08 ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)
def main_JPN_F4():
    dev.write(0x01,[0x0A,0x00, 0x09  ,0x01,0x20,0x0A ,0x01,0x25,0x62 ,0x01,0x26,0x04 ,0x01,0x27,0x00 ,0x01,0x3F,0xA5 ,0x01,0x20,0x01 ,0x01,0x3F,0xA5, 0x01,0x20,0x02 ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)
def main_JPN_F5(inst):
    dev.write(0x01,[0x0A,0x00, 0x03  ,0x01,0x20,0x10 ,0x01,0x3F,0xA5 ,0x01,0x21,0x01 ] )
    USBbuffer = dev.read(0x81,64)
    main_JPN_F1(0x5555,0xAA)
    main_JPN_F1(0x2AAA,0x55)
    main_JPN_F1(0x5555,inst)
def main_JPN_F6(data):
    dev.write(0x01,[0x0A,0x00, 0x02  ,0x01,0x20,(0xC0&data) ,0x01,0x3F,0xA5] )
    USBbuffer = dev.read(0x81,64)
def main_JPN_F7(inst):
    main_JPN_F1(0x4555,0xAA)
    main_JPN_F1(0x42AA,0x55)
    main_JPN_F1(0x4555,inst)

def main_JPN_Read(Address):
    AddHi=Address>>8
    AddLo=Address&0xFF
    dev.write(0x01,[0x10,0x00,0x00,AddHi,AddLo])
    ROMbuffer= dev.read(0x81,64)
    return (ROMbuffer[0])

def JPN_Read(Address):
    AddHi=Address>>8
    AddLo=Address&0xFF
    dev.write(0x01,[0x10,0x00,0x00,AddHi,AddLo])
    ROMbuffer= dev.read(0x81,64)
    return (ROMbuffer)

#GBA Stuff
def main_GBA_ReadHeader():
    global ROMsize
    dev.write(0x01,[0x30,0x00,0x00,0x00,0x40])
    USBbuffer = dev.read(0x81,64)
    print (str(USBbuffer[32:44],'utf-8'))
    app.ROMtitleLabel.set("ROM Title: "+str(USBbuffer[32:44],'utf-8'))
    app.MAPPERtypeLabel.set("GBA Cart: No Mapper")

    fsize=256
    if main_GBA_GetByte(0x800000)== (0,0,0,0,0,0,0,0):
        fsize=128
    if main_GBA_GetByte(0x400000)== (0,0,0,0,0,0,0,0):
        fsize=64
    if main_GBA_GetByte(0x200000)== (0,0,0,0,0,0,0,0):
        fsize=32
    if main_GBA_GetByte(0x100000)== (0,0,0,0,0,0,0,0):
        fsize=16
    if main_GBA_GetByte(0x80000)== (0,0,0,0,0,0,0,0):
        fsize=8
    app.ROMsizeLabel.set("ROM Size: "+str(fsize)+' Mbits')
    
    print ('Size Autodetected as',fsize,'Mbits (not 100% accurate)')

def main_GBA_Dump_8():
    global ROMsize
    ROMsize=1048576
    main_GBA_Dump()
def main_GBA_Dump_16():
    global ROMsize
    ROMsize=1048576*2
    main_GBA_Dump()
def main_GBA_Dump_32():
    global ROMsize
    ROMsize=1048576*4
    main_GBA_Dump()
def main_GBA_Dump_64():
    global ROMsize
    ROMsize=1048576*8
    main_GBA_Dump()
def main_GBA_Dump_128():
    global ROMsize
    ROMsize=1048576*16
    main_GBA_Dump()

def main_GBA_GetByte(Address):
    Lo=Address&0xFF
    Me=(Address&0xFF00) >> 8
    Hi=(Address&0xFF0000) >> 16
    dev.write(0x01,[0x30,0x00,Hi,Me,Lo])
    ROMbuffer= dev.read(0x81,64)
    return ROMbuffer[0],ROMbuffer[1],ROMbuffer[2],ROMbuffer[3],ROMbuffer[4],ROMbuffer[5],ROMbuffer[6],ROMbuffer[7]

def main_GBA_GetByte(Address):
    Lo=Address&0xFF
    Me=(Address&0xFF00) >> 8
    Hi=(Address&0xFF0000) >> 16
    dev.write(0x01,[0x30,0x00,Hi,Me,Lo])
    ROMbuffer= dev.read(0x81,64)
    Tbuff=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    k=0
    for t in range (1,64,2):
        Tbuff[k]=ROMbuffer[t]&1
        k=k+1
    return Tbuff

def main_GBA_EEPROM_Read(Address):
    Lo=Address&0xFF
    Me=(Address&0xFF00) >> 8
    Hi=(Address&0xFF0000) >> 16
    dev.write(0x01,[0x38,0x00,Hi,Me,Lo])
    ROMbuffer= dev.read(0x81,64)
    return ROMbuffer[0:8]


def main_GBA_EEPROM_Write(Address):
    Lo=Address&0xFF
    Me=(Address&0xFF00) >> 8
    Hi=(Address&0xFF0000) >> 16
    dev.write(0x01,[0x37,0x00,Hi,Me,Lo,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00])
    ROMbuffer= dev.read(0x81,64)
    print('done')    

def main_GBA_EEPROM_WriteFF(Address):
    Lo=Address&0xFF
    Me=(Address&0xFF00) >> 8
    Hi=(Address&0xFF0000) >> 16
    dev.write(0x01,[0x37,0x00,Hi,Me,Lo,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF])
    ROMbuffer= dev.read(0x81,64)
    print('done')    

   
def main_GBA_Dump():
    ROMfileName=asksaveasfilename(defaultextension=".GBA",filetypes=(("GBA ROM File","*.GBA"),("All Files","*.*")))
    Hi2=0
    if ROMfileName:
        ROMfile=open(ROMfileName,'wb')
        Address=0
        for Address in range(0,int(ROMsize/2),32):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Hi=(Address&0xFF0000) >> 16
            dev.write(0x01,[0x30,0x00,Hi,Me,Lo])
            ROMbuffer= dev.read(0x81,64)
            ROMfile.write(ROMbuffer)
            if Hi2 != Hi:
                print(str(Address*2)+' Bytes of '+str(ROMsize))
            Hi2=Hi
        ROMfile.close()
        print ('Done!')


def main_GBA_Flash_Erase():
     for sectors in range (0,255):
         main_GBA_Sector_Erase(sectors)
         

def main_GBA_Sector_Erase(Sector):
    Shi=Sector >> 1
    Slo=Sector << 7
    Shi=Shi&0xFF
    Slo=Slo&0xFF
    
    dev.write(0x01,[0x31,0x06,  0x00,0x05,0x55,0x00,0xA9, 0x00,0x02,0xAA,0x00,0x56, 0x00,0x05,0x55,0x00,0x80, 0x00,0x05,0x55,0x00,0xA9,  0x00,0x02,0xAA,0x00,0x56,  Shi,Slo,0x00,0x00,0x30,])
    ROMbuffer= dev.read(0x81,64)
    #Is flash busy?
    dev.write(0x01,[0x33])
    IFB = dev.read(0x81,64)
    while IFB[0]==1:
        dev.write(0x01,[0x33])
        IFB = dev.read(0x81,64)
    print ((Sector+1)*65536,'Bytes Erased')        
    

def main_GBA_Flash_ROM():
#Test for BV Flash Cart
    if main_GBA_Read_CFI()==1:
        main_LoadROM()
        Hi2=0

        secta=(int(ROMsize/65536))+1
        
        for sectors in range (0,secta):
            main_GBA_Sector_Erase(sectors)
        
        for ROMaddress in range (0,ROMsize,32):
            Address=int(ROMaddress/2)
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Hi=(Address&0xFF0000) >> 16
            Data32Bytes=ROMbuffer[ROMaddress:ROMaddress+32]
            Hi=Hi.to_bytes(1,'little')
            Me=Me.to_bytes(1,'little')
            Lo=Lo.to_bytes(1,'little')

            FlashWriteCommand=b'\x32'+Hi+Me+Lo+b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
            USBoutputPacket = FlashWriteCommand+Data32Bytes
            dev.write(0x01,USBoutputPacket)
            response=dev.read(0x81,64)
            if Hi2 != Hi:
                print (ROMaddress,' bytes of ',ROMsize ,'Written...')
                Hi2=Hi
        print (ROMsize,' Written!')
        messagebox.showinfo('Operation Complete','Writing Complete.')
        main_GBA_ReadHeader()
def main_GBA_Read_CFI():
#Enter CFI Mode
    dev.write(0x01,[0x31,0x01,  0x00,0x00,0x55,0x00,0x98])
    ROMbuffer= dev.read(0x81,64)
    dev.write(0x01,[0x30,0x00,0x00,0x00,0x10])
    ROMbuffer= dev.read(0x81,64)
    dev.write(0x01,[0x30,0x00,0x00,0x00,0x20])
    buffer= dev.read(0x81,64)
    if ROMbuffer[0]==82 and ROMbuffer[2]==81 and ROMbuffer[4]==90 :
        print ('CFI Present')
        print (2<< int(buffer[14]-1), 'bytes capacity')
        dev.write(0x01,[0x31,0x01,0x00,0x00,0x00,0x00,0xF0])#Exit from CFI mode
        buffer= dev.read(0x81,64)
        
        return(1)
    else:
        return(0)

def main_GBA_Testcode():
    dev.write(0x01,[0x30,0x00,0x00,0x00,0x00])
    ROMbuffer= dev.read(0x81,64)
    print (ROMbuffer)    
    dev.write(0x01,[0x31,0x03,  0x00,0x05,0x55,0x00,0xA9,0x00,0x02,0xAA,0x00,0x56,0x00,0x05,0x55,0x00,0x88])
    ROMbuffer= dev.read(0x81,64)
    dev.write(0x01,[0x30,0x00,0x00,0x00,0x00])
    ROMbuffer= dev.read(0x81,64)
    print (ROMbuffer)
    
def main_GBA_Dump64kSRAM():
    RAMfileName=asksaveasfilename(defaultextension=".SAV",filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if RAMfileName:
        RAMfile=open(RAMfileName,'wb')
        Address=0
        for Address in range(0,32768*2,64):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Hi=(Address&0xFF0000) >> 16
            dev.write(0x01,[0x35,0x00,Hi,Me,Lo])
            RAMbuffer= dev.read(0x81,64)
            RAMfile.write(RAMbuffer)
        RAMfile.close()
        print ('Done!')

def main_GBA_EEPROM_64k():
    RAMfileName=asksaveasfilename(defaultextension=".SAV",filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if RAMfileName:
        RAMfile=open(RAMfileName,'wb')
        Address=0
        for Address in range(0,1024):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Hi=(Address&0xFF0000) >> 16
            dev.write(0x01,[0x38,0x00,Hi,Me,Lo])
            RAMbuffer= dev.read(0x81,64)
            RAMfile.write(RAMbuffer[0:8])
        RAMfile.close()
        print ('Done!')

def main_GBA_EEPROM_4k():
    RAMfileName=asksaveasfilename(defaultextension=".SAV",filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if RAMfileName:
        RAMfile=open(RAMfileName,'wb')
        Address=0
        for Address in range(0,64):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Hi=(Address&0xFF0000) >> 16
            dev.write(0x01,[0x3C,0x00,Hi,Me,Lo])
            RAMbuffer= dev.read(0x81,64)
            RAMfile.write(RAMbuffer[0:8])
        RAMfile.close()
        print ('Done!')

def main_GBA_Write64kEEPROM():
    root.update()
    SRAMfileName=askopenfilename(filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if SRAMfileName:
        SRAMfile=open(SRAMfileName,'rb')
        SRAMbuffer=SRAMfile.read()
        SRAMsize=len(SRAMbuffer)

        for Address in range(0,1024):
            Lo2=Address&0xFF
            Me2=(Address&0xFF00) >> 8
            Data8Bytes=SRAMbuffer[(Address*8):(Address*8)+8]
            Me=Me2.to_bytes(1,'little')
            Lo=Lo2.to_bytes(1,'little')
            WriteCommand=b'\x37\x00\x00'+Me+Lo
            Dataout=WriteCommand+Data8Bytes
            dev.write(0x01,Dataout)
            RAMbuffer= dev.read(0x81,64)

            for WriteDelay in range (0,10):#10 usb write transactions = 10ms
                dev.write(0x01,[0x38,0x00,0x00,Me2,Lo2])

        SRAMfile.close()
        print ('Done!')

def main_GBA_Write4kEEPROM():
    root.update()
    SRAMfileName=askopenfilename(filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if SRAMfileName:
        SRAMfile=open(SRAMfileName,'rb')
        SRAMbuffer=SRAMfile.read()
        SRAMsize=len(SRAMbuffer)

        for Address in range(0,64):
            Lo2=Address&0xFF
            Me2=(Address&0xFF00) >> 8
            Data8Bytes=SRAMbuffer[(Address*8):(Address*8)+8]
            Me=Me2.to_bytes(1,'little')
            Lo=Lo2.to_bytes(1,'little')
            WriteCommand=b'\x3D\x00\x00'+Me+Lo
            Dataout=WriteCommand+Data8Bytes
            dev.write(0x01,Dataout)
            RAMbuffer= dev.read(0x81,64)

            for WriteDelay in range (0,10):#10 usb write transactions = 10ms
                dev.write(0x01,[0x38,0x00,0x00,Me2,Lo2])

        SRAMfile.close()
        print ('Done!')

    

def main_GBA_Dump64kFLASH():
    #Test for SRAM First!!!
    RAMfileName=asksaveasfilename(defaultextension=".SAV",filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if RAMfileName:
        RAMfile=open(RAMfileName,'wb')
        Address=0
        dev.write(0x01,[0x39,0x00,0x00,0x00,0x00,0x00])
        RAMbuffer= dev.read(0x81,64)
        for Address in range(0,32768*2,64):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Hi=(Address&0xFF0000) >> 16
            dev.write(0x01,[0x35,0x00,Hi,Me,Lo])
            RAMbuffer= dev.read(0x81,64)
            RAMfile.write(RAMbuffer)
        RAMfile.close()
        print ('Done!')


def main_GBA_Dump128kFLASH():
    #Test for SRAM First!!!
    RAMfileName=asksaveasfilename(defaultextension=".SAV",filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if RAMfileName:
        RAMfile=open(RAMfileName,'wb')
        Address=0
        dev.write(0x01,[0x39,0x00,0x00,0x00,0x00,0x00])
        RAMbuffer= dev.read(0x81,64)
        for Address in range(0,32768*2,64):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Hi=(Address&0xFF0000) >> 16
            dev.write(0x01,[0x35,0x00,Hi,Me,Lo])
            RAMbuffer= dev.read(0x81,64)
            RAMfile.write(RAMbuffer)
        dev.write(0x01,[0x39,0x00,0x00,0x00,0x00,0x01])
        RAMbuffer= dev.read(0x81,64)
        for Address in range(0,32768*2,64):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Hi=(Address&0xFF0000) >> 16
            dev.write(0x01,[0x35,0x00,Hi,Me,Lo])
            RAMbuffer= dev.read(0x81,64)
            RAMfile.write(RAMbuffer)
        RAMfile.close()
        print ('Done!')

def main_GBA_FlashSaveErase():
    dev.write(0x01,[0x3A,0x00,0x00,0x00])
    RAMbuffer= dev.read(0x81,64)
    dev.write(0x01,[0x35,0x00,0x00,0x00,0x00])
    RAMbuffer= dev.read(0x81,64)    
    while RAMbuffer[0]!=255:
        dev.write(0x01,[0x35,0x00,0x00,0x00,0x00])
        RAMbuffer= dev.read(0x81,64)
    print ('FlashSave Erased')

    

def main_GBA_Write64kSRAM():
    root.update()
    SRAMfileName=askopenfilename(filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if SRAMfileName:
        SRAMfile=open(SRAMfileName,'rb')
        SRAMbuffer=SRAMfile.read()
        SRAMsize=len(SRAMbuffer)

        for Address in range(0,SRAMsize,32):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Data32Bytes=SRAMbuffer[Address:Address+32]
            Me=Me.to_bytes(1,'little')
            Lo=Lo.to_bytes(1,'little')
            WriteCommand=b'\x36\x00\x00'+Me+Lo
            Dataout=WriteCommand+Data32Bytes
            dev.write(0x01,Dataout)
            RAMbuffer= dev.read(0x81,64)
        SRAMfile.close()
        print ('Done!')

def main_GBA_Write128kFLASHRAM():
    root.update()
    SRAMfileName=askopenfilename(filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if SRAMfileName:
        main_GBA_FlashSaveErase()
        SRAMfile=open(SRAMfileName,'rb')
        SRAMbuffer=SRAMfile.read()
        SRAMsize=len(SRAMbuffer)


        dev.write(0x01,[0x39,0x00,0x00,0x00,0x00,0x00])
        RAMbuffer= dev.read(0x81,64)

        for Address in range(0,65535,32):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Data32Bytes=SRAMbuffer[Address:Address+32]
            Me=Me.to_bytes(1,'little')
            Lo=Lo.to_bytes(1,'little')
            WriteCommand=b'\x3B\x00\x00'+Me+Lo
            Dataout=WriteCommand+Data32Bytes
            dev.write(0x01,Dataout)
            RAMbuffer= dev.read(0x81,64)
            
        dev.write(0x01,[0x39,0x00,0x00,0x00,0x00,0x01])
        RAMbuffer= dev.read(0x81,64)

        for Address in range(65536,131071,32):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Data32Bytes=SRAMbuffer[Address:Address+32]
            Me=Me.to_bytes(1,'little')
            Lo=Lo.to_bytes(1,'little')
            WriteCommand=b'\x3B\x00\x00'+Me+Lo
            Dataout=WriteCommand+Data32Bytes
            dev.write(0x01,Dataout)
            RAMbuffer= dev.read(0x81,64)


        SRAMfile.close()
        print ('Done!')

def main_GBA_Write64kFLASHRAM():
    root.update()
    SRAMfileName=askopenfilename(filetypes=(("GBA Save File","*.SAV"),("All Files","*.*")))
    if SRAMfileName:
        main_GBA_FlashSaveErase()
        SRAMfile=open(SRAMfileName,'rb')
        SRAMbuffer=SRAMfile.read()
        SRAMsize=len(SRAMbuffer)
        dev.write(0x01,[0x39,0x00,0x00,0x00,0x00,0x00])
        RAMbuffer= dev.read(0x81,64)
        for Address in range(0,SRAMsize,32):
            Lo=Address&0xFF
            Me=(Address&0xFF00) >> 8
            Data32Bytes=SRAMbuffer[Address:Address+32]
            Me=Me.to_bytes(1,'little')
            Lo=Lo.to_bytes(1,'little')
            WriteCommand=b'\x3B\x00\x00'+Me+Lo
            Dataout=WriteCommand+Data32Bytes
            dev.write(0x01,Dataout)
            RAMbuffer= dev.read(0x81,64)
        SRAMfile.close()
        print ('Done!')



def main_ELCheapo_Erase():
    print ("Erasing...")
    dev.write(0x01,[0x0A,0x01,0x06,0x0A,0xAA,0xAA,0x05,0x55,0x55,0x0A,0xAA,0x80,0x0A,0xAA,0xAA,0x05,0x55,0x55,0x0A,0xAA,0x10])
    RAMbuffer= dev.read(0x81,64)
    while main_ELCheapo_Read(0)[0]!=0xFF:
        pass
    print ("Erased")
 
def main_ELCheapo_Read(Address):
    AddHi=Address>>8
    AddLo=Address&0xFF
    dev.write(0x01,[0x10,0x00,0x00,AddHi,AddLo])
    ROMbuffer= dev.read(0x81,64)
    return (ROMbuffer)


def main_ELCheapo_Write():
    
    if main_LoadROM() == 1:
        print('Writing ROM Data') 
        main_ELCheapo_Erase()
        ROMpos=0
        waitcount=0
        for BankNumber in range (0,int((ROMsize/16384))):
            main_ROMBankSwitch(BankNumber) #Set the bank
            print ( BankNumber*16384, ' of ' ,ROMsize)
            for ROMAddress in range (0x4000,0x8000,32):
                if BankNumber==0:
                    ROMAddress=ROMAddress-0x4000
                AddHi=ROMAddress>>8
                AddLo=ROMAddress&0xFF
                Data32Bytes=ROMbuffer[ROMpos:ROMpos+32]
                
                #byte by byte write, its slow....

                AddHi=AddHi.to_bytes(1,'little')
                AddLo=AddLo.to_bytes(1,'little')

                FlashWriteCommand=b'\x24\x00'+AddHi+AddLo
                USBoutputPacket = FlashWriteCommand+Data32Bytes
                dev.write(0x01,USBoutputPacket)
                USBbuffer = dev.read(0x81,64)

                ROMpos+=32
        app.lowerLeftLabel.set(str(ROMsize)+' Bytes Written' )
        messagebox.showinfo('Operation Complete','Writing Complete.')
        #return to read mode - datasheet says write 0xFF to any address
        main_ROMBankSwitch(0)

    return


def main_ELCheapoSD_Erase():
    print ("Erasing...")

    dev.write(0x01,[0x0A,0x00,0x01,0x00,0x00,0x05]) # Enable WE and SPI
    USBbuffer = dev.read(0x81,64)
   
    dev.write(0x01,[0x0A,0x00,0x06,0x0A,0xAA,0xAA,0x05,0x55,0x55,0x0A,0xAA,0x80,0x0A,0xAA,0xAA,0x05,0x55,0x55,0x0A,0xAA,0x10])
    RAMbuffer= dev.read(0x81,64)
    while main_ELCheapo_Read(0)[0]!=0xFF:
        pass
    print ("Erased")
 
def main_ELCheapoSD_Read(Address):
    AddHi=Address>>8
    AddLo=Address&0xFF
    dev.write(0x01,[0x10,0x00,0x00,AddHi,AddLo])
    ROMbuffer= dev.read(0x81,64)
    return (ROMbuffer)


def main_ELCheapoSD_Write():
    
    if main_LoadROM() == 1:
        print('Writing ROM Data')
        print ("Erasing...")

        dev.write(0x01,[0x0A,0x00,0x01,0x00,0x00,0x05]) # Enable WE and SPI
        USBbuffer = dev.read(0x81,64)
       
        dev.write(0x01,[0x0A,0x00,0x06,0x0A,0xAA,0xAA,0x05,0x55,0x55,0x0A,0xAA,0x80,0x0A,0xAA,0xAA,0x05,0x55,0x55,0x00,0x00,0x30])
        RAMbuffer= dev.read(0x81,64)
        while main_ELCheapo_Read(0)[0]!=0xFF:
            pass
        print ("Erased")    



        ROMpos=0
        waitcount=0
        for BankNumber in range (0,int((ROMsize/16384))):
            print(main_ELCheapo_Read(0x4000))
            main_ROMBankSwitch(BankNumber) #Set the bank
            print(main_ELCheapo_Read(0x4000))

            print ( BankNumber, BankNumber*16384, ' of ' ,ROMsize)
            for ROMAddress in range (0x4000,0x8000,32):
    #            if BankNumber==0:
    #                ROMAddress=ROMAddress-0x4000
                AddHi=ROMAddress>>8
                AddLo=ROMAddress&0xFF
                Data32Bytes=ROMbuffer[ROMpos:ROMpos+32]
                
                #byte by byte write, its slow....

                AddHi=AddHi.to_bytes(1,'little')
                AddLo=AddLo.to_bytes(1,'little')

                #print(ROMAddress)

                FlashWriteCommand=b'\x25\x00'+AddHi+AddLo
                USBoutputPacket = FlashWriteCommand+Data32Bytes
                dev.write(0x01,USBoutputPacket)
                USBbuffer = dev.read(0x81,64)



                ROMpos+=32
        app.lowerLeftLabel.set(str(ROMsize)+' Bytes Written' )
        messagebox.showinfo('Operation Complete','Writing Complete.')
        #return to read mode - datasheet says write 0xFF to any address
        main_ROMBankSwitch(0)
    return

def SD_Init():
    dev.write(0x01,[0x0A,0x00,0x01,0x00,0x00,0x05]) # Map SPI to 0x3000
    USBbuffer = dev.read(0x81,64)

    for init in range (0,10):
        dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,0xFF]) # Clock out 0xFF
        USBbuffer = dev.read(0x81,64)
        dev.write(0x01,[0x0A,0x00,0x01,0x10,0x00,0x03]) # with CS high
        USBbuffer = dev.read(0x81,64)

    #CMD0
    dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,0x40]) # Clock out 0x40
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x10,0x00,0x01]) # with CS Low
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,0x00]) # Clock out 0x00
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x10,0x00,0x01]) # with CS Low
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,0x00]) # Clock out 0x00
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x10,0x00,0x01]) # with CS Low
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,0x00]) # Clock out 0x00
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x10,0x00,0x01]) # with CS Low
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,0x00]) # Clock out 0x00
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x10,0x00,0x01]) # with CS Low
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,0x95]) # Clock out 0x95
    USBbuffer = dev.read(0x81,64)
    dev.write(0x01,[0x0A,0x00,0x01,0x10,0x00,0x01]) # with CS Low
    USBbuffer = dev.read(0x81,64)
    #Wait for response
        

    for wait in range (0,4):
        dev.write(0x01,[0x0A,0x00,0x01,0x30,0x00,0xFF]) # Clock out 0xFF
        USBbuffer = dev.read(0x81,64)
        dev.write(0x01,[0x0A,0x00,0x01,0x10,0x00,0x01]) # with CS Low
        USBbuffer = dev.read(0x81,64)
        print(main_ELCheapoSD_Read(0x3000))






def main_GSWrite():
    dev.write(0x01,[0x0A,0x00,0x06 ,0x55,0x55,0xAA ,0x2A,0xAA,0x55 ,0x55,0x55,0x80 ,0x55,0x55,0xaa ,0x2a,0xaa,0x55 ,0x55,0x55,0x10])
    tmp=dev.read(0x81,64) #erase first
    
    if main_LoadROM() == 1:
        print('Writing ROM Data') 
        ROMpos=0
        waitcount=0
        dev.write(0x01,[0x0A,0x00,0x01,0x40,0x00,0x01]) #set bank 1
        tmp=dev.read(0x81,64)
        print ("Bank set")
        for ROMAddress in range (0x0000,0x1000):
            AddHi=ROMAddress>>8
            AddLo=ROMAddress&0xFF
            DataByte=ROMbuffer[ROMAddress]
            AddHi=AddHi.to_bytes(1,'little')
            AddLo=AddLo.to_bytes(1,'little')
            DataByte=DataByte.to_bytes(1,'little')
            FlashWriteCommand=b'\x0A\x00\x04\x55\x55\xAA\x2A\x2A\x55\x55\x55\xA0'+AddHi+AddLo+DataByte
            USBoutputPacket = FlashWriteCommand
            dev.write(0x01,USBoutputPacket)
            USBbuffer = dev.read(0x81,64)
    return
            
root= Tk()
root.geometry("400x300")
app = Window(root)
dev = usb.core.find(idVendor=0x046d, idProduct=0x1234)
if dev is None:
    messagebox.showinfo("USB Error","I Cant find your hardware! Check the device is plugged in and the USB driver is installed")
    exit()
if dev is not None:
    root.update()
    messagebox.showinfo("Welcome","Gen3 is a work in progress, please report any bugs or requests to Bennvenn@hotmail.com")
    dev.set_configuration()
    main_CheckVersion()
    root.mainloop()


