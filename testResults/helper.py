from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def DeleteRealA(path):
    
    for root, dirs, files in os.walk(path):
        for filename in files:
           if filename[-10:] =="real_A.png":
                removefile = path+filename
                os.remove(removefile)
                
def GetData(path):
    
    fake = []
    real =[]
    
    for root, dirs, files in os.walk(path):
        for filename in files:
                
            if filename[-10:] =="fake_B.png":
                fake.append(path+filename)
                 
            if filename[-10:] =="real_B.png":
                real.append(path+filename)

    return fake,real

def FindL1(fake,real):

    l1 =[]
    filename =[]
    count = 0 
    for i in range(len(fake)):
        #print(fake[i])
        count +=1
        a=np.array(Image.open(fake[i]).convert('RGB')).ravel()
        b=np.array(Image.open(real[i]).convert('RGB')).ravel()

        # Calculate the sum of the absolute differences divided by number of elements
        MAE = np.sum(np.abs(np.subtract(a,b,dtype=np.float))) / a.shape[0]
        filename.append([fake[i][7:],real[i][7:]])
        l1.append(MAE)
    print(count)    
    return filename,l1

def SaveToExcel(filename,l1):
    df = pd.DataFrame.from_dict({'L1 loss':l1,'FileName':filename})
    df.to_excel('testResult.xlsx',header= True,index =False)

def historPlot(train,test):

    fig, ax = plt.subplots(1,1)
    bins = np.linspace(0,50, 10)

    plt.hist(test, bins, color='g',alpha=.6, label='Test L1 loss')
    plt.hist(train, bins,color='b', alpha=0.4, label='Train L1 loss')
    plt.legend(loc='upper right')
    plt.title("Histogram plot of train & test loss")
    #pyplot.show()
    plt.savefig('train_testloss_histro.png')
    
def trainloss():

   
    filepath = 'loss_log.txt'

    epoch,G_GAN,G_L1,D_real,D_fake,lineBuff= [],[],[],[],[],[]


    with open(filepath) as fp:
       line = fp.readline()
       prev_epoch = 1
       while line:
           
           flag = line.strip()
              
           if flag[0]=="=":
            pass
           
           else:
            curr_epoch = int(flag[8:11].replace(",",""))
            lineBuff.append(flag)  
            if curr_epoch!=prev_epoch:
              prev_epoch = curr_epoch
              
              flag = lineBuff[-2]
            
              ind = flag.find('G_GAN')
              l1 = flag.find('G_L1')
              dreal = flag.find('D_real')
              dfake = flag.find('D_fake')
            
              G_GAN.append(float(flag[ind+7:ind+12]))
              G_L1.append(float(flag[l1+6:l1+12]))
              D_real.append(float(flag[dreal+7:dreal+13]))
              D_fake.append(float(flag[dfake+7:dfake+13]))

            else:
              pass
     
          
           line = fp.readline()


    epoch_count = range(1, len(G_L1) + 1)

    fig, ax = plt.subplots(1,1) 
    ax.plot(epoch_count,G_L1,'C1',label='G_L1')
    ax.plot(epoch_count,G_GAN,'b',label='G_GAN')
    ax.plot(epoch_count,D_fake,'r',label='D_Fake')
    ax.plot(epoch_count,D_real,'g', label='D_REAL')
    plt.legend(loc='best')
    #plt.show()

    plt.savefig('trainloss.png')

def video():

    os.system('python video2frame.py')
    os.system('python test.py --dataroot ./singleimage/starcraft  --name pix2pix10resnet --model pix2pix --direction AtoB --netG resnet_9blocks --checkpoints_dir trained_model --num_test 10')
    os.system('python img2video.py')
