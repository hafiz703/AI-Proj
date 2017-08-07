from appJar import gui
import os
from label_image_fullaugment import LabelImage
from PIL import Image
import time
import threading

results = dict()
 

class myApp:
    def __init__(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.im_path = self.dir_path + "/images"
        self.app = gui("ggwp")                  
        self.app.setGeometry("fullscreen")
        self.imageDirectory =""
        self.prevImage =""
        # self.app.setBg("white")
        # self.app.showSplash("GGWP", fill='red', stripe='black', fg='white', font=44)
        global results
         


    ######## Button Handlers #########
    def chooseAndSetImage(self,btn):
        # self.app.addImage("Loading", self.dir_path+"/source.gif")
        self.app.setStatusbar("Uploading...", 0)
        if(len(self.imageDirectory) ==0):
            self.state = 0
        else:
            self.state = 1
        
        self.imageDirectory = self.app.openBox(title="Select Image", dirName=self.dir_path, fileTypes=[('images', '*.png'), ('images', '*.jpg'),('images', '*.jpeg'),('images', '*.gif')])            
        
        if(len(self.imageDirectory) !=0):
            # self.app.addTextArea("Title")
            # self.app.setTextArea("Title", self.imageDirectory, callFunction=True)
            if(self.state==0):
                self.app.startLabelFrame(os.path.splitext(self.imageDirectory)[0],row=0,column=1, rowspan=0)           
            
            else:
                # self.app.openLabelFrame(self.prevImage)
                self.app.removeAllWidgets()
                 
                self.app.startLabelFrame(os.path.splitext(self.imageDirectory)[0],row=0,column=1, rowspan=0)            
            

            print(os.path.splitext(self.imageDirectory)[0])     
            if(self.getPicFormat(self.imageDirectory) == "png"):
                im = Image.open(self.imageDirectory)
                rgb_im = im.convert('RGB')
                newName = os.path.splitext(self.imageDirectory)[0]+".jpg"
                rgb_im.save(newName)
                self.imageDirectory = newName

            if(self.getPicFormat(self.imageDirectory) == "jpg" or self.getPicFormat(self.imageDirectory)=="jpeg" ):
                im = Image.open(self.imageDirectory)
                rgb_im = im.convert('RGB')
                newName = os.path.splitext(self.imageDirectory)[0]+".png"
                rgb_im.save(newName)
                self.imageDirectory = newName

            
            try:   
                # print('kek',os.path.split(imageDirectory)[0],self.dir_path.replace('\\', '/'),os.path.split(imageDirectory)[0]==self.dir_path.replace('\\', '/'))
                # copyfile(imageDirectory,self.dir_path.replace('\\', '/'))
                # self.app.startLabelFrame(os.path.basename(self.imageDirectory),row=0,column=1, rowspan=0) 
                if(self.state ==0):
                    self.app.addToolbar(["Predict"], self.runPrediction)
                    self.app.setToolbarImage("Predict", self.dir_path+"/play-button.png")
                print(os.path.splitext(self.imageDirectory)[0]) 
                self.app.addImage(os.path.splitext(self.imageDirectory)[0], self.imageDirectory)
                # self.prevImage = os.path.splitext(self.imageDirectory)[0]
                
                # else:
                #     self.app.reloadImage(self.prevImage, self.imageDirectory)
                
                self.app.setStatusbar("%s successfully uploaded"%os.path.splitext(self.imageDirectory)[0], 0)
                self.app.stopLabelFrame()         
                
            except:
                self.app.reloadImage(os.path.splitext(self.imageDirectory)[0], self.imageDirectory)
                self.app.setStatusbar("%s successfully uploaded"%os.path.splitext(self.imageDirectory)[0], 0)
            
            self.t1 = threading.Thread(target=self.predict)
                 
            self.t1.start()
    
    def runPrediction(self,btn):
        try:
            self.app.startLabelFrame("Results",0,2,1,2)
        except:
            self.app.openLabelFrame("Results")
            self.app.clearAllEntries  
        self.app.setStatusbar("Running ...", 0)
        self.app.stopLabelFrame()

        # app2 = gui("Loading","50x50")
        # app2.hideTitleBar()
        # app2.go() 
        
        # self.app.addImage("load",self.dir_path+"/loadResized.gif",0,0)
        self.t1.join() 
        self.app.openLabelFrame("Results")
        # print('%s (score = %.5f)' % (human_string, score))
        # self.app.setFont(30, font=None)
        self.app.addLabel("l1", '%s = %.5f' % ("Benign Probability ", self.results['benign']))
        # self.app.addImage("load",self.dir_path+"/loadResized.gif",0,0)
        self.app.addLabel("l2", '%s = %.5f' % ("Malignant Probability ", self.results['malignant']))

        if(self.results['benign']>=self.results['malignant']):
            self.app.addImage("benign",self.dir_path+"/good2.gif",0,2)
            self.app.setLabelBg("l1", "green")
            # self.app.setLabelFont(35)
            
            # self.app.setBg("green")
        else:
            self.app.addImage("malig",self.dir_path+"/cancer2.gif",1,2)
            self.app.setLabelBg("l2", "red")
            # self.app.setLabelFont(35)
            # self.app.setBg("red")
                


        self.app.setStatusbar("Done!", 0)
        self.app.stopLabelFrame()    
         
        
    ##################################
    def setLayout(self):         
        self.app.addToolbar(["Select Image",], self.chooseAndSetImage)         
        self.app.setToolbarImage("Select Image", self.dir_path+"/uploadbutton.png")
        self.app.addStatusbar(fields=1)
        self.app.setStatusbar("Upload Image", 0)
        # self.app.addTextArea("Results", 0,2,1,2)        
        # self.app.addButton("Select Image",self.chooseAndSetImage,2,2)        
        
    def runApp(self):
        self.app.go()

    def getPicFormat(self,s):
        res=""
        for i in s[::-1]:
            if i==".":
                break
            else:
                res+=i
        return res[::-1]

    def predict(self):
        labelimage = LabelImage(os.path.basename(self.imageDirectory),"retrained_graph_8.pb","retrained_labels_8.txt")
        label_lines, predictions = labelimage.run()
        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]    
        res = {label_lines[0]:predictions[0][0],label_lines[1]:predictions[0][1]}
        self.results = res
        # return res
    # def setPredictlayout(self):
    #     self.app.startLabelFrame("Results",0,2,1,2)  
    #     self.app.setStatusbar("Running ...", 0)
    #     self.app.addImage("baby",self.dir_path+"/baby.gif")
        
    #     # print('%s (score = %.5f)' % (human_string, score))
    #     self.app.addLabel("l1", '%s (score = %.5f)' % ("Benign Probability =", self.results['benign']))
    #     self.app.addLabel("l2", '%s (score = %.5f)' % ("Malignant Probability =", self.results['malignant']))
    #     self.app.setStatusbar("Done!", 0)
    #     ##########################
    #     self.app.stopLabelFrame()

     

 


if __name__ == "__main__":
    m = myApp()
    m.setLayout()
    m.runApp()
   
    
        
 
    
    