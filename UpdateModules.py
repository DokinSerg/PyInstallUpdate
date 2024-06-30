# pylint: disable-msg=W0611
import os,traceback,platform,ctypes,sys
# from rich import print as rpn
from time import sleep#perf_counter,
from subprocess import Popen, PIPE,TimeoutExpired#,SubprocessError
from datetime import datetime,timezone,date,timedelta
#####################################################################################################################################################
_author  = 't.me/dokin_sergey'
_version = '1.5.3'
_verdate = '2024-06-17 11:21'
_LogLocPath = os.path.dirname(__file__)
_GlobaLen = 120
#----------------------------------------------------------------------------------
try:
    while True:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            while True:
                print('\nПрограмма запущена БЕЗ прав администратора')
                print('\nПопытаться перезапустить c правами администратора      -> [Enter]')
                print('\nПродолжить с установкой модулей в профиль пользователя -> [Y]')
                print('\nЗавершить работу программы                             -> [0]')
                knu = input('\nВаш выбор :->').strip()
                if knu =='0':os._exit(0)
                if knu in ('Y','y','Д','д',''):break
            #--------------------------------------------------------------------------------
            if not knu:
                ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, __file__,None,1)
                os._exit(0)
            else:break
        break
except Exception as AMess:
    print(f'{AMess}')

#----------------------------------------------------------------------------------
class DokExcept(Exception):
    def __init__(self, message:str):
        super().__init__(message)
#-------------------------------------
debug = False
#####################################################################################################################################################
try:
    _LogFile  = fr'{_LogLocPath}\UpdMod_logg_{str(date.today())}.txt'
    _ListModl = fr'{_LogLocPath}\ModuList.txt'
except Exception as EMess:
    print(f'Ошибка: {EMess}')
    print(f'Ошибка: {traceback.format_exc()}')
#####################################################################################################################################################
def WordRead(Wrd:str)->bool:
    Wres = False
    if   Wrd.isalnum():
        Wres = True
    else:
        for iw in Wrd:
            if (ord(iw) in range(33,125)) or (ord(iw) in range(192,255)):
                Wres = True
                break
    return Wres
################################################################################################################################################################
def FileWrite(FlName:str,NetStr:str,WMess:tuple[str,...])->bool:# = '',LMess:tuple[str] = ())->bool:
    try:
        with open(FlName, mode = 'a', encoding = 'utf_8') as fwl:
            for istr in WMess:
                print(f'{NetStr}{istr}', file = fwl)
    except Exception as FMess:
        LogErrDebug('Failure',f'{FMess}','FileWrite')
        LogErrDebug('Failure',f'{traceback.format_exc()}','FileWrite')
        print(f'Ошибка: {FMess}')
        print(f'Ошибка: {traceback.format_exc()}')
        return False
    return True
################################################################################################################################################################
def LogErrDebug(Mess1:str,Mess2:str, Mess3:str = '')->bool:
    TypeMess = ('Warning','Failure','Update_','Install','Message','ErroCMD')#Caution
    if len(Mess1) == 7 and Mess1 in TypeMess:
        TMess = Mess1#+' '
        RMess = Mess2
        Funct = Mess3
    else:
        TMess = 'Message'
        RMess = Mess1
        Funct = Mess2
    ListMess = []
    try:
        dtnow = datetime.now(timezone.utc) + timedelta(hours=3)
        dtstr = dtnow.strftime("%H:%M:%S")
        PrnStr = f'{dtstr};{TMess};'
        lFN = 12
        FN = f'{Funct:{lFN}} ;' if Funct else f'{" ":{lFN}} ; '
        PrnStr += FN
        ListStr = str(RMess).splitlines()
        tstr = ''
        for iStr in ListStr:
            if iStr and not iStr.isspace():
                ListWr = iStr.split()
                for iLW in ListWr:
                    if iLW:# and WordRead(iLW):
                        tstr += f' {iLW}'
                    if len(tstr) >_GlobaLen+1:
                        ListMess.append(tstr)
                        tstr = ''
        if tstr: ListMess.append(tstr)
    #---------------------------------------------------------------------------------------------------------------------------
        TupleMess = tuple(ListMess)
        if _LogFile:
            if TMess not in ('Install','Update_'):FileWrite(_LogFile,PrnStr,TupleMess)
            if TMess == 'Install':FileWrite(_LogFile,PrnStr,(f'{RMess}',))
            if TMess == 'Update_':FileWrite(_LogFile,PrnStr,(f'{RMess}',))
        #------------------------------------------------------------------------------------------------
        if debug: print(f'{dtstr} ; [yellow]{RMess}')
    except Exception as Err:
        Led = False
        if debug:print(str(Err))
    else:
        Led = True
    return Led
