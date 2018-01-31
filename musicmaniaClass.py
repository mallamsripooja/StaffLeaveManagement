import os
class MusicClass:
    #get list of files in a folder
    def getList(filePath):
        lst=os.listdir(filePath)#ADD condition to ignore non .mp3 files
        return lst

    #to return tables
    def createList(filePath):
        ht=''
        az=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        lst=MusicClass.getList(filePath)
        playList=[]#incase the .mp3 filename starts with a non-alpha char then it is not read in the list
        for alpha in az:
            playList.append([c for c in lst if c[0].lower()==alpha])#linear expression -- sorting alpha order -- [['a..','a..',..],...,['Z..','zo...']]
        for tup in playList:
            if len(tup)!=0:
                ht1='<h3 align="center">'+tup[0][0].upper()+'</h3><div align="center">'
            else:
                ht1='<div align="center">'
            for song in tup:#here hard coding the source file path
                #ht1+='<td>'+song+'<audio controls><source src="../SG-songs/'+song+'" ></audio></td>'
                ht1+='<a href="../SG-songs/'+song+'" target="iframe_top" style="text-decoration:none" onclick="scrollToTopPlay()">'+song+'</a><br>'
            ht1+='</div><br>'
            ht+=ht1
        return ht
