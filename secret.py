
import string
import random
import math 

#frequency table of alphabets in english
frequency =['e','t','a','o','n','i','h','s','r','l','d','u','c','m','w','y','f','g','p','b','v','k','j','x','q','z']


s = low_Str =string.ascii_lowercase 
low_Str = list(low_Str) #lowercase letters
s = list(s)

value_dic = dict([(y,x) for (x,y) in enumerate(low_Str)]) #a is 0, b is 1 and so on!

#creating a displacement substitution dictionary:
disp = 5 #assume for this casea
s = s[5:]+s[:5]
d_disp = dict(zip(low_Str,s))  

#creating a random substituation dictionary:
random.shuffle(s)
d_random = dict(zip(low_Str,s))


def textstrip(filename):
    '''This takes the file and converts it to a string with all the spaces and other
    special characters removed. What remains is only the lower case letters,
    retain only the lowercase letters!
    '''
    with open(filename,'r', encoding = 'utf8') as input: #reading the input file sherlock.txt
        data = input.read().lower()            #storing the file as a string. also converting uppercase to lowercase
        check = string.ascii_lowercase                   
        output = ''                            #initiating the output
        for i in data:                         #for every character in string:
            if i in check:                     #we are checking if it is a lowercase alphabtet
                output+=i                      #if it is then add to output
        return output                          #return output



def letter_distribution(s):
    '''Consider the string s which comprises of only lowercase letters. Count
    the number of occurrences of each letter and return a dictionary
    (in addition return a frequency table ---for conveninece)
    '''
    dict = {} #create a dictionary
    for i in  s: #every element in s check
        if i in dict:#if already in dictionary increaee the frequency
            dict[i]+=1
        else:        #else add it to dictonary
            dict[i]= 1

    #creating a frequncy table:
    s = sum(dict.values())
    ftable =sorted([(x,y*100/s) for x,y in dict.items()], key = lambda x:x[1])[::-1] #sorted list in desceding order based on frequency
    return dict,ftable #return the dictionary and frequency table



def substitution_encrypt(s,d):
    '''encrypt the contents of s by using the dictionary d which comprises of
    the substitutions for the 26 letters. Return the resulting string'''
    res = ""
    for i in s: 
        res+=d[i] #keep adding the corresponding character from the dictionary
    return res #output is the final string after all the additions



def substitution_decrypt(s,d):
    '''decrypt the contents of s by using the dictionary d which comprises of
    the substitutions for the 26 letters. Return the resulting string'''
    d1 = dict((x,y) for (y,x) in d.items()) #inverse of substitutions!
    res = ""
    for i in s: 
        res+=d1[i] #keep adding the corresponding character from the dictionary
    return res #output is the final string after all the additions



def cryptanalyse_substitution_ceaser(s):
    '''Given that the string s is given to us and it is known that it was
    encrypted using some substitution cipher, predict the d
    
    this function is for when the key for substition is displaced alphabets
    '''
    #idea : the substitution dictionary is alphabets but displaced by number n
    ascii_dict = dict(enumerate(string.ascii_lowercase))
    fdict,ftable = letter_distribution(s)
    key_dic = {}

    #the letter with highest frequency is e --> assumption
    # this is almost always true in a general text 
    e_index = string.ascii_lowercase.index(ftable[0][0])

    #based on displacement of e find out the displacement of the alphabets
    disp = e_index - 4

    #create the key dictionary with the help of the displacement!
    s = string.ascii_lowercase
    s_disp = s[disp:]+s[:disp]
    key_dic = dict(zip(s,s_disp))
    return key_dic



