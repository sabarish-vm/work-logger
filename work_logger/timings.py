import datetime as dt
import pandas as pd
from argparse import ArgumentParser, RawTextHelpFormatter
import os
tIMINGSDIR=os.path.join(os.path.expanduser('~'),'.timings')
todayFile=os.path.join(tIMINGSDIR,'today.csv')
archiveFile=os.path.join(tIMINGSDIR,'archive.csv')
targetTimeHours=8
targetTimeSecs=3600*targetTimeHours

def archiveLoader(filepath) :
    if not os.path.exists(tIMINGSDIR) :
        os.makedirs(tIMINGSDIR)
    else : pass
    if os.path.exists(archiveFile) and os.path.exists(todayFile) :
        df1=pd.read_csv(archiveFile)
        df2=pd.read_csv(todayFile)
        df=pd.concat([df1,df2])
        df.to_csv(archiveFile,index=False)
        os.remove(todayFile) 
    if not os.path.exists(archiveFile) and os.path.exists(todayFile): 
        os.rename(todayFile,archiveFile)
    elif not os.path.exists(archiveFile) and not os.path.exists(todayFile):
        df = pd.DataFrame(columns=['In','Out','Duration','Comments'])
        df.to_csv(archiveFile,index=False)
        df.to_csv(todayFile,index=False)
    else : pass
    with open(filepath,'w') as f :
        f.write('')
        
def datechecker() :
    today=dt.datetime.today().date().isoformat()
    tempfile=os.path.join(tIMINGSDIR,'.'+today)
    if os.path.exists(tempfile) : pass
    else : archiveLoader(tempfile)
    
def todayLoader(path) :
    datechecker()
    if os.path.exists(path) : df = pd.read_csv(path,index_col=None)
    else : 
        df = pd.DataFrame(columns=['In','Out','Duration','Comments'])
        df.to_csv(path,index=False)
    return df

def toHumanTime(timeInSecs):
    return f"{timeInSecs//60//60:2.0f}:{timeInSecs//60 - (timeInSecs//60//60*60):2.0f}"

def imin() :
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-c',dest='comment',type=str,
                        help="Pass comments",
                        )
    args = parser.parse_args()
    comment = args.comment
    print(comment)
    df=todayLoader(todayFile)
    length = df.__len__()
    ind=length-1
    if length ==0 : 
        df.loc[0,'In'] = dt.datetime.now().isoformat()
        df.loc[0,'Comments'] = comment
    elif pd.isna(df.loc[ind]['Out']) : raise Exception("Out time not logged !")
    else : 
        df.loc[ind+1,'In'] = dt.datetime.now().isoformat()
        df.loc[0,'Comments'] = comment
    df.to_csv(todayFile,index=False)
    return df

def imout() :
    df=todayLoader(todayFile)
    length = df.__len__()
    ind=length-1
    if length == 0 : raise Exception("No logs found for today !")
    elif not pd.isna(df.loc[ind]['In']) and not pd.isna(df.loc[ind]['Out']) : raise Exception("In time not logged !")
    else :
        now = dt.datetime.now() 
        df.loc[ind,'Out'] = now.isoformat()
        intime = dt.datetime.fromisoformat(df.loc[ind,'In'])
        df.loc[ind,'Duration'] = (now-intime).seconds
        print('Time left:',toHumanTime(targetTimeSecs-df['Duration'].sum()))
    df.to_csv(todayFile,index=False)
    return df