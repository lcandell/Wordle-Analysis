var toggler = document.getElementsByTagName('td');
var i;
var curPos=0
toggler[curPos].style.color="red";

function getWrd(row) {
	var st=""
	for(var i=0;i<5;i++){
		st = st + toggler[row*5+i].innerHTML.toLowerCase();
	}
	return st
}

function setWrd(row,wrd) {
	for(var i=0;i<5;i++){
		toggler[row*5+i].innerHTML=wrd[i].toUpperCase();
	}
}

function getPat(row) {
	var st=""
	for(var i=0;i<5;i++){
		if (toggler[row*5+i].bgColor=="404040")
			st = st + "*";
		else if (toggler[row*5+i].bgColor=="CCCC00")
			st = st + "o";
		else
			st = st + 'g';
	}
	return st
}

function logKey(e) {
	// console.log(e.key);
	toggler[curPos].innerHTML = e.key.toUpperCase();
	toggler[curPos].style.color="white";
	curPos = curPos + 1;
	if (curPos==5) {
		// console.log(getWrd(0),getPat(0),bstGuess[getWrd(0)][getPat(0)]);
		setWrd(1,bstGuess[getWrd(0)][getPat(0)]);
	}
	if (curPos==30) curPos=0;
	toggler[curPos].style.color="red";
}

document.onkeypress=logKey;

for (i = 0; i < toggler.length; i++) {
  toggler[i].cid = i
  toggler[i].addEventListener("click", function() {
	//   console.log(parseInt(this.cid/5),this.cid%5);
	  toggler[curPos].style.color="white";
	  curPos=this.cid;
	  this.style.color="red"
	  if (this.bgColor==="404040") this.bgColor="CCCC00";
	  else if (this.bgColor==="CCCC00") this.bgColor="009900";
	  else this.bgColor="404040";
	  if (this.cid<5 && bstGuess[getWrd(0)] && bstGuess[getWrd(0)][getPat(0)])
	  	setWrd(1,bstGuess[getWrd(0)][getPat(0)]) 
  });
}

function evgs(wrd,guess) {
	var let = [...wrd].reduce((a, e) => { a[e] = a[e] ? a[e] + 1 : 1; return a }, {});
	return let
}