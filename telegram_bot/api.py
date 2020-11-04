from jira import JIRA
from config import api_key, login

jira_options = {'server': 'https://txcloud.atlassian.net'}
jira = JIRA(options=jira_options, basic_auth=(login, api_key))