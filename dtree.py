from __future__ import division
__author__ = 'shridharmanvi'

import pandas as pd
import math
import operator
import sys


def entropy(attribute, data, edible, poisonous):
    #  Code to calculate entropy of an attribute
    values = data[attribute].unique()
    edb = {}
    posn = {}
    dat = {}
    _entropy = 0
    #  Calculate the number of occurences of each of the attribute values in each class

    for attribute_value in values:
        # Gives numerator of P(j|t) (Adding small number to avoid log(0))
        edb[attribute_value] = len(edible[edible[attribute] == attribute_value]) + 0.0001
        posn[attribute_value] = len(poisonous[poisonous[attribute] == attribute_value]) + 0.0001
        dat[attribute_value] = {'cnt': len(data[data[attribute] == attribute_value])}

        #  Calculate entropies of individual attributes below

        edb_val = edb[attribute_value]/dat[attribute_value]['cnt']
        posn_val = posn[attribute_value]/dat[attribute_value]['cnt']
        dat[attribute_value]['entropy'] = - ((edb_val * math.log(edb_val, 2)) + (posn_val * math.log(posn_val, 2)))

        _entropy += -((dat[attribute_value]['cnt'] / len(data)) * math.log(dat[attribute_value]['cnt'] / len(data), 2))

    sub = 0
    for attribute_value in values:
        sub += ((dat[attribute_value]['cnt']/len(data)) * (dat[attribute_value]['entropy']))

    return(_entropy - sub)


def check_continuity(cur_att, test_data):
    global data
    global poisonous
    global edible
    global processed_attributes
    #  This function does an attribute test for the test data at the given level
    #  Data is current valid data - without considering class
    print test_data
    attribute_values = data[cur_att].unique()
    flag = 0
    processed_attributes = cur_att
    for value in attribute_values:
        #  print data[data[attribute] == value]['class'].unique()
        if (test_data[cur_att] == value) & (len(data[data[cur_att] == value]['class'].unique()) == 1):
            print 'Final Class assigned: ', data[data[cur_att] == value]['class'].unique()[0]
            return
        else:
            flag = 1
            if cur_att == 'bruises':  # If no more splitting attributes left
                s = data['class'].value_counts()
                print s
                print 'Final Class assigned: ', s.argmax()

    residual_data_attribute = test_data[cur_att][0] # To filter the data to pass it on to next level of tree for splitting
    data = data[data[cur_att] == residual_data_attribute]
    poisonous = data[data['class'] == 'p']
    edible = data[data['class'] == 'e']


if __name__ == '__main__':
    columns = ['class', 'cap_shape', 'cap_surface', 'cap_color', 'bruises', 'odor']
    attributes = ['cap_shape', 'cap_surface', 'cap_color', 'bruises']

    #  Tree Level 1 datasets below
    data = pd.read_csv('mushroom_Data.csv', names=columns)
    test_data = pd.read_csv('mushroom_Data.csv', names=columns)
    edible = data[data['class'] == 'e']
    poisonous = data[data['class'] == 'p']
    processed_attributes = ''
    passed_testdata = ''
    #  At each level do the following

    for i in range(0, len(attributes)):
        attributevalue_entropies = []

        if processed_attributes in attributes: attributes.remove(processed_attributes)
        for attribute in attributes:
            attributevalue_entropies.append(entropy(attribute, data, edible, poisonous))
        print attributevalue_entropies

        max_index, max_value = max(enumerate(attributevalue_entropies), key=operator.itemgetter(1))  # Gives the attribute to split on
        current_att = attributes[max_index]
        #check_continuity(current_att, test_data.iloc[21])  # Checks continuity or if leaf node encountered
        check_continuity(current_att, sys.argv[0])









