from flask import Flask,request,render_template,redirect
from neo4j import GraphDatabase
import csv

with open("cred.txt")as f1:
 data=csv.reader(f1,delimiter=",")
 for row in data:
    id=row[0]
    pwd=row[1]
 f1.close()

driver=GraphDatabase.driver(uri="bolt://100.25.170.168:33264",auth=(id,pwd))
session=driver.session()

app=Flask(__name__)
@app.route("/graph",methods=["GET","POST"])
def creategrpah():
    if request.method=="POST":
        if request.form["submit"]=="find_graph":
         
         query="""
        MATCH(a:Student)
        return a.name as name ,a.city as city
        """
         results=session.run(query)
         graphs=[]
         for result in results:
            dc={}
            name=result["name"]
            city=result["city"]
            dc.update({"Name":name,"City":city})
            graphs.append(dc)
            
        

         print(graphs)
         return render_template("results.html",list=graphs)

        elif request.form["submit"]=="find_property":
             name=request.form["name"]
             query="""
        MATCH(a:Student{name:$name})
        return a.name as name ,a.city as city
        """  
             parameter={"name":name}
             results=session.run(query,parameter)
             for result in results:
                name=result["name"]
                city=result["city"]

             return (f"{name} lives in {city}")

        elif request.form["submit"]=="find_friends":
             name_requested=request.form["friends"]
             query="""
        match(a:Student{name:$name})
with [(a)--(b)|b.name]as names
unwind names as name
return name
        """  
             parameter={"name":name_requested}
             results=session.run(query,parameter)
             friends=[]
             for result in results:
                name=result["name"]
                friends.append(name)
                
             if(len(friends)>0):
              return render_template("friends.html",list=friends,name=name_requested)
             else:
                 return("no friends or invalid person")




             
    else:
        return render_template("index.html")

if __name__=='__main__':
    app.run(port=5000)
    
