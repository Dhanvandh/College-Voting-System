'''
import pandas as pd
from pathlib import Path

# path = Path("C:/Users/Desktop/Sem-5/CS301 CN/Project/Voting/database")
path = Path("database")

def count_reset():
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Name','Gender','Roll Number','Class','Passw','hasVoted']]
    for index, row in df.iterrows():
        df['hasVoted'].iloc[index]=0
    df.to_csv(path/'voterList.csv')

    df=pd.read_csv(path/'cand_list.csv')
    df=df[['Sign','Name','Vote Count']]
    for index, row in df.iterrows():
        df['Vote Count'].iloc[index]=0
    df.to_csv (path/'cand_list.csv')


def reset_voter_list():
    df = pd.DataFrame(columns=['voter_id','Name','Gender','Roll Number','Class','Passw','hasVoted'])
    df=df[['voter_id','Name','Gender','Roll Number','Class','Passw','hasVoted']]
    df.to_csv(path/'voterList.csv')

def reset_cand_list():
    df = pd.DataFrame(columns=['Sign','Name','Vote Count'])
    df=df[['Sign','Name','Vote Count']]
    df.to_csv(path/'cand_list.csv')


def verify(vid,passw):
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Passw','hasVoted']]
    for index, row in df.iterrows():
        if df['voter_id'].iloc[index]==vid and df['Passw'].iloc[index]==passw:
            return True
    return False


def isEligible(vid):
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Name','Gender','Roll Number','Class','Passw','hasVoted']]
    for index, row in df.iterrows():
        if df['voter_id'].iloc[index]==vid and df['hasVoted'].iloc[index]==0:
            return True
    return False


def vote_update(st,vid):
    if isEligible(vid):
        df=pd.read_csv (path/'cand_list.csv')
        df=df[['Sign','Name','Vote Count']]
        for index, row in df.iterrows():
            if df['Sign'].iloc[index]==st:
                df['Vote Count'].iloc[index]+=1

        df.to_csv (path/'cand_list.csv')

        df=pd.read_csv(path/'voterList.csv')
        df=df[['voter_id','Name','Gender','Roll Number','Class','Passw','hasVoted']]
        for index, row in df.iterrows():
            if df['voter_id'].iloc[index]==vid:
                df['hasVoted'].iloc[index]=1

        df.to_csv(path/'voterList.csv')

        return True
    return False


def show_result():
    df=pd.read_csv (path/'cand_list.csv')
    df=df[['Sign','Name','Vote Count']]
    v_cnt = {}
    for index, row in df.iterrows():
        v_cnt[df['Sign'].iloc[index]] = df['Vote Count'].iloc[index]
    # print(v_cnt)
    return v_cnt


def taking_data_voter(name,gender,zone,city,passw):
    df=pd.read_csv(path/'voterList.csv')
    df=df[['voter_id','Name','Gender','Roll Number','Class','Passw','hasVoted']]
    row,col=df.shape
    if row==0:
        vid = 10001
        df = pd.DataFrame({"voter_id":[vid],
                    "Name":[name],
                    "Gender":[gender],
                    "Roll Number":[zone],
                    "Class":[city],
                    "Passw":[passw],
                    "hasVoted":[0]},)
    else:
        vid=df['voter_id'].iloc[-1]+1
        df1 = pd.DataFrame({"voter_id":[vid],
                    "Name":[name],
                    "Gender":[gender],
                    "Roll number":[zone],
                    "Class":[city],
                    "Passw":[passw],
                    "hasVoted":[0]},)

        df = pd.concat([df, df1],ignore_index=True)

    df.to_csv(path/'voterList.csv')

    return vid
'''








