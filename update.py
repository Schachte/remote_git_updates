'''
@Description 
Update script that will update the frontend or the backend based on new branch pushes

@Author
Ryan Schachte
'''
import os

'''
@VARIABLES
'''

SERVER_IP       = os.environ['DATA_VIZ_SERVER']
FRONTEND_DIR    = os.environ['FRONTEND_DIR']
BACKEND_DIR     = os.environ['BACKEND_DIR']

COMMANDS={
    'server_ssh':'ssh -l ubuntu -i ~/.ssh/*.pem %s '%(SERVER_IP),
    'update_front_remote': 'sudo git --git-dir %s pull origin '%(FRONTEND_DIR),
    'update_back_remote': 'sudo git --git-dir %s pull origin '%(BACKEND_DIR)
}

def apache_restart():
    print('Restarting apache webserver..')
    os.system(COMMANDS['server_ssh'] + ' sudo service apache2 restart')
    print('Apache2 restarted successfully!')

def update_server(portion):
    
    branch = ''
    if (portion == 0):
        branch = 'master_branch' 
    else:
        branch = 'master'
        
    #Pull changes
    if (not portion):
        os.system(COMMANDS['server_ssh'] + COMMANDS['update_front_remote'] + branch)
        restart_cmd = raw_input('%s update successfully.\n\nWould you like to restart APACHE?\n\nChoice: '%(branch))
        
        #Restart service on remote ubuntu instance
        if (restart_cmd.lower()[0] == 'y'):
            apache_restart()
        else:
            print('\n Not restarting apache webserver..')
    else:
        os.system(COMMANDS['server_ssh'] + COMMANDS['update_back_remote'] + branch)
        print('Server backend updated successfully')

        
    print('\n Update Complete!\n\n')

def server_update(choice):
    if(choice.lower() == 'a'):
        '''Updating the frontend server'''
        update_server(0)
        pass
    elif (choice.lower() == 'b'):
        '''Updating the backend server'''
        update_server(1)
        pass
    else:
        print('Invalid choice\n\n')
        
def main():
    
    #Update the frontend or the backend 
    while (1):
        choice = raw_input("Would you like to update\nA) Frontend\nB) Backend\n\nChoice:  ")
        server_update(choice)

if __name__ == "__main__":
    main()
