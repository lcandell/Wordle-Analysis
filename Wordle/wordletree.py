with open('wordle.tree') as f:
	wtree = f.readlines()


lv=0
for w in wtree:
	if w[0]=='[':
		lv+=1
	elif w[0]==']':
		lv-=1
	else:
		w=w[:-1]
		sp = ' '*lv
		if len(w)>2:
			wrd = w[1::2]
			pat = w[::2]
			print(sp,wrd,pat)

"""
def prstree(rw,lv):
	while rw<len(wtree) and wtree[rw][0]!=']':
		while len(wtree[rw])<2:
			rw+=1
		if wtree[rw][0]=='[':
			rw+=1
			if wtree[rw][1:-1:2]=='ggggg':
				rw+=4
			else:
				print('  '*(lv+1),'["',wtree[rw][1:-1:2],'",{')
				rw=prstree(rw,lv+1)
		if len(wtree[rw])>2:
			print('  '*lv,wtree[rw][:-1:2],':')
		rw+=1
	print('  '*lv,'}]')
	return rw+1

prstree(0,0)
"""
