// alert();



function parseURL(url) {
   var a =  document.createElement('a');
   a.href = url;
   return {
       source: url,
       protocol: a.protocol.replace(':',''),
       host: a.hostname,
       port: a.port,
       query: a.search,
       params: (function(){
           var ret = {},
               seg = a.search.replace(/^\?/,'').split('&'),
               len = seg.length, i = 0, s;
           for (;i<len;i++) {
               if (!seg[i]) { continue; }
               s = seg[i].split('=');
               ret[s[0]] = s[1];
           }
           return ret;
       })(),
       file: (a.pathname.match(/\/([^\/?#]+)$/i) || [,''])[1],
       hash: a.hash.replace('#',''),
       path: a.pathname.replace(/^([^\/])/,'/$1'),
       relative: (a.href.match(/tps?:\/\/[^\/]+(.+)/) || [,''])[1],
       segments: a.pathname.replace(/^\//,'').split('/')
   };
}



function get_encrypted_log(){
	var host = $("#encrypted_text")[0].value;
	var host = parseURL(host).host;
    $.get("/get_log?table=encrypted_log&host="+host,function(data,status){
      $("#log_result").html(data);
      // alert(data);
      // alert(data);
    });


}
function get_bruteforce_log(){
	var host = $("#encrypted_text")[0].value;
	var host = parseURL(host).host;
    $.get("/get_log?table=bruteforce_log&host="+host,function(data,status){
      $("#log_result").html(data);
      // alert(data);
      // alert(data);
    });


}


 function CreateDom() {
               var log = $("<textarea  style='width:700px;text-align:center;margin:0 auto; ' id='log_result'>").appendTo($("body"));
               log.attr('readonly','readonly');
               // log.attr('max-width','50px');
              log.attr('rows','10');
                // $('#log_result').html('aa');
  }



function attack_1(){
	var url = $("#encrypted_text")[0].value;
	$.get("/attack?type=1&file=|||~/Web.configs&url="+encodeURI(url),function(data,status){
		alert(data);
    });
}




function attack_2(){
	var url = $("#get_content_text")[0].value;
	$.get("/attack?type=2&url="+encodeURI(url),function(data,status){
		alert(data);
    });
}




$(document).ready(function(){

  $("#encrypted_button").click(function(){
  		attack_1();
  		CreateDom();
  		setInterval(get_encrypted_log,3000)
  		// while(true){
  		// 	setTimeout("get_encrypted_log()",200000);
  		// 	// ();
  		// 	// sleep(2000);
  		// }
  });

    $("#get_content_button").click(function(){
  		attack_2();
  		CreateDom();
  		setInterval(get_bruteforce_log,3000)
  		// while(true){
  		// 	setTimeout("get_encrypted_log()",200000);
  		// 	// ();
  		// 	// sleep(2000);
  		// }
  });



});



