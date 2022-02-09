import json

#with open('wordledict.json') as f:
#    wordleDicts = json.load(f)

#dic5 = wordleDicts['answers']
#d5lset = dic5 + wordleDicts['guesses']

with open('words5.json') as f:
    dic5 = json.load(f)

print(len(dic5))

def evgs(wrd,guess):
	let={}
	for l in wrd:
		let[l] = let.get(l,0)+1
	res = ['*']*5
	nm=[]
	for k in range(5):	
		if guess[k]==wrd[k]:
			res[k] = 'g'
			let[guess[k]]-=1
		elif guess[k] in let:
			nm.append(k)
	for k in nm:
		if let[guess[k]]>0:
			res[k] = 'o'
			let[guess[k]]-=1 
		
	return ''.join(res)

import math
def entropy(pdic):
	e=0.0
	t=0.0
	for p in pdic:
		w=len(pdic[p])
		e += w*math.log(w,2)
		t += w
	return math.log(t,2) - e/t

#These are the guess so far with the reported color values	
guesses = [('alone','****o')]#,('dirts','**gg*'),('berth','*gggg')]

cdic=dic5
for gu,pat in guesses:
	pdic = {}
	mxp=0
	mxi=''
	for wrd in cdic:
		p = evgs(wrd,gu)
		pdic[p] = pdic.get(p,[])+[wrd]
		if len(pdic[p])>mxp:
			mxp = len(pdic[p])
			mxi = p
	if pat in pdic:
		cdic = pdic[pat]
		print(gu,pat,len(cdic),mxp,mxi)
	else:
		print('No words match!',gu)
		break


#Continue down the tree, using the calculated most common pattern

while len(cdic)>1:
	mxe=0
	for gu in cdic+dic5:
		pdic = {}
		mxp=0
		for wrd in cdic:
			p = evgs(wrd,gu)
			pdic[p] = pdic.get(p,[])+[wrd]
			if len(pdic[p])>mxp:
				mxp = len(pdic[p])
				mxdic=pdic[p]
				mxi = p
		e = entropy(pdic)
		if e > mxe:
			mxe = e
			owrd = gu
			opat = mxi
			odic = mxdic
	print(owrd,opat,len(odic),mxe)
	guesses.append((owrd,opat))
	cdic = odic
	if len(cdic)<10:
		print('Remaining Words:',cdic)
	
print(guesses)
print(cdic)
