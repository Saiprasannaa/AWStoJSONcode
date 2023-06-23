import requests
from bs4 import BeautifulSoup
import json

def loopheader(url):    
    #url = "https://docs.aws.amazon.com/service-authorization/latest/reference/list_awsaccountmanagement.html"
    response = requests.get(url)
    html_data=response.content
    soup_data=BeautifulSoup(html_data, "html.parser")
    jsondata_all={}
    #jsondata_all["prefix"]=soup_data.find_all("title")[0].text.strip()
    titleval=(soup_data.find_all("title")[0].text.strip())
    titleval=titleval.replace("Actions, resources, and condition keys for","")
    titleval=titleval.replace(" - Service Authorization Reference","")
    jsondata_all["prefix"]=titleval
    

    jsondata_all["link"]=[]
    jsondata_all["link"].append(url)    
    filepath=titleval+".json"
    
    

    #print(jsondata_all)
    table_data=soup_data.find_all("div",class_="table-container")
    for table in table_data:
        jsondata_table=[]
        jsondata={}
        
        tableheader=table.find_all('tr')[0].find_all('th')
        tableheaders=[]
        #print(tableheaders)
        #if(tableheaders[0].text=="Actions"):
        if(tableheader[0].text=="Actions"):
            tableheaders=["action","desc","access","resources","conditionKeys","dependentActions"]
        if(tableheader[0].text=="Resource types"):
            tableheaders=["resourceType","arn","conditionKeys"]
        if(tableheader[0].text=="Condition keys"):
            tableheaders=["conditionKey","desc","typ"]

        for i in range(len(tableheaders)):
            jsondata[tableheaders[i]]=""
       

        table_trs=table.find_all('tr')[1:]
        rowspanval=[]
        for table_tr in table_trs:                        
            table_tds=list(table_tr.find_all('td'))
            for i in range(len(table_tds)):                                                
                res=table_tds[i].get('rowspan')                
                value = int(res) if res is not None else 0                                
                if(value):
                    for k in range(int(value)):
                        if len(rowspanval)<k+1:
                            rowspanval.append([])
                            rowspanval[k].append((table_tds[i].text.strip()))                            
                        else:
                            rowspanval[k].append((table_tds[i].text.strip()))                                                                                        
                if value==0 and len(rowspanval)==0 :
                    jsondata[tableheaders[i]]=table_tds[i].text.strip()                    
                elif value==0 and len(rowspanval)!=0 and i!=(len(table_tds)-1):                                                                             
                    rowspanval[0].append(table_tds[i].text.strip())                                        
                elif value==0 and i==(len(table_tds)-1) and len(rowspanval)!=0:
                    rowspanval[0].append(table_tds[i].text.strip())
                    for j in range(len(rowspanval[0])):
                        jsondata[tableheaders[j]]=rowspanval[0][j]
                    del rowspanval[0]                
            jsondata_table.append(jsondata.copy())
        if(tableheaders[0]=="action"):                
            jsondata_all['actions']=jsondata_table           
               
        elif(tableheaders[0]=="resourceType"):
            jsondata_all['resources']=jsondata_table           
        elif(tableheaders[0]=="conditionKey"):
            jsondata_all['conditions']=jsondata_table                       
    jsondata_conv=json.dumps(jsondata_all)
    with open(filepath, 'w') as file:
        file.write(jsondata_conv)

    

url = "https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html"
response = requests.get(url)
html_content = response.content
soup = BeautifulSoup(html_content, "html.parser")
links=soup.find("div",class_="highlights")
links_a=links.find_all('a')
for tag in links_a:
    href=tag.get('href')
    loopheader("https://docs.aws.amazon.com/service-authorization/latest/reference"+str(href[1:]))
    
    


                                           
    
            
            