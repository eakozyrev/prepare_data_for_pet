import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import glob

N_emb = 100
R = 5
first_p=2  #number of first patient in the folder for augmentation
N_aug_each_pat = 50

def generate_emb(ramla,promt,path_to_save,path_to_save_promt):

    ramla_array = np.fromfile(ramla, dtype=np.float32)
    ramla_array = np.reshape(ramla_array, (356, 150, 150))
    mean_r = np.mean(ramla_array)
    emb_array = np.zeros(shape=(356, 150, 150))
    patient_array = np.zeros(shape=(356, 150, 150))

    for el in range(N_emb):

        x = 72 + np.random.randint(-40,40)
        y = 72 + np.random.randint(-40,40)
        z = 150 + np.random.randint(-110,110)
        Nlevel = mean_r*50*(1 + np.random.rand()-0.5)
        a,b,c = (1+np.random.rand(3))
        for i in range(-R,R):
            for j in range(-R, R):
                for k in range(-R, R):
                    if i**2*a + j**2*b + k**2*c < R**2:
                        emb_array[z+k,x+i,y+j] = Nlevel
                        patient_array[z+k,x+i,y+j] = np.copy(ramla_array[z+k,x+i,y+j])
                        ramla_array[z+k,x+i,y+j] = emb_array[z+k,x+i,y+j]

    np.array(ramla_array, dtype=np.float32).tofile(path_to_save)
    del ramla_array
    iiiiffff='/spoolA/anon_explorer/anon/r001_WB_FDG_6R7/HImg/r001_WB_FDG_6R7_50m-60m_20x9_4mm_p.view.img'
    np.array(patient_array, dtype=np.float32).tofile('patient_array.i')
    os.system('scp /spoolA/anon_explorer/hdr.hdr patient_array.i.hdr')
    os.system('petview2interfile patient_array.i -ii2img -ofo -floatii')
    np.array(emb_array, dtype=np.float32).tofile('emb_array.i')
    os.system('scp patient_array.i.hdr emb_array.i.hdr')
    os.system('petview2interfile emb_array.i -ii2img -ofo -floatii')
    os.system(f'direct -oFP -i0t 3 -os 10000 -i0 patient_array.img -if {iiiiffff} -c1f 0 -c2f 0 -sf 0 -ss 1000.0 -rf 0 -ofo -of patient_array_fp -ect 1 -xpd 0 -zpd 0 -toft 1 -tofps 250 -lort 1 -lorwr 3.5 -lorwz 3.5 -imgt 1 -imgw 4 -ft 0 -fc 1.0 -fat 0 -fac 1.0 -fthr 16')
    os.system(f'direct -oFP -i0t 3 -os 10000 -i0 emb_array.img -if {iiiiffff} -c1f 0 -c2f 0 -sf 0 -ss 1000.0 -rf 0 -ofo -of emb_array_fp -ect 1 -xpd 0 -zpd 0 -toft 1 -tofps 250 -lort 1 -lorwr 3.5 -lorwz 3.5 -imgt 1 -imgw 4 -ft 0 -fc 1.0 -fat 0 -fac 1.0 -fthr 16')
    os.system('petview2interfile emb_array_fp.view.img -ofo -floatii')
    os.system('petview2interfile patient_array_fp.view.img -ofo -floatii')

    patient_array = np.fromfile('patient_array_fp.view.i', dtype=np.float32)
    patient_array = np.reshape(patient_array, (9,20,356, 150, 150))

    emb_array = np.fromfile('emb_array_fp.view.i', dtype=np.float32)
    emb_array = np.reshape(emb_array, (9,20,356, 150, 150))

    promt_ = np.fromfile(promt, dtype=np.float32)
    promt_ = np.reshape(promt_, (9,20,356, 150, 150))

    promt_ = promt_ - patient_array + emb_array
    np.array(promt_, dtype=np.float32).tofile(path_to_save_promt)

    del promt_
    del emb_array
    del patient_array


if __name__ == '__main__':
    path_what_aug= sys.argv[1] #'/data/MyBook/Data/anon_explorer/dataset/promts_atten_norm_scatt_random'

    path_with_ramla =  '/'.join(path_what_aug.split('/')[:-1])+'/ramla/'
    path_to_aug=path_what_aug+'_emb'+'/'
    path_to_aug_ramla = path_to_aug + 'ramla/'
    path_what_aug+='/'
    print('path_with_ramla = ', path_with_ramla)
    print('path_to_aug = ', path_to_aug)
    print('path_to_aug_ramla = ', path_to_aug_ramla)
    try: os.system(f'rm -rf {path_to_aug}');
    except: pass;
    try: os.mkdir(path_to_aug);
    except: pass;
    try: os.mkdir(path_to_aug_ramla);
    except: pass;

    list = sorted(glob.glob(path_with_ramla + '*.i'))
    print(list)
    save = 1
    for el in list:
        print('--------------------- el = ', el)
        if el.find(f'_{first_p}.i') <= 0: continue
        promt = path_what_aug + f'promt_{first_p}.i'
        for k in range(N_aug_each_pat):
            generate_emb(el,promt,path_to_aug_ramla+f'ramla_{save}.i',path_to_aug+f'promt_{save}.i')
            os.system(f'python plot.py '+f'{path_to_aug_ramla}ramla_{save}.i '+ path_to_aug_ramla+f'ramla_{save}.i.png')
            os.system(f'python plot.py ' + f'{path_to_aug}promt_{save}.i ' + path_to_aug + f'promt_{save}.i.png')
            save+=1
        first_p+=1

    try: os.system('rm *hdr'); os.system('rm *img'); os.system('rm *.i');  os.system('rm *hist'); os.system('rm *png');
    except: pass

