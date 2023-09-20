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
    apiCaller.setBranch(choice)

    # configure the query format of first-called api
    # TODO: add support for another type of sensor, right now only sensor of owner:TT are supported 
    q = {}
    if choice == 0:
        q = {'q':'owner:TT'}

    branch = apiSelector.branch[choice]
    loadedData = apiCaller.callApi(branch=branch, params=q, singleCall=True)

    #TODO take the parameter of interest
    apiCaller.chooseKey(loadedData)
    print('You can choose which parameter you want, please type the name of the paramter, the result will only include those parameters you want')
    filter = input()
    apiCaller.setFilter(filter)
    # TODO suport all locations
    print('Since there are so many locations, please choose some locations of your interest to save resources, please look at the location file for reference')
    location = input()
    

    print('please choose a time period of your interest. Format: YYYY-MM-DD')
    print('From: ',end='')
    timefrom = input()
    print('To: ',end='')
    timeto = input()

    userAddedParams = apiCaller.inputParameter(location,timefrom,timeto)
    if q:
        # to check if there is really something to add to prevent key error
        combinedParams = apiCaller.addQuery(userAddedParams,q=q)
    else:
        combinedParams = userAddedParams

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