#####################################################################################################################################################
def cmdexec(CMDcom:list[str],cleer:int = 1)->str:
    # global
    cmdres = ''
    try:
    #---------------------------------------------------------------------------------------------------------------------
        print('\n\t[', end = '', flush=True)
        with Popen(CMDcom, shell=True,stdout = PIPE,stderr = PIPE, encoding="cp866") as popps:#
            for ici in range(100):
                if popps.poll():break
                if not ici % 5:print('#', end = '', flush=True)
                sleep(0.1)
            print(f'] {(ici+1)/10:.2f} c\n')
            pls = popps.communicate()
        # print(f'Результат:{pls}')
        if bool(pls[0]):cmdres = str(pls[0])#.decode('cp866')
        if bool(pls[1]):
            if cleer:raise DokExcept (pls[1])
            cmdres += str(pls[1])
    #----------------------------------------------------------------------------------------------------------------------
    except DokExcept as Mess:
        print(f'Проблема:{Mess}')
        LogErrDebug('Warning',f'Проблема:{Mess}','cmdexec')
    except TimeoutExpired as Mess:
        LogErrDebug('Failure',f'Таймаут:{Mess}','cmdexec')
        print(f'Таймаут:{Mess}')
    except Exception as MErs:
        LogErrDebug('Failure',f'{MErs}','cmdexec')
        LogErrDebug('Failure',f'{traceback.format_exc()}','cmdexec')
        print(f'{MErs}')
        print(f'{traceback.format_exc()}')
    return cmdres
###########################################################################################################################
def cmdexecNoOut(CMDcom:list[str])->None:
    try:
    #,stdout = PIPE,stderr = PIPE
    #---------------------------------------------------------------------------------------------------------------------
        with Popen(CMDcom, shell=True, encoding="cp866") as popps:
            popps.communicate(timeout=120)
    #----------------------------------------------------------------------------------------------------------------------
    except TimeoutExpired as Mess:
        print(f'Таймаут:{Mess}')
        LogErrDebug('Failure',f'Таймаут:{Mess}','cmdexecNoOut')
    except Exception as MErs:
        LogErrDebug('Failure',f'{MErs}','cmdexecNoOut')
        LogErrDebug('Failure',f'{traceback.format_exc()}','cmdexecNoOut')
        print(f'{MErs}')
        print(f'{traceback.format_exc()}')
###########################################################################################################################
def InstMod(ModName:str)->bool:
    LogErrDebug('Message',f'{ModName = } ','InstMod')
    try:
        _cmdlist = ['pip3','install',ModName]
        cmdexecNoOut(_cmdlist)
        LogErrDebug('Install',f'{ModName = } ','InstMod')
    #----------------------------------------------------------------------------------------------------------------------
    except Exception as MErs:
        LogErrDebug('Failure',f'{MErs}','cmdexecNoOut')
        LogErrDebug('Failure',f'{traceback.format_exc()}','cmdexecNoOut')
        print(f'{MErs}')
        print(f'{traceback.format_exc()}')
        return False
    return True
###########################################################################################################################
def LoadIniSett(SFile:str = _ListModl)->dict[str,bool]:
    DctMod:dict[str,bool] = {}
    try:
        with  open(SFile, mode = 'r', encoding = 'utf_8') as sfl:
            filetxt = sfl.readlines()
        for ist in filetxt:
            if ist:DctMod[ist.strip()] = False
    except Exception as MErs:
        LogErrDebug('Failure',f'{MErs}','cmdexecNoOut')
        LogErrDebug('Failure',f'{traceback.format_exc()}','cmdexecNoOut')
        print(f'{MErs}')
        print(f'{traceback.format_exc()}')
    return DctMod
###########################################################################################################################
if __name__ == '__main__':
    print(f'Обновление модулей вер.{_version} для Python ver.{platform.python_version()}')
    # debug = True
    #---------------------------------------------------------------------------------------------------------------------------
    FileWrite(_LogFile,'',('*'*(_GlobaLen+20),))
    InstDict = LoadIniSett()
    #--------------------------------------------------------------------------------------------------------------------------------------
    LogErrDebug('Message',f'Программы установки и обновления Pytnob: {_version} ; от {_verdate} ; Автор {_author} ; ', os.path.basename(__file__))
    LogErrDebug('Message',f'Установлен Python ver.{platform.python_version()} ; {platform.python_build()[1]} ; {platform.python_compiler()}', os.path.basename(__file__))
#------------------------------------------------------------------------
    os.chdir(r'C:\Program Files\Python312\Scripts')
