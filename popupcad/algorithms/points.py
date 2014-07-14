# -*- coding: utf-8 -*-
"""
Written by Daniel M. Aukes.
Email: danaukes<at>seas.harvard.edu.
Please see LICENSE.txt for full license.
"""
import numpy

def twopointsthesame(pt1,pt2,tolerance):
    v = numpy.array(pt2)-numpy.array(pt1)
    l = v.dot(v)**.5
    return l<tolerance
        
def pointinpoints(pt1,pts,tolerance):
    tests = [twopointsthesame(pt1,pt2,tolerance) for pt2 in pts]
    return True in tests

def point_on_line(point,line,tolerance):
    point = numpy.array(point)
    p1 = numpy.array(line[0])
    p2 = numpy.array(line[1])
    v = p2 - p1
    lv = v.dot(v)
    
    v2 = point - p1
    lv2 = v2.dot(v2)
    vpoint = v.dot(v2)**2 - lv*lv2
    vpoint = abs(vpoint)**(.5)
#    print vpoint,tolerance
    return abs(vpoint)<abs(tolerance)

def colinear(line1,line2,tolerance):
    a = point_on_line(line2[0],line1,tolerance)
    b = point_on_line(line2[1],line1,tolerance)
    return a and b
    
def point_within_line(point,line,tol):
    if point_on_line(point,line,tol):
        point = numpy.array(point)
        p1 = numpy.array(line[0])
        p2 = numpy.array(line[1])
        v = p2 - p1
        v2 = point - p1
        lv = v.dot(v)

        l = v.dot(v2)
        return l>0 and l<lv
    return False

def shared_edge(line1,line2,tolerance):
    if colinear(line1,line2,tolerance):
        a = point_within_line(line2[0],line1,tolerance)
        b = point_within_line(line2[1],line1,tolerance)
        return a or b
    return False

def inner_segment(line1,line2,tolerance):
    points = line1
    if point_within_line(line2[0],line1,tolerance):
        if point_within_line(line1[0],(line2[0],line1[1]),tolerance):
            points = (line1[0],line2[0])
        elif point_within_line(line1[1],(line2[0],line1[0]),tolerance):
            points = (line1[1],line2[0])
        else:
            points = line2
            
    if point_within_line(line2[1],line1,tolerance):
        if point_within_line(line1[0],(line2[1],line1[1]),tolerance):
            points = (line1[0],line2[1])
        elif point_within_line(line1[1],(line2[1],line1[0]),tolerance):
            points = (line1[1],line2[1])
        else:
            points = line2

    return points
        
def calctransformfrom2lines(pointset1,pointset2,scale_x = None,scale_y = None):
    import math
    pointset1 = numpy.array(pointset1)
    pointset2 = numpy.array(pointset2)
    v1 = pointset1[1]-pointset1[0]
    v2 = pointset2[1]-pointset2[0]
    q1 = math.atan2(v1[1],v1[0])
    q2 = math.atan2(v2[1],v2[0])
    l1 = v1.dot(v1)**.5
    l2 = v2.dot(v2)**.5
    scale_internal = l2/l1

    if scale_x == None:
        scale_x = scale_internal
    if scale_y == None:
        scale_y = scale_internal
    
    T0 = numpy.eye(3)
    T0[0:2,2] = -pointset1[0]

    T1 = numpy.eye(3)
    T1[0,0] = math.cos(-q1)
    T1[0,1] = -math.sin(-q1)
    T1[1,1] = math.cos(-q1)
    T1[1,0] = math.sin(-q1)

    T2 = numpy.eye(3)
    T2[0,0] = scale_x
    T2[1,1] = scale_y
    
    T3 = numpy.eye(3)
    T3[0,0] = math.cos(q2)
    T3[0,1] = -math.sin(q2)
    T3[1,1] = math.cos(q2)
    T3[1,0] = math.sin(q2)
    T3[0:2,2] = pointset2[0]
    
    T = T3.dot(T2.dot(T1.dot(T0)))
    return T[0,0],T[0,1],T[1,0],T[1,1],T[0,2],T[1,2]  
#
def convert_to_3d(listin):
    a = numpy.array(listin)
    c = a.T[0]*0
    d = numpy.concatenate((a.T,[c]),0)
    a = d.T
    return a.tolist()

if __name__=='__main__':
#    print(colinear([[0,0],[1,1]],[[.1,.1+.9e-3],[.9,.9]],1e-3))
#    print point_within_line([2,0],[[0,0],[1,0]],1e-3)
    print(colinear([[0,0],[1,1]],[[-.1,-.1+.9e-3],[-.9,-.9]],1e-3))
    print(shared_edge([[0,0],[1,1]],[[-.1,-.1+.9e-3],[-.9,-.9]],1e-3))