def cryptanalyse_substitution(s):
    '''Given that the string s is given to us and it is known that it was
    encrypted using some substitution cipher, predict the d
    
    This funciton gives the dictionary with possible keys
    better approximation based on characteristics of english letters and how they act together '''
        
    fdic , ftable = letter_distribution(s) 
    flist = [x for x,y in ftable] 
    #idea1 : the top three letters are e,t,a 
    #idea2 : the letter with frequency higher than 12 is e:
    dic_sub = {}
    lstring = string.ascii_lowercase
    max_letter , max_frequency = ftable[0]
    if max_frequency >=12:
        dic_sub['e'] = max_letter
        dic_sub['t'] = dic_sub['a'] = [ftable[1][0],ftable[2][0]]
    else:
        dic_sub['e'] = dic_sub['t'] = dic_sub['a'] = [ftable[0][0],ftable[1][0],ftable[2][0]]
    
   
    #idea3 : h mostly comes before e but rarely after e (even though spaces are removed this can stll be valid)
    htable = dict(zip(lstring,[[0,0] for i in s]))
    e = dic_sub['e']

    for i in range(1,len(s)-1): #creating the before anf after letter table for e
        if s[i] ==e:            # the letter with highest differnce of before vs after will be h
            htable[s[i-1]][0] +=1
            htable[s[i+1]][1] +=1
    
    differnce = sorted([(x,y-z) for (x,[y,z]) in htable.items()], key = lambda x:x[1])[::-1]
    dic_sub['h'] = differnce[0][0] 

    #idea4 : the most frequent three letter words are "and" and "the"    
        # we can predict a, t , n and d more accurately!
    three_dic = {}
    for i in range(len(s)-2):
        subs = s[i]+s[i+1]+s[i+2]
        if subs in three_dic:
            three_dic[subs] +=1
        else:
            three_dic[subs] =1
    threes = sorted([(x,y) for x,y in three_dic.items()], key = lambda x:x[1] )[::-1]
    #so the two most frequent three letter words are:
    k1 = threes[0][0]
    k2 = threes[1][0]
    #we know for fact what is e and what is h: from here we can narrow down t! and by consequence a and n!!  
    if k1[1] ==dic_sub['h'][0]:
        if k1[0] in dic_sub['t'] and k1[2] == dic_sub['e'][0]: # we can narrow down t now!
            l = dic_sub['t']
            dic_sub['t'] = k1[0] #the letter before h is t
            dic_sub['a'] = [x for x in l if x != k1[0]][0] #then the other letter which occurs very frequenctly other than t must be a!
    #now we can narrow down n and d as well!!
        if k2[0] ==dic_sub['a'][0]:
            dic_sub['n'] = k2[1]
            dic_sub['d'] = k2[2]    

    #idea5: the most frequent two letter combinations are ss tt ee ff ll mm oo
    #idea6: based on the above and the frequency table of english we can predict o,s since frequency of  e>> t >>o >> s  !!
    twos_dic = {}
    for i in range(len(s)-1):
        if s[i]==s[i+1]:
            if s[i] in twos_dic:
                twos_dic[s[i]] +=1
            else:
                twos_dic[s[i]] = 1
    twos = sorted([(x,y) for x,y in twos_dic.items()], key = lambda x:x[1] )[::-1][:7] #getting the top seven combinations
    #eliminate e and t from the list since we know them 
    #traversing the frequency table and mapping based on the fact that e >>t >>o >> s     
    twos = [x for x,y in twos]
    twos.sort(key = lambda i:flist.index(i)) 
    dic_sub['o'] = twos[2]
    dic_sub['s'] = twos[3]
        
    """
    till here we have predicted reasonably well for 
    e , t, a, o, s, h , n, d
    """
    #range predictions:
    #idea7 : the letters with frequency < 1 are j,k,q,x,z
    least = [x for x,y in ftable if y < 1]  
    dic_sub[('j','k','q','x','z')] = least

    #the rest letters are mapped to the remaining alphabets
    r = [dic_sub[x] for x in ['e','t','a','o','s','h','n','d']] + least
    rest = [x for x in lstring if x not in r]
    dic_sub[('b', 'c', 'f', 'g', 'i', 'j', 'k', 'l', 'm', 'p', 'q', 'r', 'u', 'v', 'w', 'x', 'y', 'z')] = rest

    """
    this is the highest level i could go with fully randomised substituition!
    """

    return dic_sub



def vigenere_encrypt(s,password):
    '''Encrypt the string s based on the password the vigenere cipher way and
    return the resulting string'''
    res = ''       #create the result string
    p = len(password)  #find the length of password
    for i in range(len(s)):   #for every value in s
        weight = password[i%p] 
        shift = (value_dic[s[i]] + value_dic[weight])%26 #find the shift for it and encode using the shift
        res += low_Str[shift]      
    return res



def vigenere_decrypt(s,password):
    '''Decrypt the string s based on the password the vigenere cipher way and
    return the resulting string'''
    res = ''
    p = len(password) 
    for i in range(len(s)):
        weight = password[i%p]
        shift = (value_dic[s[i]] - value_dic[weight]) #same as encrypt but during decrypt just shift left!
        if shift > 25:
            shift = shift %26      
        res += low_Str[shift]
    return res
    


def rotate_compare(s,r):
    '''This rotates the string s by r places and compares s(0) with s(r) and
    returns the proportion of collisions'''
    collisions = 0
    temp = s[-r:] + s[:-r] #rotating the string by r
    for i in range(len(s)):
        if s[i] ==temp[i]: #comparing the strings for collisons
            collisions+=1  #if collide increment the counter
    return collisions/len(s) #return the proportion of collision



def cryptanalyse_vigenere_afterlength(s,k):
    '''Given the string s which is known to be vigenere encrypted with a
    password of length k, find out what is the password'''
    
    #idea: we form strings from s for corresponding letter in the password
    # now again in these new strings the letter with highest frequency must be e!
    # base on that we decrypt the password!
     
    nstring_list = ['']*k # creating a list of strings
    for i in range(len(s)):
        nstring_list[i%k]+=s[i]
    
    password = '' #initializing password
    for i in range(k):
        fdic , ftable = letter_distribution(nstring_list[i])
        sub_for_e = ftable[0][0]      #this is the letter that was substituted for e after shifting by the weightage of the password letter
        weightage = value_dic[sub_for_e] - 4 #find the password letter's weightage/value
        password += low_Str[weightage] #update the password

    return password #return password
        


