var base_url = window.location.protocol+'//'+window.location.hostname;
var api_url = base_url+'/api/';

var helperMethods = {

    ajaxHandler : function(url,method,data,callback){
        var ajax_data = {
            'url':url,
            'type':method,
            'data':data,
            'success':function(response){
                if(typeof callback!='undefined' && response){
                    callback(response)
                }
            }
        }

        var csrf_token = helperMethods.getCookie('csrftoken');
        if(csrf_token!=''){
            ajax_data['beforeSend'] = function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }

        $.ajax(ajax_data)
    },
    ajaxHandlerJWTImage : function(url,method,data,token,success_callback,failure_callback){

        var csrf_token = helperMethods.getCookie('csrftoken');

        $.ajax({
            'url':url,
            'type':method,
            'data':data,
            'contentType':false,
            'processData':false,
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                xhr.setRequestHeader("Authorization", "JWT "+ token);
            },
            'success':function(response){
                if(typeof success_callback!='undefined' && response){
                    success_callback(response)
                }
            },
            error: function(response,status,error){
                if(response.status==401){
                    helperMethods.secureHTTPRequestHandlerImage(url,method,data,success_callback,failure_callback,'expired')
                }
                else{
                    failure_callback(response,status,error)
                }
            }
        })
    },

    ajaxHandlerJWT : function(url,method,data,token,success_callback,failure_callback){

        var csrf_token = helperMethods.getCookie('csrftoken');

        $.ajax({
            'url':url,
            'type':method,
            'data':JSON.stringify(data),
            'contentType':'application/json',
            beforeSend: function(xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
                xhr.setRequestHeader("Authorization", "JWT "+ token);
            },
            'success':function(response,status,xhr){

                if(typeof success_callback!='undefined' && response){

                    success_callback(response)
                }
            },
            error: function(response,status,error){
                if(response.status==401){
                    helperMethods.secureHTTPRequestHandler(url,method,data,success_callback,failure_callback,'expired')
                }
                else{
                    failure_callback(response,status,error)
                }
            }
        })
    },

    getCookie : function(name){
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    secureHTTPRequestHandler : function(url,method,data,success_callback,failure_callback,type){

        var token = localStorage.getItem('jwt_token')
        console.log("TOKEN: "+token)
        if(token=='' || type=='expired'){
            console.log("if")
            helperMethods.ajaxHandler(base_url+'/users/token/','GET',{},function(response){
                localStorage.setItem('token',response.token)
                helperMethods.ajaxHandlerJWT(url,method,data,response.token,success_callback,failure_callback)
            })
            console.log("fi");
        }
        else{
            console.log("else");
           helperMethods.ajaxHandlerJWT(url,method,data,token,success_callback,failure_callback)
        }
    },

    secureHTTPRequestHandlerImage : function(url,method,data,success_callback,failure_callback,type){
        var token = localStorage.getItem('jwt_token')
        if(token=='' || type=='expired'){
            helperMethods.ajaxHandler(base_url+'/users/token/','GET',{},function(response){
                localStorage.setItem('token',response.token)
                helperMethods.ajaxHandlerJWTImage(url,method,data,response.token,success_callback,failure_callback)
            })
        }
        else{
           helperMethods.ajaxHandlerJWTImage(url,method,data,token,success_callback,failure_callback)
        }
    }
}







