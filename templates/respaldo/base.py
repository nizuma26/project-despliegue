import os
from datetime import datetime

archivoZip =""

fecha = datetime.today().strftime('%y_%m_%d_%H_%M')

respaldo = "C:\\RespaldoBD\\base\\respaldo_"+str(fecha)+".sql"


pathBase = "C:\\LARAGON1\\laragon\\bin\\mysql\\mysql-5.7.24-winx64\\bin\\mysqldump.exe"

archivoZip1 = "C:\\respaldoBD\\base\\respaldo_"+str(fecha)+".zip"

try:
    os.popen(pathBase+" -u 'root' bd_invtecno_5 > " + respaldo)
    print("Base respaldada correctamente en: " + respaldo)
except:
    print("Ocurrio un error no se pudo  respaldar la base de datos")
    exit

print("Esperando...")


from threading import Timer

def comprimir():
    import zipfile

    
    
    archivoZip2 = zipfile.ZipFile(archivoZip1, "w")    
    archivoZip2.write(respaldo, compress_type=zipfile.ZIP_DEFLATED)
    archivoZip2.close()

    print("Archivo comprimido en: "+archivoZip2)

t = Timer(7, comprimir)
t.start()
    
