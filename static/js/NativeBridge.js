
var ru_cryptopro_npcades_10_native_bridge = {
  callbacksCount : 1,
  callbacks : {},
  
  // Automatically called by native layer when a result is available
  resultForCallback : function resultForCallback(callbackId, resultArray) {
        var callback = ru_cryptopro_npcades_10_native_bridge.callbacks[callbackId];
        if (!callback) return;
        callback.apply(null,resultArray);
  },
  
  // Use this in javascript to request native objective-c code
  // functionName : string (I think the name is explicit :p)
  // args : array of arguments
  // callback : function with n-arguments that is going to be called when the native code returned
  call : function call(functionName, args, callback) {
    var hasCallback = callback && typeof callback == "function";
    var callbackId = hasCallback ? ru_cryptopro_npcades_10_native_bridge.callbacksCount++ : 0;
    
    if (hasCallback)
      ru_cryptopro_npcades_10_native_bridge.callbacks[callbackId] = callback;
    
    var iframe = document.createElement("IFRAME");
	var arrObjs = new Array("_CPNP_handle");
	try{
    iframe.setAttribute("src", "cpnp-js-call:" + functionName + ":" + callbackId+ ":" + encodeURIComponent(JSON.stringify(args, arrObjs)));
	} catch(e){
		alert(e);
	}
	  document.documentElement.appendChild(iframe);
    iframe.parentNode.removeChild(iframe);
    iframe = null;
  },
};


function call_ru_cryptopro_npcades_10_native_bridge(functionName, array){
	var tmpobj;
	var ex;
	ru_cryptopro_npcades_10_native_bridge.call(functionName, array, function(e, response){
					  ex = e;
					  var str='tmpobj='+response;
					  eval(str);
					  if (typeof (tmpobj) == "string"){
						tmpobj = tmpobj.replace(/\\\n/gm, "\n");
					    tmpobj = tmpobj.replace(/\\\r/gm, "\r");
					  }
					  });
	if(ex)
		throw ex;
	return tmpobj;
}
