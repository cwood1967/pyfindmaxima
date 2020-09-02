from typing import OrderedDict
import numpy as np
from numba import jit, types, typed, int32, float32
from numba.experimental import jitclass

kv_type = (types.int32, types.float32)
spec = [
    ('img', types.float32[:,:]),
    ('tol', types.float32),
    ('w', types.int32),
    ('h', types.int32),
    ('sorted_p', types.int32[:]),
    ('sorted_v', types.float32[:]),
    ('xoffsets', int32[:]),
    ('yoffsets', int32[:]),
    #('allmaxima_dict', types.DictType(*kv_type)),
]

@jitclass(spec)
class MaximumFinder:
    
    def __init__(self):
        
        self.yoffsets = np.array([-1, -1, -1,  0, 0,  1, 1, 1], dtype=np.int32)
        self.xoffsets = np.array([-1,  0,  1, -1, 1, -1, 0, 1], dtype=np.int32)
        
        #self.allmaxima_dict = typed.Dict.empty(*kv_type)
    
    def run(self, img, tol):
        self.img = img.astype(np.float32)
        self.w = img.shape[1]
        self.h = img.shape[0]
        self.tol = tol
        
        self.all_local_max()
        return self.findmax()
        
    def all_local_max(self):
        vlist = np.zeros(self.w*self.h//4, dtype=np.float32) #list()
        plist = np.zeros(self.w*self.h//4, dtype=np.uint32) #list()
        index = 0
        numpeaks = 0
        for j in range(1, self.h - 1):
            for i in range(1, self.w - 1):
                if self.img[j, i] >= self.tol:
                    p = self.img[j-1:j+2, i-1:i+2]
                    if self.img[j, i] == p.max():
                        plist[index] = j*self.w + i #.append(j*self.w + i)
                        vlist[index] = self.img[j, i] #.append(self.img[j, i])
                        numpeaks += 1
                        index += 1
              
        p = plist[:index]  #np.array(plist, dtype=np.int32)
        v = vlist[:index] #np.array(vlist, dtype=np.float32)
        sortedargs = np.argsort(v)[::-1]
        self.sorted_p = p[sortedargs]
        self.sorted_v = v[sortedargs]
        print(len(self.sorted_p), index)
        return
        
    def findmax(self):
        
        peak_img = np.zeros((self.w*self.h,), dtype=np.int32)
        noffsets= len(self.xoffsets)
        
        counter = 0
        peak_list = np.zeros(self.sorted_p.shape[0], dtype=np.uint32) #list()
        
        # iterate over all local maxima in self.sorted_p
        #print(len(self.sorted_p))
        peak_index = 0
        
        for p in self.sorted_p:
            print(p, counter)
            #iv = next(iviter)
            #plist = [p]  # add the local peak as the first pixel
            plist = np.zeros(self.sorted_p.shape[0], dtype=np.uint32)
            plist[0] = p
            plist0 = 0
            plist_index = 1
            x = p % self.w
            y = p // self.w
            v = self.img[y, x]
            is_peak = True
            '''
            If value of the peak is 0, then it hasn't been looked at and can
            be considered a peak
            '''
            if peak_img[p] == 0:
                peak_img[p] = 32   #len(self.sorted_p) - iv
                #peak_list[peak_index] = p #.append(p)
                counter += 1
                
                #print("A", counter)
            else:
                counter += 1
                #print("C", counter)
                continue
                
            #clist = np.zeros(self.sorted_p.shape[0], dtype=np.uint32) #.list()
            
            '''
            loop over plist and examine neighbors
            '''
            
            p_nbnum = 1
            
            #clist_index = 0
            clist = np.zeros(self.sorted_p.shape[0], dtype=np.uint32)
            clist_index = 0
            while p_nbnum > 0: #len(plist) > 0:
                #this_p = plist[0]
                
                this_p = plist[plist0]
                plist0 += 1
                for k in range(noffsets):
                    xn = this_p % self.w
                    yn = this_p // self.w
                    if xn >= self.w:
                        continue
                    elif xn < 0:
                        continue
                    elif yn < 0:
                        continue
                    elif yn >= self.h:
                        continue
                    i = self.xoffsets[k]
                    j = self.yoffsets[k]
                    pindex = self.w*(yn + j) + xn + i
                    if peak_img[pindex] >= 16:
                        continue
                    vnb = self.img[yn+j, xn+i]  #value of neighbor pixel
                    #clist.append(pindex)
                    clist[clist_index] = pindex
                    clist_index += 1
                    '''
                    If the neighbor pixel is greater than the local peak,
                    then not really a peak
                    '''
                    if vnb > v:
                        peak_img[p] = 2
                        peak_list[peak_index] = 0
                        is_peak = False
                        p_nbnum = 1
                        #plist.clear()
                        peak_img[clist[:clist_index]] = 4
                        break #break for
                    
                    '''
                    If the neighbor if greater than the peak value minus
                    the tolerance, then the neighbor is within the peak
                    '''
                    if vnb >= (v - self.tol):
                        if peak_img[pindex] == 8:
                            #peak_list.remove(p)
                            #plist.clear()
                            # peak_img[np.array(clist, dtype=np.int32)] = 4
                            is_peak = False
                            p_nbnum = 1
                            peak_img[clist[:clist_index]] = 4
                            peak_img[pindex] = 8
                            break #break for
                        else:
                            plist[plist_index] = pindex  #.append(pindex)
                            plist_index += 1
                            p_nbnum += 1
                            peak_img[pindex] = 16 # len(self.sorted_p) - iv
                    else:
                        peak_img[pindex] = 8 
                p_nbnum -= 1
                
            if is_peak:
                peak_list[peak_index] = p
                print(peak_index, p)
                peak_index += 1
            else:
                peak_img[p] = 1            
                
                
                # if this_p in plist:
                #     plist.remove(this_p)
                    
            # if peak_img[p] < 32:
            #     if p in peak_list:
            #         peak_list.remove(p)
                #peak_img[np.array(clist, dtype=np.int32)] = 1 
            
        return peak_img, peak_list[:peak_index]
    
    
    