from Recursive_Function import reccursiveMethod

def parallelProcess(root,target_tag,path,result_queue,repeatTags):
    out1={}
    Flist1=[]
    datasets= reccursiveMethod(root,target_tag,path,out1,Flist1,repeatTags)
    # print(datasets)
    result_queue.append(Flist1)
    # print("This is Resultlist",result_queue)
    # print("this is Flist1",Flist1) 