
import numpy as np
cimport cython
yoffsets = np.array([-1, -1, -1,  0, 0,  1, 1, 1], dtype=np.int32)
xoffsets = np.array([-1,  0,  1, -1, 1, -1, 0, 1], dtype=np.int32)
cdef int [:] xoffsets_view = xoffsets
cdef int [:] yoffsets_view = yoffsets
noffsets = 8

#@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False) 
def findmaxima(float[:, ::1] img, float tol):
    cdef int [:] alm = all_local_max(img, tol)
    return findmax(img, alm, tol)

#@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False) 
cdef int is_pixel_max(float[:,::1] img , int y0, int x0):

    cdef int height = img.shape[0]
    cdef int width = img.shape[1]
    
    cdef float pval
    pval = img[y0,x0]
    cdef Py_ssize_t j, i
    cdef int x, y
    for j in range(8):
        y = y0 + yoffsets_view[j]
        for i in range(8):
            x = x0 + xoffsets_view[i]
            if pval < img[y, x]:
                return 0
    return 1

#@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False) 
def all_local_max(float[:, ::1] img, float tol):

    cdef int height = img.shape[0]
    cdef int width = img.shape[1]

    cdef int vlen 
    vlen = width*height
    p_values = np.zeros((vlen,), dtype=np.float32)
    p_indices = np.zeros((vlen,), dtype=np.int32)

    cdef float [::1] p_values_view = p_values 
    cdef int [::1] p_indices_view = p_indices 
    cdef int found_maxima = 0

    cdef Py_ssize_t j, i
    cdef float pxy

    for j in range(1, height - 1):
        for i in range(1,width -1):
            if img[j, i] >= tol:
                if is_pixel_max(img, j, i) == 1:
                    p_values_view[found_maxima] = img[j, i]
                    p_indices_view[found_maxima] = j*width + i
                    found_maxima += 1

    
    sp_vals = np.argsort(p_values[:found_maxima])
    return np.flip(p_indices[:found_maxima][sp_vals])


#@cython.boundscheck(False)  # Deactivate bounds checking
# @cython.wraparound(False) 
# cdef int is_in(int [::1] vect, int a, int inc):
#     cdef Py_ssize_t i
#     for i in range(inc-1,-1,-1):
#         if vect[i] == a:
#             return 1
#     return 0


#@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False) 
def findmax(float [:,::1] img, int [:] p_indices, float tol):

    cdef int height = img.shape[0]
    cdef int width = img.shape[1]
    cdef int consize = width*height

    peak_img = np.zeros(height*width, dtype=np.int32)
    cdef int [::1] peak_img_view = peak_img

    cdef int ns = p_indices.shape[0]
    peak_list = np.zeros(ns, dtype=np.int32)
    cdef int [::1] peak_list_view = peak_list
    cdef int peak_inc = 0

    exlist = np.zeros(consize, dtype=np.int32)
    cdef int [::1] exlist_view = exlist

    expixels = np.zeros(consize, dtype=np.int32)
    cdef int [::1] expixels_view = expixels

    clist = np.zeros(consize, dtype=np.int32)
    cdef int [::1] clist_view = clist

    cdef int exinc, cinc, exnum
    cdef int x, y, p, ex, ey, exlist0
    cdef bint is_peak, kg
    cdef int i, j, pij
    cdef Py_ssize_t k, pic, index
    cdef float pval, exval
    cdef int status
    index = 0
    for p in p_indices:
        index += 1
        exinc = 0
        exlist0 = 0
        exlist_view[exinc] = p
        exinc += 1
        exnum = 1
        cinc = 0
        status = 0
        # for k in range(consize):
        #     clist_view[k] = 0
        #     expixels_view[k] = 0

        expixels_view[p] = index
        x = p % width
        y = p // width
        
        pval = img[y, x]
        is_peak = True
        
        if peak_img_view[p] == 0:
            peak_img_view[p] = 32
        else:
            continue
       
        while exnum > 0:
            status = 0
            pex = exlist_view[exlist0]
            exlist0 += 1
            ex = pex % width
            ey = pex // width
            #  print(index, x, y, ex, ey, "****", peak_img_view[pij])
            if (ex <= 0) or (ey <= 0):
                exnum -= 1
                continue
            if (ex >= width - 1) or (ey >= height -1):
                exnum -= 1
                continue
            
            #print(exinc, exnum, exlist0, cinc, pex)
            for k in range(noffsets):    
                i = xoffsets_view[k]
                j = yoffsets_view[k]
                pij = width*(ey + j) + ex + i
                if pij == p:
                    continue
                if pij >= width*height or pij < 0:
                    print("out of bounds", pij)
                    continue
                
                if clist_view[pij] == index:
                    status = 6
                    # if x == 675 and y == 881:
                    #     print(index, x, y, ex, ey, ex + i, ey + j, status, peak_img_view[pij], exnum)
                    continue
                #clist_view[pij] = index
                cinc += 1
                # if is_in(clist_view, pij, cinc) == 0:
                #     clist_view[cinc] = pij
                #     cinc += 1
                
                if peak_img_view[pij] >= 16:
                    status = 5
                    # if x == 675 and y == 881:
                    #     print(index, x, y, ex, ey, ex + i, ey + j, status, peak_img_view[pij], exnum)
                    continue

                exval = img[ey + j, ex + i]

                if exval > pval:
                    peak_img_view[p] = 2
                    peak_list_view[peak_inc] = 0
                    is_peak = False
                    exnum = 1
                    status = 1
                    # if x == 675 and y == 881:
                    #     print(index, x, y, ex, ey, ex + i, ey + j, status, peak_img_view[pij])
                    break

                if exval >= (pval - tol):
                    if peak_img_view[pij] == 8:

                        #kg = False
                        if clist_view[pij] == index:
                            #print(ex + i, ey + j, exval, ex, ey, pval)
                            status = 9
                            # if x == 675 and y == 881:
                            #     print(index, x, y, ex, ey, ex + i, ey + j, status, peak_img_view[pij])
                            continue
                        
                        status = 2
                        is_peak = False
                        exnum = 1

                        peak_img_view[pij] = 8
                        # if x == 675 and y == 881:
                        #     print("**", index, x, y, ex, ey, ex + i, ey + j, status, peak_img_view[pij])
                        break
                    else:
                        if expixels_view[pij] != index:
                            expixels_view[pij] = index
                        exlist_view[exinc] = pij
                        exinc += 1
                        exnum += 1
                        peak_img_view[pij] = 16
                        status = 3
                else:
                    peak_img_view[pij] = 8
                    status = 4
                clist_view[pij] = index
                # if x == 675 and y == 881:
                #     print(index, x, y, ex, ey, ex + i, ey + j, status, peak_img_view[pij], exnum)
            exnum -= 1
            
        if is_peak:
            peak_img_view[p] = 32
            peak_list_view[peak_inc] = p
            peak_inc += 1
        else:
            peak_img_view[p] = 1
    return peak_img, peak_list[:peak_inc]
                        
                    
            