#----------------------------------------------------------------------- Установка, '-a'
    while True:
        try:
            import pip
            cmdlist = ['pip','wheel']
            rez = cmdexec(cmdlist,0)
            if (rez.splitlines()[-1]).startswith(r'[notice] To update'):
                cmdlist = ['python.exe','-m','pip','install','--upgrade','pip']
                cmdexecNoOut(cmdlist)
                input(':->')
            break
        except ModuleNotFoundError as MErs:
            LogErrDebug('Failure',f'{MErs}','__main__')
            print(f'\tМодуль PIP не установлен: {MErs}')
            if not input('Установить? :-> '):
                cmdlist = ['python','-m','ensurepip','--upgrade']
                cmdexecNoOut(cmdlist)
            else:
                print('Продолжение невозможно. Выход через 3 сек.')
                sleep(3)
                os._exit(0)
#----------------------------------------------------------------------- Установка, '-a'
    while True:
        try:
            import pipdeptree
            break
        except ModuleNotFoundError as MErs:
            LogErrDebug('Failure',f'{MErs}','cmdexecNoOut')
            print(f'\tМодуль pipdeptree не установлен: {MErs}')
            if not input('Установить? :-> '):
                InstMod('pipdeptree')
            else:
                print('Продолжение невозможно. Выход через 3 сек.')
                sleep(3)
                os._exit(0)
    #--------------------------------------------------------------------------------------
    cmdlist = ['pipdeptree',]
    UpdDict = {};Inst = False;Updt = False
    rez = cmdexec(cmdlist)
    restxt = rez.splitlines()#[2:]
    if restxt:
        LogErrDebug('Install','Установлены модули ; версий', os.path.basename(__file__))
        print('\tУстановлены модули ; версий\n')
    for ipr in restxt:
        if '==' in ipr:
            ai,bi = ipr.split('==')
            LogErrDebug('Install',f'{ai:18} ; {bi}', os.path.basename(__file__))
            print(f'\t{ai:18} ; {bi}')
            UpdDict[ai] = False #Создаем словарь установленных компонентов для обновления
            if ai in InstDict: InstDict[ai] = True #Помечаем ТРЕБУЕМЫЕ компоненты как установленные
    #----------------------------------------------------------------------------------------------
    # print('\n\tНеобходимо установить\n')
    for ii,ij in InstDict.items():
        if not ij:
            print(f'\t{ii:18}')
            Inst = True
    if Inst:
        print('\nНеобходимо установить перечисленные компоненты')
        if not input('\nВыполнить? :-> '):
            LogErrDebug('Install','Дополнительно установлены', os.path.basename(__file__))
            for ii,ij in InstDict.items():
                if not ij:InstMod(f'{ii}')
    print(f'\n{'*'*100}')
    #-------------------------------------------------
    Upd2Dict = {}
    cmdlist = ['pip3', 'list','-o']
    rez = cmdexec(cmdlist)
    if  rez:
        restxt = rez.splitlines()[2:]
        if restxt:LogErrDebug('Install','Необходимо обновить указанные компоненты', os.path.basename(__file__))
        for ipr in restxt:
            name,old,new,_ = ipr.split()#[0]
            LogErrDebug('Install',f'{name:18} ; {old:8} ; {new:8}', os.path.basename(__file__))
            if name in UpdDict:
                UpdDict[name] = True #Помечаем компонентов требующие обновления
            else:Upd2Dict[name] = True #2-я очередь обновлений
    #------------------------------------------------------Обновление---------------------------------
    for ui,uj in UpdDict.items():
        if uj:
            print(f'{ui}')
            Updt = True
    if Updt:
        print('Необходимо обновить указанные компоненты')
        if not input('Выполнить? :-> \n'):
            LogErrDebug('Install','Обновленные модули', os.path.basename(__file__))
            for ui,uj in UpdDict.items():
                if uj:
                    print(f'Модуль {ui}')
                    cmdlist = ['pip3','install','-U',f'{ui}']
                    cmdexecNoOut(cmdlist)
                    LogErrDebug('Install',f'{ui:20} ', os.path.basename(__file__))
    if Upd2Dict:
        for ui,uj in Upd2Dict.items():
            if uj:
                print(f'Модуль {ui}')
                cmdlist = ['pip3','install','-U',f'{ui}']
                cmdexecNoOut(cmdlist)
                LogErrDebug('Install',f'{ui:20} ', os.path.basename(__file__))
    if not Updt and not Upd2Dict:
        print('Все модули последней версии')
    #----------------------------------------------------------------------
    # from rich import print as rpn
    # cmdlist = ['pipdeptree',]
    # rez = cmdexecNoOut(cmdlist)
    # rez = cmdexec(cmdlist)
    # restxt = rez.splitlines()#[2:]
    # for tst in restxt:
        # print(tst)
    #----------------------------------------------------------------------
    input('\nВыход :-> ')
    os._exit(0)
