from dotenv import dotenv_values


ENV_DATA = {**dotenv_values('.env')}

TOKEN_API = ENV_DATA['TOKEN_API']
API_ID = ENV_DATA['API_ID']
API_HASH = ENV_DATA['API_HASH']
NAME = ENV_DATA['NAME']
ADMINS = ENV_DATA['ADMINS'].split(', ')