'''
import pandas as pd
from pathlib import Path

path = Path("database")

class ElectionDB:
    def __init__(self):
        self.path = path
        self.path.mkdir(exist_ok=True)
        self.init_db()

    def init_db(self):
        if not (self.path/'voterList.csv').exists():
            reset_voter_list()
        if not (self.path/'cand_list.csv').exists():
            reset_cand_list()

    def verify(self, vid, passw):
        try:
            df = pd.read_csv(self.path/'voterList.csv')
            return ((df['voter_id'] == vid) & (df['Passw'] == passw)).any()
        except:
            return False

    def is_eligible(self, vid):
        try:
            df = pd.read_csv(self.path/'voterList.csv')
            return ((df['voter_id'] == vid) & (df['hasVoted'] == 0)).any()
        except:
            return False

    def vote_update(self, st, vid):
        if self.is_eligible(vid):
            # Update candidate votes
            cand_df = pd.read_csv(self.path/'cand_list.csv')
            cand_df.loc[cand_df['Sign'] == st, 'Vote Count'] += 1
            cand_df.to_csv(self.path/'cand_list.csv', index=False)
            
            # Mark voter as voted
            voter_df = pd.read_csv(self.path/'voterList.csv')
            voter_df.loc[voter_df['voter_id'] == vid, 'hasVoted'] = 1
            voter_df.to_csv(self.path/'voterList.csv', index=False)
            return True
        return False

    def get_results(self):
        try:
            df = pd.read_csv(self.path/'cand_list.csv')
            return dict(zip(df['Sign'], df['Vote Count']))
        except:
            return {}

    def register_voter(self, name, gender, roll_no, class_name, password):
        try:
            df = pd.read_csv(self.path/'voterList.csv')
            new_id = df['voter_id'].max() + 1 if not df.empty else 10001
            new_row = pd.DataFrame([{
                'voter_id': new_id,
                'Name': name,
                'Gender': gender,
                'RollNo': roll_no,
                'ClassName': class_name,
                'Passw': password,
                'hasVoted': 0
            }])
            pd.concat([df, new_row]).to_csv(self.path/'voterList.csv', index=False)
            return new_id
        except Exception as e:
            print(f"Registration error: {e}")
            return -1

# Legacy functions (keep for backward compatibility)
def count_reset():
    db = ElectionDB()
    # Reset votes
    cand_df = pd.read_csv(db.path/'cand_list.csv')
    cand_df['Vote Count'] = 0
    cand_df.to_csv(db.path/'cand_list.csv', index=False)
    
    # Reset voter status
    voter_df = pd.read_csv(db.path/'voterList.csv')
    voter_df['hasVoted'] = 0
    voter_df.to_csv(db.path/'voterList.csv', index=False)

def reset_voter_list():
    df = pd.DataFrame(columns=[
        'voter_id', 'Name', 'Gender', 'RollNo', 'ClassName', 'Passw', 'hasVoted'
    ])
    df.to_csv(path/'voterList.csv', index=False)

def reset_cand_list():
    df = pd.DataFrame(columns=['Sign', 'Name', 'Vote Count'])
    df.to_csv(path/'cand_list.csv', index=False)

def verify(vid, passw):
    return ElectionDB().verify(vid, passw)

def isEligible(vid):
    return ElectionDB().is_eligible(vid)

def vote_update(st, vid):
    return ElectionDB().vote_update(st, vid)

def show_result():
    return ElectionDB().get_results()

def taking_data_voter(name, gender, roll_no, class_name, passw):
    return ElectionDB().register_voter(name, gender, roll_no, class_name, passw)
'''

import pandas as pd
from pathlib import Path

# Define the path to the database directory
path = Path("database")
path.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

def count_reset():
    """Reset all vote counts and voter status"""
    try:
        # Reset voter status
        df = pd.read_csv(path/'voterList.csv')
        df['hasVoted'] = 0
        df.to_csv(path/'voterList.csv', index=False)
        
        # Reset candidate vote counts
        df = pd.read_csv(path/'cand_list.csv')
        df['Vote Count'] = 0
        df.to_csv(path/'cand_list.csv', index=False)
        return True
    except Exception as e:
        print(f"Error in count_reset: {e}")
        return False

def reset_voter_list():
    """Create a new empty voter list file"""
    try:
        df = pd.DataFrame(columns=[
            'voter_id', 'Name', 'Gender', 'Roll Number', 'Class', 'Passw', 'hasVoted'
        ])
        df.to_csv(path/'voterList.csv', index=False)
        return True
    except Exception as e:
        print(f"Error in reset_voter_list: {e}")
        return False

