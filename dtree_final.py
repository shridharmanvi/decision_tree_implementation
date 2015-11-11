#!/usr/bin/python
from __future__ import division
__author__ = 'shridharmanvi'

import pandas as pd
import math
import operator
import sys
import random
from random import randint


def entropy(attr, data, edible, poisonous):

    #  Code to calculate entropy of an attribute
    values = data[attribute].unique()
    edb = {}
    posn = {}
    dat = {}
    _entropy = 0
    #  Calculate the number of occurences of each of the attribute values in each class

    for attribute_value in values:
        # Gives numerator of P(j|t) (Adding small number to avoid log(0))
        edb[attribute_value] = len(edible[edible[attr] == attribute_value]) + 0.0001
        posn[attribute_value] = len(poisonous[poisonous[attr] == attribute_value]) + 0.0001
        dat[attribute_value] = {'cnt': len(data[data[attr] == attribute_value])}

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
    global flag
    #  This function does an attribute test for the test data at the given level
    #  Data is current valid data - without considering class

    attribute_values = data[cur_att].unique()

    processed_attributes = cur_att
    if flag == 0:
        for value in attribute_values:
            #  print data[data[attribute] == value]['class'].unique()
            if (test_data[cur_att] == value) & (len(data[data[cur_att] == value]['class'].unique()) == 1):
                #print 'Final Class assigned: ', data[data[cur_att] == value]['class'].unique()[0]
                op.append(data[data[cur_att] == value]['class'].unique()[0])
                flag = 1
                return
            else:
                if cur_att == 'bruises':  # If no more splitting attributes left, do majority voting
                    s = data['class'].value_counts().argmax()
                    op.append(s)
                    #print 'Final Class assigned: ', s

    residual_data_attribute = test_data[cur_att][0] # To filter the data to pass it on to next level of tree for splitting
    data = data[data[cur_att] == residual_data_attribute]
    poisonous = data[data['class'] == 'p']
    edible = data[data['class'] == 'e']


def calculate_error(actual_data, output):
    total = len(actual_data)
    pos = 0
    for i in range(0, len(actual_data)):
        if actual_data.iloc[i]['class'] == output[i]:
            #print actual_data.iloc[i]['class'], output[i]
            pos += 1

    return (pos/total) * 100



if __name__ == '__main__':
    columns = ['class', 'cap_shape', 'cap_surface', 'cap_color', 'bruises', 'odor']
    op = []
    test_dat = pd.read_csv('mushroom_testdata.csv', names=columns)
    train_dat = pd.read_csv('mushroom_data.csv', names=columns)
    rows = random.sample(train_dat.index, randint(30, 90))
    pass_data = train_dat.ix[rows]
    pass_data.to_csv('sample_training_data.csv', index=False)

    #  Tree Level 1 datasets below

    if sys.argv[1] == 'bagging':
        f = "sample_training_data.csv"
    else:
        f = "mushroom_data.csv"

    training_Dat = pd.read_csv(f, names=columns)

    for j in range(0, len(test_dat)):
        flag = 0
        attributes = ['cap_shape', 'cap_surface', 'cap_color', 'bruises']
        data = training_Dat
        edible = data[data['class'] == 'e']
        poisonous = data[data['class'] == 'p']
        processed_attributes = ''
        passed_testdata = ''
        #  At each level do the following

        for i in range(0, len(attributes)):

            attributevalue_entropies = []

            if processed_attributes in attributes: attributes.remove(processed_attributes)
            if flag == 0:
                for attribute in attributes:
                    attributevalue_entropies.append(entropy(attribute, data, edible, poisonous))
                #print attributevalue_entropies

                max_index, max_value = max(enumerate(attributevalue_entropies), key=operator.itemgetter(1))  # Gives the attribute to split on
                current_att = attributes[max_index]
                check_continuity(current_att, test_dat.iloc[j])  # Checks continuity or if leaf node encountered

    print op

    if sys.argv[1] == 'bagging':
        pass
    else:
        print 'Classification accuracy rate: ' + str(calculate_error(test_dat, op))








