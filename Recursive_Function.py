import xml.etree.ElementTree as ET
import datetime
# This is to find whether there are duplicating tags in the process. For under one department: There is Name manager and employees
# Inide employees there are two employee , So employees are duplicate with mulitple employee. 
# This Fucntion return the tags that are repreated inside a process : eg: employee tag
def find_repeated_tags_for_tag(root, tag_name):
    repeated_tags = []
    target_tag = root.find(tag_name)
    # print(f'targettages : {target_tag}')
    if target_tag is not None and len(list(target_tag))>0:
        # print(target_tag.tag)
        temp = [target_tag[0].tag]
        for i in target_tag[1:]:
            if i.tag in temp:
                repeated_tags.append(i.tag)
    # print(repeated_tags)
    return repeated_tags




def reccursiveMethod(root,target_tag,path,out,Flist,repeatTags):
    repeatTags.extend(find_repeated_tags_for_tag(root, target_tag.tag))
    #print('out received: ',out)
    #print('root',root.tag)
    if target_tag is not None :
        if len(list(target_tag)) == 0:            
                value = extractValue(target_tag) # if its a id or date then store it as it is (INT , DATETIME)
                if 'Id' in target_tag.tag or'Date' in target_tag.tag :
                        out.update({f'{str(path)}_{target_tag.tag}': value})
                else:
                        out.update({f'{str(path)}_{target_tag.tag}': str(value)})
                        
                return out

        if len(list(target_tag)) >0:
            #child_out={}
            for child in target_tag:
                # print('child in for:',child.tag)
                #i_out=reccursiveMethod(target_tag, child)
                # print('before out:',out)
                out.update(reccursiveMethod(target_tag, child,f'{str(path)}_{target_tag .tag}',out,Flist,repeatTags))
                # print('after out:',out)
                #print('repeated tags',repeatTags)
                if (child.tag in repeatTags):
                    if out not in Flist:
                        Flist.append(out.copy())
                        #print('mada flist',Flist)
                        # print('inserted into Flist')
                        # print('current Flist record number',len(Flist))
                        out={key: value for key, value in out.items() if child.tag not in key}


       
    #Flist.append(out)     
    return out

def extractValue(target_tag):
    try:
         # Try to convert to int (for Id)
        value = int(target_tag.text.strip())
    except (ValueError, AttributeError):
        try: 
            #datetime
            if target_tag.text is not None:
                value = datetime.datetime.strptime(target_tag.text.strip(), "%Y-%m-%dT%H:%M:%S")
            else:
                value=None
        except ValueError:
            # If conversion fails or target_tag.text is None,
            value = target_tag.text.strip() if target_tag.text else ''
    return value


##### NUSAL #################################


# def reccursiveMethod(root,target_tag,path,out,Flist,repeatTags):
#     repeatTags.extend(find_repeated_tags_for_tag(root, target_tag.tag))
#     #print('out received: ',out)
#     #print('root',root.tag)
#     if target_tag is not None:
#         if len(list(target_tag)) == 0: 
#             if target_tag is not None:
#                 if len(list(target_tag)) == 0:
#                     try:
#                         # Try to convert to int (for Id)
#                         value = int(target_tag.text.strip())
#                     except (ValueError, AttributeError):
#                         try:
#                             #datetime
#                             if target_tag.text is not None:
#                                 value = datetime.datetime.strptime(target_tag.text.strip(), "%Y-%m-%dT%H:%M:%S")
#                             else:
#                                 value=None
#                         except ValueError:
#                             # If conversion fails or target_tag.text is None,
#                             value = target_tag.text.strip() if target_tag.text else ''
#                     # Check if 'Id' is in the tag name
#                     if 'Id' in target_tag.tag or'Date' in target_tag.tag :
#                         out.update({f'{str(path)}_{target_tag.tag}': value})
#                     else:
#                         out.update({f'{str(path)}_{target_tag.tag}': str(value)})
                        
#                     return out

#         if len(list(target_tag)) >0:
#             #child_out={}
#             for child in target_tag:
#                 #print('child in for:',child.tag)
#                 #i_out=reccursiveMethod(target_tag, child)
#                 #print('before out:',out)
#                 out.update(reccursiveMethod(target_tag, child,f'{str(path)}_{target_tag .tag}',out,Flist,repeatTags))
#                 #print('after out:',out)
#                 #print('repeated tags',repeatTags)
#                 if (child.tag in repeatTags):
#                     if out not in Flist:
#                         Flist.append(out.copy())
#                         #print('mada flist',Flist)
#                         print('inserted into Flist')
#                         print('current Flist record number',len(Flist))
#                         out={key: value for key, value in out.items() if child.tag not in key}


       
#     #Flist.append(out)     
#     return out