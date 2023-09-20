import requests
import json

class ApiCaller:
    def __init__(self) -> None:
        f = open('config.json')
        self.secret = json.load(f)
        f.close()

        self.filter=None
        self.branch = None


    def callApi(self, branch: str, params: dict, singleCall: bool) -> json:
        prefix = self.secret['url']
        suffix = '_search'
        url = prefix + branch + suffix
        headers = {self.secret['Authorization-Header']:self.secret[branch]}

        # params = {
        #     'filter_path' : 'hits.hits._source.location',
        #     'sort' : '@timestamp:desc',
        #     'size' : 10000
        # }
        if singleCall:
            # single call mode
            response = requests.request("GET", url, headers=headers, params=params)
            print(response)
            return json.loads(response.text)

        else:
            # mutiple calls mode
            loadedData = []
            
            while True:
                response = requests.request("GET", url, headers=headers, params=params)
                print(response)
                if (json.loads(response.text))['hits']['total']['value'] == 0:
                    #ending point
                    break
                loadedData.append(json.loads(response.text))

                latesttime = loadedData[-1]['hits']['hits'][-1]['_source']['@timestamp']
                self.timeto=latesttime
                params = self.parseParameter()

            # End
            return loadedData
    
    def chooseKey(self, rawData: dict):
        for key in rawData['hits']['hits'][0]['_source'].keys():
            print(key)

    def inputParameter(self, location, timefrom, timeto):
        self.location = location
        self.timefrom = timefrom
        self.timeto = timeto
        return self.parseParameter()

    def parseParameter(self):
        # for checking later
        timeto = self.timeto
        timefrom = self.timefrom
        location = self.location

        keyOfLocation = 'location'
        if self.branch == 3:
            keyOfLocation = 'TLInstance'

        params = {
            'q': f'{keyOfLocation}:{location} AND '+'@timestamp:{'+timefrom+' TO '+timeto+'}' ,
            'filter_path':f'hits.hits._source.@timestamp,hits.total',
            'size':'10000',
            'sort' : '@timestamp:desc'
        }
        for eachfilter in self.filter:
            params['filter_path'] += f',hits.hits._source.{eachfilter}'
        return params
    
    def addParameter(self, oldParam, newParam):
        return oldParam | newParam
    
    def addQuery(self, param, q):
        '''
        appending q and q
        '''
        
        param['q'] += (' AND ' + q['q'])
        return param
     
    def parseOutput(self,data):
        output = []
        for datum in data:
            for e in datum['hits']['hits']:
                output.append(e['_source'])
        return output
    
    def setFilter(self,filter:str) -> None: 
        filterList = filter.split(',')
        self.filter = filterList

    def checkIfEnough(self,time):
        return True if time<self.timeto else False
    
    def setBranch(self, bracnch:int) -> None:
        self.branch = bracnch
