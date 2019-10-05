import tkinter as tk
from PIL import Image, ImageTk
from config import *
from random import randint
from copy import deepcopy



class Llk():
    def __init__(self):
        self.id_list = []# record the id-list of rectangle
        self.pic_dict = {}#categorize the pics added
        self.mouse_count = 0 # record the number of mouseclick 
        self.pic_select = 0#record the pic.no clicked
        self.orient_temp = ""#variable to copy the select rect in order to compare if the chosen pic is the same as before
        self.set_background()#create canvas
        
    def set_background(self):
        
        self.window = tk.Tk()
        self.window.title("llk")
        self.window.geometry('860x600')
        
        self.background = tk.Canvas(self.window,width = 860, height = 600,bg = 'pink')
        self.background.pack()
        self.set_layout()
        

    def set_layout(self):
        for i in range(BOARD_COLS):
            for j in range(BOARD_ROWS):
                self.background.create_rectangle(43*i, 50*j, 43*i+43,50*j+50, outline = 'pink'
                , fill = 'pink',tags = chr(i+65)+chr(j+65))
                self.id_list.append(chr(i+65)+chr(j+65))
        
        self.add_pieces()#add pics to the rects
        
    
    def add_pieces(self):
        pic_list = []
        remove_list = []
        for i in self.id_list:
            if (i[0]) == "A":
                remove_list.append(i)
            elif (i[0]) == "T":
                remove_list.append(i)
            elif (i[1]) == "A":
                remove_list.append(i)   
            elif (i[1]) == "L":
                remove_list.append(i)
        
        for i in remove_list:    
            self.id_list.remove(i)

        im = ImageTk.PhotoImage(file = 'images/bgi.jpg')
        pic_list.append(im)
        self.background.create_image((430,300),image = im)
        
        for i in range(9):
            for j in range(10):
                img_id = randint(1,10)
                im = ImageTk.PhotoImage(file = 'images/%d.jpg' % img_id )
                pic_list.append(im)
                grid_id = randint(0,len(self.id_list)-1)#random the rects

                
                img_x = int(self.grid_pixel(self.id_list[grid_id][0], self.id_list[grid_id][1])[0])#the center x_pix of img
                img_y = int(self.grid_pixel(self.id_list[grid_id][0], self.id_list[grid_id][1])[1])#the center y_pix of img
                self.background.create_image((img_x, img_y), image = im, anchor = 'c', tag = self.id_list[grid_id]+"p")
                self.pic_dict[self.id_list[grid_id]] = img_id
                del self.id_list[grid_id]
                
                grid_id = randint(0,len(self.id_list)-1)#random the rects
                
                img_x = int(self.grid_pixel(self.id_list[grid_id][0], self.id_list[grid_id][1])[0])#the center x_pix of img
                img_y = int(self.grid_pixel(self.id_list[grid_id][0], self.id_list[grid_id][1])[1])#the center y_pix of img
                self.background.create_image((img_x, img_y), image = im, anchor ='c',tag = self.id_list[grid_id]+"p")
                self.pic_dict[self.id_list[grid_id]] = img_id
                del self.id_list[grid_id]
            
        self.background.bind(sequence="<Button-1>", func=self.MouseEvent)#bind the mouseclick to the MouseEvent function

        self.window.mainloop()
    
    
    def grid_pixel(self,x_chr,y_chr):#return the center orientation of the pic
        orient_list = []
        x_pix = (ord(x_chr)-65) * 43 + 43/2
        y_pix = (ord(y_chr)-65) * 50 + 25
        orient_list.append(x_pix)
        orient_list.append(y_pix)
        return orient_list

    def MouseEvent(self, event):
        
        row_select = event.y // 50
        col_select = event.x // 43
        seq_select = chr(col_select+65) + chr(row_select+65)
        print(seq_select)

        if seq_select in self.pic_dict.keys():
            if self.mouse_count % 2 == 0 and self.pic_dict[seq_select]:
                
                # draw the outline
                otl_lx = self.grid_pixel(chr(col_select+65), chr(row_select+65))[0] - 43/2
                otl_rx = self.grid_pixel(chr(col_select+65), chr(row_select+65))[0] + 43/2
                otl_ty = self.grid_pixel(chr(col_select+65), chr(row_select+65))[1] - 25
                otl_by = self.grid_pixel(chr(col_select+65), chr(row_select+65))[1] + 25
                self.background.create_line(otl_lx,otl_ty,otl_rx,otl_ty,arrow = 'none', width=3, fill='white', tag = seq_select+"l")
                self.background.create_line(otl_rx,otl_ty,otl_rx,otl_by,arrow = 'none', width=3, fill='white', tag = seq_select+"l")
                self.background.create_line(otl_rx,otl_by,otl_lx,otl_by,arrow = 'none', width=3, fill='white', tag = seq_select+"l")
                self.background.create_line(otl_lx,otl_by,otl_lx,otl_ty,arrow = 'none', width=3, fill='white', tag = seq_select+"l")
                self.mouse_count += 1
                self.pic_select = self.pic_dict[seq_select]
                self.orient_temp = deepcopy(seq_select)
                
                
            else:
                
                if self.pic_dict[seq_select] == self.pic_select and self.orient_temp != seq_select and self.check_rule(self.orient_temp,seq_select):
                    
                    self.background.delete(seq_select+"p")
                    self.background.delete(self.orient_temp+"p")
                    self.background.delete(self.orient_temp+"l")
                    del self.pic_dict[seq_select]
                    del self.pic_dict[self.orient_temp]

                    self.orient_temp = ""
                    self.pic_select = 0
                    self.mouse_count += 1
                    
        
                else:
                    self.background.delete(self.orient_temp+"l")

                    self.orient_temp =""
                    self.pic_select = 0
                    self.mouse_count += 1
        else:
            if self.mouse_count % 2 == 1:
                self.background.delete(self.orient_temp+"l")
                self.mouse_count += 1
    
    def check_rule(self, pic_1, pic_2):
        if self.check_zero_corner(pic_1, pic_2):
            return True
        elif self.check_one_corner(pic_1,pic_2):
            return True
        elif self.check_two_corner(pic_1,pic_2):
            return True
        else:
            return False


    def check_zero_corner(self,pic_1,pic_2):
        first_1 = pic_1[0]
        last_1 = pic_1[1]
        first_2 = pic_2[0]
        last_2 = pic_2[1]
        
        if ord(last_1) == ord(last_2):
            if abs(ord(first_1)-ord(first_2)) == 1:
                return True
            if ord(first_1) > ord(first_2):
                for i in range(0,ord(first_2)-ord(first_1)):
                    if chr(ord(first_1)+i+1)+last_1 in self.pic_dict.keys():
                        return False
            else:
                for i in range(ord(first_1),ord(first_2)):
                    if chr(i)+last_1 in self.pic_dict.keys():
                        return False

        elif ord(first_1) == ord(first_2):
            if abs(ord(last_1)-ord(last_2)) == 1:
                return True
            if ord(last_1) > ord(last_2):
                for i in range(0,ord(last_1)-ord(last_2)):
                    if first_1+chr(ord(last_1)-i-1) in self.pic_dict.keys():
                        return False
            else:
                for i in range(ord(last_1),ord(last_2)):
                    if first_1+chr(i) in self.pic_dict.keys():
                        return False
        
        else:
            return False
        
        

    def check_one_corner(self,pic_1,pic_2):
        first_1 = pic_1[0]
        last_1 = pic_1[1]
        
        for i in range(0,ord(first_1)-65):
            if chr(ord(first_1)-i-1)+last_1 in self.pic_dict.keys():
                break
            if self.check_zero_corner(chr(ord(first_1)-i-1)+last_1,pic_2):
                return True

        for i in range(ord(first_1)+1,85):
            if chr(i)+last_1 in self.pic_dict.keys():
                break
            if self.check_zero_corner(chr(i)+last_1,pic_2):
                return True
        
        for i in range(0,ord(last_1)-65):
            if first_1+chr(ord(last_1)-i-1) in self.pic_dict.keys():
                break
            if self.check_zero_corner(first_1+chr(ord(last_1)-i-1),pic_2):
                return True
        
        for i in range(ord(last_1)+1,77):
            if first_1+chr(i) in self.pic_dict.keys():
                break
            if self.check_zero_corner(first_1+chr(i),pic_2):
                return True
        
        return False

    def check_two_corner(self,pic_1,pic_2):
        first_1 = pic_1[0]
        last_1 = pic_1[1]
        
        for i in range(0,ord(first_1)-65):
            if chr(ord(first_1)-i-1)+last_1 in self.pic_dict.keys():
                break
            if self.check_one_corner(chr(ord(first_1)-i-1)+last_1,pic_2):
                return True

        for i in range(ord(first_1)+1,85):
            if chr(i)+last_1 in self.pic_dict.keys():
                break
            if self.check_one_corner(chr(i)+last_1,pic_2):
                return True
        
        for i in range(0,ord(last_1)-65):
            if first_1+chr(ord(last_1)-i-1) in self.pic_dict.keys():
                break
            if self.check_one_corner(first_1+chr(ord(last_1)-i-1),pic_2):
                return True
        
        for i in range(ord(last_1)+1,77):
            if first_1+chr(i) in self.pic_dict.keys():
                break
            if self.check_one_corner(first_1+chr(i),pic_2):
                return True
        
        return False





    
        


                    
        
        
        







llk = Llk()
