console.log('js working');

function imgEnlarge(e){

            if(e.style.width<"90%" || e.style.width=="" ){
                e.style.width="95%";
            }
            else{
                e.style.width="";
            }

            var imgLength = document.getElementsByTagName('img').length;

            for(var i = 0; i<imgLength; i++){
                if(document.getElementsByTagName('img')[i].id==  e.id){
                    continue;
                }
                document.getElementsByTagName('img')[i].style.width="300px";

            }
        }

/*
window.onload=function() {
  console.log('onload working');
  var anchors = document.getElementsByTagName('img');
  for(var i=0; i<anchors.length; i++) {
    var anchor=anchors[i];
    anchor.onclick = function() {
      //anchor.max-width="100%";
      console.log('pic click' + i);
      anchor.style.all = "unset";
      anchor.classList.add("full-width"); 
    }
  }
}
*/
