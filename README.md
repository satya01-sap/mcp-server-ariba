# Welcome to SAP Ariba MCP server.

1. [Intoduction](#intoduction)
2. [Running & Inspecting the MCP server locally](#running-locally)
3. [Deploy the MCP server in BTP](#deploy-in-btp)
4. [Setting up the destination for the MCP server](#setup-the-destiantion)
5. [Inspecting the remotely deployed MCP server](#inspecting-the-remote-mcp)



## Intoduction


## Running & Inspecting the MCP server locally 
  
   1. To run the mcp sevre locally opn the terminal and type `uv run main.py` You can in the in the terminal Uvicorn running.  

   2.  Now open one more terminal and tye the command `uv run mcp dev main.py` It will opne the inspector, just paste the inspector url in the brower. 

   3. Set the parameters as below -        
     - Transport Type as `STDIO`.  
     - Command as `UV`.         
     - Arguments as `run --with mcp mcp run main.py`.        



      Now open the  ⚙️  **Configuration** and fill the below fileds -    
    -  Inspector Proxy Address as `http://127.0.0.1:6277 ` you can find the terminal as shown in the screenshop
    - Proxy Session Token - copy session id form the terminal ans paste.       
           

   4. Now click on the connect button and it will connect to MCP server. Now you see the `resources`,  `prompts`,  `tools` now click on tools the choose List Tools and you can see the tool that you have specified.  


   5. Provie the tool `get_event_summary` and provide the below inputs - 
    - doc_id 
    - user
    - password_adapter
    - realm  

   and click on run tool and see the output. 

    > Conclustion - We have locally tested the MCP server successfully.  



## Deploy the MCP server in BTP



## Setting up the destination for the MCP server

## Inspecting the remotely deployed MCP server

Lest inspect the remotely deployed MCP servr. 

1. Run the inspect command in terminal `uv run mcp dev main.py` 

2. Set the parameters as below in the inspector as belwo-        
     - Transport Type as `STDIO`.  
     - Command as `UV`.         
     - Arguments as `run --with mcp mcp run main.py`.        







