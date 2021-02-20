import argparse
from modules import tinder
import textwrap 



def parse_command_line():
    parser=argparse.ArgumentParser(
            formatter_class=argparse.RawTextHelpFormatter,
            description=textwrap.dedent
            ('''
            Poorly written script to keep sending like on Tinder web app
            '''),
            epilog=textwrap.dedent('''
            
            File with credentials must be formatted like in the exampe:
            username=mYc00LuserNam3
            password=Sup3rS3creTP4ssword


            File with positon location must be formatted like this:
            lng=69.696969
            lat=90.000000

            ''')
            )

    parser.add_argument('-H', action="store_false", default=True, help="set the browser visible")
    

    creds=parser.add_mutually_exclusive_group(required=True)
    creds.add_argument('-C', dest='creds_path', help="path to file containing the credentials")
    creds.add_argument('-c', dest='creds', help='credentials in this format -> username:password')

    parser.add_argument('-L', dest='location', help='path to file with lat en lng to use')

    return parser



def setup_args():
    args=parse_command_line().parse_args()
    
    if args.creds_path is None:
        password=args.creds_path.split(':')[1].strip()
        username=args.creds_path.split(':')[0].strip()

    elif args.creds is None:
        with open(args.creds_path, 'r') as f:
            for line in f.readlines():
                if 'username' in line:
                    username=line.split('=')[1].strip()
                if 'password' in line:
                    password=line.split('=')[1].strip()

    return {
            'username':username,
            'password':password,
            'location':args.location,
            'headless':args.H
            }



def run_tinder():
    args=setup_args()

    usr=args['username']
    passwd=args['password']
    loc=args['location']
    head=args['headless']
    
    tind=tinder.Tinder(usr, passwd, head, loc)
    tind.login()
    tind.love_all()




if __name__=='__main__':
    run_tinder()
