#!/usr/bin/env python3
from os import environ
import sys
import requests as req


# try:
#     serv_addr = "http://"+environ["serv_addr"]+":27017/"
# except:
#     print("Nao foi possivel configurar a variavel de ambiente")
#     serv_addr = "http://127.0.0.1:5000/" #environ["serv_addr"]

serv_addr = "http://0.0.0.0:5000/"

if sys.argv[1] == "add":     # adicionar [lista de valores dos atributos da classe]
    task = {"title":sys.argv[2], "description":sys.argv[3]}
    res = req.post(url = serv_addr + "todo/api/tasks/", json= task)
    print(res)

elif sys.argv[1] == "list":    # listar
    res = req.get(serv_addr + "todo/api/tasks/")
    print(res)

elif sys.argv[1] == "search":  # buscar
    res = req.get(serv_addr + "todo/api/tasks/" + sys.argv[2])
    print(res)

elif sys.argv[1] == "delete":  # apagar
    res = req.delete(serv_addr + "todo/api/tasks/" + sys.argv[2])
    print(res) 

elif sys.argv[1] == "update":  # atualizar [lista de valores dos atributos da classe]
    task = {"title":sys.argv[3], "description":sys.argv[4], "done":sys.argv[5]}
    res = req.put(url = serv_addr + "todo/api/tasks/" + sys.argv[2], json= task)
    print(res) 

elif sys.argv[1] == "help":  # help
    print("Comandos geream requests que interagem com um webserver Flask:\n \
           https://github.com/guipleite/Spark_REST\n")

    print("add -    Adicona uma task               :  task add \"<title>\" \"<descripton>\"")
    print("list -   Lista todas as tasks           :  task list")
    print("search - busca um post pelo seu id      :  task search id")
    print("delete - apaga um post pelo seu id      :  task delete id")
    print("update - Atualiza os campos de uma task :  task update id \"<title>\" \"<descripton>\" <done>")

    print("\nPara rodar o programa em qualquer lugar adicione ele ao PATH")
else:
    print("Nenhum comando encontrado, digite 'task help' para obter ajuda")