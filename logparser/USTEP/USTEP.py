"""
Description : This file implements the USTEP algorithm for log parsing
Author      : Outscale SAS
License     : SD 3-Clause License
"""

import io
import os
import re
from datetime import datetime
import pandas as pd

class LogGroup():
    def __init__(self, template_id, template):
        self.template_id = template_id
        self.template = template
        
    def add_log(self, splitted_log_message):
        group_message = self.template.split(' ')
        for i, token in enumerate(splitted_log_message):
            if token != group_message[i]:
                group_message[i] = '<*>'
        self.template = ' '.join(group_message)
            
        
class Node():
    def __init__(self, childs=None, log_groups=None, child_key=1):
        if childs is None:
            childs = {}
        self.childs = childs
        if log_groups is None:
            log_groups =  []
        self.log_groups = log_groups
        self.child_key = child_key
        
    def get_child(self, key):
        child = self.childs.get(key, None)
        if child is None:
            child = Node()
            self.childs[key] = child
        return self.childs[key]
    
    def get_loggroup(self, splitted_log_message):
        log_group = None
        best_sim = 0
        for group in self.log_groups:
            group_message = group.template.split(' ')
            sim = 0
            for i, token in enumerate(splitted_log_message):
                if token == group_message[i]:
                    sim += 1
            sim = sim/len(splitted_log_message)
            if sim > best_sim:
                log_group = group
                best_sim = sim
        return log_group, best_sim

        
    def is_leaf(self):
        return self.childs == {}
    
    def divide(self):
        """ Split node into multiple nodes depending on pivot """
        
        # Search for dividing pivot
        log_size = len(self.log_groups[0].template.split(' '))
        max_diversity = 0
        index = 0
        for i in range(log_size):
            token_set = set()
            local_diversity = 0
            for group in self.log_groups:
                group_token = group.template.split(' ')[i]
                if group_token not in token_set:
                    local_diversity += 1
                    token_set.add(group_token)
            if local_diversity > max_diversity:
                max_diversity = local_diversity
                index = i
        self.child_key = index
        
        # Move Log groups to new leaves
        for group in self.log_groups:
            new_node = self.get_child(group.template.split(' ')[index])
            new_node.log_groups.append(group)
        self.log_groups = []
            
        
class LogParser():
    def __init__(self, log_format: str, indir='./', outdir='./result/', st=0.5, max_loggroup=2, regexs=[]):
        self.log_format = log_format
        self.path = indir
        self.savePath = outdir
        self.root = Node()
        self.total_templates = 0
        self.st = st
        self.max_loggroup = max_loggroup
        self.regexs = regexs
  
    def preprocess(self, line):
        for regex in self.regexs:
            line = re.sub(regex, '<*>', line)
        return line

    def generate_logformat_regex(self, logformat: str):
        """ Function to generate regular expression to split log messages.
            This is used to parse log headers.
        """
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(' +', '\\\s+', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex

    def load_data(self):
        headers, regex = self.generate_logformat_regex(self.log_format)
        self.df_log = self.log_to_dataframe(os.path.join(self.path, self.logName), regex, headers, self.log_format)

    def log_to_dataframe(self, log_file, regex, headers, logformat):
        """ Function to transform log file to dataframe """
        log_messages = []
        linecount = 0
        with io.open(log_file, "r", encoding="utf-8") as fin:
            for line in fin.readlines():
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        return logdf

    def parseLog(self, log_message):
        log_message = self.preprocess(log_message)
        log_message = " ".join(log_message.split())
        splitted_message = log_message.split(' ')
        
        # Search for the corresponding length Node or create it
        current_node = self.root.get_child(len(splitted_message))
        node_is_satisfying = False
        i = 0
        # Iterate over tokens till we find a satisfying node
        while not node_is_satisfying:
            if current_node.is_leaf():
                log_group, sim = current_node.get_loggroup(splitted_message)
                if sim >= self.st:
                    log_group.add_log(splitted_message)
                else:
                    log_group = LogGroup(self.total_templates, log_message)
                    current_node.log_groups.append(log_group)
                    self.total_templates += 1
                if len(current_node.log_groups) >= self.max_loggroup:
                    current_node.divide()
                node_is_satisfying = True
            else:
                i = current_node.child_key
                token = splitted_message[i]
                current_node = current_node.get_child(token)
        return log_group

    def parse(self, logName):
        print('Parsing file: ' + os.path.join(self.path, logName))
        start_time = datetime.now()
        self.logName = logName

        self.load_data()
        #self.df_log = pd.read_csv(os.path.join(self.path, logName))

        processing_times = [0] * self.df_log.shape[0]
        logGroups = [0] * self.df_log.shape[0]
        for _, log in self.df_log.iterrows():
            processing_start_time = datetime.now()
            logID = log['LineId'] - 1
            logGroups[logID]= self.parseLog(log['Content'])
            processing_times[logID] = str(datetime.now() - processing_start_time)
        templates = [group.template for group in logGroups]
        templateids = [group.template_id for group in logGroups]
        print('Parsing done. [Time taken: {!s}]'.format(datetime.now() - start_time))

        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
            
        # Output parse file
        self.df_log['EventId'] = templateids
        self.df_log['EventTemplate'] = templates
        self.df_log['ProcessingTimes'] = processing_times
        self.df_log.to_csv(os.path.join(self.savePath, self.logName + '_structured.csv'), index=False, encoding = 'utf-8')

        # Output template file
        occ_dict = dict(self.df_log['EventTemplate'].value_counts())
        df_event = pd.DataFrame()
        df_event['EventTemplate'] = self.df_log['EventTemplate'].unique()
        df_event['Occurrences'] = df_event['EventTemplate'].map(occ_dict)
        df_event.to_csv(os.path.join(self.savePath, self.logName + '_templates.csv'), index=False, encoding = 'utf-8')



        print('Ouput generated. [Time taken: {!s}]'.format(datetime.now() - start_time))
