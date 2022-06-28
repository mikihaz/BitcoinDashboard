# Global Pacakges
import streamlit as st
import pandas as pd


# Local Packages
from hashrateindex import API
from resolvers import RESOLVERS

# WebApp Details
st.title("Hashrate Index Dashboard")
st.markdown("This is a Streamlit app that displays the Hashrate Index of the network.")
st.markdown("The Hashrate Index is a measure of the difficulty of the network. It is calculated by taking the average of the difficulty of the last 10 blocks.")

# Filter Options
# """
#     A class used to interact with Luxor's HashrateIndex GraphQL API.

#     Methods
#     -------
#     request(query, params)
#         Base function to execute operations against Luxor's GraphQL API
    
#     get_bitcoin_overview()
#         Contains Bitcoin network data overview stats.
        
#     get_hashprice(inputInterval, currency)
#         Returns Bitcoin hashprice for a specified interval
    
#     get_network_hashrate(inputInterval)
#         Returns the network hashrate for a specified interval
    
#     get_network_difficulty(inputInterval)
#         Returns the network difficulty and bitcoin price.
    
#     get_ohlc_prices(inputInterval)
#         Returns the Bitcoin OLHC prices at a specified interval.
    
#     get_asic_price_index(inputInterval, currency)
#         Returns the ASIC price index in USD for a given time interval.
# """
definedFunctions = {
    # Contains Bitcoin network data overview stats.
    'Bitcoin Overview': {
        'value' : 'get_bitcoin_overview',
        'resolver' : 'resolve_get_bitcoin_overview',
        'params': {},
        },

    # """
    #     Returns Bitcoin hashprice for a given interval

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
    #     currency : str
    #         currency for ASIC price, options are: `USD`, `BTC`
    # """
    'Hashprice' : {
        'value' : 'get_hashprice',
        'resolver' : 'resolve_get_hashprice',
        'params': {
            'inputInterval': {
                '1 Day': '_1_DAY',
                '7 Days': '_7_DAYS',
                '1 Month': '_1_MONTH',
                '3 Months': '_3_MONTHS',
                '1 Year': '_1_YEAR',
                'All': 'ALL',
            },
            'currency': {
                'USD': 'USD',
                'BTC': 'BTC',
            },
        },
    },

    # """
    #     Returns the network hashrate for a given interval

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
    # """
    'Network Hashrate' : {
        'value' : 'get_network_hashrate',
        'resolver' : 'resolve_get_network_hashrate',
        'params': {
            'inputInterval': {
                '1 Day': '_1_DAY',
                '7 Days': '_7_DAYS',
                '1 Month': '_1_MONTH',
                '3 Months': '_3_MONTHS',
                '1 Year': '_1_YEAR',
                'All': 'ALL',
            },
        },
    },

    # """
    #     Returns the network difficulty

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_3_MONTHS`, `_6_MONTHS`, `_1_YEAR`, `_3_YEAR` and `ALL`
    # """
    'Network Difficulty' : {
        'value' : 'get_network_difficulty',
        'resolver' : 'resolve_get_network_difficulty',
        'params': {
            'inputInterval': {
                '3 Months': '_3_MONTHS',
                '6 Months': '_6_MONTHS',
                '1 Year': '_1_YEAR',
                '3 Years': '_3_YEAR',
                'All': 'ALL',
            },
        },
    },

    # """
    #     Returns the Bitcoin OLHC prices at a specified interval

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_1_DAY`, `_7_DAYS`, `_1_MONTH`, `_3_MONTHS`, `_1_YEAR` and `ALL`
    # """
    'OLHC Prices' : {
        'value' : 'get_ohlc_prices',
        'resolver' : 'resolve_get_ohlc_prices',
        'params': {
            'inputInterval': {
                '1 Day': '_1_DAY',
                '7 Days': '_7_DAYS',
                '1 Month': '_1_MONTH',
                '3 Months': '_3_MONTHS',
                '1 Year': '_1_YEAR',
                'All': 'ALL',
            },
        },
    },

    # """
    #     Returns the ASIC price index in USD for a given time interval

    #     Parameters
    #     ---------
    #     inputInterval : str
    #         intervals to generate the timeseries, options are: `_3_MONTHS`, `_6_MONTHS`, `_1_YEAR` and `ALL`
    #     currency : str
    #         currency for ASIC price, options are: `USD`, `BTC`
    # """
    'ASIC Price Index' : {
        'value' : 'get_asic_price_index',
        'resolver' : 'resolve_get_asic_price_index',
        'params': {
            'inputInterval': {
                '3 Months': '_3_MONTHS',
                '6 Months': '_6_MONTHS',
                '1 Year': '_1_YEAR',
                'All': 'ALL',
            },
            'currency': {
                'USD': 'USD',
                'BTC': 'BTC',
            },
        },
    },
}

# Selecting the function to be used
selectedFunction = st.selectbox('Select Function', list(definedFunctions.keys()))
selectedFunctionParams = definedFunctions[selectedFunction]['params']

# Checking if the selected function has input intervals
selectedIntervalValue = None
if(list(selectedFunctionParams.keys()).__contains__('inputInterval')):
    selectedInterval = st.selectbox('Select Interval', list(selectedFunctionParams['inputInterval'].keys()))
    selectedIntervalValue = selectedFunctionParams['inputInterval'][selectedInterval]

# Checking if the selected function has currencies
selectedCurrencyValue = None
if(list(selectedFunctionParams.keys()).__contains__('currency')):
    selectedCurrency = st.selectbox('Select Currency', list(selectedFunctionParams['currency'].keys()))
    selectedCurrencyValue = selectedFunctionParams['currency'][selectedCurrency]

# Asking user for Api Key
apiKey = st.text_input('Enter your API Key')

# Initializing the API
myAPI = API(host = 'https://api.hashrateindex.com/graphql', method = 'POST', key = apiKey)
myRESOLVERS = RESOLVERS(df = False)

# Calling the selected function
if st.button('Get Data'):
    myFunction = getattr(myAPI, definedFunctions[selectedFunction]['value'])
    if(selectedIntervalValue != None and selectedCurrencyValue == None):
        apiResp = myFunction(selectedIntervalValue)
    elif(selectedIntervalValue != None and selectedCurrencyValue != None):
        apiResp = myFunction(selectedIntervalValue, selectedCurrencyValue)
    else:
        apiResp = myFunction()
    myData = getattr(myRESOLVERS, definedFunctions[selectedFunction]['resolver'])(apiResp)
    
    # Plotting the data from the API
    tableDictData = {}
    for key in myData[0]:
        tableDictData.update({key: []})
    for i in range(len(myData)):
        for key, value in myData[i].items():
            tableDictData[key].append(value)
    
    # Converting the data to a pandas dataframe
    tableColumns = list(tableDictData.keys())
    tablePdData = pd.DataFrame(tableDictData, columns = tableColumns).set_index(tableColumns[0])
    tablePdData.index = pd.to_datetime(tablePdData.index)
    
    # Showing the Data in the Frontend
    if(selectedFunction != 'Bitcoin Overview'):
        with st.expander('Line Chart'):
            st.line_chart(tablePdData)
        with st.expander('Area Chart'):
            st.area_chart(tablePdData)
        with st.expander('Statistics'):
            st.dataframe(tablePdData.describe())
    else:
        st.subheader('Bitcoin Metrics')
        for col in tablePdData.columns:
            st.metric(col,tablePdData[col][0])
    with st.expander('Raw Data'):
        st.dataframe(tablePdData)
    

