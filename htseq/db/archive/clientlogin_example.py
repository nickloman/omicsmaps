'''
Created on Dec 22, 2010

@author: Kathryn Hurley
'''


from authorization.clientlogin import ClientLogin
from sql.sqlbuilder import SQL
import ftclient
from fileimport.fileimporter import CSVImporter


if __name__ == "__main__":

  import sys, getpass
  username = sys.argv[1]
  password = getpass.getpass("Enter your password: ")

  token = ClientLogin().authorize(username, password)
  ft_client = ftclient.ClientLoginFTClient(token)

  #show tables
  results = ft_client.query(SQL().showTables())
  print results

  #import a table from CSV file

  datatypes = ['DATETIME', 'STRING', 'LOCATION', 'LOCATION', 'STRING', 'STRING', 'LOCATION', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER', 'NUMBER']

  tableid = int(CSVImporter(ft_client).importFile(sys.argv[2], data_types=datatypes))
  print tableid

  #drop table
  #print ft_client.query(SQL().dropTable(tableid))
