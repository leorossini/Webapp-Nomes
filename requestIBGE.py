import requests
from pprint import pprint # Pretty Print para melhor visualização

#urlLocalidades = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
#paramsLocalidades = {'view': 'nivelado'}

def requestIBGE(url, params=None):
    response = requests.get(url, params=params)
    try:
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
    except requests.exceptions.HTTPError as e:
        print(f'Falha ao acessar a API: {e}')
        return None
    else:
        responseJson = response.json()  # Parse the JSON response
    return responseJson


def getIdUFs():
    urlUFs = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    paramsUFs = {'view': 'nivelado'}
    response = requestIBGE(urlUFs, params=paramsUFs)
    if response:
        return {uf['UF-id']: uf['UF-nome'] for uf in response}
    return None

def getFrequenciaNomesPorEstados(nome, porProporcao=False):
    urlNomes = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'
    paramsNomes = {'groupby': 'UF'}
    response = requestIBGE(urlNomes, params=paramsNomes)
    if response:
        dictFreq = {}
        for nome in response:
            idUf = int(nome['localidade'])
            prop = nome['res'][0]['proporcao']
            freq = nome['res'][0]['frequencia']
            dictFreq[idUf] = prop if porProporcao else freq
        return dictFreq
    return None

def getFrequenciaNomesPorDecada(nome):
    urlNomes = f'https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}'
    paramsNomes = {}
    response = requestIBGE(urlNomes, params=paramsNomes)
    if response:
        dictFreq = {str(decada['periodo']).replace('[','').split(',')[0]: decada['frequencia'] 
                    for decada in response[0]['res']}
        return dictFreq
    return None

