import os
import errno
from importlib import import_module
from subprocess import run,CalledProcessError
from zipfile import ZipFile

def download(data_src_path:str,colab=False,repo_path=None):
    '''
    Takes data_src_path in the form of <kaggle-username>/<dataset-name> 
    and downloads the dataset into colab/local runtime using kaggle api

    Arguments:
    
    data_src_path:str : kaggle-username>/<dataset-name>
    colab:bool : Indicates whether currently active environment uses colab runtime or local runtime.
                 default is False which indicates active environment is using local runtime.
    repo_path:str : Path of local repository to which dataset must be downloaded.
                    default is None
                    This is applicable only for local runtime (when colab=False).
    
    Returns:str : directory path where kaggle dataset is downloaded and extracted.
    '''
    # Setup Kaggle api key
    if colab is True:
        userdata=import_module('google.colab.userdata')
        os.environ['KAGGLE_USERNAME'] = userdata.get('KAGGLE_USERNAME')
        os.environ['KAGGLE_KEY'] = userdata.get('KAGGLE_KEY')
    else:
        active_user = os.path.expanduser('~')
        if os.path.exists(os.path.join(active_user,'.kaggle','kaggle.json')):
            print('Kaggle api credentials present')
        else:
            print('Kaggle api credentials not present')
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT),'kaggle.json')
        


    # Download dataset from Kaggle using Kaggle API
    dpath = ''
    if colab is True:
        dpath = os.getcwd()
    else:
        dpath = repo_path

    os.mkdir(dpath+'/data')
    try:
        run(['python','-m','pip','install','kaggle'],check=True)
    except CalledProcessError as e1:
        print(f'{e1.cmd} failed')
      
    try:
        run(['kaggle','datasets','download',data_src_path,'-p',os.path.join(dpath,'data')],check=True)
    except CalledProcessError as e2:
        print(f'{e2.cmd} failed')
        
    zip_filename = os.listdir(os.path.join(dpath,'data'))[0] 
    with ZipFile(os.path.join(dpath,'data',zip_filename),'r') as zip:
        zip.extractall(path=os.path.join(dpath,'data'))
    print(f'Kaggle Dataset {data_src_path} is downloaded and extracted at {os.path.join(dpath,"data")}')
    return os.path.join(dpath,'data')