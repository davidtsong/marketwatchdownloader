
from app.d import *
from app.genGraphs import *

def run(username, password):
    key = username
    files = downloadStuffs(username,password)
    print(files)
    print("Creating Graphs")
    g = GenGraphs(files, username)
    filepaths = g.run()
    print(filepaths)

    path = os.path.join(os.getcwd(), 'app/upload/' + key + '.zip')
    print(os.getcwd() + ' ' + path)

    zipf = zipfile.ZipFile(path,'w', zipfile.ZIP_DEFLATED)
    # zipf.write(app.config['UPLOAD_FOLDER'] + 'stockGraphDataValues.csv')
    # zipf.write(app.config['UPLOAD_FOLDER'] + 'foo.pdf')
    zipf.write(filepaths[0])
    zipf.write(filepaths[1])
    zipf.close()
    return path #return path to download from
    # return send_from_directory(directory=path, filename=key+'.zip', as_attachment=True)

def test(username,password):
    key = username
    files = downloadStuffs(username,password)
    print(files)
    print("Creating Graphs")
    g = GenGraphs(files, username)
    filepaths = g.run()
    print(filepaths)

if __name__ == '__main__':
    test('','')