def cryptanalyse_vigenere_findlength(s):
    '''Given just the string s, find out the length of the password using which
    some text has resulted in the string s. We just need to return the number
    k
    
    This function is provind very accurate results for any combinations!! '''

    #idea: if n is the length of the password 
    #then the number of collisons between C0 and C(xn)(rotating by x*n where x is integer) will be maximum!
    #this is because when we rotate by n then the key word becomes the same in that place as original
    #so the chance of collison in the cipher will be same as original text which is higher 
    #atleast higher than other cases where th ekey letter itself will be different creating more randomness

    #assumption1: length of the password is assumed to be less than 28 which is the longest word in english
    l = []
    for i in range(0,200):
        l.append(rotate_compare(s,i))
    
    col_list = sorted(enumerate(l), key = lambda x:x[1])[::-1][1:11] #taking top 10 of n for which highest collision happend
                                                                     #other than 0
                                                                    
    #for redundacny and to eliminate any unexpected error
    #we are finding the gcd of 5 numbers among the top 10 
    #the gcd which occurs most is our answer

    gcd_dic = {}   

    for i in range(9):
        g = math.gcd(*[x for (x,y) in col_list[i:i+2]])
        if g in gcd_dic:
            gcd_dic[g]+=1
        else:
            gcd_dic[g]=1
    result = sorted(gcd_dic.items(), key= lambda x:x[1])[::-1] # we are ordering the gcd based on frequency
    return result[0][0]  # the gcd that occured highest meaning, the most accurate n is returned!!



def cryptanalyse_vigenere(s):
    '''Given the string s cryptanalyse vigenere, output the password as well as
    the plaintext'''
    plength  = cryptanalyse_vigenere_findlength(s) #find the length of the password
    password = cryptanalyse_vigenere_afterlength(s,plength) #find the password
    res = vigenere_decrypt(s,password) #decrypt based on the password
    return res #return the decrypted string 



#test code!!
def main():
    print("lets first load the string from the test:")
    sherlock = textstrip('sherlock.txt')

    """
        CEASER SHIFT SUBSTITUTION:
    """
    #encrypt
    print("\nfor the first test lets do ceaser shift encryption:")
    print("in our case we have taken the displacement to be 5")
    a = substitution_encrypt(sherlock,d_disp)

    print('do you want to see the encrypted message?: y/n')
    i = input()
    if i == 'y':
        print(a)
    elif i =='n':
        print('moving on!\n')
    
    #decrypt
    #lets predict the key dictionary for ceaser shift
    key_dic = cryptanalyse_substitution_ceaser(a)
    #now lets 
    print("decrypting....")
    print("....")
    b = substitution_decrypt(a,key_dic)
    print('do you want to see the decrypted message?: y/n')
    i = input()
    if i == 'y':
        print(b)
    elif i =='n':
        print('moving on!\n')

    print("let us check if the decrypted string is same as the original:")
    print(b==sherlock) #checking if the decrypter message is same as original
    print("\n")


    """
        RANDOM SUBSTITUTION:
    """    
    print("Do you want to try doing the same with random substitution?: y/n")
    i = input()
    if i=='y':
        #encrypting 
        a = substitution_encrypt(sherlock,d_random)
        print('do you want to see the encrypted message?: y/n')
        i = input()
        if i == 'y':
            print(a)
        elif i =='n':
            print('moving on!\n')
        print("In this method we can only approximately predict the key_dictionary\n")
        #decrypting
        dic = cryptanalyse_substitution(a)
        print('do you want to see the decription dictionary?: y/n')
        i = input()
        if i == 'y':
            print(dic)
        elif i =='n':
            print('moving on!\n')
        

    """
        VIGENERE ENCRYPTION:
    """
    print("\nfor the next test lets do vigenere encryption:")
    p = 'kirubananth'
    print('do you want to give the password for encryption: y/n')
    i = input()
    if i == 'y':
        p = input("please enter the password: ")
    elif i =='n':
        print('using the default password\n')
  
    #encryption:
    a = vigenere_encrypt(sherlock,p)
    print('do you want to see the encrypted message?: y/n')
    i = input()
    if i == 'y':
        print(a)
    elif i =='n':
        print('moving on!\n')
    #trying to find the length of the passwod
    k = cryptanalyse_vigenere_findlength(a)
    print('predicted length of the password:' , k)
    #predicting password
    password = cryptanalyse_vigenere_afterlength(a,k)
    print('predicted password:', password)
    #decrypting:
    b = cryptanalyse_vigenere(a)
    print('do you want to see the decrypted message?: y/n')
    i = input()
    if i == 'y':
        print(a)
    elif i =='n':
        print('moving on!\n')

    print("let us check if the decrypted string is same as the original:")
    print(b==sherlock) #checking if the decrypter message is same as original
    print("\n")

main()