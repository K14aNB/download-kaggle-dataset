import os
import errno
from importlib import import_module
from subprocess import run,CalledProcessError
from zipfile import ZipFile

def download(data_src_path:str,colab=False,competition=False,repo_path=None,nb_name=None):
    '''
    Takes data_src_path in the form of <kaggle-username>/<dataset-name> 
    and downloads the dataset into colab/local runtime using kaggle api

    Arguments:
    
    data_src_path:str : kaggle-username>/<dataset-name>
    colab:bool : Indicates whether currently active environment uses colab runtime or local runtime.
                 default is False which indicates active environment is using local runtime.
    competition:bool : Indicates whether data is from Kaggle Competition. default is False. 
    repo_path:str : Path of local repository to which dataset must be downloaded.
                    default value is None
                    This is applicable only for local runtime (when colab=False).
    nb_name:str : Current Notebook name without the extensions (.ipynb,.py...).
                  default value is None
                  This is applicable only for local runtime (when colab=False)
                  This value is needed so data can be downloaded and extracted in the 
                  path:repo_path/data/nb_name/<data_file> when using local runtime 
    
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
        if os.path.isdir(os.path.join(dpath,'data')) is False:
            os.mkdir(os.path.join(dpath,'data'))
        data_path=os.path.join(dpath,'data')
    else:
        dpath = repo_path
        if nb_name is not None:
            if os.path.isdir(os.path.join(dpath,'data',nb_name)) is False:
                os.makedirs(os.path.join(dpath,'data',nb_name))
            data_path=os.path.join(dpath,'data',nb_name)
        else:
            print('Notebook name is not provided. Default value is None')
            raise FileNotFoundError(errno.ENOENT,os.strerror(errno.ENOENT),nb_name)
    

    if os.listdir(data_path) == []:
        try:
            run(['python','-m','pip','install','kaggle'],check=True)
        except CalledProcessError as e1:
            print(f'{e1.cmd} failed')
        
        if competition is True:
            try:
                run(['kaggle','competitions','download','-c',data_src_path,'-p',data_path],check=True)
            except CalledProcessError as e2:
                print(f'{e2.cmd} failed')
        else:
            try:
                run(['kaggle','datasets','download',data_src_path,'-p',data_path],check=True)
            except CalledProcessError as e3:
                print(f'{e3.cmd} failed')
            
        zip_filename = os.listdir(data_path)[0] 
        with ZipFile(os.path.join(data_path,zip_filename),'r') as zip:
            zip.extractall(path=data_path)
    print(f'Kaggle Dataset {data_src_path} is downloaded and extracted at {data_path}')
    return data_path