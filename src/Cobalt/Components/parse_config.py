#!/usr/bin/env python

'''
Created on 2013-7-16

@author: zhouzhou
'''
import sys
from xml.etree import ElementTree

NODES_PER_NODECARD = 32
NODES_PER_MIDPLANE = 512
node_card_cache = {}

def get_min_cord(rack_set):
    ''' get minimum rack and midplane position '''
    min_r_num = 999
    min_m_num = 999
    
    for rack in rack_set:
        rack_id = rack.id
        r_num = int(rack_id[1:3])
        m_num = int(rack_id[5:6])
        
        if r_num < min_r_num:
            ''' nearer rack '''
            min_r_num = r_num
            min_m_num = m_num
        elif r_num == min_r_num:
            ''' same rack, but nearer midplane '''
            if m_num < min_m_num:
                min_m_num = m_num
    
    return min_r_num, min_m_num


def get_max_cord(rack_set):
    ''' get maximum rack and midplane position'''
    max_r_num = -1
    max_m_num = -1
    
    for rack in rack_set:
        rack_id = rack.id
        r_num = int(rack_id[1:3])
        m_num = int(rack_id[5:6])
        
        if r_num > max_r_num:
            ''' further rack '''
            max_r_num = r_num
            max_m_num = m_num
        elif r_num == max_r_num:
            ''' same rack, but further midplane '''
            if m_num > max_m_num:
                max_m_num = m_num
    
    return max_r_num, max_m_num

def get_dim(partition):
    # return the X, Y and Z coordination of a partition
    cards_set = set(partition.node_cards)
    min_rack, min_mid = get_min_cord(cards_set)
    max_rack, max_mid = get_max_cord(cards_set)
    
    X = 0
    Y = 0
    Z = 0
    
    if partition.size >= 512:
#            min_rack_x = min_rack / 10
#            min_rack_y = min_rack % 10
#            max_rack_x = max_rack / 10
#            max_rack_y = max_rack % 10
#            total_midplane = (max_rack_x - min_rack_x + 1) * (max_rack_y - min_rack_y + 1) * (max_mid - min_mid + 1)
#            if item['size'] != total_midplane * NODES_PER_MIDPLANE:
#                print "!!!!!!!!!!!!!!!!!", total_midplane, total_midplane * NODES_PER_MIDPLANE
#        
        X, Y, Z = get_X_Y_Z_cord(min_rack, max_rack, min_mid, max_mid)
    return X, Y, Z

def get_dim_accu(row, inter_row, inter_rack_pair):
    ''' return sum of all dimension '''
    return row + inter_row + inter_rack_pair


def get_X_Y_Z_cord(min_rack, max_rack, min_mid, max_mid):
    ''' X: row, Y: inter-row, Z: inter-rack-pair '''
    def _get_X_Y_Z_cord(min_rack_x, min_rack_y, max_rack_x, max_rack_y, max_mid, min_mid):
        ''' return the X, Y and Z dimension '''
        X = max_rack_x - min_rack_x + 1 # X dimension
        
        # Y dimension
        if (max_rack_y - min_rack_y + 1 ) < 2:
            Y = 1 # not a pair of racks
            Z = max_mid - min_mid + 1 # less than 4 midplanes
        else:
            Y = ( max_rack_y - min_rack_y + 1) / 2 # at least 1 pair of racks
            Z = 4
                
        return X, Y , Z

    min_rack_x = min_rack / 10
    min_rack_y = min_rack % 10
    max_rack_x = max_rack / 10
    max_rack_y = max_rack % 10
    
    return _get_X_Y_Z_cord(min_rack_x, min_rack_y, max_rack_x, max_rack_y, max_mid, min_mid)
    

def get_node_card(name):
    if not node_card_cache.has_key(name):
        node_card_cache[name] = name
        
    return node_card_cache[name]

if __name__ == '__main__':
    config_file = sys.argv.pop()
    
    system_doc = ElementTree.parse(config_file)
    system_def = system_doc.getroot()
    
    tmp_list = []
    
    for partition_def in system_def.getiterator("Partition"):
            if not partition_def.get("name").startswith("ANL"):
                continue
            
            node_list = []
            switch_list = []
            
            for nc in partition_def.getiterator("NodeCard"):
                pass

            for nc in partition_def.getiterator("NodeCard"): 
                node_list.append(get_node_card(nc.get("id"))[0:6])
            nc_count = len(node_list)
            
            for s in partition_def.getiterator("Switch"):
                switch_list.append(s.get("id"))

            tmp_list.append( dict(
                name = partition_def.get("name"),
                queue = partition_def.get("queue", "default"),
                size = NODES_PER_NODECARD * nc_count,
                node_cards = node_list,
                switches = switch_list,
                state = "idle",
            ))
    
    for item in tmp_list:
        X, Y ,Z = get_dim(item)
        print "dimension: ", "%d * %d * %d" % (Z, Y, X)
#        cards_set = set(item['node_cards'])
##        print item['node_cards']
#        print item['name']
#        print item['size']
#        min_rack, min_mid = get_min_cord(cards_set)
#        max_rack, max_mid = get_max_cord(cards_set)
#        print "Min:", "R%d-M%d" % (min_rack, min_mid)
#        print "Max:", "R%d-M%d" % (max_rack, max_mid) 
#        
#        if item['size'] >= 512:
##            min_rack_x = min_rack / 10
##            min_rack_y = min_rack % 10
##            max_rack_x = max_rack / 10
##            max_rack_y = max_rack % 10
##            total_midplane = (max_rack_x - min_rack_x + 1) * (max_rack_y - min_rack_y + 1) * (max_mid - min_mid + 1)
##            if item['size'] != total_midplane * NODES_PER_MIDPLANE:
##                print "!!!!!!!!!!!!!!!!!", total_midplane, total_midplane * NODES_PER_MIDPLANE
##        
#            X, Y, Z = get_X_Y_Z_cord(min_rack, max_rack, min_mid, max_mid)
#            print "Dimension: ", "%d * %d * %d" % (Z, Y, X)
            
        print "*****************************************"