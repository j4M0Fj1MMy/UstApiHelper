from ApiSelector import ApiSelector,ApiCaller
from DataWriter import DataWriter

def dialog() -> None:
    pass

def parseApiResult():
    #TODO parse the data for output
    pass

def writeToFile(data):
    #TODO write the data into a desired format

    dataWriter = DataWriter.DataWriter(data,'output.csv')
    dataWriter.writeTocsv()


def main():
    apiSelector = ApiSelector.ApiSelector()
    apiCaller = ApiCaller.ApiCaller()
    print('Which of the following Api do you want? [0-9]')
    print(apiSelector.branch)
    choice = int(input())

    # TODO: add support for another type of sensor, right now only sensor of owner:TT are supported 
    branch = apiSelector.branch[choice]
    q = {'q':'owner:TT'}
    loadedData = apiCaller.callApi(branch=branch, params=q, singleCall=True)

    #TODO take the parameter of interest
    apiCaller.chooseKey(loadedData)
    print('You can choose which parameter you want, please type the name of the paramter, the result will only include those parameters you want')
    filter = input()
    apiCaller.setFilter(filter)
    # TODO suport all locations
    print('Since there are more than 1000 locations, please choose some locations of your interest to save resources, please look at the location file for reference')
    location = input()
    

    print('please choose a time period of your interest. Format: YYYY-MM-DD')
    print('From: ',end='')
    timefrom = input()
    print('To: ',end='')
    timeto = input()

    userAddedParams = apiCaller.inputParameter(location,timefrom,timeto)
    combinedParams = apiCaller.addQuery(userAddedParams,q=q)
    print(combinedParams)
    data = apiCaller.callApi(branch=branch,params=combinedParams,singleCall=False)
    output = apiCaller.parseOutput(data=data)

    writeToFile(output)

    

main()

'''
#test data:
0
humidity,temperature
Coffeeshop
2023-07-01
2023-08-03

'''