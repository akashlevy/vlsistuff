
import string,types
import logs
KNOWNFUNCTIONS = 'ext sxt resize conv_std_logic_vector conv_integer unsigned'.split()

Transtable = {}
Transtable['!PureExt'] = ['input','output','inout']
Transtable['!IntKind'] = ['wire','reg']

Varsx = []
def matches(List,Seq,Verbose=False):
    global Varsx
    if Verbose:
        logs.log_info('try list=%s pattern=%s'%(List,Seq))
    if type(Seq) is list:
        return listMatches(List,Seq,Verbose)
    if type(Seq) is tuple:
        return listMatches(List,Seq,Verbose)
    Lseq = Seq.split()
    if len(List)!=len(Lseq): 
        if Verbose: logs.log_info('matches stopped at length %d<>%d iseq=%s who=%s '%(len(Lseq),len(List),Lseq,List))
        return False
    Vars=[]
    for ind,Iseq in enumerate(Lseq):
        Lind = List[ind]
        if isinstance(Lind,(tuple,list)):
            Litem = Lind[1]
        else:
            Litem = Lind

        if Iseq == '?': 
            Vars.append(List[ind])
        elif Iseq[0] == '?': 
            Kind = Iseq[1:]
            if Lind[1]!=Kind:
                return False
            else:
                Vars.append(Lind)
           
        elif Iseq[0] == '!': 
            if Iseq in Transtable:
                Options = Transtable[Iseq]
                if List[ind][0] in Options:
                    Vars.append(List[ind])
                else:
                    return False
            elif (Iseq[1:]!=List[ind][0])and(Iseq[1:]!=List[ind][1]): 
                if Verbose: logs.log_info('matches stopped(0) at iseq=%s who=%s '%(Iseq,List[ind]))
                return False
            else:
                Vars.append(List[ind])
        elif Iseq == '$': 
            Who = List[ind]
            if Who in KNOWNFUNCTIONS:
                Vars.append(List[ind])
            else:
                if Verbose: logs.log_info('matches stopped(1) at iseq=%s who=%s '%(Iseq,Who))
                return False

        elif (Iseq!=Litem):
            if Verbose: logs.log_info('matches stopped(2) at iseq=|%s| who=|%s| %s '%(Iseq,Litem,List[ind]))
            return False
    Varsx = Vars[:]
    if Vars==[]: return True 
    return Vars 


def listMatches(List,Seq,Verbose):
    global Varsx
    X0 = listMatches__(List,Seq,Verbose)
    if Verbose: logs.log_info('listMatches match(x0)=%s %s %s'%(X0,List,Seq))
    Varsx = X0
    return X0

def listMatches__(List,Seq,Verbose):
    if type(List) is int:
        List = str(List)
    if Seq=='?':
        return [List]

    if type(List) is tuple: List = list(List)
    if type(Seq) is tuple: Seq = list(Seq)
    if Verbose:
        logs.log_info('try(0) list=%s pattern=%s'%(List,Seq))
    if str(List)==str(Seq):
        pass
    elif (isinstance(List,(tuple,list)))and(isinstance(Seq,(tuple,list))): 
        pass
    elif type(List)!=type(Seq): 
        if Verbose: logs.log_info('failed on dff types %s %s list=%s pattern=%s'%(type(List),type(Seq),List,Seq))
        return False
    if type(List) is str:
        if Seq=='?': return [List]
        Ok =  str(Seq)==str(List)
        if Verbose and not Ok: logs.log_info('failed on dff token list=%s pattern=%s'%(List,Seq))
        return Ok
    if len(List)!=len(Seq): 
        if Verbose: logs.log_info('failed on dff len list=%s pattern=%s'%(List,Seq))
        return False
    Res=[]
    for ind,Item in enumerate(List):
        V = listMatches(Item,Seq[ind],Verbose)
        if not V: return False
        if isinstance(V,(list,tuple)):
            Res.extend(V)
    if Res==[]:  return True
    return Res 

