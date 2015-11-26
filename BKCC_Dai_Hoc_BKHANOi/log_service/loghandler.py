# -*- coding: utf-8 -*-
#
# Copyright 2014 - StackStorm, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd
import glob
import config
import datetime
import time

__author__ = 'techbk,thang,nhat'


class LogHandler(object):
    def __init__(self, path=None):
        if not path:
            self._path = config.LOG_PATH
        else:
            self._path = path
        
        self._log = None #dat_frame
        


    def _understand_resource(resource):
        for project in self._list_of_project:
            if resource.find(project):
                return project.upper(project)

    def _fomat_log(self, dataframe):
        for index, row in dataframe.iterrows(): 
            # print(row)
            # print(row['resource'])
            row['project'] = self._understand_resource(row['resource'])


    def _log_path(self,project):
        path = {
            'nova' : [],
            'glance' : [],
            'neutron' : [],
            'all' :[]
        }
        for file in glob.glob(self._path + 'n-*.log*'):
            path['nova'].append(file)
            path['all'].append(file)
        for file in glob.glob(self._path + 'g-*.log*'):
            path['glance'].append(file)
            path['all'].append(file)
        #for file in glob.glob(self._path + 'key.log*'):
            #path.append(file)
        for file in glob.glob(self._path + 'q-*.log*'):
            path['neutron'].append(file)
            path['all'].append(file)
        return path[project]

    def _filter_log(self, level, date_start, date_finish):         
        log = self._log
        log = log[(log['time'] >= date_start) & (log['time'] <= date_finish)]
        if level != 'all':
            log = log[(log['level'] == level)]
        return log

    def _statistic_log(self):
        #nhat viet
        log = self._log
        #dem so log moi loai moi ngay
        statistic = pd.DataFrame({'count' : log.groupby( ["level"] ).size()}).reset_index()
        return statistic.to_json(orient="records")
    

    def _read_log(self,project):
        path = self._log_path(project)
        cols = ['time', 'level', 'resource', 'message']  # Set columns for DataFrame
        log = pd.DataFrame()
        for log_file in path:
            rl = pd.read_csv(log_file, sep=',', names=cols, skiprows=5)  # Read file log and display to dataframe's format
            rl['project'] = pd.Series(project.upper(), index=rl.index)
            log = log.append(rl, ignore_index=True)
        # print(log)
        sorted_log = log.sort_values(['time'])  # sort time
        sorted_log = sorted_log.reset_index(drop=True)
        # sorted_log = self._fomat_log(sorted_log)
        # print(sort)
        # print(sort.to_json(orient='index'))
        return sorted_log

    def project_log(self, project,level,start,end):

        self._log = self._read_log(project)
        log = self._filter_log(level,start,end)
        return log.to_json(orient='index')

    def tong_hop(self, project,level,start,end):
        self._log = self._read_log(project)
        return self._statistic_log()

if __name__ == "__main__":
    handler = LogHandler()

    for i in handler._log_path():
        print(i)

    l = handler.project_log('all', 'all', '2015-11-25 00:00:00', '2015-11-27 00:00:00')
    #print(l)