def reset_cand_list():
    """Create a new empty candidate list file"""
    try:
        df = pd.DataFrame(columns=['Sign', 'Name', 'Vote Count'])
        # Add default candidates
        candidates = [
            {'Sign': 'cs', 'Name': 'Cyber Security', 'Vote Count': 0},
            {'Sign': 'ds', 'Name': 'Data Science', 'Vote Count': 0},
            {'Sign': 'ss', 'Name': 'Software Systems', 'Vote Count': 0},
            {'Sign': 'tcs', 'Name': 'Theoretical Computer Science', 'Vote Count': 0},
            {'Sign': 'nota', 'Name': 'None of the Above', 'Vote Count': 0}
        ]
        df = pd.DataFrame(candidates)
        df.to_csv(path/'cand_list.csv', index=False)
        return True
    except Exception as e:
        print(f"Error in reset_cand_list: {e}")
        return False

def verify(vid, passw):
    """Verify voter credentials"""
    try:
        df = pd.read_csv(path/'voterList.csv')
        for index, row in df.iterrows():
            if df['voter_id'].iloc[index] == vid and df['Passw'].iloc[index] == passw:
                return True
        return False
    except Exception as e:
        print(f"Error in verify: {e}")
        return False

def isEligible(vid):
    """Check if voter is eligible to vote (hasn't voted yet)"""
    try:
        df = pd.read_csv(path/'voterList.csv')
        for index, row in df.iterrows():
            if df['voter_id'].iloc[index] == vid and df['hasVoted'].iloc[index] == 0:
                return True
        return False
    except Exception as e:
        print(f"Error in isEligible: {e}")
        return False

def vote_update(st, vid):
    """Record a vote for a candidate and mark voter as having voted"""
    if isEligible(vid):
        try:
            # Update candidate votes
            df = pd.read_csv(path/'cand_list.csv')
            for index, row in df.iterrows():
                if df['Sign'].iloc[index] == st:
                    df.at[index, 'Vote Count'] += 1
            df.to_csv(path/'cand_list.csv', index=False)
            
            # Mark voter as voted
            df = pd.read_csv(path/'voterList.csv')
            for index, row in df.iterrows():
                if df['voter_id'].iloc[index] == vid:
                    df.at[index, 'hasVoted'] = 1
            df.to_csv(path/'voterList.csv', index=False)
            
            return True
        except Exception as e:
            print(f"Error in vote_update: {e}")
            return False
    return False

def show_result():
    """Return a dictionary of voting results"""
    try:
        df = pd.read_csv(path/'cand_list.csv')
        v_cnt = {}
        for index, row in df.iterrows():
            v_cnt[df['Sign'].iloc[index]] = df['Vote Count'].iloc[index]
        return v_cnt
    except Exception as e:
        print(f"Error in show_result: {e}")
        return {'cs': 0, 'ds': 0, 'ss': 0, 'tcs': 0, 'nota': 0}

def taking_data_voter(name, gender, zone, city, passw):
    """Register a new voter and return the assigned voter ID"""
    try:
        # Check if voter list file exists, create if not
        if not (path/'voterList.csv').exists():
            reset_voter_list()
            
        df = pd.read_csv(path/'voterList.csv')
        
        # Determine new voter ID
        if len(df) == 0:
            vid = 10001
        else:
            vid = df['voter_id'].max() + 1
            
        # Create new voter entry
        new_voter = pd.DataFrame({
            'voter_id': [vid],
            'Name': [name],
            'Gender': [gender],
            'Roll Number': [zone],
            'Class': [city],
            'Passw': [passw],
            'hasVoted': [0]
        })
        
        # Add to existing data
        df = pd.concat([df, new_voter], ignore_index=True)
        df.to_csv(path/'voterList.csv', index=False)
        
        return vid
    except Exception as e:
        print(f"Error in taking_data_voter: {e}")
        return -1

# Initialize the database files if they don't exist
if not (path/'voterList.csv').exists():
    reset_voter_list()
    
if not (path/'cand_list.csv').exists():
    reset_cand_list()

